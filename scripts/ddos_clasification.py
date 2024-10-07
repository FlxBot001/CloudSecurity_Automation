import joblib
import pandas as pd
from scapy.all import sniff, conf
from sklearn.preprocessing import StandardScaler
import numpy as np
import logging
import time
import json
import smtplib
from email.mime.text import MIMEText
import signal
import sys
import os

# Load pre-trained model and scaler
model = joblib.load('../ml/models/ddos_model.pkl')
scaler = joblib.load('../ml/models/scaler.pkl')

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Email configuration for alert notifications
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
ALERT_RECIPIENT = os.getenv('ALERT_RECIPIENT')

# Real-time traffic capture using Scapy
def capture_traffic(duration=10):
    logger.info(f"Capturing traffic for {duration} seconds...")
    packets = sniff(timeout=duration)
    features = [extract_features(pkt) for pkt in packets if pkt is not None]  # Extract features
    return pd.DataFrame(features)

# Extract relevant features from network packets
def extract_features(packet):
    try:
        # Extract features from each packet
        features = {
            'packet_size': len(packet),
            'protocol': packet.proto,
            'src_port': packet.sport if packet.haslayer('TCP') or packet.haslayer('UDP') else 0,
            'dst_port': packet.dport if packet.haslayer('TCP') or packet.haslayer('UDP') else 0,
            'src_ip': packet[0][1].src,
            'dst_ip': packet[0][1].dst
        }
        return features
    except Exception as e:
        logger.error(f"Error extracting features from packet: {e}")
        return None

# Predict DDoS type
def classify_ddos(df):
    if df.empty:
        logger.warning("No data to classify.")
        return []

    # Select and scale the features
    features = df[['packet_size', 'protocol', 'src_port', 'dst_port']].values
    scaled_data = scaler.transform(features)

    # Predict using the model
    predictions = model.predict(scaled_data)
    return predictions

# Send alert notification
def send_alert(predictions):
    message = f"DDoS Attack Detected! Classes: {np.unique(predictions)}"
    msg = MIMEText(message)
    msg['Subject'] = 'DDoS Attack Alert'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = ALERT_RECIPIENT

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
            logger.info("Alert sent successfully.")
    except Exception as e:
        logger.error(f"Failed to send alert: {e}")

# Signal handler for graceful shutdown
def signal_handler(sig, frame):
    logger.info("Shutting down gracefully...")
    sys.exit(0)

# Real-time classification
def run_classification():
    signal.signal(signal.SIGINT, signal_handler)  # Handle CTRL+C gracefully

    while True:
        df_traffic = capture_traffic(duration=60)
        predictions = classify_ddos(df_traffic)

        if len(predictions) > 0:
            unique_classes = np.unique(predictions)
            logger.info(f"Detected DDoS Attack Classes: {unique_classes}")

            # Send alert if an attack is detected
            if unique_classes.size > 0:
                send_alert(predictions)
        else:
            logger.info("No DDoS attacks detected.")

        time.sleep(1)  # Adjust sleep time as needed

if __name__ == "__main__":
    run_classification()
