from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from colorama import Fore, init
from database import Database
from time import sleep
import sys
import re
import io

#Resetando a cor do prompt 
init(autoreset=True)

#Banco de Dados
db= Database()

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
    try:
        if price and price != 'Frete Grátis':
            return float(price.replace('R$', '').replace('ou', '').strip().replace(',', '.'))
        else:
            return 0.0
    except:
        return 0.0
    
    
def retry(action, max_attempts=5, wait_seconds=1, on_fail=None):
    """
    Executa uma ação repetidamente até dar certo ou atingir o máximo de tentativas.
    
    Parameters:
    - action: função a ser executada
    - max_attempts: número máximo de tentativas
    - wait_seconds: tempo de espera entre tentativas
    - on_fail: função a ser chamada quando todas falharem (opcional)
    
    Returns:
    - Resultado da ação (se tiver sucesso), ou None
    """
    for attempt in range(max_attempts):
        try:
            return action()
        except Exception as e:
            if attempt < max_attempts - 1:
                sleep(wait_seconds)
            else:
                if on_fail:
                    on_fail(e)
                return None

    

# Scraping
def scrape_price(driver, link, xpaths, site, prices_dict, prices_freight, freight_actions=None):
    global terabyte_product
    try:
        print(Fore.CYAN + f'Acessando: {site}')
        driver.get(link)
        
        if site not in prices_dict:
            prices_dict[site] = {}
            
        if site not in prices_freight:
            prices_freight[site] = {}
        
        #Fecha a aba de anúncio
        if site == 'Terabyte' and terabyte_product == 0:
            def fechar_popup_terabyte():
                sleep(2.5)
                driver.execute_script("""
                    document.evaluate('(//button[@class= "close"])[3]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click();
                """)
                driver.execute_script('window.scrollTo(0, 600);')
                sleep(1)

            result = retry(fechar_popup_terabyte, max_attempts=5, wait_seconds=1)
            if result is not None or result is None:  # Continua sempre, mesmo se falhar
                terabyte_product += 1


        # Coletando os preços
        for key, xpath_list in xpaths.items():
            try:
                for x in xpath_list:
                    element_text = wait_for_element(driver, By.XPATH, x).text
                    if element_text:
                        match = re.search(r'^\s*([\d.,]+)', element_text)
                        if match:
                            prices_dict[site][key] = formatted_price(match.group(1)) # Adiciona valor formatado
                            break
                    try:
                        prices_dict[site][key]= formatted_price(element_text)
                        break
                    except:
                        pass

            except Exception as e:
                print(f'[Erro] Coleta de preço para "{key}": {e}')

        
        #Coletando o frete
        if freight_actions: #Verifica se existe e não está vazia
            for action in freight_actions: #Executa cada ação
                sleep(0.7)
                result = retry(lambda: action(driver), max_attempts=5, wait_seconds=0.7)
                if isinstance(result, str):
                    try:
                        prices_freight[site]['frete'] = formatted_price(result)
                    except:
                        prices_freight[site]['frete'] = 0.0   

    except Exception as e:
        print(f'Erro ao acessar o site {site}: {e}')

terabyte_product= 0

# Função principal
def main():
    xpaths = [
        {
            'site': 'Magazine Luiza',
            'xpaths_price': {
                'price_in_cash': ['//p[@data-testid= "price-value"]'],
                'price_full': ['((//div[@data-testid= "mod-bestinstallment"]//div/div)[2]/p)[1]', '//div[@data-testid="price-default"]/span']
            },
            'xpaths_freight':[
                lambda driver: driver.execute_script('window.scrollTo(0, 300);'),
                lambda driver: driver.find_element(By.XPATH, '//span[@class= "sc-fscmHZ ldoANx"]').click(),
                lambda driver: wait_for_element(driver, By.XPATH, '//input[@data-testid= "zipcode-input"]').send_keys(db.cep()),
                lambda _: sleep(2),
                lambda driver: driver.execute_script('window.scrollTo(0, 400);'),
                lambda driver: driver.find_element(By.XPATH, '(//div[@data-testid= "shipping-item"]/p)[2]').text
            ]
        },
        {
            'site': 'Kabum',
            'xpaths_price': {
                'price_in_cash': ['//div[@id= "blocoValores"]/div[2]//h4'],
                'price_full': ['//div/b[@class="regularPrice"]']
            },
            'xpaths_freight': [
                lambda driver : driver.execute_script('window.scrollTo(0, 300);'),
                lambda driver: wait_for_element(driver, By.XPATH, '//input[@data-testid= "ZipCodeInput"]').send_keys(db.cep()),
                lambda driver: driver.find_element(By.XPATH, '//form[@id= "formularioCalcularFrete"]//button').click(),
                lambda driver: wait_for_element(driver, By.XPATH, '//div[@id= "listaOpcoesFrete"]/div[2]/span[2]').text
                ] 
        },
        {   
            'site': 'Terabyte',
            'xpaths_price': {
                'price_in_cash': ['//p[@id="valVista"]'],
                'price_full': ['(//span[@id="valParc"])[2]']
            },
            'xpaths_freight': [
                lambda driver: driver.execute_script('window.scrollTo(0, 600);'),
                lambda driver: driver.find_element(By.XPATH, '//button[@class= "btComDet btn tbt_comprar"]').click(),
                lambda driver: wait_for_element(driver, By.XPATH, '//input[@class= "cepInput shopp-cep"]').send_keys(db.cep()),
                lambda driver: driver.find_element(By.XPATH, '//button[@class= "calcFrete btcalcular visible"]').click(),
                lambda driver: wait_for_element(driver, By.XPATH, '(//div[@class= "minicart-frete-value"])[1]').text
            ]
        }
    ]

    driver = start_driver()
    try:
        prices = {}
        freight = {}
        products= db.products_active()
        for product in products:
            if product[0] == 'Magazine Luiza':
                scrape_price(driver, product[1], xpaths[0]['xpaths_price'], product[0], prices, freight, freight_actions=xpaths[0]['xpaths_freight'])
            elif product[0] == 'Kabum':
                scrape_price(driver, product[1], xpaths[1]['xpaths_price'], product[0], prices, freight, freight_actions=xpaths[1]['xpaths_freight'])
            elif product[0] == 'Terabyte':
                scrape_price(driver, product[1], xpaths[2]['xpaths_price'], product[0], prices, freight, freight_actions=xpaths[2]['xpaths_freight'])

        product_id= db.products_active()[0][2]
        for site, price_data in prices.items():
            db.save_history(product_id, site, price_data['price_in_cash'], price_data['price_full'], freight[site]['frete'])
        
        def calcular_preco_total(loja, tipo_preco):
            return round(float(prices[loja][tipo_preco]) + float(freight[loja]['frete']), 2)
                

        lojas = ['Magazine Luiza','Kabum', 'Terabyte']
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
        
if __name__ == '__main__':
    main()