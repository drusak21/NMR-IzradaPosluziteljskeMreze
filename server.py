import socket
import threading
import urllib.parse
import json

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
    response = ""
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
            elif path.startswith("/images/"): 
                image_path = "." + path 
                try:
                    with open(image_path, 'rb') as img_file:
                        image_data = img_file.read()
                    client_socket.send(f"HTTP/1.1 200 OK\r\nContent-Type: image/jpeg\r\n\r\n".encode())
                    client_socket.send(image_data)
                    return 
                except Exception as e:
                    response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html; charset=utf-8\r\n\r\n" + \
                               "<html><body><h1>404 - Slika nije pronađena</h1></body></html>"
            else:
                response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html; charset=utf-8\r\n\r\n" + \
                           "<html><body><h1>404 - Stranica nije pronađena</h1></body></html>"

        elif method == "POST":
            if path == "/dodaj-auto":
                body = request.split("\r\n\r\n")[1]
                data = urllib.parse.parse_qs(body)
                
                proizvodac = data.get("proizvodac", [""])[0]
                model = data.get("model", [""])[0]
                godina = data.get("godina", [""])[0]
                boja = data.get("boja", [""])[0]
                cijena = data.get("cijena", [""])[0]

                car_data = {
                    "proizvodac": proizvodac,
                    "model": model,
                    "godina": godina,
                    "boja": boja,
                    "cijena": cijena
                }

                response_body = json.dumps({"message": "Auto spremljen!", "car_data": car_data}, ensure_ascii=False, indent=4)

                response = "HTTP/1.1 200 OK\r\nContent-Type: application/json; charset=utf-8\r\n\r\n" + response_body

            else:
                response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html; charset=utf-8\r\n\r\n" + \
                           "<html><body><h1>404 - Stranica nije pronađena</h1></body></html>"

        else:
            response = "HTTP/1.1 405 Method Not Allowed\r\nContent-Type: text/html; charset=utf-8\r\n\r\n" + \
                       "<html><body><h1>405 - Metoda nije dopuštena</h1></body></html>"

        if response: 
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
