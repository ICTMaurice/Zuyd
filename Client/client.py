import socket
import json

# Serverinstellingen
HOST = "127.0.0.1"
PORT = 65432

def start_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))
        
        # Ontvang welkomsbericht
        data = client.recv(1024).decode()
        print(json.loads(data)["message"])
        
        while True:
            question_data = client.recv(1024).decode()
            if not question_data:
                break
            
            question = json.loads(question_data)
            print("\nVraag:", question["question"])
            
            if question["type"] == "multiple":
                print("Keuzeopties:", ", ".join(question["options"]))
            
            answer = input("Jouw antwoord: ")
            client.sendall(answer.encode())
            
            feedback = json.loads(client.recv(1024).decode())
            print(feedback["message"])
        
        client.close()

if __name__ == "__main__":
    start_client()

