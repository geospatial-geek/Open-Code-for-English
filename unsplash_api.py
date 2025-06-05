import requests
import json
import os

# --- 1. Replace with your actual Access Key ---
# It's best practice to store API keys securely, e.g., in environment variables.
# For this example, we'll put it directly, but for production, use os.getenv()
# Example: export UNSPLASH_ACCESS_KEY="YOUR_KEY_HERE" in your terminal
# Or create a .env file and use a library like python-dotenv
 # <--- REPLACE THIS!

 # ...existing code...
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")
# ...existing code...

if UNSPLASH_ACCESS_KEY == "YOUR_UNSPLASH_ACCESS_KEY":
    print("WARNING: Please replace 'YOUR_UNSPLASH_ACCESS_KEY' with your actual Unsplash Access Key.")
    print("You can get one from unsplash.com/developers after registering an application.")
    exit()

def search_unsplash_photos(query, per_page=10, page=1):
    """
    Searches Unsplash for photos matching the given query.

    Args:
        query (str): The search term.
        per_page (int): Number of results per page (max 30).
        page (int): The page number of results to retrieve.

    Returns:
        dict: A dictionary containing the JSON response from the API.
    """
    url = "https://api.unsplash.com/search/photos"
    headers = {
        "Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}",
        "Accept-Version": "v1"
    }
    params = {
        "query": query,
        "per_page": per_page,
        "page": page
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def display_photo_info(photo_data):
    """
    Prints relevant information for a single photo.
    """
    if photo_data:
        print(f"--- Photo ID: {photo_data['id']} ---")
        print(f"Description: {photo_data.get('alt_description') or 'N/A'}")
        print(f"Photographer: {photo_data['user']['name']}")
        print(f"Photographer Profile: {photo_data['user']['links']['html']}?utm_source=YOUR_APP_NAME&utm_medium=referral")
        print(f"Regular Image URL: {photo_data['urls']['regular']}")
        print(f"Full Image URL: {photo_data['urls']['full']}")
        print(f"Download Location URL (MUST BE TRIGGERED ON DOWNLOAD): {photo_data['links']['download_location']}")
        print("-" * 30)

def track_download(download_location_url):
    """
    Triggers the Unsplash download endpoint.
    This is REQUIRED by Unsplash API guidelines when a user "downloads" an image.
    """
    headers = {
        "Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}",
        "Accept-Version": "v1"
    }
    try:
        response = requests.get(download_location_url, headers=headers)
        response.raise_for_status()
        print(f"Download tracked successfully for: {download_location_url}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to track download: {e}")

# --- Main usage ---
if __name__ == "__main__":
    search_term = input("Enter a search term for images (e.g., 'nature', 'cities', 'dogs'): ")
    results = search_unsplash_photos(search_term, per_page=5) # Get 5 photos

    if results and results['results']:
        print(f"\nFound {results['total']} total photos for '{search_term}'. Showing top {len(results['results'])}:")
        for photo in results['results']:
            display_photo_info(photo)

            # Example: Simulate a download and track it for the first photo
            if photo == results['results'][0]:
                print("\nSimulating download for the first photo...")
                track_download(photo['links']['download_location'])
    elif results:
        print(f"No photos found for '{search_term}'.")
    else:
        print("Failed to retrieve search results.")

    # Example: Get a random photo
    print("\n--- Getting a random photo ---")
    random_url = "https://api.unsplash.com/photos/random"
    headers = {
        "Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}",
        "Accept-Version": "v1"
    }
    params = {
        "query": "cats" # You can add a query for random photos too
    }
    try:
        random_response = requests.get(random_url, headers=headers, params=params)
        random_response.raise_for_status()
        random_photo = random_response.json()
        print("Random photo found:")
        display_photo_info(random_photo)
        track_download(random_photo['links']['download_location']) # Track download
    except requests.exceptions.RequestException as e:
        print(f"An error occurred getting random photo: {e}")
