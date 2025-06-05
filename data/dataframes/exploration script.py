import pandas as pd

# Load the TF-IDF data file
file_path = 'tfidf/tfidf-over-0.3.csv'
data = pd.read_csv(file_path)

# Print column names and a quick preview
print("TF-IDF Data Columns:", data.columns.tolist())
print("Sample rows:\n", data.head())

# Prepare the nodes from both filename-1 and filename-2 sides
part1 = data[['filename-1', 'title-1', 'year-1']].rename(columns={
    'filename-1': 'Id',
    'title-1': 'Label',
    'year-1': 'Year'
})

part2 = data[['filename-2', 'title-2', 'year-2']].rename(columns={
    'filename-2': 'Id',
    'title-2': 'Label',
    'year-2': 'Year'
})

# combining both parts and remove duplicates
nodes = pd.concat([part1, part2], ignore_index=True).drop_duplicates(subset='Id')

# Preparing edges with similarity threshold
edges = data[['filename-1', 'filename-2', 'similarity']].rename(columns={
    'filename-1': 'Source',
    'filename-2': 'Target',
    'similarity': 'Weight'
})

# filtering edges where similarity is 0.6 or more
edges_filtered = edges[edges['Weight'] >= 0.6]

# exporting nodes and edges to CSV
nodes.to_csv('yearly-gephi-nodes.csv', index=False)
edges_filtered.to_csv('yearly-gephi-edges.csv', index=False)

print("Files saved:")
print("- yearly-gephi-nodes.csv")
print("- yearly-gephi-edges.csv")


 
