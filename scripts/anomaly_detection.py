import json
import boto3
import numpy as np

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('AnomalyData')
sns = boto3.client('sns')

def detect_traffic_anomalies(current_traffic, historical_data):
    mean_traffic = np.mean(historical_data)
    std_dev_traffic = np.std(historical_data)

    if std_dev_traffic == 0:
        return ["No variation in historical traffic data; cannot detect anomalies."]
    
    z_score = (current_traffic - mean_traffic) / std_dev_traffic
    threshold = 3  # Threshold for Z-score
    anomalies = []

    if abs(z_score) > threshold:
        anomalies.append('Unusual traffic spike detected')
    
    return anomalies

def detect_configuration_anomalies(current_config, historical_configs):
    anomalies = []
    # Example logic for detecting configuration anomalies
    if current_config['instance_type'] not in ['t2.micro', 't2.small', 't2.medium']:
        anomalies.append('Unsupported instance type detected')

    if current_config['security_group'] not in historical_configs['allowed_security_groups']:
        anomalies.append('Unrecognized security group configuration detected')

    return anomalies

def notify_admin(anomalies):
    topic_arn = 'arn:aws:sns:region:account-id:topic-name'  # Replace with your SNS topic ARN
    message = "Anomalies detected:\n" + "\n".join(anomalies)
    sns.publish(TopicArn=topic_arn, Message=message)

def lambda_handler(event, context):
    # Parse incoming data
    current_data = json.loads(event['body'])
    
    # Separate data types
    current_traffic = current_data.get('traffic', None)
    current_config = current_data.get('configuration', None)

    anomalies = []

    # Fetch historical data from DynamoDB
    response = table.scan()
    historical_data = [item['traffic'] for item in response['Items'] if item['type'] == 'traffic']
    historical_configs = {
        'allowed_security_groups': ['sg-01234', 'sg-56789'],  # Example allowed security groups
    }

    # Detect anomalies
    if current_traffic is not None:
        traffic_anomalies = detect_traffic_anomalies(current_traffic, historical_data)
        anomalies.extend(traffic_anomalies)

    if current_config is not None:
        config_anomalies = detect_configuration_anomalies(current_config, historical_configs)
        anomalies.extend(config_anomalies)

    # Log the results to CloudWatch
    print("Anomalies detected:", anomalies)
    
    # Notify admin if critical anomalies are found
    if anomalies:
        notify_admin(anomalies)

    # Save current traffic and config data to DynamoDB
    if current_traffic is not None:
        table.put_item(Item={'id': str(current_traffic), 'type': 'traffic', 'traffic': current_traffic})

    if current_config is not None:
        table.put_item(Item={'id': str(current_config['instance_id']), 'type': 'config', 'configuration': json.dumps(current_config)})

    return {
        'statusCode': 200,
        'body': json.dumps({"anomalies": anomalies})
    }