import customtkinter as ctk
from tkinter import messagebox

class ResetDBWindow(ctk.CTkToplevel):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.title('Resetar Banco de Dados')
        self.geometry('340x180')
        self.minsize(340, 180)
        self.maxsize(340, 180)

        self.db = db

        # Interface
        ctk.CTkLabel(
            self,
            text='Tem certeza que deseja apagar TODOS os dados?',
            wraplength=300,
            font=ctk.CTkFont(weight='bold')
        ).pack(pady=(20, 10))

        self.entry= ctk.CTkEntry(self, width= 160, placeholder_text= 'Digite "Apagar" e confirme')
        self.entry.pack()

        self.frame = ctk.CTkFrame(self, fg_color='transparent')
        self.frame.pack(pady=10)

        self.btn_confirm= ctk.CTkButton(self.frame, text='Confirmar', fg_color='#E51200', command=self.resetar)
        self.btn_confirm.grid(row=0, column=0, padx=10)

        self.btn_cancelar= ctk.CTkButton(self.frame, text='Cancelar', command=self.destroy)
        self.btn_cancelar.grid(row=0, column=1, padx=10)

    def resetar(self):
        try:
            if self.entry.get().strip() == 'Apagar':
                self.db.reset_db()  # Essa função deve limpar todas as tabelas
                messagebox.showinfo('Sucesso', 'Banco de dados resetado.')
                self.destroy()
            else:
                messagebox.showerror('Erro', f'Caso queira confirmar o exclusão, digite exatamente "Apagar"')
                return

        except Exception as e:
                messagebox.showerror('Erro', f'Erro ao resetar banco:\n{e}')