import time
from fella.fella_brain import FellaBrain

def run():
    print('[FELLA: COMBINATORIAL GENERATION TEST]')
    print('Loading physical substrate...')
    brain = FellaBrain.load_state('fella_checkpoint.json')
    
    print('\n[TEACHING PREMISE 1]')
    p1 = "developer writes code."
    brain.converse(p1)

    print('\n[TEACHING PREMISE 2]')
    p2 = "code executes on computers."
    brain.converse(p2)
    
    for _ in range(8):
        brain.converse(p1)
        brain.converse(p2)

    print('\n[TESTING COMBINATORIAL EMERGENT THOUGHT]')
    
    query = "developer computers"
    print(f'User: {query}')
    res = brain.converse(query)
    
    print(f'FELLA: \'{res["last_response"]}\'')
    print(f'   -> Inner Critic Logs: {res["last_thought"]}')

if __name__ == '__main__':
    run()
