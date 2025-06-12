### 📖 README - Web Scraping com Selenium 🕵️‍♂️

---

## 🚀 Sobre o Projeto
Este projeto utiliza a biblioteca **Selenium** para realizar o _web scraping_ de preços em diferentes sites.   

# 🕵️ Comparador de Preços com Selenium

Este projeto realiza a coleta automatizada de preços e frete de produtos em diferentes e-commerces brasileiros usando Selenium com Chrome indetectável (undetected-chromedriver). Tem o objetivo de facilitar a comparação de preços de um produto específico. Queria comprar esse gabinete, então resolvi fazer um código que comparasse o preço desse gabinete em diferentes sites e me retornasse qual o site com menor preço, tanto para pagamentos à vista quanto para pagamento parcelado, além de calcular o frete.

---

## 💻 Funcionalidades
- Acesso automatizado a páginas de produto
- Captura de preço à vista e parcelado
- Simulação de cálculo de frete via CEP
- Exibição da melhor loja com base no valor final (produto + frete)

---

## 📦 Executável

Se você só quer **usar o programa**, baixe o arquivo `comparador.exe` (disponível na aba de releases ou na pasta raiz) e execute normalmente. 

> ⚠️ Dica: Ao executar o `.exe`, aguarde o carregamento das páginas. Algumas lojas têm elementos que demoram um pouco para aparecer.

---

## 🧑‍💻 Para desenvolvedores

Caso queira rodar o código-fonte ou modificar o script, siga os passos abaixo:

### 🔧 Pré-requisitos

Você precisa ter o Python instalado. Em seguida, instale as dependências:

```bash
pip install selenium undetected-chromedriver colorama
```

### ▶️ Como executar

```bash
python app.py
```

O script abrirá um navegador automaticamente, acessará os sites e mostrará no terminal o melhor preço (à vista e parcelado), com frete incluso.

---

## 🏪 Lojas monitoradas
- Magazine Luiza
- Kabum (2 variações)
- Terabyte

---

## ✏️ Personalização

Para adicionar mais produtos ou lojas, edite a lista `links` no final do código. Cada entrada pode conter:
- `site`: Nome da loja
- `url`: Link do produto
- `xpaths_price`: XPaths para preços
- `xpaths_freight`: Ações a serem executadas para buscar o frete

---

## 🔚 Exemplo de Saída

```bash
Magazine Luiza: {'price_in_cash': 254.1, 'price_full': 269.9}
Magazine Luiza: {'frete': 19.9}
...
Caso você for comprar à vista, o melhor preço é na loja Kabum (2) com o valor de 248.5 reais.
```

[![Assista ao vídeo](https://img.youtube.com/vi/4eml7UQJIso/hqdefault.jpg)](https://www.youtube.com/watch?v=4eml7UQJIso)


---

## 🛠️ Feito com:
- [Python](https://www.python.org/)
- [Selenium](https://selenium.dev/)
- [Undetected ChromeDriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver)
- [Colorama](https://pypi.org/project/colorama/)

---

### 📬 Contato
Qualquer dúvida, entre em contato pelo e-mail: **c.neves8903@gmail.com**.