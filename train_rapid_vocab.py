import time
from fella.fella_brain import FellaBrain

def run():
    print('[FELLA: RAPID VOCABULARY & CURIOSITY TRAINING]')
    print('Loading physical substrate...')
    brain = FellaBrain.load_state('fella_checkpoint.json')
    print(f'Initial Neurons: {len(brain.substrate.neurons)}')

    print('\n[READING CORPUS]')
    with open('vocab_corpus.txt', 'r', encoding='utf-8') as f:
        lines = [l.strip() for l in f if l.strip()]

    print(f'Training on {len(lines)} sentences using pure physical thermodynamics...')
    
    for i, line in enumerate(lines):
        res = brain.converse(line)
        print(f'[{i+1}/{len(lines)}] Ingesting: {line}')
        print(f'   -> FELLA: {res["last_response"]}')
        print(f'   -> STATE: {res["last_thought"]}')

    print('\n[SAVING EXPANDED BRAIN]')
    brain.save_state('fella_checkpoint.json')
    print(f'Final Neurons: {len(brain.substrate.neurons)}')

    print('\n[TESTING NOVELTY & EMERGENT CURIOSITY]')
    print('User: \'Alice is a human.\'')
    res = brain.converse('Alice is a human.')
    print(f'FELLA: \'{res["last_response"]}\'')
    print(f'   -> Inner Critic Logs: {res["last_thought"]}')

if __name__ == '__main__':
    run()
