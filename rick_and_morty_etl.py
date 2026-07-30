import sys
import requests
import pandas as pd
import awswrangler as wr
import datetime
import time;


# --- CONFIGURATION ---
S3_BUCKET = "s3://my-data-lake-bucket/rick_and_morty"

ENDPOINTS = {
    "characters": "https://rickandmortyapi.com/api/character",
    "locations": "https://rickandmortyapi.com/api/location",
    "episodes": "https://rickandmortyapi.com/api/episode"
}

def extract_api_data(url):
    """Paginates through the Rick and Morty API endpoint."""
    try:
   
        res = requests.get(url)
        
        # 1. Handle Rate Limiting (429) specifically
        if res.status_code == 429:
            print(f"⚠️ Rate limited on {url}. Waiting 5 seconds before retrying...")
            time.sleep(5)
            continue # Skips the rest of the loop and retries the EXACT same URL
            
        # 2. Handle other potential errors (like 404 or 500)
        res.raise_for_status()
        
        # 3. Process successful response
        data = res.json()
        results.extend(data['results'])
        url = data['info']['next']
        
        # 4. Be a polite scraper: Pause for half a second before the next page
        time.sleep(0.5)
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        break # Exit the loop if it's a fatal error (not a 429)
            
    print(f"✅ Extracted {len(results)} records.")
    return results

def extract_ids(url_list):
    """Extracts integer IDs from URL strings."""
    if not isinstance(url_list, list):
        return []
    return [int(u.split('/')[-1]) for u in url_list if u]

def transform_characters(raw_data):
    df = pd.json_normalize(raw_data)
    
    # Safe renaming
    rename_cols = {
        'origin.name': 'origin_name', 'origin.url': 'origin_url',
        'location.name': 'location_name', 'location.url': 'location_url'
    }
    df = df.rename(columns={k: v for k, v in rename_cols.items() if k in df.columns})
    
    if 'episode' in df.columns:
        df['episode_ids'] = df['episode'].apply(extract_ids)
        df = df.drop(columns=['episode'])
        
    df['created'] = pd.to_datetime(df['created'])
    return df

def main():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 1. Process Characters
    raw_chars = extract_api_data(ENDPOINTS['characters'])
    df_chars = transform_characters(raw_chars)
    
    # Write directly to S3 as Parquet using AWS Wrangler
    char_s3_path = f"{S3_BUCKET}/characters/data_{timestamp}.parquet"
    print(f"Writing characters to {char_s3_path}...")
    wr.s3.to_parquet(
        df=df_chars,
        path=char_s3_path,
        dataset=False # Set to True if you want partitioned dataset folders
    )
    
    print("Glue ETL Job Completed Successfully!")

if __name__ == "__main__":
    main()