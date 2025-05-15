import customtkinter as ctk
from tkinter import messagebox

class EditLinkWindow(ctk.CTkToplevel):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.title('Editar link')
        self.geometry('350x240')
        self.maxsize(350,240)
        self.minsize(350,240)
        self.db

        #Nome produto
        ctk.CTkLabel(self, text= 'Nome do produto:').pack(pady= (15,5))
        self.product_entry= ctk.CTkEntry(self, width= 250)
        self.product_entry.pack(pady= 5)

        #site
        ctk.CTkLabel(self, text= 'Site:').pack(pady= (15, 5))
        self.site_entry= ctk.CTkEntry(self, width= 250)
        self.site_entry.pack(pady= 5)

        #Novo link
        ctk.CTkLabel(self, text= 'Novo link (url): ').pack(pady= (15, 5))
        self.url_entry= ctk.CTkEntry(self, width= 250)
        self.url_entry.pack(pady= 5)

        #Botões
        btn_frame= ctk.CTkFrame(self, fg_color= 'transparent')
        btn_frame.pack(pady= 10)

        ctk.CTkButton(btn_frame, text= 'Salvar', command= self.att_url).grid(row= 0, column= 0, padx= 10)
        ctk.CTkButton(btn_frame, text= 'Cancelar', command= self.destroy).grid(row= 0, column= 1, padx= 10)

    #Função
    def att_url(self):
        product= self.product_entry.get().strip()
        site= self.site_entry.get().strip().lower()
        url= self.url_entry.get().strip()

        if not product or not site or not url:
            messagebox.showwarning('Campos Obriogatórios', 'Preencha todos os campos.')
            return
        
        product_db= self.db.id_produto(product)

        if not product_db:
            messagebox.showerror('Erro', f'Produto {product} não encontrado.\n Verifique o nome digitado e tente novamente.')
            return
        
        try:
            self.db.edit_url(product_db['id'], site, url)
            messagebox.showinfo('Sucesso', f'Link do produto "{product}", no site "{site}" foi atualizado')
            self.destroy()
        except Exception as e:
            messagebox.showerror('Error', f'Erro ao atualizar o link:\n{e}')