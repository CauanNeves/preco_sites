from views.new_product_view import NewProductWindow
from views.edit_link_view import EditLinkWindow
from views.table_view import ListProductWindow
from views.reset_db_view import ResetDBWindow
from views.cep_view import CepWindow
from views.about_view import AboutWindow
from database import Database
from views.start_view.start_view import startWindow
from tkinter import messagebox
import customtkinter as ctk

#Banco de dados
db= Database()

#Tema
ctk.set_appearance_mode('dark')

#Funções
def start():
    startWindow(window)

def cep():
    CepWindow(window, db)

def new_product():
    NewProductWindow(window, db)

def edit_link():
    EditLinkWindow(window, db)

def table():
    ListProductWindow(window, db)

def about():
    AboutWindow(window)

def reset_db():
    ResetDBWindow(window, db)

#Iniciando
window= ctk.CTk()
window.title('Economiza Aí')
window.geometry('300x220')
window.minsize(300, 220)
window.maxsize(300, 220)

#Elementos
btn_start = ctk.CTkButton(window, width= 280, height= 40, corner_radius= 4, text= ('START'),fg_color= ('#76A646'), command= start)
btn_start.grid(row= 0, padx= 5, pady= 5, columnspan= 3, column= 0)

btn_cep= ctk.CTkButton(window, width= 135, height= 40, corner_radius= 4, text= ('CEP'), command= cep)
btn_cep.grid(row= 1, column= 0, pady= 5, padx= 5)


btn_new= ctk.CTkButton(window, width= 135, height= 40, corner_radius= 4, text= ('Novo produto'), command= new_product)
btn_new.grid(row= 1, column= 1, pady= 5, padx= 5)

btn_link= ctk.CTkButton(window, width= 135, height= 40, corner_radius= 4, text= ('Editar link'), command= edit_link)
btn_link.grid(row= 2, column= 0, pady= 5, padx= 5)

btn_table= ctk.CTkButton(window, width= 135, height= 40, corner_radius= 4, text= ('Ver Tabela'), command= table)
btn_table.grid(row= 2, column= 1, pady= 5, padx= 5)

btn_about= ctk.CTkButton(window, width= 135, height= 40, corner_radius= 4, text= ('Sobre'), command= about)
btn_about.grid(row= 3, column= 0, pady= 5, padx= 5)

btn_reset= ctk.CTkButton(window, width= 135, height= 40, corner_radius= 4, text= ('Resetar BD'),fg_color= ('#E51200'), command= reset_db)
btn_reset.grid(row= 3, column= 1, pady= 5, padx= 5)

window.mainloop()