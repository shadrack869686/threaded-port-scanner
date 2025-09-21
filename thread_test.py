# threaded_port_enum.py
from concurrent.futures import ThreadPoolExecutor
import socket
import csv

# =====================
# Helper functions
# =====================
def load_hosts(path_or_host):
    """Load host(s) kutoka file au directly IP"""
    try:
        with open(path_or_host, "r", encoding="utf-8") as f:
            hosts = [line.strip() for line in f if line.strip() and not line.startswith("#")]
            if hosts:
                return hosts
    except FileNotFoundError:
        pass
    return [path_or_host]

def check_port(host, port, timeout=1.5):
    """Jaribu ku-connect kwenye host+port"""
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

def grab_banner(host, port, timeout=1.5):
    """Jaribu kupata service banner"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            sock.connect((host, port))          # correct method
            banner = sock.recv(1024).decode().strip()
            return banner
    except Exception:
        return ""  # kama error, return empty string

def save_results_csv(results, filename="scan_results.csv"):
    """Save results kwenye CSV"""
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Host", "Port", "Status", "Banner"])
        for row in results:
            writer.writerow(row)

# =====================
# Main Threaded Scan
# =====================
hosts = load_hosts("127.0.0.1")   # change to "hosts.txt" or any IP
ports = [22, 80, 443, 3306]       # example ports
results = []

def scan_port_thread(host, port):
    """Threaded scan function with banner grabbing"""
    status = check_port(host, port)[2]             # "open" / "closed"
    banner = grab_banner(host, port) if status == "open" else ""
    result = (host, port, status, banner)
    results.append(result)
    print(result)  # optional: kuona progress

# Run threaded scan
with ThreadPoolExecutor(max_workers=10) as executor:
    for host in hosts:
        for port in ports:
            executor.submit(scan_port_thread, host, port)

# Save results
save_results_csv(results)
print("Results saved to scan_results.csv")
