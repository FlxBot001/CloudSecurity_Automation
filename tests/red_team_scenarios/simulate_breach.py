import json
import random
import logging
from sklearn.ensemble import IsolationForest
import numpy as np

# Set up logging
logging.basicConfig(filename='breach_simulation.log', level=logging.INFO)

def generate_fake_traffic(num_samples=1000):
    """ Generate fake network traffic data for anomaly detection. """
    packet_sizes = np.random.randint(40, 1500, size=num_samples)  # Random packet sizes
    protocols = random.choices(['TCP', 'UDP'], k=num_samples)
    src_ports = np.random.randint(1024, 65535, size=num_samples)
    dst_ports = np.random.randint(1024, 65535, size=num_samples)

    return np.column_stack((packet_sizes, protocols, src_ports, dst_ports))

def detect_anomalies(data):
    """ Detect anomalies in network traffic using Isolation Forest. """
    model = IsolationForest(contamination=0.05)
    model.fit(data)
    anomalies = model.predict(data)

    # Convert anomalies to a list of indexes where -1 indicates an anomaly
    return np.where(anomalies == -1)[0]

def simulate_breach():
    """ Simulate a cloud breach and log the results. """
    # Generate fake traffic data
    traffic_data = generate_fake_traffic()

    # Detect anomalies
    anomalies = detect_anomalies(traffic_data[:, [0, 2, 3]])  # Packet size, src port, dst port
    if len(anomalies) > 0:
        logging.info(f"Simulated breach detected with {len(anomalies)} anomalies in the traffic.")
        return {
            "status": "breach detected",
            "anomalies_count": len(anomalies),
            "anomalies": anomalies.tolist()
        }
    else:
        logging.info("No anomalies detected; system remains secure.")
        return {
            "status": "no breach detected",
            "anomalies_count": 0
        }

if __name__ == "__main__":
    result = simulate_breach()
    print(json.dumps(result, indent=4))
