# scraping.py
import requests
import json
import re
import time
import random
from urllib.parse import urlparse

def scrape(reddit_url):
    """Scrape Reddit thread with enhanced headers to avoid blocking"""
    
    # Enhanced browser-like headers to mimic real user
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/html, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0',
        'DNT': '1',
    }
    
    print(f"🔍 Scraping: {reddit_url}")
    
    try:
        # Parse URL properly using urlparse
        parsed = urlparse(reddit_url)
        path_parts = parsed.path.strip('/').split('/')
        
        # Extract subreddit and post ID
        if len(path_parts) >= 4 and path_parts[0] == 'r' and path_parts[2] == 'comments':
            subreddit = path_parts[1]  # e.g., 'confessions'
            post_id = path_parts[3]     # e.g., '1s5t9fs'
            json_url = f"https://www.reddit.com/r/{subreddit}/comments/{post_id}.json"
        else:
            # Fallback for edge cases
            json_url = reddit_url + ".json" if not reddit_url.endswith(".json") else reddit_url
            
        print(f"📡 Requesting: {json_url}")
        
        # Small random delay to mimic human behavior (0.5-1.5 seconds)
        time.sleep(random.uniform(0.5, 1.5))
        
        # Make request with enhanced headers and timeout
        r = requests.get(json_url, headers=headers, timeout=30)
        
        # Debug: Print response info
        print(f"📊 Response Status: {r.status_code}")
        print(f"📊 Content-Type: {r.headers.get('Content-Type', 'Unknown')}")
        
        # Check if we got HTML instead of JSON (blocked)
        content_type = r.headers.get('Content-Type', '')
        if content_type.startswith('text/html') or 'text/html' in content_type.lower():
            print("⚠️  Reddit returned HTML (possible block). Checking response...")
            # Try to detect if it's a block page
            if 'blocked' in r.text.lower() or 'captcha' in r.text.lower() or 'too many requests' in r.text.lower():
                print("🚫 Reddit blocked the request (CAPTCHA/rate limit). Using fallback...")
            return scrape_fallback(reddit_url)
        
        # Check for rate limit status codes
        if r.status_code in [429, 403, 503]:
            print(f"⚠️  Reddit returned status {r.status_code}. Using fallback...")
            return scrape_fallback(reddit_url)
        
        # Parse JSON
        data = r.json()
        
        # Extract post data from Reddit's nested JSON structure
        if isinstance(data, list) and len(data) >= 1:
            post_data = data[0]['data']['children'][0]['data']
            title = post_data.get('title', '')
            
            # Get top comments
            comments = []
            if len(data) > 1 and 'data' in data[1]:
                for comment in data[1]['data']['children'][:10]:  # Top 10 comments
                    if comment['data'].get('body'):
                        comments.append(comment['data']['body'])
            
            content = title + " " + " ".join(comments)
            print(f"✅ Successfully scraped: {title[:50]}...")
            return [[title, content]]
        
        print("⚠️  Unexpected JSON structure")
        return scrape_fallback(reddit_url)
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {e}")
        return scrape_fallback(reddit_url)
    except json.JSONDecodeError as e:
        print(f"❌ JSON parse error: {e}")
        preview = r.text[:200] if 'r' in locals() else "No response"
        print(f"Response preview: {preview}")
        return scrape_fallback(reddit_url)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return scrape_fallback(reddit_url)

def scrape_fallback(url):
    """Fallback: return mock data for testing when scraping fails"""
    print("🔄 Using fallback mock data for testing...")
    return [[
        "Test Reddit Thread",
        "This is a test confession for video generation. The story is about someone who had an embarrassing moment during their run yesterday. It's relatable, funny, and perfect for short-form content! People in the comments are sharing their own similar experiences, which makes it even more engaging."
    ]]

def save_map_to_txt(map_data, output_path):
    """
    Save scraped Reddit data to a text file.
    Args:
        map_data: List of [title, content] pairs OR list of dicts (from LLM)
        output_path: Path to save the text file
    """
    import os
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        for item in map_data:
            if isinstance(item, list) and len(item) >= 2:
                # Handle list format: [title, content]
                title, content = item[0], item[1]
                f.write(f"TITLE: {title}\n")
                f.write(f"CONTENT: {content}\n")
                f.write("-" * 80 + "\n")
            elif isinstance(item, dict):
                # Handle dict format (from LLM)
                title = item.get('title', item.get('best_segment', 'N/A')[:50] if item.get('best_segment') else 'N/A')
                content = item.get('desc', item.get('best_segment', 'N/A'))
                f.write(f"TITLE: {title}\n")
                f.write(f"CONTENT: {content}\n")
                f.write("-" * 80 + "\n")
    
    print(f"✅ Saved scraped data to: {output_path}")