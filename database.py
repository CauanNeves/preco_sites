import sqlite3

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
                    nome_produto TEXT NOT NULL,
                    site TEXT NOT NULL,
                    url TEXT NOT NULL,
                );
            ''')
            conn.commit()

            #Tabela CEP
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cep(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    
    #Adicionando dados na tabela produto
    def add_product(self, nome_produto, site, url):
        with self._connect() as conn:
            cursor= conn.cursor()
            cursor.execute('INSERT INTO produto (nome_produto, site, url) VALUES (?, ?, ?)', (nome_produto, site, url))
            conn.commit()
    
    #Exibindo tabela produto
    def products(self):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM produto')
            return cursor.fetchall()
    
    def edit_url(self, nome_produto, novo_url, site):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE produto SET url = ? WHERE nome_produto = ? and site = ?", (novo_url, nome_produto, site))
            conn.commit()

    def del_product(self, nome_produto):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM produto WHERE nome_produto = ?', (nome_produto,))
            conn.commit()

    #Adicionando CEP
    def add_cep(self, cep):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM cep')  # mantém um único CEP
            cursor.execute('INSERT INTO cep (id, n_cep) VALUES (1, ?)' (cep,))
            conn.commit()
    
    #Retornando CEP
    def cep(self):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT n_cep FROM cep WHERE id = 1')
            result = cursor.fetchone()
            return result[0] if result else None
    