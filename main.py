import customtkinter as ctk 
from usuario import usuario

#aspecto general de la app
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

#ventana principal
ventana = ctk.CTk()
ventana.geometry("400x350")#ancho y alto
ventana.title("Sistema de Medición de Tanques")

def menu_ingresar_medidas(pestana_ingreso): 
     # encabezados de columnas
    ctk.CTkLabel(pestana_ingreso, text="Combustible", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=20, pady=10)
    ctk.CTkLabel(pestana_ingreso, text="Pulgadas (PULG)", font=("Arial", 14, "bold")).grid(row=0, column=1, padx=20, pady=10)
    ctk.CTkLabel(pestana_ingreso, text="Galones (GLS)", font=("arial", 14, "bold")).grid(row=0, column=2, padx=20, pady=10)
    ctk.CTkLabel(pestana_ingreso, text="Galones Disponibles para la venta", font=("arial", 14, "bold")).grid(row=0, column=3, padx=20, pady=10)
    
    # FILA DIESEL
    ctk.CTkLabel(pestana_ingreso, text="⛽ DIESEL:", font=("Arial", 14)).grid(row=1, column=0, padx=20, pady=10, sticky="w")
    entrada_diesel_pulg = ctk.CTkEntry(pestana_ingreso, placeholder_text="0", width=100)
    entrada_diesel_pulg.grid(row=1, column=1, padx=20, pady=10)

    
    entrada_diesel_gls = ctk.CTkEntry(pestana_ingreso, placeholder_text="0", width=100, state="readonly")
    entrada_diesel_gls.grid(row=1, column=2, padx=20, pady=10)

    entrada_diesel_venta = ctk.CTkEntry(pestana_ingreso, placeholder_text="0", width=100, state="readonly")
    entrada_diesel_venta.grid(row=1, column=3, padx=20, pady=10)
    
    # FILA REGULAR
    ctk.CTkLabel(pestana_ingreso, text="⛽ REGULAR:", font=("Arial", 14)).grid(row=2, column=0, padx=20, pady=10, sticky="w")
    entrada_regular_pulg = ctk.CTkEntry(pestana_ingreso, placeholder_text="0", width=100)
    entrada_regular_pulg.grid(row=2, column=1, padx=20, pady=10)
    
    
    entrada_regular_gls = ctk.CTkEntry(pestana_ingreso, placeholder_text="0", width=100, state="readonly")
    entrada_regular_gls.grid(row=2, column=2, padx=20, pady=10)
    entrada_regular_venta = ctk.CTkEntry(pestana_ingreso, placeholder_text="0", width=100, state="readonly")
    entrada_regular_venta.grid(row=2, column=3, padx=20, pady=10)

    # FILA SÚPER
    ctk.CTkLabel(pestana_ingreso, text="⛽ SÚPER:", font=("Arial", 14)).grid(row=3, column=0, padx=20, pady=10, sticky="w")
    entrada_super_pulg = ctk.CTkEntry(pestana_ingreso, placeholder_text="0", width=100)
    entrada_super_pulg.grid(row=3, column=1, padx=20, pady=10)
    
   
    entrada_super_gls = ctk.CTkEntry(pestana_ingreso, placeholder_text="0", width=100, state="readonly")
    entrada_super_gls.grid(row=3, column=2, padx=20, pady=10)
    entrada_super_venta = ctk.CTkEntry(pestana_ingreso, placeholder_text="0", width=100, state="readonly")
    entrada_super_venta.grid(row=3, column=3, padx=20, pady=10)

    boton_calcular = ctk.CTkButton(pestana_ingreso, text="CALCULAR MEDIDA")
    boton_calcular.grid(row=4, column=0, columnspan=4, pady=20)
    
    boton_guardar = ctk.CTkButton(pestana_ingreso, text="GUARDAR REGISTRO", fg_color="green", hover_color="darkgreen")

    return{
        "diesel_pulg": entrada_diesel_pulg, "diesel_gls": entrada_diesel_gls, "diesel_venta": entrada_diesel_venta,
        "regular_pulg": entrada_regular_pulg, "regular_gls": entrada_regular_gls, "regular_venta": entrada_regular_venta,
        "super_pulg": entrada_super_pulg, "super_gls": entrada_super_gls, "super_venta": entrada_super_venta,
        "btn_calcular": boton_calcular, "btn_guardar": boton_guardar
    }



def abrir_ventana_empleado():
    ventana.withdraw() 
    
    ventana_emp = ctk.CTkToplevel()
    ventana_emp.geometry("800x500")
    ventana_emp.title("Panel de Empleado")

    ventana_emp.protocol("WM_DELETE_WINDOW", cerrar_programa) 
    
    ctk.CTkLabel(ventana_emp, text="👤 Empleado", font=("Arial", 20, "bold")).pack(pady=10)
    
    tabs = ctk.CTkTabview(ventana_emp, width=750, height=400)
    tabs.pack(pady=10)
    
    tabs.add("INGRESAR MEDIDA")
    tabs.add("VER HISTORIAL")

    componentes_emp = menu_ingresar_medidas(tabs.tab("INGRESAR MEDIDA"))
    
    
   


def abrir_ventana_admin():
    ventana.withdraw() 
    
    ventana_admin = ctk.CTkToplevel()
    ventana_admin.geometry("800x500")
    ventana_admin.title("Panel de Administrador")

    ventana_admin.protocol("WM_DELETE_WINDOW",cerrar_programa)
    
    ctk.CTkLabel(ventana_admin, text="⚙️ ADMINISTRADOR", font=("Arial", 20, "bold")).pack(pady=10)
    
    # Pestañas del Admin 
    tabs = ctk.CTkTabview(ventana_admin, width=750, height=400)
    tabs.pack(pady=10)
    
    tabs.add("Añadir")
    tabs.add("Historial")
    tabs.add("Buscar")
    tabs.add("actualizar")
    tabs.add("Eliminar")

    componentes_admin = menu_ingresar_medidas(tabs.tab("Añadir"))

#funcion para finalizar el programa
def cerrar_programa():
    ventana.quit()
    ventana.destroy()

def intentar_login():
    
    u = entrada_usuario.get().strip()
    p = entrada_password.get().strip()
    
    print(f"Intentando entrar con -> Usuario: '{u}' | Password: '{p}'")
    
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
