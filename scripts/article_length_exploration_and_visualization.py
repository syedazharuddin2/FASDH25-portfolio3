# We will Try to Explore Here:
# Question: How does average article length vary by month, and are there outliers?

# Import necessary libraries
import pandas as pd  
import plotly.express as px

# Load article length data by year and month
df = pd.read_csv("../data/dataframes/length/length-year-month.csv")  

# Exploration 1: Do articles published during conflict periods tend to be shorter than those in calmer periods?
# Flag rows that fall within the Oct–Dec 2023 conflict period 
df['conflict_period'] = df.apply(lambda x: 1 if (x['year'] == 2023) and (x['month'] >= 10) else 0, axis=1)  
# Print to check
print(df['conflict_period'])
# Plot a line chart of article length by month for each year to visualize trends
fig = px.bar(df, x='month', y='length-mean', color='year',  
              title='Average Article Length by Month (2021-2024)',  
              labels={'length-mean': 'Length (characters)', 'month': 'Month'},
              barmode='group')
# Visually highlight the conflict period (Oct to Dec) on the chart
fig.add_vrect(x0=10, x1=12, fillcolor="red", opacity=0.1, line_width=0,  
              annotation_text="2023 Conflict Period", annotation_position="top left")
# Improve readability: show tooltips across all years when hovering over a month
fig.update_layout(hovermode='x unified', font=dict(size=12))
# Save as interactive HTML
fig.write_html("../outputs/visualization/article_lengths_conflict.html")  
# Save as csv
df['conflict_period'].to_csv('../outputs/exploration/article_lengths_conflict.csv')


# Average article length over time to observe monthly trends
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
fig.write_html("../outputs/visualization/article_lengths_over_time.html")
# Save as csv
df['date'].to_csv('../outputs/exploration/article_lengths_overtime.csv')


# Article lengths by month during wartime
# Define start of wartime period (Oct 2023)
war_start = pd.to_datetime("2023-10-01")  # Start from beginning of October to include whole month

# Keep only data from wartime months (Oct 2023 onward)
wartime_df = df[df['date'] >= war_start]
# Print to check
print(wartime_df)
# Visualize article lengths by month during wartime
fig = px.bar(wartime_df, x='date', y='length-mean',
             title='Monthly Average Article Length After October 2023 (Wartime)',
             labels={'length-mean': 'Average Length (characters)', 'date': 'Month'},
             barmode='group')
# Show wartime monthly chart
fig.show()
# Save wartime-only chart to HTML for use in comparisons
fig.write_html("../outputs/visualization/article_lengths_wartime_only.html")
# Save wartime data separately
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
yearly_period_avg.to_csv("../outputs/exploration/yearly_article_lengths_by_period_wartime_vs_Calm.csv", index=False)


