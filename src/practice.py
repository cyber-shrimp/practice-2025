from scapy.all import sniff, IP, TCP, Raw
from collections import defaultdict
import subprocess
import re
import time

# Настройки
LIMIT = 30  # допустимое количество запросов
TIME_WINDOW = 10  # секунд
activity = defaultdict(list)


def block_ip(ip):
    print(f"[!] Блокировка IP: {ip}")
    subprocess.run(["sudo", "ipset", "add", "banned_ip", ip],
                   stderr=subprocess.DEVNULL)


def check_sql_injection(payload):
    # Простые сигнатуры
    return any(keyword in payload.lower() for keyword in ["' or 1=1", "union select", "--", "drop table"])


def process_packet(pkt):
    if pkt.haslayer(IP) and pkt.haslayer(TCP) and pkt.haslayer(Raw):
        ip = pkt[IP].src
        payload = pkt[Raw].load.decode(errors="ignore")

        now = time.time()
        activity[ip] = [t for t in activity[ip] if now - t < TIME_WINDOW]
        activity[ip].append(now)

        if len(activity[ip]) > LIMIT:
            block_ip(ip)

        if check_sql_injection(payload):
            print(f"[!] SQL-инъекция от {ip}")
            block_ip(ip)


print("[*] Запуск мониторинга трафика на 80 порту...")
sniff(filter="tcp port 80", prn=process_packet, store=0)
