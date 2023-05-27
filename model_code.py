import requests
from bs4 import BeautifulSoup
import signal


class Scraper:

  def __init__(self, url):
    self.url = url
    self.visited_links = set()
    self.parser = BeautifulSoupParser()
    self.data_extractor = CustomDataExtractor()
    self.counts = {}
    self.total_count = 0

  def scrape(self):
    signal.signal(signal.SIGALRM, self._handle_timeout)
    signal.alarm(#)  # no "#", mudar a quantidade de tempo que o código vai ficar executando (em segundos)
    try:
      self._scrape_page(self.url, depth=#)  # no "#", mudar a profundidade máxima de busca
    except Exception as e:
      print(f"Erro ao executar o scraper: {e}")
    finally:
      signal.alarm(0)  # cancelar alarme

    total_counts = sum(self.counts.values())
    print(f"\nTotal de ocorrências:\n{self.total_count}\n")

  def _handle_timeout(self, signum, frame):
    print("Tempo limite excedido. Encerrando a execução.")
    raise TimeoutError()

  def _scrape_page(self, url, depth):
    if url in self.visited_links:
      return

    print(f"Scraping {url}")
    self.visited_links.add(url)

    content = self._fetch_content(url)
    if content is None:
      return

    data = self.parser.parse(content)
    count = self.data_extractor.extract(data, "#") # no "#";  mudar nome a ser buscado na página
    self.counts[url] = count
    self.total_count += count

    if depth > 0:
      for link in self.parser.get_links(content):
        self._scrape_page(link, depth=depth - 1)

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


class DataExtractor:

  def extract(self, data):
    raise NotImplementedError()


class Parser:

  def parse(self, content):
    raise NotImplementedError()

  def get_links(self, content):
    raise NotImplementedError()


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


class CustomDataExtractor(DataExtractor):

  def extract(self, data, word):
    content = str(data)
    count = content.count(word)
    print(f"A palavra '{word}' aparece {count} vezes na página.")
    return count


if __name__ == "__main__":
  url = "#" # no "#", inserir o link para busca
  scraper = Scraper(url)
  scraper.scrape()

  print("Contagem de ocorrências da palavra 'Fortaleza':")
  for url, count in scraper.counts.items():
    print(f"{url}: {count}")
