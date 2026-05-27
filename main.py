import customtkinter as ctk 
from usuario import usuario
import datetime
import calculo_T
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


def conexion():
    try:
        URL_CONEXION = os.getenv("DATABASE_URL")
        return psycopg2.connect(URL_CONEXION)
    except Exception as e:
        print(f"Error de conexion: {e}")
        return None


def login_db(nombre, password):
    conn = conexion()
    if conn is None:
        return None

    try:
        cur = conn.cursor()
        query = "SELECT rol FROM usuarios WHERE nombre=%s AND password=%s"
        cur.execute(query, (nombre, password))
        resultado = cur.fetchone()
        cur.close()
        conn.close()

        if resultado:
            return resultado[0]
        return None

    except Exception as e:
        print("Error login:", e)
        return None


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

ventana = ctk.CTk()
ventana.geometry("400x350")
ventana.title("Sistema de Medición de Tanques")


def intentar_login():
    u = entrada_usuario.get().strip()
    p = entrada_password.get().strip()

    rol = login_db(u, p)

    if rol == "admin":
        mensaje_error.configure(text="")
        abrir_ventana_admin()

    elif rol == "empleado":
        mensaje_error.configure(text="")
        abrir_ventana_empleado()

    else:
        mensaje_error.configure(text="Error: Usuario o contraseña incorrectos")


titulo = ctk.CTkLabel(ventana, text="LOGIN AL SISTEMA", font=("Arial",20,"bold"))
titulo.pack(pady=20)

entrada_usuario = ctk.CTkEntry(ventana, placeholder_text="usuario", width=200)
entrada_usuario.pack(pady=10)

entrada_password = ctk.CTkEntry(ventana, placeholder_text="contraseña", show="*", width=200)
entrada_password.pack(pady=10)

boton_entrar = ctk.CTkButton(ventana, text="Ingresar", command=intentar_login)
boton_entrar.pack(pady=20)

mensaje_error = ctk.CTkLabel(ventana, text="", text_color="red")
mensaje_error.pack(pady=5)


def menu_ingresar_medidas(pestana_ingreso): 
    fecha_actual = datetime.date.today().strftime("%Y-%m-%d")

    for i in range(4):
        pestana_ingreso.grid_columnconfigure(i, weight=1)

    ctk.CTkLabel(
        pestana_ingreso, 
        text=f"📅 Fecha del Registro: {fecha_actual}", 
        font=("Arial", 14, "italic"),
        text_color="gray"
    ).grid(row=0, column=0, columnspan=4, pady=10)

    ctk.CTkLabel(pestana_ingreso, text="Combustible", font=("Arial", 14, "bold")).grid(row=1, column=0)
    ctk.CTkLabel(pestana_ingreso, text="Pulgadas", font=("Arial", 14, "bold")).grid(row=1, column=1)
    ctk.CTkLabel(pestana_ingreso, text="Galones", font=("Arial", 14, "bold")).grid(row=1, column=2)
    ctk.CTkLabel(pestana_ingreso, text="Venta", font=("Arial", 14, "bold")).grid(row=1, column=3)

    ctk.CTkLabel(pestana_ingreso, text="⛽ DIESEL", font=("Arial", 13, "bold")).grid(row=2, column=0)
    entrada_diesel_pulg = ctk.CTkEntry(pestana_ingreso, width=120)
    entrada_diesel_pulg.grid(row=2, column=1)

    entrada_diesel_gls = ctk.CTkEntry(pestana_ingreso, width=120)
    entrada_diesel_gls.grid(row=2, column=2)

    entrada_diesel_venta = ctk.CTkEntry(pestana_ingreso, width=120)
    entrada_diesel_venta.grid(row=2, column=3)

    ctk.CTkLabel(pestana_ingreso, text="⛽ REGULAR", font=("Arial", 13, "bold")).grid(row=3, column=0)
    entrada_regular_pulg = ctk.CTkEntry(pestana_ingreso, width=120)
    entrada_regular_pulg.grid(row=3, column=1)

    entrada_regular_gls = ctk.CTkEntry(pestana_ingreso, width=120)
    entrada_regular_gls.grid(row=3, column=2)

    entrada_regular_venta = ctk.CTkEntry(pestana_ingreso, width=120)
    entrada_regular_venta.grid(row=3, column=3)

    ctk.CTkLabel(pestana_ingreso, text="⛽ SUPER", font=("Arial", 13, "bold")).grid(row=4, column=0)
    entrada_super_pulg = ctk.CTkEntry(pestana_ingreso, width=120)
    entrada_super_pulg.grid(row=4, column=1)

    entrada_super_gls = ctk.CTkEntry(pestana_ingreso, width=120)
    entrada_super_gls.grid(row=4, column=2)

    entrada_super_venta = ctk.CTkEntry(pestana_ingreso, width=120)
    entrada_super_venta.grid(row=4, column=3)

    def ejecutar_calculo():
        pulg_d = entrada_diesel_pulg.get().strip()
        pulg_r = entrada_regular_pulg.get().strip()
        pulg_s = entrada_super_pulg.get().strip()

        tot_d, ven_d = calculo_T.buscar_medida("DIESEL", pulg_d)
        tot_r, ven_r = calculo_T.buscar_medida("REGULAR", pulg_r)
        tot_s, ven_s = calculo_T.buscar_medida("SUPER", pulg_s)

        entrada_diesel_gls.delete(0, 'end')
        entrada_diesel_gls.insert(0, str(tot_d))

        entrada_diesel_venta.delete(0, 'end')
        entrada_diesel_venta.insert(0, str(ven_d))

        entrada_regular_gls.delete(0, 'end')
        entrada_regular_gls.insert(0, str(tot_r))

        entrada_regular_venta.delete(0, 'end')
        entrada_regular_venta.insert(0, str(ven_r))

        entrada_super_gls.delete(0, 'end')
        entrada_super_gls.insert(0, str(tot_s))

        entrada_super_venta.delete(0, 'end')
        entrada_super_venta.insert(0, str(ven_s))

    boton_calcular = ctk.CTkButton(pestana_ingreso, text="CALCULAR MEDIDA", command=ejecutar_calculo)
    boton_calcular.grid(row=5, column=0, columnspan=4, pady=20)

    boton_guardar = ctk.CTkButton(pestana_ingreso, text="GUARDAR REGISTRO", fg_color="green")
    boton_guardar.grid(row=6, column=0, columnspan=4, pady=10)

    return {
        "btn_calcular": boton_calcular,
        "btn_guardar": boton_guardar
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

    menu_ingresar_medidas(tabs.tab("INGRESAR MEDIDA"))


def abrir_ventana_admin():
    ventana.withdraw() 
    
    ventana_admin = ctk.CTkToplevel()
    ventana_admin.geometry("800x500")
    ventana_admin.title("Panel de Administrador")

    ventana_admin.protocol("WM_DELETE_WINDOW", cerrar_programa)

    ctk.CTkLabel(ventana_admin, text="⚙️ ADMINISTRADOR", font=("Arial", 20, "bold")).pack(pady=10)

    tabs = ctk.CTkTabview(ventana_admin, width=750, height=400)
    tabs.pack(pady=10)

    tabs.add("Añadir")
    tabs.add("Historial")
    tabs.add("Buscar")
    tabs.add("Editar")
    tabs.add("Eliminar")

    menu_ingresar_medidas(tabs.tab("Añadir"))


def cerrar_programa():
    ventana.quit()
    ventana.destroy()


ventana.mainloop()


