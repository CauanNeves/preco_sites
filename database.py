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
                    id_produto INTEGER NOT NULL,
                    site TEXT NOT NULL,
                    url TEXT NOT NULL,
                    ativado TEXT NOT NULL,
                    FOREIGN KEY (id_produto) REFERENCES produto(id)
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
                    id_produto INTEGER NOT NULL,
                    site TEXT NOT NULL,
                    preco_vista REAL,
                    preco_parcelado REAL,
                    frete REAL,
                    data TEXT NOT NULL,
                    hora TEXT NOT NULL,
                    FOREIGN KEY (id_produto) REFERENCES produto(id) 
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

    def insert_link(self, id_produto, site, url):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO link (id_produto, site, url, ativado) VALUES (?, ?, ?, ?)', (id_produto, site, url, 'Sim'))
            conn.commit()

    #Adicionando Produto
    def insert_product_with_links(self, nome_produto, lista_sites_links):
        id_produto = self.insert_product(nome_produto)
        for site, link in lista_sites_links:
            self.insert_link(id_produto, site, link)
        with self._connect() as conn:
            cursor= conn.cursor()
            cursor.execute('UPDATE link SET ativado = ? WHERE id_produto != ?', ('Não', id_produto))
            conn.commit()

    #Buscar id do produto
    def id_produto(self, nome_produto):
        with self._connect() as conn:
            cursor= conn.cursor()
            cursor.execute('SELECT id FROM produto WHERE nome_produto = ?', (nome_produto,))
            result= cursor.fetchone()

            return result[0] if result else None
    
    #Editando link
    def edit_url(self, id_produto, site, novo_url):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE link SET url = ? WHERE id_produto = ? and site = ? ', (novo_url, id_produto , site))
            conn.commit()


    #Buscando links de um produto
    def get_links_by_produto(self, id_produto):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT site, url FROM link WHERE id_produto = ?', (id_produto,))
            return cursor.fetchall()


    #Excluindo Produto
    def del_product(self, id_produto):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM link WHERE id_produto = ?', (id_produto,))
            cursor.execute('DELETE FROM historico WHERE id_produto = ?', (id_produto,))
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
    def save_history(self, id_produto, site, preco_vista, preco_parcelado, frete):
        date= datetime.now().strftime('%d/%m/%Y')
        hour= datetime.now().strftime('%H:%M')
        with self._connect() as conn:
            cursor= conn.cursor()
            cursor.execute('INSERT INTO historico (id_produto, site, preco_vista, preco_parcelado, frete, data, hora) VALUES (?, ?, ?, ?, ?, ?, ?)', (id_produto, site, preco_vista, preco_parcelado, frete, date, hour))
            conn.commit()
    
    #Buscando no Histórico
    def search_history(self, id_produto):
        with self._connect() as conn:
            cursor= conn.cursor()
            cursor.execute('SELECT date, preco_vista, preco_parcelado FROM historico WHERE id_produto = ?', (id_produto,))
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

    def table(self):
        with self._connect() as conn:
            cursor= conn.cursor()
            cursor.execute('''
                SELECT
                    l.id as id_link,
                    p.nome_produto as produto,
                    l.site as site,
                    l.url as link,
                    l.ativado
                FROM produto p
                JOIN link l ON p.id = l.id_produto
                ORDER BY l.id desc
            ''')
            return cursor.fetchall()
        
    def del_selected_link(self, id_link):
        with self._connect() as conn:
            cursor= conn.cursor()
            cursor.execute('DELETE FROM link WHERE id = ?', (id_link, ))
            conn.commit()

    def filter_product(self, product):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT
                    l.id as id_link,
                    p.nome_produto as produto,
                    l.site as site,
                    l.url as link,
                    l.ativado as ativado
                FROM produto p
                JOIN link l ON p.id = l.id_produto
                WHERE p.nome_produto LIKE ?
                ORDER BY l.ativado DESC
            ''', (f"%{product}%",))
            return cursor.fetchall()
        
    def activate(self, id, site):
        with self._connect() as conn:
            cursor= conn.cursor()
            cursor.execute('UPDATE link SET ativado = ? WHERE id = ? AND site = ?', ('Sim', id, site))
            conn.commit()
            
    def disable(self, id):
        with self._connect() as conn:
            cursor= conn.cursor()
            cursor.execute('UPDATE link SET ativado = ? WHERE id = ?', ('Não', id))
            conn.commit()

    #Função em conjunto com a ativação de produtos do views.table_view. 
    def product_active(self):
        with self._connect() as conn:
            cursor= conn.cursor()

            is_active= cursor.execute('SELECT p.nome_produto FROM produto p JOIN link l on p.id = l.id_produto WHERE l.ativado == ?', ('Sim', ))
            try:
                return is_active.fetchone()[0]
            
            except IndexError:
                return None
            
    def products_active(self):
        with self._connect() as conn:
            cursor= conn.cursor()

            products= cursor.execute('SELECT site, url, id_produto FROM link')
            try:
                return products.fetchall()
            except:
                return None