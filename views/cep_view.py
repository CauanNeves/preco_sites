import customtkinter as ctk
from tkinter import messagebox

class CepWindow(ctk.CTkToplevel):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.focus_force()
        
        #config
        self.title('Atualizando CEP')
        self.geometry('300x180')
        self.minsize(300, 180)
        self.maxsize(300, 180)

        self.db= db

        #Interface
        self.label= ctk.CTkLabel(self, text= 'Digite o CEP (sem traço): ')
        self.label.pack(pady= (20, 5))

        self.entry= ctk.CTkEntry(self, width= 200)
        self.entry.pack()

        self.btn_save= ctk.CTkButton(self, text= 'Salvar', command= self.save)
        self.btn_save.pack(pady= (15, 5))

        self.btn_back= ctk.CTkButton(self, text= 'Voltar', command= self.destroy)
        self.btn_back.pack(pady= (15, 5))

    def save(self):
        cep= self.entry.get().strip() #coletando texto digitado
        if not cep.isdigit() or len(cep) != 8:
            messagebox.showwarning('CEP INválido', 'Digite um CEP válido de 8 dígitos')
            return
        
        try:
            self.db.add_cep(cep)
            messagebox.showinfo('Sucesso', 'CEP salvo!')
            self.destroy()
            
        except Exception as e:
            messagebox.showerror('Erro', f'Erro ao salvar o CEP:\n{e}')