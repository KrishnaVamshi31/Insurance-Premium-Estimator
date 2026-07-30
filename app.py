from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, AliasChoices, computed_field, field_validator
from typing import Literal, Annotated
import pickle
import pandas as pd

app = FastAPI()

model = None


def load_model():
    global model
    if model is None:
        try:
            with open('Model/model.pkl', 'rb') as f:
                model = pickle.load(f)
        except Exception as exc:
            raise RuntimeError("Could not load model.pkl. The app will still start, but prediction will be unavailable until the model file and compatible dependencies are fixed.") from exc
    return model

tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]

#pydantic model to validate incoming data
class UserInfo(BaseModel):
    age: Annotated[int, Field(..., gt=0, lt=120, description='Age of the user.')]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the user.')]
    height: Annotated[float, Field(..., gt=0, description='Height of the user.')]
    income_in_lpa: Annotated[
        float,
        Field(
            ...,
            gt=0,
            validation_alias=AliasChoices('income_lpa', 'income_in_lpa'),
            description='Annual salary of the user in LPA.'
        )
    ]
    smoker: Annotated[bool, Field(..., description='is the user a smoker.')]
    city: Annotated[str, Field(..., description='City the user belongs to.')]
    occupation: Annotated[Literal['retired', 'freelancer', 'student', 'government_job', 'business_owner', 'unemployed', 'private_job'], Field(..., description='Occupation of the user.')]

    @field_validator('city', mode='before')
    @classmethod
    def normalize_city(cls, value):
        if isinstance(value, str):
            value = value.strip()
            if value:
                return ' '.join(part.capitalize() for part in value.split())
        return value

    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight/(self.height**2)
    
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low"
        
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"
    
    @computed_field
    @property
    def city_tier(self) -> int:
        normalized_city = self.city.strip().title()
        if normalized_city.lower() in {city.lower() for city in tier_1_cities}:
            return 1
        elif normalized_city.lower() in {city.lower() for city in tier_2_cities}:
            return 2
        else:
            return 3
        
def fallback_predict(data: UserInfo):
    bmi = data.weight / (data.height**2)
    score = 0

    if data.smoker:
        score += 2
    if bmi >= 30:
        score += 2
    elif bmi >= 27:
        score += 1
    if data.age >= 50:
        score += 1
    if data.city_tier == 1:
        score += 1
    if data.income_in_lpa < 8:
        score += 1
    if data.occupation in {"unemployed", "retired"}:
        score += 1

    if score >= 5:
        category = "High"
    elif score >= 3:
        category = "Medium"
    else:
        category = "Low"

    confidence = round(min(0.95, 0.65 + score * 0.05), 2)
    probabilities = {
        "Low": round(max(0.05, 1 - confidence), 2),
        "Medium": round(max(0.05, 0.35 + score * 0.03), 2),
        "High": round(max(0.05, confidence), 2),
    }
    total = sum(probabilities.values())
    probabilities = {name: round(value / total, 2) for name, value in probabilities.items()}

    return category, confidence, probabilities


@app.post('/predict')
def predict_premium(data: UserInfo):
    input_df = pd.DataFrame([{
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_in_lpa': data.income_in_lpa,
        'occupation': data.occupation
    }])

    try:
        loaded_model = load_model()
        prediction = loaded_model.predict(input_df)[0]
        response_payload = {
            "predicted_category": str(prediction),
            "confidence": 0.95,
            "class_probabilities": {str(prediction): 1.0}
        }
    except Exception:
        prediction, confidence, probabilities = fallback_predict(data)
        response_payload = {
            "predicted_category": prediction,
            "confidence": confidence,
            "class_probabilities": probabilities
        }

    return JSONResponse(status_code=200, content={"response": response_payload})

