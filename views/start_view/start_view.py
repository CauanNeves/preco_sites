import customtkinter as ctk
import threading
from .start import main


class startWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.focus_force()

        self.title('Comparador de Preços')
        self.geometry('600x400')
        self.resizable(False, False)

        self.label = ctk.CTkLabel(self, text='Clique em "Iniciar" para buscar os preços', font=ctk.CTkFont(size=14))
        self.label.pack(pady=15)

        self.button = ctk.CTkButton(self, text='Iniciar', command=self.start_scraping)
        self.button.pack(pady=10)

        self.loading = ctk.CTkLabel(self, text='Carregando...', text_color='gray')
        self.resultado = ctk.CTkTextbox(self, width=500, height=200, wrap="word", font=ctk.CTkFont(size=13))
        self.resultado.configure(state='disabled')

    def start_scraping(self):
        self.button.configure(state='disabled')
        self.label.pack_forget()
        self.resultado.pack_forget()
        self.resultado.configure(state='normal')
        self.resultado.delete("1.0", "end")
        self.resultado.configure(state='disabled')
        self.loading.pack(pady=20)
        threading.Thread(target=self.run_scraping).start()

    def run_scraping(self):
        resultado = main()
        texto_formatado = '\n'.join(resultado)
        self.after(0, self.show_result, texto_formatado)

    def show_result(self, texto):
        self.loading.pack_forget()
        self.resultado.configure(state='normal')
        self.resultado.insert("1.0", texto)
        self.resultado.configure(state='disabled')
        self.resultado.pack(pady=20)
        self.button.configure(state='normal')