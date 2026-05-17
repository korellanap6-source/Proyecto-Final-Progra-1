import customtkinter as ctk 
from usuario import usuario

#aspecto general de la app
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

#ventana principal
ventana = ctk.CTk()
ventana.geometry("400x350")#ancho y alto
ventana.title("Sistema de Medición de Tanques")


def abrir_ventana_empleado():
    ventana.withdraw() # Oculta la ventana de login
    
    
    ventana_emp = ctk.CTkToplevel()
    ventana_emp.geometry("800x500")
    ventana_emp.title("Panel de Empleado")
    
    
    ctk.CTkLabel(ventana_emp, text="👤 Empleado", font=("Arial", 20, "bold")).pack(pady=10)
    
    
    tabs = ctk.CTkTabview(ventana_emp, width=750, height=400)
    tabs.pack(pady=10)
    
    tabs.add("INGRESAR MEDIDA")
    tabs.add("VER HISTORIAL")
    
    
    ctk.CTkLabel(tabs.tab("INGRESAR MEDIDA"), text="Aquí pondremos las filas DIESEL, REGULAR, SUPER").pack(pady=50)
    ctk.CTkButton(tabs.tab("INGRESAR MEDIDA"), text="GUARDAR REGISTRO").pack(side="bottom", pady=20)


def abrir_ventana_admin():
    ventana.withdraw() 
    
    ventana_admin = ctk.CTkToplevel()
    ventana_admin.geometry("800x500")
    ventana_admin.title("Panel de Administrador")
    
    ctk.CTkLabel(ventana_admin, text="⚙️ ADMINISTRADOR", font=("Arial", 20, "bold")).pack(pady=10)
    
    # Pestañas del Admin 
    tabs = ctk.CTkTabview(ventana_admin, width=750, height=400)
    tabs.pack(pady=10)
    
    tabs.add("Añadir")
    tabs.add("Historial")
    tabs.add("Buscar")
    tabs.add("Eliminar")


def intentar_login():
    # El .strip() es la clave: borra espacios en blanco al inicio o al final
    u = entrada_usuario.get().strip()
    p = entrada_password.get().strip()
    
    # Esto te chismorreará en la consola qué está leyendo exactamente Python
    print(f"Intentando entrar con -> Usuario: '{u}' | Password: '{p}'")
    
    # Crear los usuarios de prueba (U mayúscula)
    usuario_admin = usuario("admin", "1234")
    usuario_trab = usuario("gas", "5678")
    
    # Validar
    if usuario_admin.validar(u, p):
        mensaje_error.configure(text="")
        abrir_ventana_admin()
    elif usuario_trab.validar(u, p):
        mensaje_error.configure(text="")
        abrir_ventana_empleado()
    else:
        # Si falla mostramos el error en rojo
        mensaje_error.configure(text="Error: Usuario o contraseña incorrectos")

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
boton_entrar = ctk.CTkButton(ventana, text="Ingresar", command=intentar_login)
boton_entrar.pack(pady=20)

mensaje_error = ctk.CTkLabel(ventana, text="", text_color="red")
mensaje_error.pack(pady=5)

ventana.mainloop()
