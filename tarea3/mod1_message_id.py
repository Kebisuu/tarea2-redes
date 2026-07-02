from scapy.all import *
from netfilterqueue import NetfilterQueue

def procesar_paquete(packet):
    scapy_pkt = IP(packet.get_payload())
    
    if scapy_pkt.haslayer(TCP) and scapy_pkt.haslayer(Raw):
        if scapy_pkt[TCP].dport == 1935 or scapy_pkt[TCP].sport == 1935:
            payload = bytearray(scapy_pkt[Raw].load)
            
            # --- MODIFICACIÓN ESPECÍFICA 1: Message Type ID ---
            if len(payload) > 50:
                tipo_original = payload[7]
                payload[7] = 255 
                
                print(f"[!] MODIFICACIÓN 1: 'Message Type ID' alterado de {tipo_original} a 255.")
            
            scapy_pkt[Raw].load = bytes(payload)
            del scapy_pkt[IP].len
            del scapy_pkt[IP].chksum
            del scapy_pkt[TCP].chksum
            packet.set_payload(bytes(scapy_pkt))
            
    packet.accept()

nfqueue = NetfilterQueue()
nfqueue.bind(1, procesar_paquete)

print("[*] Interceptor Klis activado: Modificación 1 (Message Type ID)...")
try:
    nfqueue.run()
except KeyboardInterrupt:
    print("\n[*] Apagando interceptor...")
nfqueue.unbind()
