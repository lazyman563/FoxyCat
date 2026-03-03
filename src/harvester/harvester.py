import os
import subprocess
import concurrent.futures

# --- SETTINGS (GYAM ENGINE) ---
# Saving directly to public/vault so the UI can find it
VAULT_PATH = "public/vault/"
SOURCES_FILE = "config/sources.txt"

# Ensure the vault exists
os.makedirs(VAULT_PATH, exist_ok=True)

def raw_harvesting(url):
    """
    Universal extraction engine using yt-dlp.
    No limits, maximum quality, metadata extraction.
    """
    print(f"[*] Starting deep extraction: {url}")

    cmd = [
        "yt-dlp",
        "--extract-audio",
        "--audio-format", "mp3",
        "--audio-quality", "0",
        "--yes-playlist",
        "--ignore-errors",
        "--no-check-certificates",
        "--output", f"{VAULT_PATH}%(title)s.%(ext)s",
        "--add-metadata",
        url
    ]

    try:
        subprocess.run(cmd, check=True)
    except Exception as e:
        print(f"[!] Extraction failed for {url}, skipping...")

def start_industrial_dump():
    if not os.path.exists(SOURCES_FILE):
        print("[!] Error: sources.txt not found!")
        return

    with open(SOURCES_FILE, "r") as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    print(f"[*] FoxyCat FM Engine: Harvesting {len(urls)} hubs...")

    # Force: 10 threads for parallel dumping
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(raw_harvesting, urls)

if __name__ == "__main__":
    print("--- CRAWLER MODE ACTIVATED (GYAM DUMP) ---")
    start_industrial_dump()
    print("[+] Harvesting cycle complete. Vault is full.")
