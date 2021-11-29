import tkinter as tk
from PIL import Image, ImageTk
import webbrowser

def about():
    #nueva ventana
    new_window = tk.Toplevel()
    new_window.iconbitmap('images/LOGO_GIA_transparente.ico')
    new_window.title("About GIA's Base Control System")
    new_window.geometry("600x400")
    new_window.config(bg = '#F2F2F2')
    about_text = 'Version 1.1.1\n\
    Fecha 15/10/21\n\
    Python 3.8.4\n\
    Escrito por Alvaro Bermudez Marin y Wilbert\n\
    Con la ayuda de: ....\n\
    Contacto: alvarobermudez04@gmail.com'

    

    #label para la imagen
    gia_logo = ImageTk.PhotoImage(Image.open('images/LOGO GIA transparente v3.png').resize((200, 200)))
    aboutlabellogo = tk.Label(new_window,image=gia_logo)
    #aboutlabellogo.image = gia_logo
    aboutlabellogo.pack()
    
    #texto de about
    aboutlabeltext = tk.Label(new_window,text = about_text,bg = '#F2F2F2',font = ('Arial',10),justify = tk.LEFT)
    aboutlabeltext.pack()
    new_window.mainloop()


def link_github():
    webbrowser.open_new_tab("https://github.com/giaucr")


def link_notion():
    webbrowser.open_new_tab("https://www.notion.so/3219bbe5cac04ceb919a40840e748152?v=656e70a9e6f84b04aedb273ae38bfc18")
