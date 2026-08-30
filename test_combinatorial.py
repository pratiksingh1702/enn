import time
from fella.fella_brain import FellaBrain

def run():
    print('[FELLA: COMBINATORIAL GENERATION TEST]')
    print('Loading physical substrate...')
    brain = FellaBrain.load_state('fella_checkpoint.json')
    
    print('\n[TEACHING PREMISE 1]')
    p1 = "Wolves hunt foxes."
    print(f'Ingesting: {p1}')
    brain.converse(p1)

    print('\n[TEACHING PREMISE 2]')
    p2 = "Foxes bite apples."
    print(f'Ingesting: {p2}')
    brain.converse(p2)
    
    # Repeat a few times to widen the synapses so electricity can easily flow
    for _ in range(5):
        brain.converse(p1)
        brain.converse(p2)

    print('\n[TESTING COMBINATORIAL EMERGENT THOUGHT]')
    print('Note: She was NEVER taught that Wolves and Apples have any connection.')
    print('If she outputs a sentence combining them, she successfully navigated her own topological graph.')
    
    query = "Do wolves eat apples?"
    print(f'User: {query}')
    res = brain.converse(query)
    
    print(f'FELLA: \'{res["last_response"]}\'')
    print(f'   -> Inner Critic Logs: {res["last_thought"]}')

if __name__ == '__main__':
    run()
