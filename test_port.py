from enum_helpers import check_port

print(check_port("127.0.0.1", 22))  # test SSH
print(check_port("127.0.0.1", 80))  # test HTTP
