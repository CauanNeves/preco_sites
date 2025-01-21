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

# Função genérica para scraping
def scrape_price(driver, link, xpaths):
    driver.get(link)
    prices = {}
    for key, xpath in xpaths.items():
        element = wait_for_element(driver, By.XPATH, xpath).text
        prices[key] = formatted_price(element)
    return prices

# Função principal
def main():
    links = [
        {   
            "site": "Terabyte",
            "url": "https://www.terabyteshop.com.br/produto/31959/gabinete-gamer-redragon-wideload-extreme-mid-tower-rgb-vidro-curvado-temperado-atx-black-sem-fonte-sem-fan-ca-605b",
            "xpaths": {
                "price_in_cash": '//p[@id="valVista"]',
                "price_full": '(//span[@id="valParc"])[2]'
            }
        },
        {
            "site": "Kabum",
            "url": "https://www.kabum.com.br/produto/627947",
            "xpaths": {
                "price_in_cash": '//div/h4[@class="sc-5492faee-2 ipHrwP finalPrice"]',
                "price_full": '//div/b[@class="regularPrice"]'
            }
        }
    ]

    driver = start_driver()
    try:
        for link_info in links:
            prices = scrape_price(driver, link_info["url"], link_info["xpaths"])
            print(f"Preços para {link_info['site']}: {prices}")
    except Exception as e:
        print(f'Erro ao consultar os preços: {e}')
    finally:
        driver.quit()
        print('Programa Finalizado!')

if __name__ == '__main__':
    main()
