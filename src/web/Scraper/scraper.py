from scholarly import scholarly, ProxyGenerator

from src.web.Scraper.paperManager import paperManager

class Scraper:
    """
    Scraper class for scraping Google Scholar
    """
    def __init__(self):
        self.paperManager = paperManager()
        self.proxy_generated = False
    
    def searchYear(self, year: int):
        """
        Search for papers citing sasview in a given year
        """
        if self.proxy_generated:
            query = f"/scholar?as_ylo={year}&q=\"SasView\"&hl=en&as_sdt=0,21"
            search_query = scholarly.search_pubs_custom_url(query)
            print(f"Searching for papers citing SasView in {year}")
            for article in search_query:
                print(article)
        else:
            raise Exception("Proxy not generated. Dangerous to procede; Stopping.")
    
    def initiate_proxy(self):
        """
        Initiates a proxy for the scraper
        """
        print("Initializing Scraper")
        self.pg = ProxyGenerator()
        connection_success = self.pg.FreeProxies()
        if not connection_success:
            raise Exception("Failed to connect to a proxy server. Dangerous to procede; Stopping.")
        scholarly.use_proxy(self.pg)
        print("Connected to a proxy server")
        self.proxy_generated = True
        