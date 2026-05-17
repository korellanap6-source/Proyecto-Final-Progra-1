import customtkinter as ctk 
from usuario import usuario

#aspecto general de la app
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

#ventana principal
ventana = ctk.CTk()
ventana.geometry("400x350")#ancho y alto
ventana.title("Sistema de Medición de Tanques")

ventana.mainloop()
