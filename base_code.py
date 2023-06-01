# importação das bibliotecas necessárias
import requests
from bs4 import BeautifulSoup
import signal

# definição da classe scraper, que contém as informações necessárias. o construtor inicializa as variáveis necessárias pro scraper
class Scraper:

  def __init__(self, url):
    self.url = url
    self.visited_links = set()
    self.parser = BeautifulSoupParser()
    self.data_extractor = CustomDataExtractor()
    self.counts = {}
    self.total_count = 0

  # método que inicia o scraping. usa o signal alarm pra evitar que o scraper fique preso em uma página, chama o método _scrape_page para realizar o scraping e no final, exibe o total de ocorrências encontradas.

  def scrape(self):
    signal.signal(signal.SIGALRM, self._handle_timeout)
    signal.alarm(30)  # definir alarme para 30 segundos
    try:
      self._scrape_page(self.url, depth=2)  # profundidade máxima de 2
    except Exception as e:
      print(f"Erro ao executar o scraper: {e}")
    finally:
      signal.alarm(0)  # cancelar alarme

    total_counts = sum(self.counts.values())
    print(f"\nTotal de ocorrências:\n{self.total_count}\n")
    
# Método que é chamado quando o alarme é disparado. Exibe uma mensagem de erro e encerra a execução.

  def _handle_timeout(self, signum, frame):
    print("Tempo limite excedido. Encerrando a execução.")
    raise TimeoutError()
# Método que realiza o scraping de uma página. Verifica se a página já foi visitada. Obtém o conteúdo da página e extrai os dados relevantes. Armazena as informações em um dicionário. Se a profundidade permitir, chama o método _scrape_page para realizar o scraping das páginas encontradas.
   
  def _scrape_page(self, url, depth):
    if url in self.visited_links:
      return

    print(f"Scraping {url}")
    self.visited_links.add(url)

    content = self._fetch_content(url)
    if content is None:
      return

    data = self.parser.parse(content)
    count = self.data_extractor.extract(data, "Fortaleza")
    self.counts[url] = count
    self.total_count += count

    if depth > 0:
      for link in self.parser.get_links(content):
        self._scrape_page(link, depth=depth - 1)

# método que obtém o conteúdo de uma página. verifica se a página foi acessada com sucesso. retorna o conteúdo da página ou None em caso de erro.
        
  def _fetch_content(self, url):
    try:
      response = requests.get(url)
      if response.status_code == 200:
        return response.content
      else:
        print(f"Erro ao acessar a URL: {response.status_code}")
    except requests.exceptions.RequestException as e:
      print(f"Erro ao acessar a URL: {e}")

    return None

# Definição das classes DataExtractor e Parser, que são utilizadas para extrair os dados relevantes e os links das páginas.

class DataExtractor:

  def extract(self, data):
    raise NotImplementedError()


class Parser:

  def parse(self, content):
    raise NotImplementedError()

  def get_links(self, content):
    raise NotImplementedError()

# definição da classe BeautifulSoupParser, que é utilizada para extrair os dados relevantes e os links das páginas utilizando a biblioteca BeautifulSoup.

class BeautifulSoupParser(Parser):

  def parse(self, content):
    return BeautifulSoup(content, 'html.parser')

  def get_links(self, content):
    soup = self.parse(content)
    links = []
    for link in soup.find_all('a'):
      href = link.get('href')
      if href is not None:
        links.append(href)
    return links

# definição da classe CustomDataExtractor, que é utilizada para extrair os dados relevantes das páginas.

class CustomDataExtractor(DataExtractor):

  def extract(self, data, word):
    content = str(data)
    count = content.count(word)
    print(f"A palavra '{word}' aparece {count} vezes na página.")
    return count

# Código que é executado quando o arquivo é executado diretamente. Define a URL a ser utilizada e chama o método scrape para realizar o scraping. Exibe a contagem de ocorrências encontradas.

  
if __name__ == "__main__":
  url = "https://fortaleza1918.com.br/"
  scraper = Scraper(url)
  scraper.scrape()

  print("Contagem de ocorrências da palavra 'Fortaleza':")
  for url, count in scraper.counts.items():
    print(f"{url}: {count}")
