import customtkinter as ctk
from tkinter import ttk, messagebox

class ListProductWindow(ctk.CTkToplevel):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.focus_displayof()
        self.db= db

        self.title('Tabela dos Produtos')
        self.geometry('600x400')

        top_frame= ctk.CTkFrame(self)
        top_frame.pack(pady= 10, padx= 10, fill= 'x')

        ctk.CTkLabel(top_frame, text='Produtos Registrados', font=ctk.CTkFont(size=16, weight='bold')).pack(side='left', padx=5)

        self.entry_filter= ctk.CTkEntry(top_frame, placeholder_text= 'Filtrar por Nome...', width= 200)
        self.entry_filter.pack(side= 'left', padx= 5)

        self.btn_filter= ctk.CTkButton(top_frame, text= 'Filtrar', command= self.apply_filter).pack(side= 'left', padx= 5)

        frame= ctk.CTkFrame(self)
        frame.pack(pady= 10, fill= 'both', expand= True)

        style= ttk.Style()
        style.theme_use('default')
        style.configure('Treeview', background='#2A2D2E', foreground='white', fieldbackground='#2A2D2E', rowheight=25)
        style.map('Treeview', background=[('selected', '#4D93D9')])

        self.tree= ttk.Treeview(frame, columns= ('id', 'produto', 'site', 'url'), show= 'headings')
        self.tree.heading('id', text= 'ID')
        self.tree.heading('produto', text= 'Produto')
        self.tree.heading('site', text= 'Site')
        self.tree.heading('url', text= 'URL')

        self.tree.column('id', width= 40, anchor= 'center')
        self.tree.column('produto', width= 150)
        self.tree.column('site', width= 100)
        self.tree.column('url', width= 290)

        self.tree.pack(fill= 'both', expand= True)

        self.load_data()
        
        btn_frame= ctk.CTkFrame(self)
        btn_frame.pack(pady= 10)

        # ctk.CTkButton(btn_frame, text= 'Ativar Produto', fg_color= '##4D93D9', command= self.activate_product).pack(side= 'left', padx= 10)
        ctk.CTkButton(btn_frame, text= 'Deletar produto', fg_color= '#E51200', command= self.del_row).pack(side= 'left', padx= 10)
        ctk.CTkButton(btn_frame, text= 'Fechar', command= self.destroy).pack(pady= 10)

    def apply_filter(self):
        product= self.entry_filter.get()
        self.load_data(product)
    
    def del_row(self):
        selected= self.tree.selection()
        if not selected:
            messagebox.showwarning('Aviso', 'Selecione a linha que deseja excluir')
            return
        
        product= self.tree.item(selected)
        id_link= product['values'][0]
        product_name= product['values'][1]

        confirm= messagebox.askyesno('Confirmação', f'Tem certeza que deseja apagar essa linha?')
        if confirm:
            try:
                self.db.del_selected_link(id_link)
                self.tree.delete(selected)
                messagebox.showinfo('Aviso', 'Linha apagada com sucesso')
            
            except Exception as e:
                messagebox.showerror('Error', f'Erro ao deletar: {e}')

    def load_data(self, filtered_product= ''):
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            products= self.db.filter_product(filtered_product)
            for product in products:
                self.tree.insert('', 'end', values= product)

        except Exception as e:
            messagebox.showerror('ERRO', f'Erro ao carregar tabela, erro: {e}')