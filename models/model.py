import pickle
from sklearn.preprocessing import LabelEncoder, StandardScaler
import pandas as pd
import os



script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)


with open('final_model.pkl', 'rb') as f:
    final_model = pickle.load(f)

with open('label_encoders.pkl', 'rb') as f:
    label_encoders = pickle.load(f)

with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)


# Function to make predictions
def predict(user_input):
    print("User Input:", user_input)  # Debugging line to check input

    # Convert input dictionary to DataFrame
    user_input_df = pd.DataFrame([user_input])

    # Ensure all expected columns are present
    for col, encoder in label_encoders.items():
        if col in user_input_df.columns:
            known_categories = set(encoder.classes_)
            new_categories = set(user_input_df[col].unique())
            unseen_categories = new_categories - known_categories

            # Handle unseen categories by mapping them to a default value (e.g., the first known category)
            if unseen_categories:
                default_value = encoder.classes_[0]
                user_input_df[col] = user_input_df[col].apply(lambda x: x if x in known_categories else default_value)
            # Transform the column using the label encoder
            user_input_df[col] = encoder.transform(user_input_df[col])

    # Scale numerical features
    user_input_scaled = scaler.transform(user_input_df)

    # Make prediction
    user_churn_prediction = final_model.predict(user_input_scaled)

    # Check if the model has predict_proba method
    if hasattr(final_model, "predict_proba"):
        user_churn_prediction_proba = final_model.predict_proba(user_input_scaled)
        return user_churn_prediction[0], user_churn_prediction_proba[0]
    else:
        return user_churn_prediction[0], None