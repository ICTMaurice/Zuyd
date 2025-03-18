import socket
import threading
import json

# Quizvragen over Software Engineering en Security & Cloud
quiz_questions = [
    {"question": "Is Python een programmeertaal?", "type": "yesno", "answer": "ja"},
    {"question": "Wat betekent HTML?", "type": "open", "answer": "HyperText Markup Language"},
    {"question": "Welke HTTP-statuscode betekent 'Niet gevonden'?", "type": "multiple", "options": ["200", "404", "500"], "answer": "404"},
    {"question": "Is een firewall een software- of hardwarecomponent?", "type": "yesno", "answer": "ja"},
    {"question": "Wat doet een VPN?", "type": "open", "answer": "Versleutelt internetverkeer"},
    {"question": "Welke van deze is GEEN programmeertaal?", "type": "multiple", "options": ["Python", "JavaScript", "HTML"], "answer": "HTML"},
    {"question": "Wat is de belangrijkste taak van een database?", "type": "open", "answer": "Data opslaan en beheren"},
    {"question": "Is een DDOS-aanval schadelijk?", "type": "yesno", "answer": "ja"}
]

# Serverinstellingen
HOST = "127.0.0.1"
PORT = 65432
clients = []

# Verwerk clientverbindingen
def handle_client(conn, addr):
    print(f"Nieuwe verbinding: {addr}")
    conn.sendall(json.dumps({"message": "Welkom bij de quiz!"}).encode())
    score = 0
    
    for q in quiz_questions:
        conn.sendall(json.dumps(q).encode())
        answer = conn.recv(1024).decode().strip()
        
        if answer.lower() == q["answer"].lower():
            conn.sendall(json.dumps({"message": "Correct!"}).encode())
            score += 1
        else:
            conn.sendall(json.dumps({"message": f"Fout! Het juiste antwoord is {q['answer']}"}).encode())
    
    conn.sendall(json.dumps({"message": f"Quiz voorbij! Jouw score: {score}/{len(quiz_questions)}"}).encode())
    conn.close()

# Server starten
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server draait op {HOST}:{PORT}")
    
    while True:
        conn, addr = server.accept()
        clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
