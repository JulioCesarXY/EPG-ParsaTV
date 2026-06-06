import requests
import re
import os
import time
from bs4 import BeautifulSoup

url_home = "https://www.parsatv.com/"
headers = {
    "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
}

cookies = {
    "_ga": "GA1.1.513506447.1780755242",
    "cf_clearance": "MCIofMs.zYbGcHYgLu3uDRXpPaTHaxtmu_ScrYIAtSs-1780755634-1.2.1.1-eXvlwL_MmI1IylP6oobvBg4_KcsWhlf4iEDbaROQzAk9aNXgFW4w45dLtGnjvxxT3V3SkwIlaa7JifxWPhNz_tIsG_NxhRtn0hK9rjWXDY7DhhMWePCGgAbCQFyzwoUQwffhH.yBpPFExe1rhoXg8IkUEFF.n3lXflh2ORXwXcDWHI8adY.w1fpNY3pBoCvZvurGX6.zqfYaY41xWXVEVni4NP3Kx4UGjGjTtzGb3YPIkhf0nEqpragw.zqmMttKGH5EO5FrLIqPlVCzFmYt9LU1NRK9hqKBQjZffuvHrILeTh6t5ixOCL3iJp7wcd94wkiSiFn2MiZP5Q4cNjOADg",
    "_ga_WHWK7821VV": "GS2.1.s1780755242$o1$g1$t1780755786$j54$l0$h0"
}

def obter_todos_canais_por_categoria():
    print("--- Passo 1: Mapeando Categorias (Análise Avançada) ---")
    try:
        response = requests.get(url_home, headers=headers, cookies=cookies, timeout=15)
        if response.status_code != 200:
            print(f"[X] Erro ao acessar Home: {response.status_code}")
            return []
            
        soup = BeautifulSoup(response.text, 'html.parser')
        ul_main = soup.find('ul', id='myUL')
        
        if not ul_main:
            print("[X] Lista 'myUL' não encontrada.")
            return []
            
        canais_mapeados = []
        
        # Encontra todos os TDs que definem os títulos das seções/categorias
        td_categorias = ul_main.find_all('td', id=True)
        
        for td in td_categorias:
            id_categoria = td.get('id')
            nome_categoria = id_categoria.replace('-', ' ').title()
            
            # Encontra a tabela de canais que vem logo após ou está associada a esta categoria
            tabela_associada = td.find_next('table')
            if tabela_associada:
                # Pega todos os links de canais dentro desta tabela específica
                links = tabela_associada.find_all('a', href=re.compile(r'/m/name='))
                for link in links:
                    href = link.get('href')
                    url_completa = f"https://www.parsatv.com{href}" if href.startswith('/') else href
                    
                    # Evita duplicar o mesmo canal na mesma categoria
                    if url_completa not in [c['url'] for c in canais_mapeados]:
                        canais_mapeados.append({
                            'url': url_completa,
                            'categoria': nome_categoria
                        })
                        
        # Caso o parser dinâmico falhe em alguma seção, busca global como plano de fundo
        if not canais_mapeados:
            print("[!] Alerta: Estrutura em blocos falhou. Usando modo de segurança global...")
            for link in ul_main.find_all('a', href=re.compile(r'/m/name=')):
                href = link.get('href')
                url_completa = f"https://www.parsatv.com{href}" if href.startswith('/') else href
                canais_mapeados.append({'url': url_completa, 'categoria': 'Geral'})

        print(f"[+] Sucesso: {len(canais_mapeados)} canais mapeados para varredura.\n")
        return canais_mapeados
        
    except Exception as e:
        print(f"[X] Erro ao mapear a home: {e}")
        return []

def extrair_stream(url_canal):
    # Limpa o nome removendo parâmetros e IDs residuais
    nome_cru = url_canal.split("name=")[-1].split('#')[0]
    nome_canal = nome_cru.replace("-", " ").replace("%20", " ")
    
    try:
        response = requests.get(url_canal, headers=headers, cookies=cookies, timeout=10)
        if response.status_code == 200:
            # Captura o link .m3u8 puro de dentro do script da página
            links_m3u8 = re.findall(r'https?://[^\s"\']+\.m3u8', response.text)
            if links_m3u8:
                return nome_canal, links_m3u8[0]
    except Exception:
        pass
    return nome_canal, None

def main():
    dados_canais = obter_todos_canais_por_categoria()
    if not dados_canais:
        print("[!] Nenhum canal para processar. Verifique os cookies.")
        return

    print("--- Passo 2: Extraindo Streams Globais (Aguarde...) ---")
    lista_final = []
    
    # Processa TODOS os canais encontrados no site de forma sequencial
    for i, item in enumerate(dados_canais, 1):
        nome, stream_url = extrair_stream(item['url'])
        if stream_url:
            print(f"[{i}/{len(dados_canais)}] [OK] [{item['categoria']}] {nome}")
            lista_final.append({
                'nome': nome,
                'stream': stream_url,
                'categoria': item['categoria']
            })
        else:
            print(f"[{i}/{len(dados_canais)}] [SEM SINAL] {nome}")
        
        time.sleep(0.2) # Delay curto para estabilidade no mobile

    # --- Passo 3: Geração da Nova Lista Organizada ---
    if lista_final:
        nome_arquivo = "lista_completa_parsatv.m3u"
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            for canal in lista_final:
                f.write(f'#EXTINF:-1 group-title="{canal["categoria"]}",{canal["nome"]}\n')
                f.write(f"{canal['stream']}\n")
                
        print("\n=========================================")
        print(f"🎉 NOVA LISTA GLOBAL GERADA!")
        print(f"Arquivo: {os.path.abspath(nome_arquivo)}")
        print(f"Total de streams extraídas: {len(lista_final)}")
        print("=========================================")
    else:
        print("\n[!] Nenhuma stream ativa pôde ser coletada.")

if __name__ == "__main__":
    main()
