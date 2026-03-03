import os

CID_FILE = "config/latest_cid.txt"
INDEX_HTML = "public/index.html"

def gerar_spotify_do_cleitin():
    if not os.path.exists(CID_FILE):
        return

    with open(CID_FILE, "r") as f:
        cid_mestre = f.read().strip()

    conteudo_html = f"""<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FoxyCat FM - No Limits</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {{ background-color: #090909; color: #ffffff; font-family: sans-serif; }}
        .spotify-green {{ color: #1DB954; }}
        .bg-spotify {{ background-color: #121212; }}
        .card:hover {{ background-color: #282828; cursor: pointer; }}
        ::-webkit-scrollbar {{ width: 8px; }}
        ::-webkit-scrollbar-track {{ background: #121212; }}
        ::-webkit-scrollbar-thumb {{ background: #333; border-radius: 4px; }}
    </style>
</head>
<body class="p-8">
    <header class="flex justify-between items-center mb-8">
        <h1 class="text-4xl font-bold spotify-green">🦊 FOXYCAT FM</h1>
    </header>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div class="bg-spotify p-6 rounded-lg shadow-xl sticky top-8 h-fit">
            <h2 class="text-xl font-bold mb-4">Tocando Agora</h2>
            <audio id="main-player" controls class="w-full mb-4"></audio>
            <div id="current-track" class="text-spotify-green font-bold">...</div>
        </div>

        <div class="bg-spotify p-6 rounded-lg shadow-xl">
            <h2 class="text-xl font-bold mb-4">Vault</h2>
            <div id="playlist" class="space-y-2 max-h-[600px] overflow-y-auto pr-2"></div>
        </div>
    </div>

    <footer class="mt-12 pt-8 border-t border-gray-800 text-center">
        <p class="text-gray-400 mb-4 font-bold">Check us out on GitHub!</p>
        <a href="https://github.com/lazyman563/FoxyCat" target="_blank" class="inline-block hover:scale-110 transition-transform">
            <svg height="40" width="40" viewBox="0 0 16 16" fill="#ffffff"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path></svg>
        </a>
    </footer>

    <script>
        const cid = "{cid_mestre}";
        const gateway = "https://ipfs.io/ipfs/";
        
        async function load() {{
            const res = await fetch(`https://gateway.pinata.cloud/ipfs/${{cid}}?format=json`);
            const data = await res.json();
            const list = document.getElementById('playlist');
            data.objects.forEach(f => {{
                if(f.name.endsWith('.mp3')) {{
                    const d = document.createElement('div');
                    d.className = 'card p-3 rounded bg-[#181818] flex justify-between';
                    d.innerHTML = `<span>${{f.name}}</span><span class="spotify-green">PLAY</span>`;
                    d.onclick = () => {{
                        const p = document.getElementById('main-player');
                        p.src = gateway + cid + '/' + f.name;
                        p.play();
                        document.getElementById('current-track').innerText = f.name;
                    }};
                    list.appendChild(d);
                }}
            }});
        }}
        load();
    </script>
</body>
</html>
"""
    with open(INDEX_HTML, "w") as f:
        f.write(conteudo_html)

if __name__ == "__main__":
    gerar_spotify_do_cleitin()
