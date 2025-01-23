from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Configuração do WebDriver
def start_driver():
    chrome_options = Options()
    chrome_options.add_argument('--lang=pt-BR')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--incognito')
    chrome_options.add_experimental_option('prefs', {
        'download.directory_upgrade': True,
        'download.prompt_for_download': False,
        'profile.default_content_setting_values.notifications': 2,
        'profile.default_content_setting_values.automatic_downloads': 1,
    })
    return webdriver.Chrome(options=chrome_options)

# Função para esperar o elemento
def wait_for_element(driver, by, value, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )

# Formatação de preço
def formatted_price(price):
    return float(price.replace('R$', '').strip().replace(',', '.'))

# Scraping
def scrape_price(driver, link, xpaths, site, prices_dict):
    try:
        print(f'Acessando: {site}')
        driver.get(link)
        
        if site not in prices_dict:
            prices_dict[site] = {}
        
        for key, xpath in xpaths.items():
            try:
                element = wait_for_element(driver, By.XPATH, xpath).text
                prices_dict[site][key] = formatted_price(element)
            
            except Exception as e:
                print(f"Erro ao buscar o preço '{key}' em {site}: {e}")
                
    except Exception as e:
        print(f'Erro ao acessar o site {site}: {e}')

# Função principal
def main():
    links = [
                {
            'site': 'Kabum',
            'url': 'https://www.kabum.com.br/produto/627947',
            'xpaths': {
                'price_in_cash': '//div/h4[@class="sc-5492faee-2 ipHrwP finalPrice"]',
                'price_full': '//div/b[@class="regularPrice"]'
            }
        },
        {   
            'site': 'Terabyte',
            'url': 'https://www.terabyteshop.com.br/produto/31959/gabinete-gamer-redragon-wideload-extreme-mid-tower-rgb-vidro-curvado-temperado-atx-black-sem-fonte-sem-fan-ca-605b',
            'xpaths': {
                'price_in_cash': '//p[@id="valVista"]',
                'price_full': '(//span[@id="valParc"])[2]'
            }
        }
    ]

    driver = start_driver()
    try:
        print('''
  ▄████ ▄▄▄      ▄▄▄▄   ██▓███▄    █▓████▄▄▄█████▓█████      ▄████ ▄▄▄      ███▄ ▄███▓█████ ██▀███  
 ██▒ ▀█▒████▄   ▓█████▄▓██▒██ ▀█   █▓█   ▓  ██▒ ▓▓█   ▀     ██▒ ▀█▒████▄   ▓██▒▀█▀ ██▓█   ▀▓██ ▒ ██▒
▒██░▄▄▄▒██  ▀█▄ ▒██▒ ▄█▒██▓██  ▀█ ██▒███ ▒ ▓██░ ▒▒███      ▒██░▄▄▄▒██  ▀█▄ ▓██    ▓██▒███  ▓██ ░▄█ ▒
░▓█  ██░██▄▄▄▄██▒██░█▀ ░██▓██▒  ▐▌██▒▓█  ░ ▓██▓ ░▒▓█  ▄    ░▓█  ██░██▄▄▄▄██▒██    ▒██▒▓█  ▄▒██▀▀█▄  
░▒▓███▀▒▓█   ▓██░▓█  ▀█░██▒██░   ▓██░▒████▒▒██▒ ░░▒████▒   ░▒▓███▀▒▓█   ▓██▒██▒   ░██░▒████░██▓ ▒██▒
 ░▒   ▒ ▒▒   ▓▒█░▒▓███▀░▓ ░ ▒░   ▒ ▒░░ ▒░ ░▒ ░░  ░░ ▒░ ░    ░▒   ▒ ▒▒   ▓▒█░ ▒░   ░  ░░ ▒░ ░ ▒▓ ░▒▓░
  ░   ░  ▒   ▒▒ ▒░▒   ░ ▒ ░ ░░   ░ ▒░░ ░  ░  ░    ░ ░  ░     ░   ░  ▒   ▒▒ ░  ░      ░░ ░  ░ ░▒ ░ ▒░
░ ░   ░  ░   ▒   ░    ░ ▒ ░  ░   ░ ░   ░   ░        ░      ░ ░   ░  ░   ▒  ░      ░     ░    ░░   ░ 
      ░      ░  ░░      ░          ░   ░  ░         ░  ░         ░      ░  ░      ░     ░  ░  ░     
                      ░                                                                             
                      ''')
        prices = {}
        for link in links:
            scrape_price(driver, link['url'], link['xpaths'], link['site'], prices)
            
        for site, price_data in prices.items():
            print(f'{site}: {price_data}')
        
        if prices['Kabum']['price_in_cash'] < prices['Terabyte']['price_in_cash']:
            print(f"\nCaso você for comprar à vista o melhor preço é na loja Kabum com o preço de {prices['Kabum']['price_in_cash']} reais.")
        else:
            print(f"\nCaso você for comprar à vista o melhor preço é na loja Terabyte, como o preço de {prices['Kabum']['price_in_cash']} reais.")
          
    except Exception as e:
        print(f'Erro ao consultar os preços: {e}')
        
    finally:
        driver.quit()
        print('Programa Finalizado!')

if __name__ == '__main__':
    main()

'''
Ideias:
Calcular o frete do usuário, comparar os preços dos sites e ver qual a melhor opção
'''