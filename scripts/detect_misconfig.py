import json
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from app import db

# Define the ThreatIntel model for threat intelligence database
class ThreatIntel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    threat_type = db.Column(db.String(128), nullable=False)
    source = db.Column(db.String(256), nullable=False)
    risk_level = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return f'<ThreatIntel {self.threat_type} from {self.source}>'

# Function to load and preprocess historical configuration data
def load_historical_configurations():
    # Simulated loading from a database or file
    # In a real scenario, this could be a database query to fetch the configurations
    historical_data = {
        'instance_types': ['t2.micro', 't2.small', 't2.medium'],
        'security_groups': ['sg-01234', 'sg-56789'],
        'max_instances': [1, 2, 3]
    }
    return pd.DataFrame(historical_data)

# Function to detect configuration anomalies
def detect_configuration_anomalies(current_config):
    historical_data = load_historical_configurations()
    features = []

    # Check instance type
    instance_type = current_config.get('instance_type')
    if instance_type not in historical_data['instance_types'].values:
        features.append(1)  # Flag as anomaly
    else:
        features.append(0)  # Normal

    # Check security groups
    security_group = current_config.get('security_group')
    if security_group not in historical_data['security_groups'].values:
        features.append(1)  # Flag as anomaly
    else:
        features.append(0)  # Normal

    # Check max instances
    max_instances = current_config.get('max_instances', 1)
    if max_instances > max(historical_data['max_instances']):
        features.append(1)  # Flag as anomaly
    else:
        features.append(0)  # Normal

    return features

# Function to predict misconfigurations using AI model
def predict_misconfiguration(current_config):
    # Convert current config to DataFrame for model input
    config_df = pd.DataFrame([current_config])
    
    # Load your pre-trained Isolation Forest model (this should be trained in advance)
    # model = joblib.load('models/misconfig_model.pkl')  # Uncomment when model is available

    # For demonstration purposes, let's simulate model prediction
    # In practice, you'd use the loaded model for prediction
    # Here we use a dummy prediction based on features
    features = detect_configuration_anomalies(current_config)
    
    # Use a threshold to determine if a config is misconfigured
    if sum(features) > 0:
        return True  # Misconfiguration detected
    return False  # No misconfiguration

# Function to log misconfiguration in the database
def log_misconfiguration(current_config):
    threat = ThreatIntel(
        threat_type='Misconfiguration',
        source='Real-time Detection',
        risk_level='High'
    )
    db.session.add(threat)
    db.session.commit()

# Main function to handle incoming configuration data
def handle_configuration_data(event):
    try:
        current_config = json.loads(event['body'])
    except json.JSONDecodeError:
        return {'statusCode': 400, 'body': json.dumps({"error": "Invalid JSON format."})}
    
    if predict_misconfiguration(current_config):
        log_misconfiguration(current_config)
        return {
            'statusCode': 200,
            'body': json.dumps({"message": "Misconfiguration detected and logged."})
        }
    
    return {
        'statusCode': 200,
        'body': json.dumps({"message": "No misconfiguration detected."})
    }

# Example invocation
if __name__ == "__main__":
    # Simulate incoming configuration data
    example_event = {
        'body': json.dumps({
            'instance_type': 't2.large',  # Example of a misconfigured instance type
            'security_group': 'sg-01234',
            'max_instances': 2
        })
    }
    response = handle_configuration_data(example_event)
    print(response)
