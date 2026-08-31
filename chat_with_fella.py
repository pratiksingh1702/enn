import urllib.request
import json
import sys

def chat():
    print("==================================================")
    print("           CONNECTED TO FELLA'S MIND              ")
    print("             Type 'quit' to exit                  ")
    print("==================================================")
    
    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ['quit', 'exit']:
                print("Disconnecting from Fella...")
                break
                
            if not user_input.strip():
                continue
                
            req = urllib.request.Request("http://localhost:5050", data=user_input.encode('utf-8'), method="POST")
            response = urllib.request.urlopen(req)
            data = json.loads(response.read().decode('utf-8'))
            
            print(f"\n[Fella's Inner Thought]: {data['thought']}")
            print(f"FELLA: {data['response']}")
            
        except ConnectionRefusedError:
            print("\n[ERROR] Fella's brain is asleep! You need to run 'fella_server.py' in the background first.")
        except Exception as e:
            print(f"\n[ERROR] Connection issue: {e}")

if __name__ == '__main__':
    chat()
