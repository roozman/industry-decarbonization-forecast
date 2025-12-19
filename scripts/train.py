import pandas as pd
import joblib
from xgboost import XGBRegressor

df_train_lag = pd.read_csv("./../data/preprocessed/train_lag.csv")
df_test_lag = pd.read_csv("./../data/preprocessed/test_lag.csv")

target = "Energy_ktoe"

cols_to_drop = ["Year", "End_Use","Energy_ktoe"]
feature_cols_lag = [col for col in df_train_lag.columns if col not in cols_to_drop]

xgb_lag = XGBRegressor(
    n_estimators=100,
    learning_rate=0.05,
    max_depth=3,
    random_state=42,
    n_jobs=-1
)

xgb_lag.fit(df_train_lag[feature_cols_lag], df_train_lag[target])

#Exporting the best model

filename = './../model/xgboost_residential_lag.bin'

joblib.dump(xgb_lag, filename)

print(f"Model saved successfully as {filename}")