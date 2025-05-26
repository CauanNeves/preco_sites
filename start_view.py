import customtkinter as ctk
import threading
from start import main

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('Comparador de Preços')
        self.geometry('500x300')

        self.label = ctk.CTkLabel(self, text='Clique em "Iniciar" para buscar os preços')
        self.label.pack(pady=20)

        self.button = ctk.CTkButton(self, text='Iniciar', command=self.start_scraping)
        self.button.pack(pady=10)

        self.loading = ctk.CTkLabel(self, text='Carregando...', text_color='gray')
        
        self.resultado = ctk.CTkLabel(self, text='', wraplength=400)

    def start_scraping(self):
        self.button.configure(state='disabled')
        self.label.pack_forget()
        self.loading.pack(pady=20)
        threading.Thread(target=self.run_scraping).start()

    def run_scraping(self):
        resultado = main()
        # Formata os resultados em uma única string com quebras de linha
        texto_formatado = '\n'.join(resultado)
        # Mostra o resultado na interface (executado na thread principal)
        self.after(0, self.show_result, texto_formatado)

    def show_result(self, texto):
        self.loading.pack_forget()
        self.resultado.configure(text=texto)
        self.resultado.pack(pady=20)
        self.button.configure(state='normal')

if __name__ == '__main__':
    ctk.set_appearance_mode('dark')
    ctk.set_default_color_theme('blue')
    app = App()
    app.mainloop()
