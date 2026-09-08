import requests
import sys

SOURCE_URL = "https://live-event-by-rtxcric.rtxcric.workers.dev/playlist.m3u"
OUTPUT_FILE = "bb.m3u"

def update_m3u():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    print(f"Fetching playlist from: {SOURCE_URL}")
    try:
        response = requests.get(SOURCE_URL, headers=headers, timeout=30)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error downloading playlist: {e}")
        sys.exit(1)
        
    content = response.text.strip()
    
    # ഡാറ്റ സാധുവായ M3U ആണോ എന്ന് പരിശോധിക്കുന്നു
    if not content:
        print("Warning: Retrieved empty playlist.")
        sys.exit(1)
        
    # ഫയലിലേക്ക് സേവ് ചെയ്യുന്നു
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(content + "\n")
        
    print(f"Successfully updated and saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    update_m3u()

