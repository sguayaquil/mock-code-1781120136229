# Data Fetcher

A Python utility for fetching and processing data from REST APIs using requests and pandas.

## Features

- Fetch user data from REST APIs
- Process and transform data using pandas DataFrames
- Aggregate statistics across multiple users
- Export processed data to CSV files
- Session management for efficient API requests
- Error handling for robust data fetching

## Requirements

- Python 3.6+
- requests
- pandas

## Installation

```bash
pip install requests pandas
```

## Usage

```python
from data_fetcher import DataFetcher

# Initialize the fetcher
fetcher = DataFetcher("https://api.example.com")

# Fetch user data
user_ids = [1, 2, 3]
users = fetcher.fetch_multiple_users(user_ids)

# Convert to DataFrame
df = fetcher.process_data_to_dataframe(users)

# Get aggregated statistics
stats = fetcher.aggregate_user_stats(user_ids)

# Export to CSV
fetcher.export_to_csv(df, "output.csv")
```

## Methods

- `fetch_user_data(user_id)`: Fetch data for a single user
- `fetch_multiple_users(user_ids)`: Fetch data for multiple users
- `process_data_to_dataframe(raw_data)`: Convert raw data to pandas DataFrame
- `fetch_posts_by_user(user_id, limit)`: Fetch posts for a specific user
- `aggregate_user_stats(user_ids)`: Generate aggregated statistics
- `export_to_csv(dataframe, filename)`: Export DataFrame to CSV file