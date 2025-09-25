from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


from pydantic import ValidationError
from auth2 import *
from models.model import predict
from model_req import LoginInput, UserInput, PredictionResponse


import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Authentication Endpoints
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: LoginInput = Depends()):

    # authenticate user
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

bearer_scheme = HTTPBearer()
# Dependency to get current user from Bearer token
def get_current_active_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    user = login_for_access_token(token)  # You should implement this function in auth2.py
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user

## Model Prediction Endpoint
@app.post("/predict", response_model=PredictionResponse)
async def model_predict(
    payload: UserInput,
    token:User = Depends(get_current_active_user)
):
    try:
        # Convert Pydantic model to dictionary
        payload_dict = payload.model_dump(exclude_none=True)
        churn_prediction, churn_prediction_proba = predict(payload_dict)

        prediction_msg = (
            "The user is likely to churn." if churn_prediction == 1
            else "The user is not likely to churn."
        )

        probability_msg = (
            f"{churn_prediction_proba:.2f}" if churn_prediction_proba is not None else None
        )

        return PredictionResponse(
            prediction=prediction_msg,
            probability=probability_msg
        )

    except ValidationError as ve:
        raise HTTPException(status_code=400, detail=f"Validation error: {ve}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

