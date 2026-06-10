import requests
import pandas as pd
from datetime import datetime
import json

class DataFetcher:
    def __init__(self, base_url="https://api.example.com"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "DataFetcher/1.0",
            "Accept": "application/json"
        })
    
    def fetch_user_data(self, user_id):
        """Fetch user data from API"""
        try:
            response = self.session.get(f"{self.base_url}/users/{user_id}")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching user {user_id}: {e}")
            return None
    
    def fetch_multiple_users(self, user_ids):
        """Fetch data for multiple users"""
        users_data = []
        for uid in user_ids:
            data = self.fetch_user_data(uid)
            if data:
                users_data.append(data)
        return users_data
    
    def process_data_to_dataframe(self, raw_data):
        """Convert raw API data to pandas DataFrame"""
        if not raw_data:
            return pd.DataFrame()
        
        df = pd.DataFrame(raw_data)
        
        # Clean and transform data
        if 'created_at' in df.columns:
            df['created_at'] = pd.to_datetime(df['created_at'])
        
        if 'age' in df.columns:
            df['age_group'] = pd.cut(df['age'], 
                                     bins=[0, 18, 30, 50, 100],
                                     labels=['<18', '18-30', '30-50', '50+'])
        
        return df
    
    def fetch_posts_by_user(self, user_id, limit=100):
        """Fetch posts for a specific user"""
        params = {'user_id': user_id, 'limit': limit}
        try:
            response = self.session.get(f"{self.base_url}/posts", params=params)
            response.raise_for_status()
            posts = response.json()
            
            # Convert to DataFrame and add metadata
            df = pd.DataFrame(posts)
            df['user_id'] = user_id
            df['fetch_timestamp'] = datetime.now()
            
            return df
        except requests.RequestException as e:
            print(f"Error fetching posts: {e}")
            return pd.DataFrame()
    
    def aggregate_user_stats(self, user_ids):
        """Generate aggregated statistics for users"""
        all_posts = pd.DataFrame()
        
        for uid in user_ids:
            posts_df = self.fetch_posts_by_user(uid)
            all_posts = pd.concat([all_posts, posts_df], ignore_index=True)
        
        if all_posts.empty:
            return pd.DataFrame()
        
        # Calculate statistics
        stats = all_posts.groupby('user_id').agg({
            'id': 'count',
            'likes': ['sum', 'mean', 'max'],
            'comments': ['sum', 'mean']
        })
        
        stats.columns = ['_'.join(col).strip() for col in stats.columns.values]
        stats.rename(columns={'id_count': 'total_posts'}, inplace=True)
        
        return stats
    
    def export_to_csv(self, dataframe, filename="output.csv"):
        """Export DataFrame to CSV file"""
        if not dataframe.empty:
            dataframe.to_csv(filename, index=False)
            print(f"Data exported to {filename}")
        else:
            print("No data to export")

# Example usage
if __name__ == "__main__":
    # Initialize fetcher
    fetcher = DataFetcher("https://jsonplaceholder.typicode.com")
    
    # Fetch sample data
    user_ids = [1, 2, 3, 4, 5]
    
    # Get user data
    users = fetcher.fetch_multiple_users(user_ids)
    users_df = fetcher.process_data_to_dataframe(users)
    
    # Get aggregated statistics
    stats_df = fetcher.aggregate_user_stats(user_ids[:3])
    
    # Display results
    print("\nUser Data:")
    print(users_df.head())
    
    print("\nAggregated Statistics:")
    print(stats_df)
    
    # Export to CSV
    fetcher.export_to_csv(users_df, "users_data.csv")
    fetcher.export_to_csv(stats_df, "user_statistics.csv")