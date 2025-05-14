import customtkinter as ctk

class About(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Sobre')
        self.geometry('300x400')
        
        ctk.CTkLabel(
            self, text='On the other hand, we denounce with righteous indignation and dislike men who are so beguiled and demoralized by the charms of pleasure of the moment, so blinded by desire, that they cannot foresee the pain and trouble that are bound to ensue; and equal blame belongs to those who fail in their duty through weakness of will, which is the same as saying through shrinking from toil and pain. These cases are perfectly simple and easy to distinguish. In a free hour, when our power of choice is untrammelled and when nothing prevents our being able to do what we like best, every pleasure is to be welcomed and every pain avoided. But in certain circumstances and owing to the claims of duty or the obligations of business it will frequently occur that pleasures have to be repudiated and annoyances accepted. The wise man therefore always holds in these matters to this principle of selection: he rejects pleasures to secure other greater pleasures, or else he endures pains to avoid worse pains',
            width= 300, height= 260,
            wraplength= 280, 
            justify= 'left', anchor= 'w').pack(padx= 5, pady= 5)

        self.btn_back= ctk.CTkButton(self, text='Voltar', command= self.destroy, width= 180)
        self.btn_back.pack()