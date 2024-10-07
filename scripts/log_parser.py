import json
import pandas as pd
from sklearn.ensemble import IsolationForest
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class LogParser:
    def __init__(self):
        # Initialize the anomaly detection model
        self.model = IsolationForest(contamination=0.05)
        self.history = []  # Store historical log data for anomaly detection

    def parse_logs(self, log_data):
        """Parse logs from Huawei Cloud LTS or any source and extract relevant information."""
        parsed_logs = []

        # Simulate parsing JSON log data (this should be adjusted based on actual log format)
        try:
            logs = json.loads(log_data)  # Assuming log_data is in JSON format
            for entry in logs:
                source = entry.get('source', 'Unknown')
                message = entry.get('message', 'No message')
                parsed_logs.append({'source': source, 'message': message})

                # Store historical log entries for anomaly detection
                self.history.append(entry)

        except json.JSONDecodeError:
            logger.error("Invalid log data format. Unable to parse.")
            return []

        return parsed_logs

    def detect_anomalies(self):
        """Detect anomalies in the log data using Isolation Forest."""
        if len(self.history) < 2:
            logger.info("Not enough data to detect anomalies.")
            return []

        # Convert historical data to DataFrame for model input
        df = pd.DataFrame(self.history)
        
        # Assuming the log entries have a 'severity' level, we need to convert it to numerical for ML
        if 'severity' in df.columns:
            df['severity'] = df['severity'].map({'low': 1, 'medium': 2, 'high': 3})  # Example mapping

        # Fit the model with relevant features; adjust based on log structure
        features = df[['severity', 'source']] if 'severity' in df.columns else df[['source']]
        
        # Encode categorical variables (e.g., source) for ML processing
        features = pd.get_dummies(features)

        # Train the model if there's sufficient data
        self.model.fit(features)

        # Predict anomalies
        predictions = self.model.predict(features)
        anomalies = df[predictions == -1]  # Identify anomalies
        
        return anomalies.to_dict(orient='records')

if __name__ == "__main__":
    # Sample log data in JSON format for demonstration
    sample_log_data = json.dumps([
        {'source': 'Firewall', 'message': 'Blocked unauthorized access', 'severity': 'high'},
        {'source': 'Web Server', 'message': 'Received request from 192.168.1.1', 'severity': 'low'},
        {'source': 'Database', 'message': 'Query execution time exceeded', 'severity': 'medium'},
        {'source': 'Firewall', 'message': 'Blocked access from suspicious IP', 'severity': 'high'}
    ])

    log_parser = LogParser()
    logs = log_parser.parse_logs(sample_log_data)
    print("Parsed Logs:", logs)

    # Detect anomalies in the parsed logs
    anomalies = log_parser.detect_anomalies()
    if anomalies:
        print("Detected Anomalies:", anomalies)
    else:
        print("No anomalies detected.")
