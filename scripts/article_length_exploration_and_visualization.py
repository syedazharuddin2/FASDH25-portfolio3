# We will Try to Explore Here:
# Question: How does average article length vary by month, and are there outliers?

# Import necessary libraries
import pandas as pd  
import plotly.express as px

# Load article length data by year and month
df = pd.read_csv("../data/dataframes/length/length-year-month.csv")  

# Exploration 1: average article length over time to observe monthly trends
# Display column names to verify structure
print("Columns:", df.columns.tolist())

# Print summary statistics to understand data distribution
print("Summary Stats:\n", df.describe())  

# Check for any missing values in the dataset 
print("Missing Values:\n", df.isnull().sum())  

# Create a datetime column to enable chronological sorting 
df['date'] = pd.to_datetime(df[['year','month']].assign(day=1))  # Create date for sorting  
# Plot average article length over time to observe monthly trends
fig = px.bar(df, x='date', y='length-mean',  
              title='Average Article Length by Year',  
              labels={'length-mean': 'Average Length (characters)', 'date': 'year'},
             barmode='group')
# Display the monthly length bar chart
fig.show()
# Save the full time-series chart to an HTML file for reporting
fig.write_html("../outputs/exploration/article_lengths_over_time.html")

# Exploration 2: article lengths by month during wartime
# Define start of wartime period (Oct 2023)
war_start = pd.to_datetime("2023-10-01")  # Start from beginning of October to include whole month

# Keep only data from wartime months (Oct 2023 onward)
wartime_df = df[df['date'] >= war_start]

# Visualize article lengths by month during wartime
fig = px.bar(wartime_df, x='date', y='length-mean',
             title='Monthly Average Article Length After October 2023 (Wartime)',
             labels={'length-mean': 'Average Length (characters)', 'date': 'Month'},
             barmode='group')
# Show wartime monthly chart
fig.show()
# Save wartime-only chart to HTML for use in comparisons
fig.write_html("../outputs/exploration/article_lengths_wartime_only.html")
# Optional: Save wartime data separately
wartime_df.to_csv("../outputs/exploration/article_lengths_wartime_only.csv", index=False)


# Visualization:  article lengths by year and period (war and calm)
# Recreate datetime column (for consistency if above was skipped)
df['date'] = pd.to_datetime(df[['year', 'month']].assign(day=1))

# Redefine war start date to apply in classification
war_start = pd.to_datetime("2023-10-01")

# Label each row as 'Wartime' or 'Calm' based on its date
df['period'] = df['date'].apply(lambda x: 'Wartime' if x >= war_start else 'Calm')

# Group by year and period to compare average lengths during conflict vs calm
yearly_period_avg = df.groupby(['year', 'period'])['length-mean'].mean().reset_index()

# Bar chart comparing article lengths by year and period
fig = px.bar(yearly_period_avg, x='year', y='length-mean', color='period',
             barmode='group',
             title='Yearly Average Article Length by Period (Wartime vs Calm)',
             labels={'length-mean': 'Average Length (characters)', 'year': 'Year', 'period': 'Period'},
             color_discrete_map={'Wartime': 'firebrick', 'Calm': 'royalblue'})
# Show comparison chart
fig.update_layout(font=dict(size=12))
# Show comparison chart
fig.show()

# Save
fig.write_html("../outputs/visualization/article_lengths_by_year_and_period_by_period_wartime_vs_Calm.html")
# Save the grouped data to CSV
yearly_period_avg.to_csv("../outputs/visualization/yearly_article_lengths_by_period_wartime_vs_Calm.csv", index=False)


