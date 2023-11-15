from scapy.all import sniff

def packet_callback(packet):
    print(packet.summary())

try:
    # Using Scapy's sniff function to capture packets
    sniff(prn=packet_callback, store=0)

except KeyboardInterrupt:
    print("Packet sniffing stopped")
