import socket

def load_hosts(path_or_host):
    try:
        with open(path_or_host, "r", encoding="utf-8") as f:
            hosts = [line.strip() for line in f if line.strip() and not line.startswith("#")]
            if hosts:
                return hosts
    except FileNotFoundError:
        pass
    return [path_or_host]

def check_port(host, port, timeout=1.5):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            if result == 0:
                return (host, port, "open")
            else:
                return (host, port, "closed")
    except Exception as e:
        return (host, port, f"error: {e}")
import socket

def grab_banner(host, port, timeout=1.5):
    """
    Jaribu kupata service banner kutoka kwenye port iliyofunguka
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            sock.connect((host, port))
            banner = sock.recv(1024).decode().strip()
            return banner
    except Exception as e:
        return f"error: {e}"
