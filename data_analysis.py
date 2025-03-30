import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Load the dataset
data = pd.read_csv('disease_dataset.csv')

# Handle missing values
numeric_columns = data.select_dtypes(include=[np.number]).columns
data[numeric_columns] = data[numeric_columns].fillna(data[numeric_columns].mean())

# Encode categorical variables
data = pd.get_dummies(data, drop_first=True)

# Define features and target
target_columns = ['disease_Healthy', 'disease_Leaf Spot', 'disease_Powdery Mildew', 'disease_Root Rot']
X = data.drop(target_columns, axis=1)
y = data[target_columns]

# Save feature names
joblib.dump(X.columns.tolist(), 'feature_columns.pkl')

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Save the scaler
joblib.dump(scaler, 'scaler.pkl')

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Save the trained model
joblib.dump(model, 'disease_model.pkl')

# Evaluate the model
y_pred = model.predict(X_test_scaled)
print("Classification Report:\n", classification_report(y_test, y_pred))
print("Model Accuracy:", accuracy_score(y_test, y_pred))
