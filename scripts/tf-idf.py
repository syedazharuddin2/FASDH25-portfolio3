# How has the overall similarity between articles changed over time?

import pandas as pd
import plotly.express as px
import os

# Load the TF-IDF similarity data
df = pd.read_csv("../data/dataframes/tfidf/tfidf-over-0.3.csv")
df = pd.read_csv("../data/dataframes/tfidf/tfidf-over-0.3-len100.csv")
df = pd.read_csv("../data/dataframes/tfidf/tfidf-over-0.3-len200.csv")

# Convert 'month-1' to datetime for grouping
df['month-1'] = pd.to_datetime(df['month-1'])

# Group by month and calculate average similarity
monthly_avg = df.groupby(df['month-1'].dt.to_period("M"))['similarity'].mean().reset_index()
monthly_avg['month'] = monthly_avg['month-1'].astype(str)
monthly_avg = monthly_avg.rename(columns={'similarity': 'Average Similarity'})

# Plotting the trend using Plotly
fig = px.line(monthly_avg, x='month', y='Average Similarity',
              title='Average TF-IDF Article Similarity by Month',
              labels={'month': 'Month', 'Average Similarity': 'Avg TF-IDF Similarity'},
              markers=True)


fig.show()

# Save plot data to CSV for reproducibility
os.makedirs("outputs", exist_ok=True)
monthly_avg.to_csv("outputs/tf-idf_avg.csv", index=False)
print("CSV file with monthly averages saved to 'outputs' folder.")
