#librerias
import tkinter as tk
from numpy import bitwise_xor
from numpy.lib.npyio import recfromtxt
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import serial

#nuevo archivo
def new(window):
    #config de la ventana new mission
    new_window = tk.Toplevel()
    new_window.iconbitmap('images/LOGO_GIA_transparente.ico')
    new_window.title("New mission")
    new_window.geometry("400x300")
    new_window.config(bg = '#F2F2F2')

    #labels y entradas para nombre de mision y lugar de lanzamiento
    mission_var = tk.StringVar()
    place_var = tk.StringVar()
    tk.Label(new_window,text='Nombre de la mision:',justify=tk.LEFT).grid(row=0,column=0)
    tk.Entry(new_window,textvariable = mission_var).grid(row=0,column=1)
    tk.Label(new_window,text='Lugar de la mision:',justify=tk.LEFT).grid(row=1,column=0)
    tk.Entry(new_window,textvariable = place_var).grid(row=1,column=1) 
    
    
    #boton que llama la interfase con los argumentos window, mission y place en el window y destruye new window
    bt = tk.Button(new_window,text='Save', command = lambda : 
    [interface(window,mission_var.get(),place_var.get()),new_window.destroy()])
    bt.place(relx=0.9,rely=0.9)

    new_window.mainloop()

#funcion que quita los widgets place en la ventana
def close(window):
    place_list = window.place_slaves()
    for l in place_list:
        l.place_forget()

running = None
secs = 0

def interface(window,mission_name,launch_place):
    #colores usados en el GIU
    figure_bg  = '#ffcc5c'           #amarillo crema
    graphic_bg = '#ffeead'          #amarillo fuerte
    text_font  = ('Arial',11)        #font para texto de la informacion

    def ardu():
        global running
        global secs
        secs += 1
        if secs % 1 == 0:  
            #nuevos datos
            datos = get_data()
            #recalculo de variables
            #variables para graficos 3d
            gps_latitud       = datos['GPS_LATITUD']
            gps_longitud      = datos['GPS_LONGITUD']
            gps_altitud       = datos['GPS_ALTITUD']
            #variables para graficos 2d
            tiempo            = datos['TIEMPO_INSTANTANEO']
            presion           = datos['PRESION']
            temperatura       = datos['TEMP']
            tension           = datos['TENSION_ELECTRICA_BATERIA']
            #dato actual (ultima fila en el data frame)
            tiempo_gps        = str(datos['TIEMPO_GPS'].iloc[-1]) 
            paquetes          = str(datos['CONTEO_PAQUETE'].iloc[-1]) 
            etapa             = str(datos['ETAPA'].iloc[-1])
            satelites         = str(datos['GPS_SATS'].iloc[-1]) 
            iteraciones       = str(datos['NUMERO_DE_ITERACION'].iloc[-1]) 
            #Datos interesantes/importantes
            altura_max        = str(datos['ALTITUD'].max())
            presion_max       = str(round(datos['PRESION'].max(),2)) 
            temperatura_max   = str(datos['TEMP'].max()) 

            ax3d.clear()
            a1.clear()
            a2.clear()
            a3.clear()

            ax3d.grid(True) 
            ax3d.set_facecolor(graphic_bg)
            ax3d.set_xlabel('Latitud')
            ax3d.set_ylabel('Longitud')
            ax3d.set_zlabel('Altitud (m)')
            ax3d.set_title('Posicion GPS en el tiempo')

            #graficos de la derecha
            #grafico 1
            a1.patch.set_facecolor(graphic_bg)
            a1.set_xlabel('Tiempo (s)',fontsize=9)
            a1.set_ylabel('Presion (Pa)',fontsize=9)
            a1.set_title('Tiempo contra presion',fontsize=10)
            a1.grid(True)

            #grafico 2
            a2.patch.set_facecolor(graphic_bg)
            a2.set_xlabel('Tiempo (s)',fontsize=9)
            a2.set_ylabel('Temperatura (\u2103)',fontsize=9)
            a2.set_title('Tiempo contra temperatura',fontsize=10)
            a2.grid(True)
            
            #grafico 3
            a3.patch.set_facecolor(graphic_bg)
            a3.set_xlabel('Tiempo (s)',fontsize=9)
            a3.set_ylabel('Tension (V)',fontsize=9)
            a3.set_title('Tiempo contra tension',fontsize=10)
            a3.grid(True)

            #plotea
            ax3d.plot(gps_latitud,gps_longitud,gps_altitud)
            a1.plot(tiempo,presion)
            a2.plot(tiempo,temperatura)
            a3.plot(tiempo,tension)
            figure3d.canvas.draw()
            figure2d.canvas.draw()

            var.set('Mision: ' + mission_name + 
            '\nLugar: ' + launch_place + 
            '\nTiempo actual: ' + tiempo_gps + 
            '\nPaquetes recibidos: ' + paquetes + 
            '\nEtapa actual: ' + etapa + 
            '\nSatelites captados: ' + satelites + 
            '\nIteraciones realizadas: ' + iteraciones + 
            '\nAltura maxima: ' + altura_max + ' (m)' +
            '\nPresion maxima: ' + presion_max + ' (Pa)' +
            '\nTemperatura maxima: ' + temperatura_max + ' (C'u'\N{DEGREE SIGN}'')')

        #despues de hacer el ciclo se llama a si misma
        running = window.after(100, ardu)  # Check again in 0.5 second.

    #llama a ardu y empieza secs
    def start():
        global secs
        secs = 0
        ardu()  # Start repeated checking.

    #hace que running sea nada y detiene el ciclo de ardu
    def stop():
        global running
        if running:
            window.after_cancel(running)
            running = None
        
    
    #frames para colocar graficos y datos actuales de vuelo
    #variables locales para calculo de tamaño de frames
    borde        = 0.01
    big_width    = 0.45  
    big_height   = 1-2*borde
    small_width  = (1-4*borde-big_width)/2 
    small_height = 0.60
    
    #frame para la informacion
    information_frame = tk.Frame(window,bg = figure_bg)
    information_frame.place(relx=borde, rely=borde, relwidth= small_width, relheight=small_height)
    #frame para el grafico 3d
    position_graphic_frame = tk.Frame(window, bg=figure_bg, bd=4)
    position_graphic_frame.place(relx=2*borde+small_width, rely=borde, relwidth=big_width, relheight=small_height)
    #frame para los graficos
    graphic_frame = tk.Frame(window)
    graphic_frame.place(relx=3*borde+small_width+big_width, rely=borde, relwidth=small_width, relheight=big_height)
    #frame para botones o acelerometro idk
    acelerometer_frame = tk.Frame(window,bg = figure_bg)
    acelerometer_frame.place(relx=borde, rely=2*borde+small_height, relwidth=borde+big_width+small_width, relheight=1-3*borde-small_height)
    
    #botones para inicio y finalizacion de toma de datos de la consola de arduino
    start_button = tk.Button(information_frame,text ='Start',command = lambda : start())
    start_button.place(relx=0.05,rely=0.9,relwidth=0.425,height=35)
    stop_button  = tk.Button(information_frame,text ='Finish',command = lambda : stop())
    stop_button.place(relx=0.525,rely=0.9,relwidth=0.425,height=35)

    #figura grafico3d del centro
    figure3d = plt.Figure(figsize=(5,6), dpi=100)
    figure3d.patch.set_facecolor(graphic_bg)
    canvas3d = FigureCanvasTkAgg(figure3d, position_graphic_frame)
    canvas3d.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH,expand=1)

    #figura graficos 2d derecha
    figure2d = plt.Figure(figsize=(5,6), dpi=100, constrained_layout = True)
    figure2d.patch.set_facecolor(figure_bg)
    canvas2d = FigureCanvasTkAgg(figure2d, graphic_frame)
    canvas2d.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH,expand=1)
    canvas2d.draw()

    #grafico 3D
    ax3d = figure3d.add_subplot(111,projection = '3d')
    ax3d.grid(True) 
    ax3d.set_facecolor(graphic_bg)
    ax3d.set_xlabel('Latitud')
    ax3d.set_ylabel('Longitud')
    ax3d.set_zlabel('Altitud (m)')
    ax3d.set_title('Posicion GPS en el tiempo')

    #graficos de la derecha
    #grafico 1
    a1 = figure2d.add_subplot(311)
    a1.patch.set_facecolor(graphic_bg)
    a1.set_xlabel('Tiempo (s)',fontsize=9)
    a1.set_ylabel('Presion (Pa)',fontsize=9)
    a1.set_title('Tiempo contra presion',fontsize=10)
    a1.grid(True)

    #grafico 2
    a2 = figure2d.add_subplot(312)
    a2.patch.set_facecolor(graphic_bg)
    a2.set_xlabel('Tiempo (s)',fontsize=9)
    a2.set_ylabel('Temperatura (\u2103)',fontsize=9)
    a2.set_title('Tiempo contra temperatura',fontsize=10)
    a2.grid(True)
    
    #grafico 3
    a3 = figure2d.add_subplot(313)
    a3.patch.set_facecolor(graphic_bg)
    a3.set_xlabel('Tiempo (s)',fontsize=9)
    a3.set_ylabel('Tension (V)',fontsize=9)
    a3.set_title('Tiempo contra tension',fontsize=10)
    a3.grid(True)

    #labels para poner texto
    var = tk.StringVar()
    label1 = tk.Label(information_frame,textvariable = var, bg = figure_bg, font = text_font, justify = tk.LEFT)
    label1.pack()
    label1.place(x=10,y=5)

#obtiene los datos del serial del arduino y los guarda como dataframe
matrix=[]                                               #lista vacia
ser = serial.Serial("COM4", 9600)                       #serial port of Arduino COM4 y los baudios del serial port
def get_data():                                        
    getData = (ser.readline().decode())                 #lee la ultima linea
    row = getData[:-2].split(",")                       #Separo las columnas por las comas
    for i in range(len(row)):                           #convierto el tipo
        #if i == 1:
            #row[i] = int(row[i])                       #si el row son x convierto los str a int
        if ((i == 6)or(i == 11)):
            pass
        else:
            row[i]=float(row[i])
    matrix.append(row)                                  #añade las filas a la matriz
    return pd.DataFrame(matrix,columns = ['TIEMPO_INSTANTANEO','CONTEO_PAQUETE','ALTITUD','TEMP','PRESION'
    ,'TENSION_ELECTRICA_BATERIA','TIEMPO_GPS','GPS_LATITUD','GPS_LONGITUD','GPS_ALTITUD','GPS_SATS',
    'ETAPA','NUMERO_DE_ITERACION'])                     #regresa los datos de la matris como df

#salva el dataframe como .csv
def save_csv(data):
    pass
    #data.to_csv('Data_mision_'+mission)