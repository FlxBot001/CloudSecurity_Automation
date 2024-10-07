import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
import numpy as np

# Load datasets for DDoS classification and misconfiguration detection
ddos_data_path = "data/DDos.csv"
misconfig_data_path = "data/misconfig.csv"

# ------------------ Load and Prepare DDoS Dataset ------------------
print("Loading DDoS dataset...")
ddos_df = pd.read_csv(ddos_data_path)

# Features and target for DDoS classification
X_ddos = ddos_df[['packet_size', 'protocol', 'src_port', 'dst_port']]  # Add more relevant features if needed
y_ddos = ddos_df['attack_type']

# Split the DDoS data
X_ddos_train, X_ddos_test, y_ddos_train, y_ddos_test = train_test_split(X_ddos, y_ddos, test_size=0.3, random_state=42)

# Feature scaling for DDoS
scaler_ddos = StandardScaler()
X_ddos_train = scaler_ddos.fit_transform(X_ddos_train)
X_ddos_test = scaler_ddos.transform(X_ddos_test)

# Initialize the DDoS classification model
ddos_model = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the DDoS model
print("Training DDoS classification model...")
ddos_model.fit(X_ddos_train, y_ddos_train)

# Make predictions and evaluate
y_ddos_pred = ddos_model.predict(X_ddos_test)
accuracy_ddos = accuracy_score(y_ddos_test, y_ddos_pred)
f1_ddos = f1_score(y_ddos_test, y_ddos_pred, average='macro')
precision_ddos = precision_score(y_ddos_test, y_ddos_pred, average='macro')
recall_ddos = recall_score(y_ddos_test, y_ddos_pred, average='macro')

print(f"DDoS Model Performance:\n Accuracy: {accuracy_ddos:.2f}\n F1 Score: {f1_ddos:.2f}\n Precision: {precision_ddos:.2f}\n Recall: {recall_ddos:.2f}")

# Save the DDoS classification model and scaler
ddos_model_path = 'models/ddos_model.pkl'
print(f"Saving DDoS model to {ddos_model_path}")
joblib.dump(ddos_model, ddos_model_path)
joblib.dump(scaler_ddos, 'models/scaler_ddos.pkl')

# ------------------ Load and Prepare Misconfiguration Dataset ------------------
print("\nLoading Misconfiguration dataset...")
misconfig_df = pd.read_csv(misconfig_data_path)

# Features and target for misconfiguration detection
X_misconfig = misconfig_df.drop(columns=['misconfig_flag'])  # Drop the target column
y_misconfig = misconfig_df['misconfig_flag']  # Target is a binary column indicating misconfigurations

# Split the misconfig data
X_misconfig_train, X_misconfig_test, y_misconfig_train, y_misconfig_test = train_test_split(X_misconfig, y_misconfig, test_size=0.3, random_state=42)

# Scale the features for misconfiguration detection
scaler_misconfig = StandardScaler()
X_misconfig_train = scaler_misconfig.fit_transform(X_misconfig_train)
X_misconfig_test = scaler_misconfig.transform(X_misconfig_test)

# Initialize the misconfiguration detection model
misconfig_model = LogisticRegression(random_state=42)

# Train the misconfiguration detection model
print("Training misconfiguration detection model...")
misconfig_model.fit(X_misconfig_train, y_misconfig_train)

# Make predictions and evaluate
y_misconfig_pred = misconfig_model.predict(X_misconfig_test)
accuracy_misconfig = accuracy_score(y_misconfig_test, y_misconfig_pred)
f1_misconfig = f1_score(y_misconfig_test, y_misconfig_pred, average='macro')
precision_misconfig = precision_score(y_misconfig_test, y_misconfig_pred, average='macro')
recall_misconfig = recall_score(y_misconfig_test, y_misconfig_pred, average='macro')

print(f"Misconfig Model Performance:\n Accuracy: {accuracy_misconfig:.2f}\n F1 Score: {f1_misconfig:.2f}\n Precision: {precision_misconfig:.2f}\n Recall: {recall_misconfig:.2f}")

# Save the misconfiguration detection model and scaler
misconfig_model_path = 'models/misconfig_model.pkl'
print(f"Saving misconfig model to {misconfig_model_path}")
joblib.dump(misconfig_model, misconfig_model_path)
joblib.dump(scaler_misconfig, 'models/scaler_misconfig.pkl')

print("Training and saving models completed.")
