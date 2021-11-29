#librerias
import tkinter as tk

#import otros archivos python
from options import help_options as ho
from options import archive_options as ao

#configuracion de la ventana
if __name__ == '__main__':
    window = tk.Tk()
    #icono, titulo de ventana, tamaño y fondo 
    window.iconbitmap('images/LOGO_GIA_transparente.ico')
    window.title("GIA's Base Control System")
    window.geometry("940x650") 
    window.config(bg = '#96ceb4') #verde suave

    #barras de menu de la ventanta
    menubar = tk.Menu(window)
    window.config(menu=menubar)

    #menu de archivo
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Nueva misión", command=lambda : ao.new(window))
    #añadir opcion para exportar la mision en el .csv
    filemenu.add_command(label="Exportar misión", command=lambda : ao.save_csv())
    filemenu.add_command(label="Cerrar misión", command=lambda : ao.close(window))
    filemenu.add_separator()
    filemenu.add_command(label="Salir", command=window.quit)

    #menu de edicion talvez lo quito
    editmenu = tk.Menu(menubar, tearoff=0)
    editmenu.add_command(label="Cortar")
    editmenu.add_command(label="Copiar")
    editmenu.add_command(label="Pegar")

    #menu de ayuda
    helpmenu = tk.Menu(menubar, tearoff=0)
    help_submenu = tk.Menu(helpmenu, tearoff=0)
    helpmenu.add_cascade(label='Ayuda',menu=help_submenu)
    helpmenu.add_separator()
    helpmenu.add_command(label="Acerca de..." ,command = ho.about)

    #links y submenu de ayuda
    help_submenu.add_command(label="Ir al git", command= ho.link_github)
    help_submenu.add_command(label="Ir al notion", command = ho.link_notion)

    #labels de los menus
    menubar.add_cascade(label="Archivo", menu=filemenu)
    menubar.add_cascade(label="Editar", menu=editmenu)
    menubar.add_cascade(label="Ayuda", menu=helpmenu)

    window.mainloop()