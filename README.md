 # 📺 ParsaTV IPTV Stream Extractor

![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Automated-blue?logo=githubactions&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10-green?logo=python&logoColor=white)
![IPTV](https://img.shields.io/badge/IPTV-M3U%20Playlist-orange)

Este repositório contém um script automatizado em Python que realiza a raspagem (scraping) diária de canais e transmissões ao vivo diretamente da plataforma ParsaTV. O script categoriza os canais de forma inteligente e extrai os links diretos de transmissão (`.m3u8`), incluindo os logotipos oficiais de cada canal.

A atualização é feita de forma 100% automatizada através do **GitHub Actions**, garantindo que os links estejam sempre funcionais e atualizados sem a necessidade de intervenção manual.

---

## 🚀 Como usar a Lista no seu Player de IPTV

Para usar a lista gerada por este repositório no seu aplicativo favorito (VLC, IPTV Smarters, TiviMate, Perfect Player, etc.), utilize o link **estático (Raw)** abaixo:

```text
https://raw.githubusercontent.com/JulioCesarXY/EPG-ParsaTV/main/lista_completa_parsatv.m3u

```
> ⚠️ **Importante:** Lembre-se de substituir SEU_USUARIO_DO_GITHUB e NOME_DO_SEU_REPOSITORIO pelos dados reais da sua conta para que o link funcione.
> 
## 🛠️ Recursos e Funcionalidades
 * **Categorização por Abas:** Os canais são divididos automaticamente em grupos (Persian, Sports, News, etc.) usando a tag group-title, criando pastas organizadas no seu player.
 * **Suporte a Logotipos:** Coleta os ícones e logos dos canais usando o parâmetro tvg-logo.
 * **Filtro de Sinais:** Testa as conexões em tempo real e ignora automaticamente canais offline para manter a lista limpa.
 * **Execução Crônica (Automática):** O GitHub Actions roda o script de raspagem todos os dias às **06:00 AM UTC**.
## 🗂️ Estrutura do Arquivo M3U Gerado
O formato de saída gerado pelo script segue o padrão universal do ecossistema IPTV:
```text
#EXTM3U
#EXTINF:-1 group-title="Nome Da Categoria" tvg-logo="[https://www.parsatv.com/logo.png](https://www.parsatv.com/logo.png)",Nome Do Canal
[https://servidor-de-stream.live/hls/stream.m3u8](https://servidor-de-stream.live/hls/stream.m3u8)

```
## ⚙️ Como Funciona o Ambiente
Se você quiser clonar e rodar o projeto localmente (ou no Pydroid 3 / Termux), o projeto baseia-se nas seguintes dependências:
 1. **extrator.py**: O motor de raspagem que lê a estrutura HTML do site usando BeautifulSoup e valida os links de vídeo via expressões regulares (re).
 2. **requirements.txt**: Bibliotecas necessárias para a execução.
 3. **.github/workflows/atualizar_lista.yml**: Arquivo de automação que acorda um servidor Linux, instala o ecossistema, roda o script e commita o resultado atualizado de volta ao repositório.
### Instalação Manual:
```bash
# Clonar o repositório
git clone https://github.com/JulioCesarXY/EPG-ParsaTV.git

# Entrar na pasta
cd EPG-ParsaTV

# Instalar dependências
pip install -r requirements.txt

# Executar o extrator
python extrator.py

```
## 📄 Licença
Este projeto possui finalidades estritamente educacionais e de automação de ferramentas de código aberto. Os streams e logotipos pertencem aos seus respectivos criadores e à plataforma indexadora original.
```

