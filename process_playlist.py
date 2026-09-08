import sys
import re
from curl_cffi import requests

SOURCE_URL = "https://live-event-by-rtxcric.rtxcric.workers.dev/playlist.m3u"
OUTPUT_FILE = "bb.m3u"

# NS Player-ൽ ആവശ്യമായ യൂസർ ഏജന്റ്
DEFAULT_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
DEFAULT_REF = "https://live-event-by-rtxcric.rtxcric.workers.dev/"

def format_for_ns_player(raw_content):
    lines = raw_content.splitlines()
    formatted_lines = []
    
    # M3U ഹെഡർ ഉറപ്പാക്കുന്നു
    if not any(line.strip().startswith("#EXTM3U") for line in lines):
        formatted_lines.append("#EXTM3U")
    
    for line in lines:
        cleaned = line.strip()
        if not cleaned:
            continue
            
        if cleaned.startswith("#EXTINF"):
            formatted_lines.append(cleaned)
            # NS Player / VLC പ്ലെയറുകൾക്കായി ഹെഡറുകൾ ചേർക്കുന്നു
            formatted_lines.append(f'#EXTVLCOPT:http-user-agent={DEFAULT_UA}')
            formatted_lines.append(f'#EXTVLCOPT:http-referrer={DEFAULT_REF}')
        elif cleaned.startswith("http"):
            # ചില NS Player വേർഷനുകൾ URL-ന്റെ കൂടെ തന്നെയുള്ള ഹെഡർ ഫോർമാറ്റാണ് സപ്പോർട്ട് ചെയ്യുന്നത്
            if "|" not in cleaned:
                stream_url = f"{cleaned}|User-Agent={DEFAULT_UA}&Referer={DEFAULT_REF}"
                formatted_lines.append(stream_url)
            else:
                formatted_lines.append(cleaned)
        elif not cleaned.startswith("#EXTVLCOPT"):
            formatted_lines.append(cleaned)
            
    return "\n".join(formatted_lines)

def update_m3u():
    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": DEFAULT_REF,
    }
    
    print(f"Fetching playlist from: {SOURCE_URL}")
    try:
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
    
    if not content:
        print("Warning: Retrieved empty playlist.")
        sys.exit(1)
        
    # NS Player ഫോർമാറ്റിലേക്ക് മാറ്റുന്നു
    processed_content = format_for_ns_player(content)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(processed_content + "\n")
        
    print(f"Successfully updated and optimized for NS Player in {OUTPUT_FILE}")

if __name__ == "__main__":
    update_m3u()
