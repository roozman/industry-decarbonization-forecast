# Residential Energy Consumption Forecasting

## Project Overview

This project aims to develop machine learning models to predict **residential energy consumption** measured in **ktoe (kilotonnes of oil equivalent)**. Accurate forecasting of residential energy demand can support:

- Grid load management  
- Infrastructure planning  
- Energy trading and policy analysis  

The project combines **exploratory data analysis**, **classical machine learning models**, and a **foundation time-series model (TimesFM)** to benchmark predictive performance.

---

## Evaluation Metrics

To ensure robustness across different consumption scales, the following metrics were used:

- **MAE (Mean Absolute Error)**  
  Measures the average prediction error in real units (ktoe). Easily interpretable for operational use.

- **RMSE (Root Mean Square Error)**  
  Penalizes large errors more heavily than MAE. Particularly important for avoiding severe underestimation of peak demand.

- **MAPE (Mean Absolute Percentage Error)**  
  Expresses error as a percentage, enabling comparison across sectors with vastly different energy magnitudes.

- **WMAPE (Weighted Mean Absolute Percentage Error)**  
  Weights errors by actual energy consumption, preventing small-volume sectors from disproportionately skewing results.

---

## Data Source

The dataset is sourced from the **JRC Data Catalogue**, the official open-access repository of the European Commission’s Joint Research Centre.

- Dataset link:  
  https://data.jrc.ec.europa.eu/dataset/1f0b480c-6d21-4d95-897d-20c7ca33df6f

---

## Exploratory Data Analysis (EDA)

Exploratory analysis is performed in `EDA.ipynb` located in the `./notebooks/` directory.

### Focus Areas

- Long-term trends in residential energy consumption  
- Impact of climate variables (HDD / CDD)  
- Relationship between economic activity and energy demand  

---

## Model Selection and Training

Models were trained and evaluated using two datasets:
- With lag features
- Without lag features

### Trained Models

- Linear Regression  
- Decision Tree Regressor  
- XGBoost Regressor  
- TimesFM (benchmark)

The metrics for the performane of the models can be find in `train.ipynb` located in the `./notebooks/` directory.

---

## Running the Project

### Local
1. **Clone the repository**

```bash
  git clone https://github.com/roozman/industry-decarbonization-forecast.git
  cd industry-decarbonization-forecast
```

2. **Setting up the environment**
```bash 
  pip install -r requirements.txt
```

3. **Running the service**
```bash 
  python ./api/main.py
```
The service will start at http://127.0.0.1:8000.


### Docker

1. **Build the docker image**
```bash
  docker build -t energy-consumption-api .
```

2. **Run the container**
```bash
  docker run -p 8000:8000 energy-consumption-api
```

The service will start at http://127.0.0.1:8000.

### Accessing the deployed service on Render.com <br>
The project is also deployed and accessible online via Render. You can interact with the service directly at:
<a href="https://energy-forecast-api.onrender.com/">Energy Consumption Forecast Service</a>

## API Usage Example

The API provides a `/predict` endpoint to predict CO2 emissions based on vehicle specifications. You can easily test and interact with the API using FastAPI's built-in documentation.

### Using FastAPI Docs

1. **Start the Service**
   Make sure the service is running locally or via Docker:
```bash
   python ./api/main.py
```

2. **Access API docs**
```bash
   http://127.0.0.1:8000/docs
```

3. **Test the predict endpoint** <br>
You can edit the placeholder values for the model and then press **Execute** to test the model.   
4. **View the response** <br>
The API will return a JSON response with the predicted CO2 emissions.

## Project Structure

├── README.md <br>
├── LICENSE <br>
├── api/ <br>
│   └── .dockerignore <br>
│   └── dockerfile <br>
│   └── main.py <br>
│   └── requirements.txt <br>
│   └── xgboost_residential_lag.bin #saved model <br>
├── data/       #Directory for datasets <br>
│   └── integrated-data/ #Where raw data was put together before preprocessing <br>
│       └── data_raw.csv <br>
│       └── residential_panel_data.csv <br>
│   └── preprocessed <br>
│       └── test_lag.csv <br>
│       └── test.csv <br>
│       └── train_lag.csv <br>
│       └── train.csv <br>
│   └── raw <br>
│       └── JRC-IDEES-2023_Macro_DE.csv <br>
│       └── JRC-IDEES-2023_Residential_DEt.csv <br>
├── model/       #Directory for the exported model <br>
│   └── xgboost_residential_lag.bin #Best model <br>
├── notebooks/       #Directory for jupyter notebooks <br>
│   └── EDA.ipynb       #Exploratory Data Analysis <br>
│   └── melt.ipynb       #Melting the raw data into panel data <br>
│   └── preprocessing.ipynb       #Preprocessing the data into the train and test datasets <br>
│   └── train.ipynb       #Training the models and evaluating them <br>
├── scripts/       #Directory for python scripts <br>
│   └── melt.py       #Melting the raw data into panel data <br>
│   └── preprocessing.py       #Preprocessing the data into the train and test datasets <br>
└ └── train.py       #Training and exporting the model <br>