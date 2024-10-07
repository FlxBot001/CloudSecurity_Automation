import json
import boto3  # For AWS
import azure.storage.blob  # For Azure
import google.cloud.storage  # For GCP
import cx_Oracle  # For Oracle
import numpy as np
import logging
from sklearn.ensemble import IsolationForest

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Initialize AWS services
aws_dynamodb = boto3.resource('dynamodb')
aws_table = aws_dynamodb.Table('AnomalyData')
aws_sns = boto3.client('sns')

# Set up global constants for cloud provider types
CLOUD_PROVIDERS = {
    'AWS': 'AWS',
    'Azure': 'Azure',
    'GCP': 'GCP',
    'Oracle': 'Oracle'
}

def detect_traffic_anomalies(current_traffic, historical_data):
    """Detects anomalies in traffic data using Isolation Forest."""
    model = IsolationForest(contamination=0.05)
    
    # Reshape data for model input
    historical_data = np.array(historical_data).reshape(-1, 1)
    model.fit(historical_data)
    
    # Predict anomaly
    current_data = np.array([[current_traffic]])
    prediction = model.predict(current_data)

    anomalies = []
    if prediction[0] == -1:
        anomalies.append(f'Unusual traffic spike detected: {current_traffic}')
    
    logger.info(f"Traffic anomaly prediction: {prediction[0]}, Current Traffic: {current_traffic}")
    return anomalies

def detect_configuration_anomalies(current_config, historical_configs):
    """Detects anomalies in the current configuration across different cloud providers."""
    anomalies = []
    
    # Example checks for instance types and security groups (customize as needed)
    if current_config['instance_type'] not in historical_configs['allowed_instance_types']:
        anomalies.append(f'Unsupported instance type detected: {current_config["instance_type"]}')

    if current_config['security_group'] not in historical_configs['allowed_security_groups']:
        anomalies.append(f'Unrecognized security group configuration detected: {current_config["security_group"]}')

    logger.info(f"Configuration anomalies: {anomalies}")
    return anomalies

def notify_admin(anomalies):
    """Notifies admin of detected anomalies using SNS or appropriate service."""
    topic_arn = 'arn:aws:sns:region:account-id:topic-name'  # Replace with your SNS topic ARN
    message = "Anomalies detected:\n" + "\n".join(anomalies)
    aws_sns.publish(TopicArn=topic_arn, Message=message)
    logger.info("Admin notified about detected anomalies.")

def fetch_historical_data(cloud_provider):
    """Fetches historical data based on the cloud provider."""
    if cloud_provider == CLOUD_PROVIDERS['AWS']:
        response = aws_table.scan()
        historical_data = [item['traffic'] for item in response['Items'] if item['type'] == 'traffic']
        historical_configs = {
            'allowed_instance_types': ['t2.micro', 't2.small', 't2.medium'],  # Example types
            'allowed_security_groups': ['sg-01234', 'sg-56789']
        }
    
    elif cloud_provider == CLOUD_PROVIDERS['Azure']:
        # Implement Azure logic to fetch historical data
        # Example: Use Azure Blob Storage or Cosmos DB
        historical_data = []  # Fetch from Azure
        historical_configs = {'allowed_instance_types': [], 'allowed_security_groups': []}
        
    elif cloud_provider == CLOUD_PROVIDERS['GCP']:
        # Implement GCP logic to fetch historical data
        # Example: Use Google Cloud Storage or BigQuery
        historical_data = []  # Fetch from GCP
        historical_configs = {'allowed_instance_types': [], 'allowed_security_groups': []}
        
    elif cloud_provider == CLOUD_PROVIDERS['Oracle']:
        # Implement Oracle logic to fetch historical data
        connection = cx_Oracle.connect('username/password@host:port/service_name')
        cursor = connection.cursor()
        cursor.execute("SELECT traffic FROM anomaly_data WHERE type='traffic'")
        historical_data = [row[0] for row in cursor.fetchall()]
        historical_configs = {'allowed_instance_types': [], 'allowed_security_groups': []}

    return historical_data, historical_configs

def lambda_handler(event, context):
    """Main handler for the anomaly detection Lambda function."""
    # Determine cloud provider from environment or event (customize as needed)
    cloud_provider = event.get('cloud_provider', CLOUD_PROVIDERS['AWS'])  # Default to AWS
    
    # Parse incoming data
    try:
        current_data = json.loads(event['body'])
    except json.JSONDecodeError:
        logger.error("Error decoding JSON from event body.")
        return {'statusCode': 400, 'body': json.dumps({"error": "Invalid JSON format."})}

    current_traffic = current_data.get('traffic', None)
    current_config = current_data.get('configuration', None)

    anomalies = []

    # Fetch historical data
    historical_data, historical_configs = fetch_historical_data(cloud_provider)

    # Detect anomalies
    if current_traffic is not None:
        traffic_anomalies = detect_traffic_anomalies(current_traffic, historical_data)
        anomalies.extend(traffic_anomalies)

    if current_config is not None:
        config_anomalies = detect_configuration_anomalies(current_config, historical_configs)
        anomalies.extend(config_anomalies)

    # Log results
    logger.info("Anomalies detected: %s", anomalies)

    # Notify admin if anomalies found
    if anomalies:
        notify_admin(anomalies)

    # Save current traffic and config data based on the cloud provider
    try:
        if current_traffic is not None:
            if cloud_provider == CLOUD_PROVIDERS['AWS']:
                aws_table.put_item(Item={'id': str(current_traffic), 'type': 'traffic', 'traffic': current_traffic})
            elif cloud_provider == CLOUD_PROVIDERS['Azure']:
                # Implement Azure save logic
                pass
            elif cloud_provider == CLOUD_PROVIDERS['GCP']:
                # Implement GCP save logic
                pass
            elif cloud_provider == CLOUD_PROVIDERS['Oracle']:
                # Implement Oracle save logic
                pass
            logger.info(f"Saved current traffic data: {current_traffic}")

        if current_config is not None:
            if cloud_provider == CLOUD_PROVIDERS['AWS']:
                aws_table.put_item(Item={'id': str(current_config['instance_id']), 'type': 'config', 'configuration': json.dumps(current_config)})
            elif cloud_provider == CLOUD_PROVIDERS['Azure']:
                # Implement Azure save logic
                pass
            elif cloud_provider == CLOUD_PROVIDERS['GCP']:
                # Implement GCP save logic
                pass
            elif cloud_provider == CLOUD_PROVIDERS['Oracle']:
                # Implement Oracle save logic
                pass
            logger.info(f"Saved current configuration data: {current_config}")

    except Exception as e:
        logger.error(f"Error saving data: {e}")

    return {
        'statusCode': 200,
        'body': json.dumps({"anomalies": anomalies})
    }
