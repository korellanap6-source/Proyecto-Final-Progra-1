import customtkinter as ctk 
from usuario import usuario

#aspecto general de la app
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

#ventana principal
ventana = ctk.CTk()
ventana.geometry("400x350")#ancho y alto
ventana.title("Sistema de Medición de Tanques")

#titulo principal 
titulo = ctk.CTkLabel(ventana, text="LOGIN AL SISTEMA", font=("Arial",20,"bold"))
titulo.pack(pady=20)

#usuario
entrada_usuario = ctk.CTkEntry(ventana, placeholder_text="usuario", width=200)
entrada_usuario.pack(pady=10)

#contraseña
entrada_password = ctk.CTkEntry(ventana, placeholder_text="contraseña", show="*", width=200)
entrada_password.pack(pady=10)

#boton ingresar
boton_entrar = ctk.CTkButton(ventana, text="Ingresar")
boton_entrar.pack(pady=20)

mensaje_error = ctk.CTkLabel(ventana, text="", text_color="red")
mensaje_error.pack(pady=5)

ventana.mainloop()
