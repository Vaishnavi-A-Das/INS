
import socket
import ssl

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain("cert.pem", "key.pem")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("127.0.0.1", 8443))
    sock.listen(1)

    print("TLS server waiting on port 8443...")

    with context.wrap_socket(sock, server_side=True) as server:
        conn, addr = server.accept()
        with conn:
            print("Secure connection from:", addr)
            print("TLS version:", conn.version())

            data = conn.recv(1024)
            print("Received:", data.decode())

            conn.sendall(b"Secure response from server")
