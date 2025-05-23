import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import os
import numpy as np

df = pd.read_csv('StudentsPerformance.csv')

# Add dummy attendance and study_hours columns for demonstration
np.random.seed(42)
df['attendance'] = np.random.randint(60, 101, size=len(df))
df['study_hours'] = np.random.randint(1, 11, size=len(df))

X = df[['math score', 'reading score', 'writing score', 'attendance', 'study_hours']]
y = (df['math score'] >= 60).astype(int)  # 1: Pass, 0: Fail

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier()
model.fit(X_train, y_train)

os.makedirs('predictor/ml_model', exist_ok=True)
joblib.dump(model, 'predictor/ml_model/model.pkl')
print("Model trained and saved!")
