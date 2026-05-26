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
    
# Aspecto general de la app
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Ventana principal
ventana = ctk.CTk()
ventana.geometry("400x350")  # Ancho y alto
ventana.title("Sistema de Medición de Tanques")

def crear_tabla_si_no_existe():
    conn = conexion()
    cursor = None
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS registros_medidas (
                    id SERIAL PRIMARY KEY,
                    fecha DATE NOT NULL,
                    diesel_pulg NUMERIC,
                    diesel_gls NUMERIC,
                    diesel_venta NUMERIC,
                    regular_pulg NUMERIC,
                    regular_gls NUMERIC,
                    regular_venta NUMERIC,
                    super_pulg NUMERIC,
                    super_gls NUMERIC,
                    super_venta NUMERIC
                )
            ''')
            conn.commit()
        except Exception as e:
            print(f"Error al crear tabla: {e}")
        finally:
            # Garantiza el cierre de conexiones para evitar saturación
            if cursor:
                cursor.close()
            if conn:
                conn.close()

crear_tabla_si_no_existe()

def menu_ingresar_medidas(pestana_ingreso): 
    fecha_actual = datetime.date.today().strftime("%Y-%m-%d")

    # Cuadro que muestra la fecha
    ctk.CTkLabel(
        pestana_ingreso, 
        text=f"Fecha del Registro: {fecha_actual} (Automática por el Sistema)", 
        font=("Arial", 13, "italic"),
        text_color="gray"
    ).grid(row=0, column=0, columnspan=4, pady=10, sticky="w", padx=20)

    # Encabezados de columnas
    ctk.CTkLabel(pestana_ingreso, text="Combustible", font=("Arial", 14, "bold")).grid(row=1, column=0, padx=20, pady=10)
    ctk.CTkLabel(pestana_ingreso, text="Pulgadas (PULG)", font=("Arial", 14, "bold")).grid(row=1, column=1, padx=20, pady=10)
    ctk.CTkLabel(pestana_ingreso, text="Galones (GLS)", font=("arial", 14, "bold")).grid(row=1, column=2, padx=20, pady=10)
    ctk.CTkLabel(pestana_ingreso, text="Galones Disponibles para la venta", font=("arial", 14, "bold")).grid(row=1, column=3, padx=20, pady=10)
    
    # FILA DIESEL
    ctk.CTkLabel(pestana_ingreso, text="⛽ DIESEL:", font=("Arial", 14)).grid(row=2, column=0, padx=20, pady=10, sticky="w")
    entrada_diesel_pulg = ctk.CTkEntry(pestana_ingreso, placeholder_text="0", width=100)
    entrada_diesel_pulg.grid(row=2, column=1, padx=20, pady=10)

    entrada_diesel_gls = ctk.CTkEntry(pestana_ingreso, placeholder_text="0", width=100, state="readonly")
    entrada_diesel_gls.grid(row=2, column=2, padx=20, pady=10)

    entrada_diesel_venta = ctk.CTkEntry(pestana_ingreso, placeholder_text="0", width=100, state="readonly")
    entrada_diesel_venta.grid(row=2, column=3, padx=20, pady=10)
    
    # FILA REGULAR
    ctk.CTkLabel(pestana_ingreso, text="⛽ REGULAR:", font=("Arial", 14)).grid(row=3, column=0, padx=20, pady=10, sticky="w")
    entrada_regular_pulg = ctk.CTkEntry(pestana_ingreso, placeholder_text="0", width=100)
    entrada_regular_pulg.grid(row=3, column=1, padx=20, pady=10)
    
    entrada_regular_gls = ctk.CTkEntry(pestana_ingreso, placeholder_text="0", width=100, state="readonly")
    entrada_regular_gls.grid(row=3, column=2, padx=20, pady=10)
    entrada_regular_venta = ctk.CTkEntry(pestana_ingreso, placeholder_text="0", width=100, state="readonly")
    entrada_regular_venta.grid(row=3, column=3, padx=20, pady=10)

    # FILA SÚPER
    ctk.CTkLabel(pestana_ingreso, text="⛽ SÚPER:", font=("Arial", 14)).grid(row=4, column=0, padx=20, pady=10, sticky="w")
    entrada_super_pulg = ctk.CTkEntry(pestana_ingreso, placeholder_text="0", width=100)
    entrada_super_pulg.grid(row=4, column=1, padx=20, pady=10)
    
    entrada_super_gls = ctk.CTkEntry(pestana_ingreso, placeholder_text="0", width=100, state="readonly")
    entrada_super_gls.grid(row=4, column=2, padx=20, pady=10)
    entrada_super_venta = ctk.CTkEntry(pestana_ingreso, placeholder_text="0", width=100, state="readonly")
    entrada_super_venta.grid(row=4, column=3, padx=20, pady=10)

    def ejecutar_calculo():
        pulg_d = entrada_diesel_pulg.get().strip()
        pulg_r = entrada_regular_pulg.get().strip()
        pulg_s = entrada_super_pulg.get().strip()

        # Las funciones internas de calculo_T deben manejar internamente si viene texto inválido
        tot_d, ven_d = calculo_T.buscar_medida("DIESEL", pulg_d)
        tot_r, ven_r = calculo_T.buscar_medida("REGULAR", pulg_r)
        tot_s, ven_s = calculo_T.buscar_medida("SUPER", pulg_s)

        def llenar_cajas(caja_tot, caja_ven, tot, ven):
            caja_tot.configure(state="normal")
            caja_tot.delete(0, 'end')
            caja_tot.insert(0, str(tot))
            caja_tot.configure(state="readonly")

            caja_ven.configure(state="normal")
            caja_ven.delete(0, 'end')
            caja_ven.insert(0, str(ven))
            caja_ven.configure(state="readonly")

        llenar_cajas(entrada_diesel_gls, entrada_diesel_venta, tot_d, ven_d)
        llenar_cajas(entrada_regular_gls, entrada_regular_venta, tot_r, ven_r)
        llenar_cajas(entrada_super_gls, entrada_super_venta, tot_s, ven_s)

        boton_guardar.grid(row=6, column=0, columnspan=4, pady=20)

    boton_calcular = ctk.CTkButton(pestana_ingreso, text="CALCULAR MEDIDA", command=ejecutar_calculo)
    boton_calcular.grid(row=5, column=0, columnspan=4, pady=20)

    mensaje_guardado = ctk.CTkLabel(pestana_ingreso, text="", font=("Arial", 12))
    mensaje_guardado.grid(row=7, column=0, columnspan=4, pady=5)

    def guardar_en_bd():
        conn = conexion()
        cursor = None
        if not conn:
            mensaje_guardado.configure(text="Error de conexión a BD", text_color="red")
            return
            
        try:
            cursor = conn.cursor()
            consulta = """
                INSERT INTO registros_medidas 
                (fecha, diesel_pulg, diesel_gls, diesel_venta, 
                 regular_pulg, regular_gls, regular_venta, 
                 super_pulg, super_gls, super_venta) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            # Validación preventiva local por si se ingresan letras
            def obtener_valor(entrada):
                val = entrada.get().strip()
                try:
                    return float(val) if val else 0.0
                except ValueError:
                    return 0.0

            valores = (
                fecha_actual,
                obtener_valor(entrada_diesel_pulg), obtener_valor(entrada_diesel_gls), obtener_valor(entrada_diesel_venta),
                obtener_valor(entrada_regular_pulg), obtener_valor(entrada_regular_gls), obtener_valor(entrada_regular_venta),
                obtener_valor(entrada_super_pulg), obtener_valor(entrada_super_gls), obtener_valor(entrada_super_venta)
            )
            
            cursor.execute(consulta, valores)
            conn.commit()
            mensaje_guardado.configure(text="¡Registro guardado exitosamente!", text_color="green")
            
        except Exception as e:
            print(f"Error al guardar en BD: {e}")
            mensaje_guardado.configure(text="Error al guardar el registro", text_color="red")
        finally:
            # El bloque finally asegura el cierre de flujos ocurra o no una excepción
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # Corrección: Se añade command=guardar_en_bd
    boton_guardar = ctk.CTkButton(pestana_ingreso, text="GUARDAR REGISTRO", fg_color="green", hover_color="darkgreen", command=guardar_en_bd)

    return {
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

    ventana_admin.protocol("WM_DELETE_WINDOW", cerrar_programa)
    
    ctk.CTkLabel(ventana_admin, text="⚙️ ADMINISTRADOR", font=("Arial", 20, "bold")).pack(pady=10)
    
    # Pestañas del Admin 
    tabs = ctk.CTkTabview(ventana_admin, width=750, height=400)
    tabs.pack(pady=10)
    
    tabs.add("Añadir")
    tabs.add("Historial")
    tabs.add("Buscar")
    tabs.add("Editar")
    tabs.add("Eliminar")

    componentes_admin = menu_ingresar_medidas(tabs.tab("Añadir"))

# Función para finalizar el programa
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

# Título principal 
titulo = ctk.CTkLabel(ventana, text="LOGIN AL SISTEMA", font=("Arial", 20, "bold"))
titulo.pack(pady=20)

# Usuario
entrada_usuario = ctk.CTkEntry(ventana, placeholder_text="usuario", width=200)
entrada_usuario.pack(pady=10)

# Contraseña
entrada_password = ctk.CTkEntry(ventana, placeholder_text="contraseña", show="*", width=200)
entrada_password.pack(pady=10)

# Botón ingresar
boton_entrar = ctk.CTkButton(ventana, text="Ingresar", command=intentar_login)
boton_entrar.pack(pady=20)

mensaje_error = ctk.CTkLabel(ventana, text="", text_color="red")
mensaje_error.pack(pady=5)

ventana.mainloop()

