from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep

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
def scrape_price(driver, link, xpaths, site, prices_dict, prices_freight, freight_actions=None):
    try:
        print(f'Acessando: {site}')
        driver.get(link)
        
        if site not in prices_dict:
            prices_dict[site] = {}
            
        if site not in prices_freight:
            prices_freight[site] = {}
        
        if site == 'Terabyte':
            wait_for_element(driver, By.XPATH, '(//button[@class= "close"])[3]')
            sleep(0.5)
            driver.execute_script("""document.evaluate('(//button[@class= "close"])[3]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click();""")

        #Preço
        for key, xpath in xpaths.items():
            try:
                element = wait_for_element(driver, By.XPATH, xpath).text
                prices_dict[site][key] = formatted_price(element)
            except Exception as e:
                print(f"Erro ao buscar o preço '{key}' em {site}: {e}")
        
        #Frete
        if freight_actions: #Verifica se existe e não está vazia
            for action in freight_actions: #Executa cada ação
                try:
                    sleep(0.7)
                    result = action(driver) #Retorna os valores de cada função (no caso só a última que vai ter algum valor)
                    if isinstance(result, str):
                        prices_freight[site]['frete'] = formatted_price(result)
                except Exception as e:
                    print(f"Erro ao executar ação de frete em {site}: Bloqueio do bot")
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
                lambda driver: wait_for_element(driver, By.ID, 'inputCalcularFrete').send_keys('23900650'),
                lambda driver: driver.find_element(By.XPATH, '//button[@class= "calcFrete btcalcular visible"]').click(),
                lambda driver: wait_for_element(driver, By.XPATH, '(//div[@class= "minicart-frete-value"])[1]').text
            ]
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
        freight = {}
        for link in links:
            scrape_price(driver, link['url'], link['xpaths_price'], link['site'], prices, freight, freight_actions=link['xpaths_freight'])
            
        for site, price_data in prices.items():
            print(f'{site}: {price_data}')
            if site in freight and freight[site].get('frete'):
                print(f"{site}: {freight[site]}")
        
        if (float(prices['Kabum']['price_in_cash']) + (float(freight['Kabum']['frete'])) < (float(prices['Terabyte']['price_in_cash']) + float(freight['Terabyte']['frete']))):
            print(f"\nCaso você for comprar à vista o melhor preço é na loja Kabum com o valor de {prices['Kabum']['price_in_cash']} reais.")
        else:
            print(f"\nCaso você for comprar à vista o melhor preço é na loja Terabyte, como o valor de {prices['Kabum']['price_in_cash']} reais.")

        if (float(prices['Kabum']['price_full']) + (float(freight['Kabum']['frete'])) < (float(prices['Terabyte']['price_full']) + float(freight['Terabyte']['frete']))):
            print(f"\nCaso você for comprar parcelado o melhor preço é na loja Kabum com o valor de {prices['Kabum']['price_full']} reais.")
        else:
            print(f"\nCaso você for comprar parcelado o melhor preço é na loja Terabyte, como o valor de {prices['Kabum']['price_in_cash']} reais.")
          
    except Exception as e:
        print(f'Erro ao consultar os preços: {e}')
        
    finally:
        driver.quit()
        print('Programa Finalizado!')

if __name__ == '__main__':
    main()