import os
import subprocess
import json
import concurrent.futures

# --- CONFIGURAÇÕES DO CLEITIN (DUMP TOTAL) ---
VAULT_PATH = "vault/"
SOURCES_FILE = "config/sources.txt"
SETTINGS_FILE = "config/settings.yaml"

# Garante que o porão (vault) existe
os.makedirs(VAULT_PATH, exist_ok=True)

def pilhagem_bruta(url):
    """
    O Cleitin entra no wrapper e extrai TUDO. 
    Usa o yt-dlp como motor de extração universal.
    """
    print(f"🏴‍☠️ Cleitin iniciando extração profunda em: {url}")
    
    # Comando do Cleitin: Sem limites, qualidade máxima, extração de metadados
    # --flat-playlist garante que ele pegue todos os IDs de um hub/feed sem travar
    cmd = [
        "yt-dlp",
        "--extract-audio",
        "--audio-format", "mp3",
        "--audio-quality", "0",
        "--yes-playlist",
        "--ignore-errors",
        "--no-check-certificates",
        "--output", f"{VAULT_PATH}%(title)s.%(ext)s",
        "--write-thumbnail",
        "--add-metadata",
        url
    ]
    
    try:
        subprocess.run(cmd, check=True)
    except Exception as e:
        print(f"⚠️ Cleitin encontrou uma trava em {url}, pulando pro próximo ID...")

def iniciar_saque_industrial():
    if not os.path.exists(SOURCES_FILE):
        print("❌ Cleitin avisou: Sem mapa de fontes (sources.txt)! Onde tá o dump?")
        return

    with open(SOURCES_FILE, "r") as f:
        # Pega as linhas que não são comentários nem vazias
        urls = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    print(f"🦊 FoxyCat FM - Cleitin Engine: Iniciando Dump de {len(urls)} hubs...")

    # Força Bruta: Cleitin usa 10 braços (threads) pra baixar tudo de uma vez
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(pilhagem_bruta, urls)

if __name__ == "__main__":
    # O Lema do Cleitin: Se funciona, não precisa de trava.
    print("--- MODO CRAWLER ATIVADO (CLEITIN DUMP) ---")
    iniciar_saque_industrial()
    print("✅ Cleitin terminou o turno de pilhagem. O vault tá entupido!")
