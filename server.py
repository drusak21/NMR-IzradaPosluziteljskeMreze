import socket
import threading
import urllib.parse

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
    try:
        request = client_socket.recv(1024).decode()
        print(f"Primljeni zahtjev:\n{request}")

        lines = request.split("\r\n")
        method, path, _ = lines[0].split(" ")

        if method == "GET":
            if path == "/":
                response = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n" + load_html("index.html")
            elif path == "/about":
                response = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n" + load_html("about.html")
            elif path == "/styles.css": 
                response = "HTTP/1.1 200 OK\r\nContent-Type: text/css; charset=utf-8\r\n\r\n" + load_css("styles.css")
            elif path == "/addcar":
                response = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n" + load_html("addNewCar.html")
            else:
                response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html; charset=utf-8\r\n\r\n" + \
                           "<html><body><h1>404 - Stranica nije pronađena</h1></body></html>"

        elif method == "POST":
            if path == "/dodaj-auto":
                # Pronađite sadržaj tijela zahtjeva (POST podaci)
                body = request.split("\r\n\r\n")[1]

                # Dekodirajte URL-enkodirane podatke
                data = urllib.parse.parse_qs(body)
                proizvodac = data.get("proizvodac", [""])[0]
                model = data.get("model", [""])[0]
                godina = data.get("godina", [""])[0]
                boja = data.get("boja", [""])[0]
                cijena = data.get("cijena", [""])[0]

                # HTML odgovor za prikaz spremljenih podataka
                response = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n" + \
                           f"<html><link rel='stylesheet' href='styles.css'><body><h1>Auto spremljen!</h1>" + \
                           f"<div class='carData'>"+\
                           f"<p>Proizvodac:{proizvodac}</p>"+\
                           f"<p>Model:{model}</p>"+\
                           f"<p>Godina: ({godina})</p>"+\
                           f"<p>Boja: {boja}</p>"+\
                           f"<p>Cijena: {cijena} €</p></body></html>"+\
                           f"</div>"

            else:
                response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html; charset=utf-8\r\n\r\n" + \
                           "<html><body><h1>404 - Stranica nije pronađena</h1></body></html>"

        else:
            response = "HTTP/1.1 405 Method Not Allowed\r\nContent-Type: text/html; charset=utf-8\r\n\r\n" + \
                       "<html><body><h1>405 - Metoda nije dopuštena</h1></body></html>"

        client_socket.send(response.encode())

    except Exception as e:
        print(f"Dogodila se greška: {e}")
    finally:
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
