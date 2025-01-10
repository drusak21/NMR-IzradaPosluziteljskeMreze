import socket
import threading

def load_html(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Greška pri učitavanju datoteke: {e}"

def load_css(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Greška pri učitavanju datoteke: {e}"

def handle_client(client_socket):
    request = client_socket.recv(1024).decode()
    print(f"Primljeni zahtjev: {request}")

    lines = request.split("\r\n")
    method, path, _ = lines[0].split(" ")

    if method == "GET":
        if path == "/":
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n" + load_html("index.html")
        elif path == "/about":
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n" + load_html("about.html")
        elif path == "/styles.css": 
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/css; charset=utf-8\r\n\r\n" + load_css("styles.css")
        else:
            response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html; charset=utf-8\r\n\r\n" + \
                       "<html><body><h1>404 - Stranica nije pronađena</h1></body></html>"

    elif method == "POST":
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n" + \
                   "<html><body><h1>Podaci uspješno primljeni!</h1></body></html>"

    else:
        response = "HTTP/1.1 405 Method Not Allowed\r\nContent-Type: text/html; charset=utf-8\r\n\r\n" + \
                   "<html><body><h1>405 - Metoda nije dopuštena</h1></body></html>"

    client_socket.send(response.encode())
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 5000))
    server.listen(5)
    print("Poslužitelj pokrenut na http://127.0.0.1:5000/")

    while True:
        client_socket, addr = server.accept()
        print(f"Veza uspostavljena s {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
