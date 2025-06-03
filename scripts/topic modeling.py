# Importing libraries
import pandas as pd
import plotly.express as px

# Loading the CSV data
df = pd.read_csv("../data/dataframes/topic-model/topic-model.csv")

# Keeping only classified articles
df = df[df["Topic"] != -1]

# Creating readable topic labels by combining topic_1 to topic_4
df["Topic_Label"] = df[["topic_1", "topic_2", "topic_3", "topic_4"]].agg(", ".join, axis=1)

# Count total articles per topic
topic_counts = df["Topic_Label"].value_counts()

# Get top 5 and bottom 5 topics by frequency
top_5_topics = topic_counts.head(5).index.tolist()
bottom_5_topics = topic_counts.tail(5).index.tolist()

# Combine both sets of topics
selected_topics = top_5_topics + bottom_5_topics

# Filter DataFrame for just those 10 topics and make a copy
filtered_df = df[df["Topic_Label"].isin(selected_topics)].copy()

# Group by year and topic label to count articles
grouped_data = filtered_df.groupby(["year", "Topic_Label"]).size().reset_index(name="Article_Count")

# Convert year to string for categorical x-axis
grouped_data["year"] = grouped_data["year"].astype(str)

# Create the bar chart
fig = px.bar(
    grouped_data,
    x="year",
    y="Article_Count",
    color="Topic_Label",
    barmode="group",
    labels={
        "year": "Year",
        "Article_Count": "Number of Articles",
        "Topic_Label": "Topic"
    },
    title="Top 5 vs Bottom 5 Topics by Article Count Over the Years"
)

# Show the plot
fig.show()

# Save to HTML
fig.write_html("../outputs/exploration/topic_modeling-top5-vs-bottom5-topics.html")




# Create a new column for Year-Month format (safe assignment)
filtered_df.loc[:, "YearMonth"] = pd.to_datetime(
    filtered_df[["year", "month"]].assign(day=1)
).dt.to_period("M").astype(str)

# Group by YearMonth and Topic_Label
grouped_data = filtered_df.groupby(["YearMonth", "Topic_Label"]).size().reset_index(name="Article_Count")

# Create bar chart (monthly trend)
fig = px.bar(
    grouped_data,
    x="YearMonth",
    y="Article_Count",
    color="Topic_Label",
    barmode="group",
    labels={
        "YearMonth": "Month",
        "Article_Count": "Number of Articles",
        "Topic_Label": "Topic"
    },
    title="Top 5 vs Bottom 5 Topics by Article Count (Monthly Trend)"
)

# Show the plot
fig.show()

# Save plot to HTML
fig.write_html("../outputs/exploration/topic_modeling-top5-vs-bottom5-monthly.html")



# Convert to datetime using year, month, day (safe assignment)
filtered_df.loc[:, "date"] = pd.to_datetime(
    filtered_df[["year", "month", "day"]],
    errors="coerce"
)

# Define Gaza war start (no fixed end)
war_start = pd.to_datetime("2023-10-07")

# Filter for articles on or after war start
war_period_df = filtered_df[filtered_df["date"] >= war_start]

# Group by YearMonth and Topic_Label during war period
grouped_war_data = war_period_df.groupby(["YearMonth", "Topic_Label"]).size().reset_index(name="Article_Count")



# Create bar chart for war period onwards
fig = px.bar(
    grouped_war_data,
    x="YearMonth",
    y="Article_Count",
    color="Topic_Label",
    barmode="group",
    labels={
        "YearMonth": "Month",
        "Article_Count": "Number of Articles",
        "Topic_Label": "Topic"
    },
    title="Top 5 vs Bottom 5 Topics from Gaza War Onward (Monthly)"
)

# Show the plot
fig.show()

# Save plot to separate HTML file
fig.write_html("../outputs/exploration/topic_modeling-top5-vs-bottom5-gaza-war-onward.html")




# Step 1: Import the necessary libraries
import pandas as pd
import plotly.express as px

# Step 2: Load the dataset
df = pd.read_csv("../data/dataframes/topic-model/topic-model.csv")

# Step 3: Keep only articles that have a valid topic
df = df[df["Topic"] != -1]

# Step 4: Combine topic keywords into one label for each article
df["Topic_Label"] = df[["topic_1", "topic_2", "topic_3", "topic_4"]].agg(", ".join, axis=1)

# Step 5: Create a proper date column from year, month, and day
df["date"] = pd.to_datetime(df[["year", "month", "day"]], errors='coerce')

# Step 6: Create a column for year and month (like "2023-11")
df["YearMonth"] = df["date"].dt.to_period("M").astype(str)

# Step 7: Define keywords to search for in the topic labels
keywords = ["Israel", "Gaza", "Hamas", "war"]

# Step 8: Filter the articles that mention any of the keywords
df = df[df["Topic_Label"].str.contains("|".join(keywords), case=False, na=False)]

# Step 9: If no matching articles found, print a message
if df.empty:
    print("No matching articles found.")
else:
    print(f"{len(df)} articles found on the topic.")

# Step 10: Count how many articles there are for each month
grouped = df.groupby("YearMonth").size().reset_index(name="Article_Count")

# Step 11: Create a line graph to show the trend
fig = px.line(
    grouped,
    x="YearMonth",
    y="Article_Count",
    title="Trend of Articles on 'Israel, Gaza, Hamas, war'",
    labels={"YearMonth": "Month", "Article_Count": "Number of Articles"},
    markers=True
)

# Step 12: Show the graph
fig.show()

# Step 13: Save the graph to a file you can open in a web browser
fig.write_html("../outputs/visualization/visualization-israel-gaza-hamas-trend.html")
