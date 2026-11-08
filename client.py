
import socket
import ssl

context = ssl.create_default_context(cafile="cert.pem")

with socket.create_connection(("127.0.0.1", 8443)) as sock:
    with context.wrap_socket(
        sock, server_hostname="localhost"
    ) as secure_sock:

        print("Connected using:", secure_sock.version())

        secure_sock.sendall(b"Hello from client")
        response = secure_sock.recv(1024)

        print("Server response:", response.decode())
