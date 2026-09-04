import os
import sys
import time
import json
import re
import urllib.request
import urllib.parse
import numpy as np

# Ensure enn is in path
sys.path.append(r"c:\Users\Dell\Downloads\enn")
from fella.fella_brain import FellaBrain

USER_AGENT = "FellaNeuromorphicAgent/2.0 (Autonomous Cognitive Research Substrate; contact: cognitive-fella@enn.ai)"

# Functional/grammar words that shouldn't be primary curiosity targets
STOP_WORDS = {
    "there", "their", "theirs", "where", "which", "whose", "whoever", "whomever",
    "earlier", "later", "becomes", "became", "becoming", "unlike", "likely",
    "about", "above", "after", "again", "against", "almost", "along", "already",
    "also", "although", "always", "among", "another", "anyone", "anything",
    "around", "because", "before", "behind", "being", "below", "beside",
    "between", "beyond", "cannot", "could", "during", "either", "enough",
    "every", "everyone", "everything", "everywhere", "further", "having",
    "here", "herself", "himself", "itself", "myself", "yourself", "yourselves",
    "indeed", "inside", "instead", "into", "itself", "little", "mainly",
    "maybe", "might", "mostly", "neither", "never", "nobody", "none",
    "nothing", "nowhere", "often", "other", "others", "otherwise", "outside",
    "perhaps", "quite", "rather", "really", "seldom", "several", "should",
    "since", "somebody", "someone", "something", "somewhere", "sometimes",
    "still", "such", "than", "that", "them", "then", "there", "therefore",
    "these", "they", "this", "those", "though", "through", "throughout",
    "together", "toward", "towards", "under", "until", "upon", "very",
    "well", "whatever", "whenever", "wherever", "whether", "while",
    "without", "would", "downward", "upward", "heels", "quantities", "arranged"
}

def safe_api_request(url: str, retries: int = 3) -> dict:
    """Performs HTTP request with exponential backoff on HTTP 429 (Too Many Requests)."""
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=12) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait_time = (attempt + 1) * 4.0
                print(f" [RATE-LIMIT 429] Throttled. Backing off for {wait_time:.1f}s...")
                time.sleep(wait_time)
            else:
                break
        except Exception:
            break
    return {}

def search_wikipedia_topics(query: str, site: str = "en.wikipedia.org", limit: int = 3) -> list[str]:
    """Searches Wikipedia for relevant articles matching a query."""
    time.sleep(0.6) # Polite pacing
    url = (
        f"https://{site}/w/api.php?action=query&list=search"
        f"&srsearch={urllib.parse.quote(query)}&format=json&srlimit={limit}"
    )
    data = safe_api_request(url)
    search_items = data.get("query", {}).get("search", [])
    return [item["title"] for item in search_items]

def fetch_wikipedia_extract(title: str, site: str = "en.wikipedia.org", max_chars: int = 3500) -> str:
    """Fetches substantive plain-text extract of a given title from Wikipedia API."""
    time.sleep(0.6) # Polite pacing
    url = (
        f"https://{site}/w/api.php?action=query&prop=extracts"
        f"&explaintext=true&format=json&titles={urllib.parse.quote(title)}"
    )
    data = safe_api_request(url)
    pages = data.get("query", {}).get("pages", {})
    for pid, pdata in pages.items():
        if pid != "-1":
            raw_text = pdata.get("extract", "")
            return raw_text[:max_chars]
    return ""

def clean_and_segment_sentences(text: str) -> list[list[str]]:
    """Segments raw text into clean, informative token sequences for Hebbian event recording."""
    # Remove parenthetical pronunciation guides and bracketed citations
    clean_text = re.sub(r"\[\d+\]", "", text)
    clean_text = re.sub(r"\([^)]*\)", "", clean_text)
    clean_text = re.sub(r"[{}\[\]/\\;]", " ", clean_text)
    
    raw_sentences = re.split(r"[.!?\n]+", clean_text)
    tokenized_sentences = []

    for raw_s in raw_sentences:
        tokens = [w.strip(".,!?:;\"'()-_/").lower() for w in raw_s.split() if w.strip(".,!?:;\"'()-_/")]
        # Keep informative sentences with 4 to 25 words
        filtered = [t for t in tokens if t.isalpha() and len(t) > 1]
        if 4 <= len(filtered) <= 25:
            tokenized_sentences.append(filtered)

    return tokenized_sentences

def compute_epistemic_followup(brain, causal_matrix, in_deg, parent_word: str, visited_thread: set) -> str:
    """
    Epistemic Follow-up Curiosity:
    Computes the highest-gradient concept directly related to parent_word in episodic memory:
    Salience = CausalCoupling * (1.0 + 3.0 * WaveCosine) * Novelty * HubPenalty
    """
    p_lower = parent_word.lower()
    if p_lower not in brain.neurons:
        return None

    key_to_idx = {k: i for i, k in enumerate(brain.matrix_keys)}
    p_idx = key_to_idx.get(p_lower)
    if p_idx is None:
        return None

    p_deg = float(in_deg[p_idx]) if p_idx < len(in_deg) else 1.0
    p_wave = brain.neurons[p_lower].x_wave
    p_norm = np.linalg.norm(p_wave) + 1e-9

    p_evs = brain.neurons[p_lower].z_events
    candidate_words = set()

    for ev_id in p_evs:
        if ev_id in brain.events:
            for neuron in brain.events[ev_id]:
                w = neuron.text.lower()
                if w in key_to_idx and w not in visited_thread and w.isalpha() and len(w) > 3 and w not in STOP_WORDS:
                    candidate_words.add(w)

    if not candidate_words:
        return None

    best_score = -1.0
    best_word = None

    for cand in candidate_words:
        c_idx = key_to_idx[cand]
        c_deg = float(in_deg[c_idx]) if c_idx < len(in_deg) else 1.0
        hub_penalty = 1.0 / (1.0 + np.log(1.0 + c_deg / 35.0))

        # Causal coupling across T-matrix
        t_fwd = causal_matrix[p_idx, c_idx] if p_idx < causal_matrix.shape[0] and c_idx < causal_matrix.shape[1] else 0.0
        t_bwd = causal_matrix[c_idx, p_idx] if c_idx < causal_matrix.shape[0] and p_idx < causal_matrix.shape[1] else 0.0
        deg_scale = np.sqrt((1.0 + p_deg) * (1.0 + c_deg))
        coupling = (t_fwd + t_bwd + 1.0) / deg_scale

        # 256D Continuous Wave Resonance
        c_wave = brain.neurons[cand].x_wave
        c_norm = np.linalg.norm(c_wave) + 1e-9
        cos_sim = max(0.0, float(np.dot(p_wave, c_wave) / (p_norm * c_norm)))

        # Novelty (lower memory count = higher learning value)
        ev_count = len(brain.neurons[cand].z_events)
        novelty = 1.0 / np.sqrt(1.0 + ev_count)

        score = coupling * (1.0 + 3.0 * cos_sim) * novelty * hub_penalty
        if score > best_score:
            best_score = score
            best_word = cand

    return best_word

def run_study_session(target_topics: list = None, max_articles: int = 10, continuous: bool = False, rabbit_depth: int = 3, checkpoint_file="fella_hyper_mind.json"):
    """
    Autonomous Epistemic Study Engine 3.0:
    - Rabbit Hole Epistemic Threading: Explores coherent scientific deep-dives (depth 3-4 hops).
    - Joint Vector Bigram Search: Queries 'parent child' conjunctions to eliminate pop-culture disambiguations.
    - Multi-Source Web Extraction: Pulls substantive mechanistic explanations from Wikipedia & Simple Wikipedia.
    - Zero Hardcoding: Driven purely by Causal Coupling, 256D Wave Resonance, and Novelty Entropy.
    """
    print("================================================================================")
    print("FELLA EPISTEMIC CURIOSITY ENGINE 3.0 (AUTONOMOUS RABBIT-HOLE LEARNER)")
    print("================================================================================")
    print("• Epistemic Vector Threading: Causal Coupling x Continuous 256D Wave Resonance.")
    print("• Joint Vector Bigram Queries: Mechanistic Search without Pop-Culture Collisions.")
    if continuous:
        print("• Mode: CONTINUOUS DEEP INQUIRY (Runs indefinitely, press Ctrl+C to stop).")
    else:
        print(f"• Mode: Targeted Session (Goal: {max_articles} articles | Thread Depth: {rabbit_depth}).")
    print("================================================================================")

    brain = FellaBrain(dim=256)
    if os.path.exists(checkpoint_file):
        brain.load_state(checkpoint_file)
        print(f"[FELLA ONLINE] Initial State: {len(brain.neurons)} concepts, {brain.z_counter} Z-events.", flush=True)
    else:
        print(f"[ERROR] Checkpoint '{checkpoint_file}' not found.")
        return

    start_concepts = len(brain.neurons)
    start_events = brain.z_counter
    articles_read = 0

    # Build initial causal graph & in-degrees
    N = len(brain.matrix_keys)
    key_to_idx = {k: i for i, k in enumerate(brain.matrix_keys)}
    causal_T = np.zeros((N, N), dtype=np.float32)
    in_deg = np.zeros(N, dtype=np.float32)

    print("[GRAPH INITIALIZATION] Computing causal topology from episodic memory...")
    for z in brain.events:
        words = [n.text.lower() for n in brain.events[z] if n.text.lower() in key_to_idx]
        for i in range(len(words)):
            p_idx = key_to_idx[words[i]]
            in_deg[p_idx] += 1.0
            for j in range(i + 1, min(i + 5, len(words))):
                n_idx = key_to_idx[words[j]]
                if p_idx != n_idx:
                    causal_T[p_idx, n_idx] += 1.0 / (j - i)

    frontier_queue = list(target_topics) if target_topics else []

    try:
        while True:
            if not continuous and articles_read >= max_articles:
                break

            # 1. Select Root Topic for New Epistemic Thread
            if frontier_queue:
                root_topic = frontier_queue.pop(0)
            else:
                # Find low-connectivity blindspots with high conceptual length
                candidates = [
                    w for w, n in brain.neurons.items()
                    if w.isalpha() and 1 <= len(n.z_events) <= 3 and len(w) > 4 and w.lower() not in STOP_WORDS
                ]
                if not candidates:
                    candidates = [w for w in brain.neurons if w.isalpha() and len(w) > 4 and w.lower() not in STOP_WORDS]
                np.random.shuffle(candidates)
                root_topic = candidates[0]

            print(f"\n================================================================================")
            print(f"[NEW EPISTEMIC THREAD] Starting deep inquiry at root: '{root_topic.upper()}'")
            print(f"================================================================================")

            curr_topic = root_topic
            visited_thread = {root_topic.lower()}

            for hop in range(rabbit_depth):
                if not continuous and articles_read >= max_articles:
                    break

                print(f"\n--------------------------------------------------------------------------------")
                print(f"[THREAD HOP {hop + 1}/{rabbit_depth}] Exploring: '{curr_topic}' (Total Read: {articles_read + 1})")

                # Formulate search query: if in a follow-up hop, use joint bigram
                if hop == 0:
                    search_query = curr_topic
                else:
                    search_query = f"{prev_topic} {curr_topic}"

                print(f" * Search Query: \"{search_query}\"")
                
                # Try English Wikipedia first, then Simple Wikipedia
                search_results = search_wikipedia_topics(search_query, site="en.wikipedia.org", limit=3)
                chosen_site = "en.wikipedia.org"
                
                if not search_results:
                    search_results = search_wikipedia_topics(search_query, site="simple.wikipedia.org", limit=3)
                    chosen_site = "simple.wikipedia.org"
                if not search_results:
                    search_results = [curr_topic]

                valid_text = None
                target_title = None

                for candidate_title in search_results:
                    print(f" * Checking Article: '{candidate_title}' ({chosen_site})")
                    text = fetch_wikipedia_extract(candidate_title, site=chosen_site, max_chars=3500)
                    if text and len(text) >= 80 and "may refer to:" not in text.lower():
                        valid_text = text
                        target_title = candidate_title
                        break

                if not valid_text:
                    print(f" * No substantive extract found for '{search_query}', ending thread branch.")
                    break

                print(f" * Ingesting: '{target_title}'")
                sentences = clean_and_segment_sentences(valid_text)
                print(f" * Consolidating {len(sentences)} conceptual sentences into 256D Substrate...")

                events_before = brain.z_counter
                for tokens in sentences:
                    brain.record_event(tokens)

                events_added = brain.z_counter - events_before
                articles_read += 1
                print(f" * Learned {events_added} new episodic Z-events from '{target_title}'")

                # Save checkpoint periodically
                brain.save_state(checkpoint_file)

                # Dynamically update causal matrix capacity and weights
                new_N = len(brain.matrix_keys)
                if new_N > causal_T.shape[0]:
                    pad_len = new_N - causal_T.shape[0]
                    causal_T = np.pad(causal_T, ((0, pad_len), (0, pad_len)), mode='constant')
                    in_deg = np.pad(in_deg, (0, pad_len), mode='constant')
                    key_to_idx = {k: i for i, k in enumerate(brain.matrix_keys)}

                for tokens in sentences:
                    token_indices = [key_to_idx[t] for t in tokens if t in key_to_idx]
                    for idx_i in range(len(token_indices)):
                        p_i = token_indices[idx_i]
                        in_deg[p_i] += 1.0
                        for idx_j in range(idx_i + 1, min(idx_i + 5, len(token_indices))):
                            n_j = token_indices[idx_j]
                            if p_i != n_j:
                                causal_T[p_i, n_j] += 1.0 / (idx_j - idx_i)

                # Compute next follow-up concept along maximum epistemic gradient
                next_target = compute_epistemic_followup(brain, causal_T, in_deg, curr_topic, visited_thread)
                if not next_target:
                    print(f" * [LOCAL CONVERGENCE] Epistemic uncertainty around '{curr_topic}' resolved.")
                    break

                print(f" * [EPISTEMIC FOLLOW-UP] Next curiosity rabbit hole: '{next_target}'")
                visited_thread.add(next_target.lower())
                prev_topic = curr_topic
                curr_topic = next_target

                time.sleep(1.0) # Polite crawling interval

    except KeyboardInterrupt:
        print("\n\n[USER INTERRUPT] Stopping epistemic study session gracefully...")

    print("\n================================================================================")
    print("EPISTEMIC STUDY SESSION FINISHED")
    print("================================================================================")
    print(f" * Articles Ingested : {articles_read}")
    print(f" * New Concepts Added: {len(brain.neurons) - start_concepts}")
    print(f" * Total Concepts    : {len(brain.neurons)}")
    print(f" * New Memories (Z)  : {brain.z_counter - start_events}")
    print(f" * Total Memories    : {brain.z_counter}")
    print(f" * Checkpoint Saved  : {checkpoint_file}")
    print("================================================================================")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Fella Epistemic Curiosity Engine 3.0")
    parser.add_argument("--topics", nargs="+", help="Specific topics to explore")
    parser.add_argument("--count", type=int, default=6, help="Number of articles to study (default: 6)")
    parser.add_argument("--depth", type=int, default=3, help="Epistemic rabbit-hole depth per thread (default: 3)")
    parser.add_argument("--continuous", action="store_true", help="Study indefinitely until stopped with Ctrl+C")
    args = parser.parse_args()

    run_study_session(target_topics=args.topics, max_articles=args.count, continuous=args.continuous, rabbit_depth=args.depth)
