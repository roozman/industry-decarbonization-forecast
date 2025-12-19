import pandas as pd

df = pd.read_csv("./../data/integrated-data/residential_panel_data.csv")

df_lag = df.copy()
df_lag['Energy_Lag1'] = df_lag.groupby(['End_Use', 'Fuel_Technology'])['Energy_ktoe'].shift(1)

df_processed = pd.get_dummies(df, columns=['Fuel_Technology'], prefix='Tech')
df_lag_processed = pd.get_dummies(df_lag, columns=['Fuel_Technology'], prefix='Tech')

df_lag_clean = df_lag_processed.dropna(subset=['Energy_Lag1'])

train_df = df_processed[df_processed['Year'] <= 2021].copy()
test_df  = df_processed[df_processed['Year'] > 2021].copy()

train_df_lag = df_lag_clean[df_lag_clean['Year'] <= 2021].copy()
test_df_lag  = df_lag_clean[df_lag_clean['Year'] > 2021].copy()

train_df.to_csv("./../data/preprocessed/train.csv", index=False)
test_df.to_csv("./../data/preprocessed/test.csv", index=False)

train_df_lag.to_csv("./../data/preprocessed/train_lag.csv", index=False)
test_df_lag.to_csv("./../data/preprocessed/test_lag.csv", index=False)