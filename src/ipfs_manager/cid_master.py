import os
import subprocess
import json

# --- CONFIGURAÇÕES DO CLEITIN (FUSÃO DE CID) ---
VAULT_PATH = "vault/"
MFS_ROOT = "/FoxyCat_Vault"  # Caminho virtual dentro do IPFS

def rodar_comando(cmd):
    """Executa e retorna a saída do shell pro Cleitin ler."""
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    return result.stdout.strip()

def fundir_tesouro():
    print(f"🦊 Cleitin iniciando a fundição no MFS: {MFS_ROOT}")

    # 1. Garante que o diretório raiz existe no MFS
    rodar_comando(f"ipfs files mkdir -p {MFS_ROOT}")

    # 2. Varre o vault e joga cada arquivo pro MFS
    arquivos = [f for f in os.listdir(VAULT_PATH) if os.path.isfile(os.path.join(VAULT_PATH, f))]
    
    if not arquivos:
        print("⚠️ Cleitin avisou: O vault tá vazio! Nada pra fundir.")
        return None

    print(f"🏴‍☠️ Cleitin processando {len(arquivos)} arquivos...")

    for arquivo in arquivos:
        caminho_local = os.path.join(VAULT_PATH, arquivo)
        caminho_mfs = f"{MFS_ROOT}/{arquivo.replace(' ', '_')}" # Remove espaços pra não dar pau

        # Adiciona ao IPFS e pega o CID individual
        cid_temp = rodar_comando(f"ipfs add -Q '{caminho_local}'")
        
        # Copia do IPFS pro MFS (Se já existir, o Cleitin ignora ou sobrescreve)
        rodar_comando(f"ipfs files rm {caminho_mfs} 2>/dev/null")
        rodar_comando(f"ipfs files cp /ipfs/{cid_temp} {caminho_mfs}")

    # 3. O GRANDE FINAL: Gera o CID MESTRE do diretório todo
    cid_mestre = rodar_comando(f"ipfs files stat --hash {MFS_ROOT}")
    
    print("\n" + "="*40)
    print(f"✅ FUSÃO COMPLETA!")
    print(f"🔑 CID MESTRE: {cid_mestre}")
    print("="*40)
    
    # Salva o CID num arquivo pra o site_generator usar depois
    with open("config/latest_cid.txt", "w") as f:
        f.write(cid_mestre)
    
    return cid_mestre

if __name__ == "__main__":
    fundir_tesouro()
