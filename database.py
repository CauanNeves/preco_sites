import sqlite3
from datetime import datetime 

class Database:
    def __init__(self, db_path= 'precos.db'):
        self.db_path= db_path
        self._create_table()

    def _connect(self):
        return sqlite3.connect(self.db_path)
    
    def _create_table(self):
        with self._connect() as conn:
            cursor= conn.cursor()

            #Tabela Produto
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS produto (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome_produto TEXT NOT NULL
                );
            ''')
            conn.commit()

            #Tabela Link
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS link (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    produto_id INTEGER NOT NULL,
                    site TEXT NOT NULL,
                    url TEXT NOT NULL,
                    FOREIGN KEY (produto_id) REFERENCES produto(id)
                );
            ''')
            conn.commit()

            #Tabela CEP
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cep(
                    id INTEGER,
                    n_cep INTEGER NOT NULL           
                );
            ''')
            conn.commit()

            #Tabela Histórico
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS historico(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    produto_id INTEGER NOT NULL,
                    data TEXT NOT NULL,
                    preco_vista REAL,
                    preco_parcelado REAL,
                    FOREIGN KEY (produto_id) REFERENCES produto(id) 
                )
            ''')
            conn.commit()
    
    #
    def insert_product(self, nome_produto):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO produto (nome_produto) VALUES (?)', (nome_produto,))
            conn.commit()
            return cursor.lastrowid  # retorna o id do novo produto

    def insert_link(self, produto_id, site, url):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO link (produto_id, site, url) VALUES (?, ?, ?)', (produto_id, site, url))
            conn.commit()

    #Adicionando Produto
    def insert_product_with_links(self, nome_produto, lista_sites_links):
        produto_id = self.insert_product(nome_produto)
        for site, link in lista_sites_links:
            self.insert_link(produto_id, site, link)

    #Buscar id do produto
    def id_produto(self, nome_produto):
        with self._connect() as conn:
            cursor= conn.cursor()
            cursor.execute('SELECT id FROM produto WHERE nome_produto = ?', (nome_produto,))
            result= cursor.fetchone()

            return result[0] if result else None
    
    #Editando link
    def edit_url(self, produto_id, site, novo_url):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE link SET url = ? WHERE produto_id = ? and site = ? ', (novo_url, produto_id , site))
            conn.commit()


    #Buscando links de um produto
    def get_links_by_produto(self, produto_id):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT site, url FROM link WHERE produto_id = ?', (produto_id,))
            return cursor.fetchall()


    #Excluindo Produto
    def del_product(self, id_produto):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM link WHERE produto_id = ?', (id_produto,))
            cursor.execute('DELETE FROM historico WHERE produto_id = ?', (id_produto,))
            cursor.execute('DELETE FROM produto WHERE id = ?', (id_produto,))
            conn.commit()

    #Adicionando CEP
    def add_cep(self, cep):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM cep')  # mantém um único CEP
            cursor.execute('INSERT INTO cep (id, n_cep) VALUES (?, ?)', (1, cep))
            conn.commit()
    
    #Retornando CEP
    def cep(self):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT n_cep FROM cep WHERE id = 1')
            result = cursor.fetchone()
            return result[0] if result else None
        
    #Historico
    def save_history(self, produto_id, preco_vista, preco_parcelado):
        date= datetime.now().strftime('%d/%m/%Y')
        with self._connect() as conn:
            cursor= conn.cursor()
            cursor.execute('INSERT INTO historico (produto_id, data, preco_vista, preco_parcelado) VALUES (?, ?, ?, ?)', (produto_id, date, preco_vista, preco_parcelado))
            conn.commit()
    
    #Buscando no Histórico
    def search_history(self, produto_id):
        with self._connect() as conn:
            cursor= conn.cursor()
            cursor.execute('SELECT date, preco_vista, preco_parcelado FROM historico WHERE produto_id = ?', (produto_id,))
            return cursor.fetchall()
    
    #RESETANDO BANCO DE DADOS
    def reset_db(self):
        with self._connect() as conn:
            cursor= conn.cursor()
            cursor.execute('DELETE FROM produto')
            cursor.execute('DELETE FROM cep')
            cursor.execute('DELETE FROM historico')
            cursor.execute('DELETE FROM link')
            cursor.execute('DELETE FROM sqlite_sequence')

            conn.commit()