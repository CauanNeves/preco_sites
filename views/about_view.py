import customtkinter as ctk
import webbrowser

class AboutWindow(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title('Sobre o Sistema')
        self.geometry('400x550')
        self.resizable(False, False)

        self.label_title = ctk.CTkLabel(self, text='Sistema de Comparação de Preços', font=ctk.CTkFont(size=16, weight='bold'))
        self.label_title.pack(pady=(20, 5))

        self.label_version = ctk.CTkLabel(self, text='Versão 2.0', font=ctk.CTkFont(size=14))
        self.label_version.pack(pady=5)

        self.label_author = ctk.CTkLabel(self, text='Desenvolvido por Cauan Silva das Neves', font=ctk.CTkFont(size=14))
        self.label_author.pack(pady=5)

        self.label_description = ctk.CTkLabel(self, text='''
Este é um sistema de comparação de preços desenvolvido em Python, com interface gráfica construída usando a biblioteca CustomTkinter.
O sistema permite o cadastro de produtos e links de diferentes sites, com opção de ativar ou desativar cada link individualmente.

Por meio de uma rotina de raspagem de dados (scraping), os preços são atualizados automaticamente a partir dos links ativos.
O objetivo é identificar o menor preço disponível entre os sites cadastrados para facilitar a tomada de decisão de compra.

A estrutura do banco de dados foi implementada com SQLite e o sistema oferece uma interface simples e direta para visualização, filtragem e atualização dos dados''',
                                              wraplength= 280, anchor= 'w', justify='center', font=ctk.CTkFont(size=13))
        self.label_description.pack(pady=(10, 20))

        # Links clicáveis
        link_font = ctk.CTkFont(underline=True)
        link_color = '#1E90FF'

        github_link = ctk.CTkLabel(self, text='GitHub', text_color=link_color, font=link_font, cursor='hand2')
        github_link.pack()
        github_link.bind('<Button-1>', lambda e: webbrowser.open_new('https://github.com/CauanNeves'))

        linkedin_link = ctk.CTkLabel(self, text='LinkedIn', text_color=link_color, font=link_font, cursor='hand2')
        linkedin_link.pack(pady=(0, 10))
        linkedin_link.bind('<Button-1>', lambda e: webbrowser.open_new('https://www.linkedin.com/in/cauan-neves/'))

        ctk.CTkButton(self, text='Fechar', command=self.destroy).pack(pady=10)