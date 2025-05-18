import os

def gerar_openair_a_partir_de_zonas(zonas, caminho_completo):
    conteudo = ""
    for z in zonas:
        conteudo += f"AC {z.get('tipo', 'R')}\n"
        conteudo += f"AN {z.get('nome', 'SEM_NOME')}\n"
        conteudo += f"AL {z.get('al', 'SFC')}\n"
        conteudo += f"AH {z.get('ah', 'UNL')}\n"
        conteudo += f"DP {z['lat']} {z['lon']}\n"
        conteudo += f"DC {z.get('raio', 5)}\n\n"

    os.makedirs(os.path.dirname(caminho_completo), exist_ok=True)  # Garante que o diretório exista
    with open(caminho_completo, "w", encoding="utf-8") as f:
        f.write(conteudo)
    print(f"[OK] Arquivo gerado: {caminho_completo}")
    return caminho_completo