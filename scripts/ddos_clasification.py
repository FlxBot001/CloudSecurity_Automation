import joblib
import pandas as pd
from scapy.all import sniff
from sklearn.preprocessing import StandardScaler

# Load pre-trained model
model = joblib.load('../ml/models/ddos_model.pkl')
scaler = joblib.load('../ml/models/scaler.pkl')

# Real-time traffic capture using Scapy
def capture_traffic(duration=10):
    packets = sniff(timeout=duration)
    features = [extract_features(pkt) for pkt in packets]  # Extract features
    return pd.DataFrame(features)

# Extract relevant features from network packets
def extract_features(packet):
    return {
        'packet_size': len(packet),
        'protocol': packet.proto,
        'src_port': packet.sport if packet.haslayer('TCP') or packet.haslayer('UDP') else 0,
        'dst_port': packet.dport if packet.haslayer('TCP') or packet.haslayer('UDP') else 0,
        'src_ip': packet[0][1].src,
        'dst_ip': packet[0][1].dst
    }

# Predict DDoS type
def classify_ddos(df):
    scaled_data = scaler.transform(df[['packet_size', 'protocol', 'src_port', 'dst_port']].values)
    predictions = model.predict(scaled_data)
    return predictions.argmax(axis=1)

# Real-time classification
def run_classification():
    df_traffic = capture_traffic(duration=60)
    predictions = classify_ddos(df_traffic)
    print(f"Detected DDoS Attacks: {predictions}")

if __name__ == "__main__":
    run_classification()
