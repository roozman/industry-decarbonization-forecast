from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI(title="Residential Energy Forecast API")

model_path = "./xgboost_residential_lag.bin"
model = joblib.load(model_path)

MODEL_FEATURES = [
    'Population', 'Households', 'Inhabitants per household', 'HDD', 'CDD', 
    'GDP', 'Expenditure', 'Energy_Lag1', 'Tech_Advanced electric heating', 
    'Tech_Air conditioning', 'Tech_Biomass', 'Tech_Conventional electric heating', 
    'Tech_Diesel oil', 'Tech_Distributed heat', 'Tech_Electricity', 
    'Tech_Electricity in circulation', 'Tech_Geothermal', 'Tech_Liquified petroleum gas (LPG)', 
    'Tech_Natural gas', 'Tech_Solar', 'Tech_Solids'
]

class ForecastRequest(BaseModel):
    Year: int
    Population: float
    Households: float
    Inhabitants_per_household: float 
    HDD: float
    CDD: float
    GDP: float
    Expenditure: float
    Energy_Lag1: float
    Fuel_Technology: str

def preprocess_input(data: ForecastRequest):

    input_data = {col: 0 for col in MODEL_FEATURES}

    input_data['Population'] = data.Population
    input_data['Households'] = data.Households
    input_data['Inhabitants per household'] = data.Inhabitants_per_household
    input_data['HDD'] = data.HDD
    input_data['CDD'] = data.CDD
    input_data['GDP'] = data.GDP
    input_data['Expenditure'] = data.Expenditure
    input_data['Energy_Lag1'] = data.Energy_Lag1

    #OHE
    tech_col_name = f"Tech_{data.Fuel_Technology}"
    if tech_col_name in input_data:
        input_data[tech_col_name] = 1
        
    df = pd.DataFrame([input_data])
    df = df[MODEL_FEATURES]
    return df

@app.post("/predict")
def predict_energy(request: ForecastRequest):
    X_input = preprocess_input(request)
    
    prediction_val = model.predict(X_input)[0]
    
    return {
        "status": "success",
        "year": request.Year,
        "technology": request.Fuel_Technology,
        "predicted_energy_ktoe": float(prediction_val)
    }

@app.get("/")
def home():
    return {"message": "Energy Forecasting API is Running"}