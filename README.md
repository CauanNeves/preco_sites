### 📖 README - Web Scraping com Selenium 🕵️‍♂️

---

## 🚀 Sobre o Projeto
Este projeto utiliza a biblioteca **Selenium** para realizar o _web scraping_ de preços em diferentes sites. Ele permite comparar preços de produtos em lojas específicas e exibir o melhor preço encontrado para compras à vista e parcelado, Além de calcular o frete.  

---

## 📋 Pré-requisitos

Antes de executar o projeto, você precisará ter instalado:

1. **Python 3.7 ou superior** 🐍  
2. **Google Chrome** (versão compatível com o WebDriver do Selenium) 🌐  
3. **WebDriver do Chrome** (chromedriver) 🛠️  
4. As dependências do projeto, instaláveis com o comando:
   ```bash
   pip install selenium
   ```

---

## 🛠️ Configuração

1. **Baixe o WebDriver:**  
   Certifique-se de que o `chromedriver` está disponível em seu sistema e que sua versão corresponde à versão do navegador Google Chrome instalada.  

2. **Adapte os Links e XPath dos Produtos:**  
   - Insira os URLs dos produtos que você deseja monitorar.  
   - Ajuste os `XPath` para corresponder aos elementos específicos que contêm os preços nas páginas-alvo.  

3. **Configuração de Idioma e Preferências do Navegador:**  
   O script utiliza opções como modo incógnito, idioma configurado para `pt-BR` e desabilitação de notificações.  

---

## 🧩 Estrutura do Código

- **`start_driver`**: Configura e inicia o navegador com as opções desejadas.  
- **`wait_for_element`**: Aguarda até que um elemento esteja presente na página antes de interagir com ele.  
- **`formatted_price`**: Converte o preço extraído de texto para formato numérico (float).  
- **`scrape_price`**: Realiza o acesso ao site e coleta os preços usando os XPath fornecidos.  
- **`main`**: Ponto de entrada do programa, orquestrando o scraping, comparação de preços e exibição dos resultados.  

---

## 🖥️ Como Executar

1. Clone este repositório em sua máquina local:
   ```bash
   git clone https://github.com/CauanNeves/preco_sites.git
   ```

2. Acesse o diretório do projeto:
   ```bash
   cd preco-sites
   ```

3. Instale as dependências necessárias:
   ```bash
   pip install -r requirements.txt
   ```

4. Execute o script principal:
   ```bash
   python app.py
   ```

---

## ✨ Funcionalidades

1. **Coleta de Preços**:
   - Monitora produtos em múltiplos sites.  
   - Realiza o parsing de preços à vista e a prazo.  

2. **Comparação de Preços**:
   - Determina qual loja oferece o preço mais baixo para pagamento à vista.  

3. **Relatórios Dinâmicos**:
   - Exibe os resultados em um formato simples e legível.  

---

## 🐛 Possíveis Problemas e Soluções

- **Problema**: O XPath do preço mudou ou está incorreto.  
  **Solução**: Atualize os valores de XPath no código de acordo com a estrutura do site.

- **Problema**: O `chromedriver` não está compatível com a versão do Google Chrome.  
  **Solução**: Atualize o `chromedriver` para a versão correspondente.  

- **Problema**: Bloqueios no site por automação.  
  **Solução**: Utilize atrasos entre requisições ou métodos como "User-Agent Spoofing".  

---

## 🏆 Contribuições

Sinta-se à vontade para abrir _issues_ ou _pull requests_ para melhorar o código ou sugerir novas funcionalidades!  

---

### 📬 Contato
Qualquer dúvida, entre em contato pelo e-mail: **c.neves8903@gmail.com**.

---

**Divirta-se raspando os preços!** 🎉
