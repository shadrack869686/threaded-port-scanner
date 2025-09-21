def load_hosts(path_or_host):
    try:
        with open(path_or_host, "r", encoding="utf-8") as f:
            hosts = [line.strip() for line in f if line.strip() and not line.startswith("#")]
            if hosts:
                return hosts
    except FileNotFoundError:
        pass
    return [path_or_host]

print(load_hosts("127.0.0.1"))
