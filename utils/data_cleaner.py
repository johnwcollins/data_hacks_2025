import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


df = pd.read_csv("../data/pokemon_data.csv")
#print(df.head())
print(df.columns)
df.drop(columns=['Height (m)', 'Weight (kg)', 'Generation', 'Classification'], inplace=True)
#print(df.head())
df['Pokedex Number'] = df['Pokedex Number'].astype(str).str.zfill(3)
#print(df.head())


# Convert 'Legendary' to boolean
df['Legendary'] = df['Legendary Status'].apply(lambda x: 1 if x == 'Yes' else 0)
#print(df.head())
df.drop(columns=['Legendary Status'], inplace=True)
#print(df)

# Split the data into training and test sets
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

# Function to split rows with both Type1 and Type2
def split_types(df):
    type2_rows = df[df['Type2'].notna()].copy()
    type2_rows['Type1'] = type2_rows['Type2']
    type2_rows['Type2'] = None
    result_df = pd.concat([df, type2_rows], ignore_index=True)
    result_df.drop(columns=['Type2'], inplace=True)
    result_df.rename(columns={'Type1': 'Type'}, inplace=True)  # Rename 'Type1' column to 'Type'
    return result_df

# Apply the row splitting function to both training and test sets
train_df = split_types(train_df)

# Combine 'Type1' and 'Type2' columns into 'Type' column with comma separation
test_df['Type'] = test_df[['Type1', 'Type2']].apply(lambda x: ', '.join(x.dropna()), axis=1)
print(test_df.columns)

# Drop 'Type1' and 'Type2' columns
test_df.drop(columns=['Type1', 'Type2'], inplace=True)
train_df = train_df.sort_values('Pokedex Number')
test_df = test_df.sort_values('Pokedex Number')
# Print the resulting DataFrames
print(train_df.head())
print(test_df.head())
# Save the resulting DataFrames as CSV files
train_df.to_csv('/Users/johncollins/Documents/GitHub/data_hacks_2025/train_dataset.csv', index=False)
test_df.to_csv('/Users/johncollins/Documents/GitHub/data_hacks_2025/test_dataset.csv', index=False)