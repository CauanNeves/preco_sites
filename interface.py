from database import Database

db= Database()

xpaths = [
    {
        'site': 'Magazine Luiza',
        'xpaths_price': {
            'price_in_cash': '//p[@class= "sc-dcJsrY eLxcFM sc-kUdmhA cvHkKW"]',
            'price_full': '((//div[@data-testid= "mod-bestinstallment"]//div/div)[2]/p)[1]'
        },
        'xpaths_freight':[
            lambda driver: driver.execute_script('window.scrollTo(0, 300);'),
            lambda driver: driver.find_element(By.XPATH, '//span[@class= "sc-fscmHZ ldoANx"]').click(),
            lambda driver: wait_for_element(driver, By.ID, 'zipcode').send_keys(cep),
            lambda driver: sleep(2),
            lambda driver: driver.execute_script('window.scrollTo(0, 300);'),
            lambda driver: wait_for_element(driver, By.XPATH, '//p[@class= "sc-dcJsrY eLxcFM sc-pKqro cAJMya"]').text
        ]
    },
    {
        'site': 'Kabum',
        'xpaths_price': {
            'price_in_cash': '//div/h4[@class="sc-5492faee-2 ipHrwP finalPrice"]',
            'price_full': '//div/b[@class="regularPrice"]'
        },
        'xpaths_freight': [
            lambda driver : driver.execute_script('window.scrollTo(0, 300);'),
            lambda driver: driver.find_element(By.ID, 'inputCalcularFrete').send_keys(cep),
            lambda driver: driver.find_element(By.ID, 'botaoCalcularFrete').click(),
            lambda driver: wait_for_element(driver, By.XPATH, '(//span[@class= "sc-4253a8e4-2 etvZuo"])[2]').text
            ] 
    },
    {   
        'site': 'Terabyte',
        'xpaths_price': {
            'price_in_cash': '//p[@id="valVista"]',
            'price_full': '(//span[@id="valParc"])[2]'
        },
        'xpaths_freight': [
            lambda driver: driver.execute_script('window.scrollTo(0, 600);'),
            lambda driver: driver.find_element(By.XPATH, '//button[@class= "btComDet btn tbt_comprar"]').click(),
            lambda driver: wait_for_element(driver, By.XPATH, '//input[@class= "cepInput shopp-cep"]').send_keys(cep),
            lambda driver: driver.find_element(By.XPATH, '//button[@class= "calcFrete btcalcular visible"]').click(),
            lambda driver: wait_for_element(driver, By.XPATH, '(//div[@class= "minicart-frete-value"])[1]').text
        ]
    }
]

links= []
while True:
    site= input('Qual link deseja adicionar? (Terabyte, Magazine Luiza, Kabum)')
    if site.lower() in ['terabyte', 'magazine luiza', 'kabum']:
        if site == 'magazine luiza':
            nome= input('\nnome do produto:')
            link= input('\nLink: ')
            links.append(xpaths[0])
            links[0]['url']= link

            db.add_product(nome, site, link)
            
        if site == 'kabum':
            link= input('\nLink: ')
            links.append(xpaths[1])
            links[0]['url']= link

        if site == 'terabyte':
            link= input('\nLink: ')
            links.append(xpaths[2])
            links[0]['url']= link

        ask_continue= input('\nDeseja adicionar mais algum link? (s/n)')
        if ask_continue.lower() == 's':
            pass
        
        else:
            print('Atualmente não há nenhum link, por favor adicione.')
        
    else:
        print('Não está na lista')


    # link_magazineLuiza= input('Link do produto na loja Magazine luiza:\n')
    # link_kabum = input('\nLink do produto na Loja Kabum:\n')
    # link_terabyte= input('\nLink do produto na loja da Terabyte:\n')
    # cep= input('\nDigite o CEP:')