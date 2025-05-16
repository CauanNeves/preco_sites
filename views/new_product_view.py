import customtkinter as ctk
from tkinter import messagebox

class NewProductWindow(ctk.CTkToplevel):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.focus_force()
        
        self.title('Novo Produto')
        self.geometry('500x400')
        self.db = db

        self.site_entries = []

        # Nome do produto
        self.label_nome = ctk.CTkLabel(self, text='Nome do Produto:')
        self.label_nome.pack(pady=(10, 0))
        self.entry_nome = ctk.CTkEntry(self, width=400)
        self.entry_nome.pack(pady=(0, 10))

        # Container para os sites
        self.site_frame = ctk.CTkFrame(self)
        self.site_frame.pack(pady=5)

        self.add_site_fields()  # primeiro bloco

        self.btn_add_site = ctk.CTkButton(self, text='+ Adicionar site', command=self.add_site_fields)
        self.btn_add_site.pack(pady=5)

        self.btn_salvar = ctk.CTkButton(self, text='Salvar', command=self.salvar)
        self.btn_salvar.pack(pady=10)

    def add_site_fields(self):
        row_frame = ctk.CTkFrame(self.site_frame)
        row_frame.pack(pady=5)

        site_entry = ctk.CTkEntry(row_frame, width=120, placeholder_text='Nome do site')
        site_entry.pack(side='left', padx=5)

        link_entry = ctk.CTkEntry(row_frame, width=300, placeholder_text='Links (separar por vírgula)')
        link_entry.pack(side='left', padx=5)

        self.site_entries.append((site_entry, link_entry))

    def salvar(self):
        nome_produto = self.entry_nome.get().strip()
        if not nome_produto:
            messagebox.showwarning('Aviso', 'Informe o nome do produto.')
            return

        links_por_site = []
        for site_entry, link_entry in self.site_entries:
            site = site_entry.get().strip()
            links = [url.strip() for url in link_entry.get().split(',') if url.strip()]
            if site and links:
                for link in links:
                    links_por_site.append((site, link))

        if not links_por_site:
            messagebox.showwarning('Aviso', 'Adicione pelo menos um site com link.')
            return

        try:
            self.db.insert_product_with_links(nome_produto, links_por_site)
            messagebox.showinfo('Sucesso', 'Produto salvo com sucesso!')
            self.destroy()
        except Exception as e:
            messagebox.showerror('Erro', f'Erro ao salvar:\n{e}')
