from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import undetected_chromedriver as uc
import sys
import io
from colorama import Fore, Style, init
#Resetando a cor do prompt 
init(autoreset=True)

# Evita chamada duplicada de quit() após o script finalizar
uc.Chrome.__del__ = lambda self: None

#Resolvendo erro wind6
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def start_driver():
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument('--lang=pt-BR')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--incognito')
    
    chrome_prefs = {
        'download.directory_upgrade': True,
        'download.prompt_for_download': False,
        'profile.default_content_setting_values.notifications': 2,
        'profile.default_content_setting_values.automatic_downloads': 1,
    }
    chrome_options.add_experimental_option('prefs', chrome_prefs)

    driver = uc.Chrome(options=chrome_options)
    return driver


# Função para esperar o elemento
def wait_for_element(driver, by, value, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )

# Formatação de preço
def formatted_price(price):
    return float(price.replace('R$', '').strip().replace(',', '.'))

# Scraping
def scrape_price(driver, link, xpaths, site, prices_dict, prices_freight, freight_actions=None):
    try:
        print(Fore.CYAN + f'Acessando: {site}')
        driver.get(link)
        
        if site not in prices_dict:
            prices_dict[site] = {}
            
        if site not in prices_freight:
            prices_freight[site] = {}
        
        #Fecha a aba de anúncio
        if site == 'Terabyte':
            sleep(2)
            driver.execute_script("""document.evaluate('(//button[@class= "close"])[3]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click();""")
            driver.execute_script('window.scrollTo(0, 600);')
            sleep(1)

        #Coletando os preços
        for key, xpath in xpaths.items():  
            try:
                element = wait_for_element(driver, By.XPATH, xpath).text
                prices_dict[site][key] = formatted_price(element) #Adiciona o valor formatado ao dicionário
            except Exception as e:
                print(f"Erro ao buscar o preço '{key}' em {site}: {e}")
        
        #Coletando o frete
        if freight_actions: #Verifica se existe e não está vazia
            for action in freight_actions: #Executa cada ação
                try:
                    sleep(0.7)
                    result = action(driver) #Retorna os valores de cada função (no caso só a última que vai ter algum valor)
                    if isinstance(result, str):
                        prices_freight[site]['frete'] = formatted_price(result) #Adiciona o valor formatado ao dicionário
                except Exception as e:
                    print(f"Erro ao executar ação de frete em {site}: {e}")
                    break
                
    except Exception as e:
        print(f'Erro ao acessar o site {site}: {e}')

# Função principal
def main():
    links = [
                {
            'site': 'Kabum',
            'url': 'https://www.kabum.com.br/produto/627947',
            'xpaths_price': {
                'price_in_cash': '//div/h4[@class="sc-5492faee-2 ipHrwP finalPrice"]',
                'price_full': '//div/b[@class="regularPrice"]'
            },
            'xpaths_freight': [
                lambda driver : driver.execute_script("window.scrollTo(0, 300);"),
                lambda driver: driver.find_element(By.ID, 'inputCalcularFrete').send_keys('23900650'),
                lambda driver: driver.find_element(By.ID, 'botaoCalcularFrete').click(),
                lambda driver: wait_for_element(driver, By.XPATH, '(//span[@class= "sc-4253a8e4-2 etvZuo"])[2]').text
                ] 
        },
        {   
            'site': 'Terabyte',
            'url': 'https://www.terabyteshop.com.br/produto/31959/gabinete-gamer-redragon-wideload-extreme-mid-tower-rgb-vidro-curvado-temperado-atx-black-sem-fonte-sem-fan-ca-605b',
            'xpaths_price': {
                'price_in_cash': '//p[@id="valVista"]',
                'price_full': '(//span[@id="valParc"])[2]'
            },
            'xpaths_freight': [
                lambda driver: driver.execute_script('window.scrollTo(0, 600);'),
                lambda driver: driver.find_element(By.XPATH, '//button[@class= "btComDet btn tbt_comprar"]').click(),
                lambda driver: wait_for_element(driver, By.XPATH, '//input[@class= "cepInput shopp-cep"]').send_keys('23900650'),
                lambda driver: driver.find_element(By.XPATH, '//button[@class= "calcFrete btcalcular visible"]').click(),
                lambda driver: wait_for_element(driver, By.XPATH, '(//div[@class= "minicart-frete-value"])[1]').text
            ]
        }
    ]

    driver = start_driver()
    try:
        print(Fore.LIGHTGREEN_EX +'''
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
        freight = {}
        for link in links:
            scrape_price(driver, link['url'], link['xpaths_price'], link['site'], prices, freight, freight_actions=link['xpaths_freight'])
            
        for site, price_data in prices.items():
            print(f'{site}: {price_data}')
            if site in freight and freight[site].get('frete'):
                print(f'{site}: {freight[site]}')
        
        def calcular_preco_total(loja, tipo_preco):
            return round(float(prices[loja][tipo_preco]) + float(freight[loja]['frete']), 2)

        lojas = ['Kabum', 'Terabyte']
        tipos = {
            'price_in_cash': 'à vista',
            'price_full': 'parcelado'
        }

        precos_totais = {
            loja: {
                tipo: calcular_preco_total(loja, tipo)
                for tipo in tipos
            }
            for loja in lojas
        }

        for tipo, descricao in tipos.items():
            melhor_loja = min(lojas, key=lambda loja: precos_totais[loja][tipo])
            melhor_preco = precos_totais[melhor_loja][tipo]
            print(Fore.LIGHTYELLOW_EX + f"\nCaso você for comprar {descricao}, o melhor preço é na loja {melhor_loja} com o valor de {melhor_preco} reais.")
        
    except Exception as e:
        print(f'Erro ao consultar os preços: {e}')
        
    finally:
        if driver:
            driver.quit()
            driver = None  # <- Evita o __del__ tentar agir em algo já encerrado
        print('Programa Finalizado!')

if __name__ == '__main__':
    main()