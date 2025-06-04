# We will Try to Explore Here:
# Question: How does average article length vary by month, and are there outliers?


import pandas as pd  
import plotly.express as px  

# Read data 
df = pd.read_csv("../data/dataframes/length/length-year-month.csv")  


# Explore columns and stats  
print("Columns:", df.columns.tolist())

#Print the Summary Statistics of the DataFrame
print("Summary Stats:\n", df.describe())  

# Check for missing values  
print("Missing Values:\n", df.isnull().sum())  

# Plot average length by month-year  
df['date'] = pd.to_datetime(df[['year','month']].assign(day=1))  # Create date for sorting  
fig = px.bar(df, x='date', y='length-mean',  
              title='Average Article Length by Year',  
              labels={'length-mean': 'Average Length (characters)', 'date': 'year'},
             barmode='group')
fig.show()
fig.write_html("../outputs/exploration/article_lengths_over_time.html")
# Define war start date
war_start = pd.to_datetime("2023-10-01")  # Start from beginning of October to include whole month

# Filter wartime months
wartime_df = df[df['date'] >= war_start]

# Plot bar chart for each month after war start
fig = px.bar(wartime_df, x='date', y='length-mean',
             title='Monthly Average Article Length After October 2023 (Wartime)',
             labels={'length-mean': 'Average Length (characters)', 'date': 'Month'},
             barmode='group')

fig.show()
fig.write_html("../outputs/exploration/article_lengths_wartime_only.html")
# Optional: Save wartime data separately
wartime_df.to_csv("../outputs/exploration/article_lengths_wartime_only.csv", index=False)

# Create datetime column
df['date'] = pd.to_datetime(df[['year', 'month']].assign(day=1))

# Define war start date
war_start = pd.to_datetime("2023-10-01")

# Add 'period' column
df['period'] = df['date'].apply(lambda x: 'Wartime' if x >= war_start else 'Calm')

# Group by year and period, then calculate average article length
yearly_period_avg = df.groupby(['year', 'period'])['length-mean'].mean().reset_index()

# Bar chart
fig = px.bar(yearly_period_avg, x='year', y='length-mean', color='period',
             barmode='group',
             title='Yearly Average Article Length by Period (Wartime vs Calm)',
             labels={'length-mean': 'Average Length (characters)', 'year': 'Year', 'period': 'Period'},
             color_discrete_map={'Wartime': 'firebrick', 'Calm': 'royalblue'})

fig.update_layout(font=dict(size=12))
fig.show()

# Save
fig.write_html("../outputs/visualization/article_lengths_by_year_and_period_by_period_wartime_vs_Calm.html")
# Save the grouped data to CSV
yearly_period_avg.to_csv("../outputs/visualization/yearly_article_lengths_by_period_wartime_vs_Calm.csv", index=False)


