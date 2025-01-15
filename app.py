from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Funções do Webdriver
def start_driver():
    chrome_options = Options()
    arguments = ['--lang=pt-BR', '--start-maximized', 'incognito']

    for argument in arguments:
        chrome_options.add_argument(argument)

    chrome_options.add_experimental_option('prefs', {
        'download.directory_upgrade': True,
        'download.prompt_for_download': False,
        'profile.default_content_setting_values.notifications': 2,
        'profile.default_content_setting_values.automatic_downloads': 1,
    })

    driver = webdriver.Chrome(options=chrome_options)

    return driver


def wait_for_element(driver, by, value, timeout=60):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )
