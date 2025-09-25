from pydantic import BaseModel
from typing import Literal

# login input model
class LoginInput(BaseModel):
    username: str
    password: str

# Pydantic models for request and response schemas
class Token(BaseModel):
    access_token: str
    token_type: str

# Data stored in the token
class TokenData(BaseModel):
    username: str | None = None

# User model
class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

# User model with hashed password
class UserInDB(User):
    hashed_password: str

# prediction response model
class PredictionResponse(BaseModel):
    prediction: str
    probability: str | None = None

# Input data model for prediction
class UserInput(BaseModel):
    gender: Literal['Male', 'Female']
    SeniorCitizen: Literal[0, 1]
    Partner: Literal['Yes', 'No']
    Dependents: Literal['Yes', 'No']
    tenure: int
    PhoneService: Literal['Yes', 'No']
    MultipleLines: Literal['Yes', 'No', 'No phone service']
    InternetService: Literal['DSL', 'Fiber optic', 'No']
    OnlineSecurity: Literal['Yes', 'No', 'No internet service']
    OnlineBackup: Literal['Yes', 'No', 'No internet service']
    DeviceProtection: Literal['Yes', 'No', 'No internet service']
    TechSupport: Literal['Yes', 'No', 'No internet service']
    StreamingTV: Literal['Yes', 'No', 'No internet service']
    StreamingMovies: Literal['Yes', 'No', 'No internet service']
    Contract: Literal['Month-to-month', 'One year', 'Two year']
    PaperlessBilling: Literal['Yes', 'No']
    PaymentMethod: Literal['Electronic check', 'Mailed check', 'Bank transfer', 'Credit card']
    MonthlyCharges: float
    TotalCharges: float
