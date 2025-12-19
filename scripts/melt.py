import pandas as pd
import numpy as np

df = pd.read_csv("./../data/integrated-data/data_raw.csv")

rows = ['Population', 'Number of households', 'Inhabitants per household',
    'Actual heating degree-days', 'Actual cooling degree-days',
    'Gross domestic product', 'Household consumption expenditure']

parent_categories = ['Space heating', 'Space cooling', 'Water heating', 'Cooking']

df_transpose = df[df.iloc[:, 0].isin(rows)].copy()
df_transpose.set_index(df_transpose.columns[0], inplace=True)
df_transpose = df_transpose.T
df_transpose.index.name = "Year"
df_transpose.reset_index(inplace=True)

for col in df_transpose.columns:
    if col != 'Year':
        df_transpose[col] = df_transpose[col].astype(str).str.replace(',', '').astype(float)

rename_map = {
    'Actual heating degree-days': 'HDD',
    'Actual cooling degree-days': 'CDD',
    'Gross domestic product': 'GDP',
    'Household consumption expenditure': 'Expenditure',
    'Number of households': 'Households'
}

df_transpose.rename(columns=rename_map, inplace=True)

panel_data = []
current_end_use = None

for index, row in df.iterrows():
    label = str(row.iloc[0]).strip()
    
    if label in parent_categories:
        current_end_use = label
        continue 

    if current_end_use and label not in rows and label != 'Final energy consumption (ktoe)':
    
        row_data = row.iloc[1:].to_dict()
        for year, value in row_data.items():
            panel_data.append({
                'Year': year,
                'End_Use': current_end_use,
                'Fuel_Technology': label,
                'Energy_ktoe': value
            })

df_energy = pd.DataFrame(panel_data)
df_energy['Energy_ktoe'] = df_energy['Energy_ktoe'].astype(str).str.replace(',', '')
df_energy['Energy_ktoe'] = pd.to_numeric(df_energy['Energy_ktoe'], errors='coerce')

df_transpose['Year'] = df_transpose['Year'].astype(int)
df_energy['Year'] = df_energy['Year'].astype(int)

df_final = pd.merge(df_energy, df_transpose, on='Year', how='left')
df_final = df_final.sort_values(by=['Year', 'End_Use', 'Fuel_Technology'])

df_final["Energy_ktoe"].fillna(0, inplace=True)
df_final.reset_index(drop=True, inplace=True)

df_final.to_csv('./../data/integrated-data/residential_panel_data.csv', index=False)