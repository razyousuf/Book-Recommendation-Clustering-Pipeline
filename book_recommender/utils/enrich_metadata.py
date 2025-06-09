import requests
import time

def fetch_genre(title, author=None):
    query = f"{title} {author}" if author else title
    try:
        res = requests.get(f"https://openlibrary.org/search.json?q={query}")
        data = res.json()
        if data['docs']:
            subjects = data['docs'][0].get('subject', [])
            # Return a comma-separated string of relevant tags
            return ', '.join(subjects[:5]) if subjects else "Unknown"
    except Exception as e:
        return "Unknown"
    return "Unknown"
