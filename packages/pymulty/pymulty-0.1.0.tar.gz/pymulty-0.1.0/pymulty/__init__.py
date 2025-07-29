import socket
import threading
import json

PORT = 12345
BUFFER = 1024

_connections = []
_socket = None
_get_state = None
_set_state = None

def _recv_loop(sock):
    while True:
        try:
            data = sock.recv(BUFFER)
            if not data:
                break
            msg = json.loads(data.decode())
            if _set_state:
                _set_state(msg)
        except:
            break

def host(get_state_fn, set_state_fn):
    global _get_state, _set_state
    _get_state = get_state_fn
    _set_state = set_state_fn

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(1)
    print("[HOST] Waiting for client...")

    conn, addr = server_socket.accept()
    print(f"[HOST] Client connected from {addr}")
    _connections.append(conn)

    threading.Thread(target=_recv_loop, args=(conn,), daemon=True).start()

def client(ip, get_state_fn, set_state_fn):
    global _socket, _get_state, _set_state
    _get_state = get_state_fn
    _set_state = set_state_fn

    _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _socket.connect((ip, PORT))
    print("[CLIENT] Connected to host.")

    threading.Thread(target=_recv_loop, args=(_socket,), daemon=True).start()

def send_state():
    state = _get_state()
    message = json.dumps(state).encode()
    for conn in _connections:
        conn.sendall(message)
    if _socket:
        _socket.sendall(message)
