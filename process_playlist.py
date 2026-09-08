import sys
from curl_cffi import requests

SOURCE_URL = "https://live-event-by-rtxcric.rtxcric.workers.dev/playlist.m3u"
OUTPUT_FILE = "bb.m3u"

def update_m3u():
    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://live-event-by-rtxcric.rtxcric.workers.dev/",
    }
    
    print(f"Fetching playlist from: {SOURCE_URL}")
    try:
        # impersonate="chrome124" mimics authentic Chrome network fingerprints
        response = requests.get(
            SOURCE_URL,
            headers=headers,
            impersonate="chrome124",
            timeout=30
        )
        response.raise_for_status()
    except Exception as e:
        print(f"Error downloading playlist: {e}")
        sys.exit(1)
        
    content = response.text.strip()
    
    if not content or "#EXTM3U" not in content:
        print("Warning: Retrieved invalid or empty playlist.")
        sys.exit(1)
        
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(content + "\n")
        
    print(f"Successfully updated and saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    update_m3u()
