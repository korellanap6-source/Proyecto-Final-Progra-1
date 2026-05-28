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
    
# aspecto general de la app
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ventana principal
ventana = ctk.CTk()
ventana.geometry("400x350")
ventana.title("Sistema de Medición de Tanques")


def crear_interfaz_cajas(contenedor, fila_inicio):
    """ Función recicladora para generar la cuadrícula de textos de las medidas """
    # encabezados de columnas
    ctk.CTkLabel(contenedor, text="Combustible", font=("Arial", 14, "bold")).grid(row=fila_inicio, column=0, padx=20, pady=10)
    ctk.CTkLabel(contenedor, text="Pulgadas (PULG)", font=("Arial", 14, "bold")).grid(row=fila_inicio, column=1, padx=20, pady=10)
    ctk.CTkLabel(contenedor, text="Galones (GLS)", font=("arial", 14, "bold")).grid(row=fila_inicio, column=2, padx=20, pady=10)
    ctk.CTkLabel(contenedor, text="Galones Disponibles (Venta)", font=("arial", 14, "bold")).grid(row=fila_inicio, column=3, padx=20, pady=10)
    
    # FILA DIESEL
    ctk.CTkLabel(contenedor, text="⛽ DIESEL:", font=("Arial", 14)).grid(row=fila_inicio+1, column=0, padx=20, pady=10, sticky="w")
    entrada_diesel_pulg = ctk.CTkEntry(contenedor, placeholder_text="0", width=100)
    entrada_diesel_pulg.grid(row=fila_inicio+1, column=1, padx=20, pady=10)
    entrada_diesel_gls = ctk.CTkEntry(contenedor, placeholder_text="0", width=100, state="readonly")
    entrada_diesel_gls.grid(row=fila_inicio+1, column=2, padx=20, pady=10)
    entrada_diesel_venta = ctk.CTkEntry(contenedor, placeholder_text="0", width=100, state="readonly")
    entrada_diesel_venta.grid(row=fila_inicio+1, column=3, padx=20, pady=10)
    
    # FILA REGULAR
    ctk.CTkLabel(contenedor, text="⛽ REGULAR:", font=("Arial", 14)).grid(row=fila_inicio+2, column=0, padx=20, pady=10, sticky="w")
    entrada_regular_pulg = ctk.CTkEntry(contenedor, placeholder_text="0", width=100)
    entrada_regular_pulg.grid(row=fila_inicio+2, column=1, padx=20, pady=10)
    entrada_regular_gls = ctk.CTkEntry(contenedor, placeholder_text="0", width=100, state="readonly")
    entrada_regular_gls.grid(row=fila_inicio+2, column=2, padx=20, pady=10)
    entrada_regular_venta = ctk.CTkEntry(contenedor, placeholder_text="0", width=100, state="readonly")
    entrada_regular_venta.grid(row=fila_inicio+2, column=3, padx=20, pady=10)

    # FILA SÚPER
    ctk.CTkLabel(contenedor, text="⛽ SÚPER:", font=("Arial", 14)).grid(row=fila_inicio+3, column=0, padx=20, pady=10, sticky="w")
    entrada_super_pulg = ctk.CTkEntry(contenedor, placeholder_text="0", width=100)
    entrada_super_pulg.grid(row=fila_inicio+3, column=1, padx=20, pady=10)
    entrada_super_gls = ctk.CTkEntry(contenedor, placeholder_text="0", width=100, state="readonly")
    entrada_super_gls.grid(row=fila_inicio+3, column=2, padx=20, pady=10)
    entrada_super_venta = ctk.CTkEntry(contenedor, placeholder_text="0", width=100, state="readonly")
    entrada_super_venta.grid(row=fila_inicio+3, column=3, padx=20, pady=10)

    return {
        "d_pulg": entrada_diesel_pulg, "d_gls": entrada_diesel_gls, "d_ven": entrada_diesel_venta,
        "r_pulg": entrada_regular_pulg, "r_gls": entrada_regular_gls, "r_ven": entrada_regular_venta,
        "s_pulg": entrada_super_pulg, "s_gls": entrada_super_gls, "s_ven": entrada_super_venta
    }


def menu_ingresar_medidas(pestana_ingreso): 
    fecha_actual = datetime.date.today().strftime("%Y-%m-%d")

    ctk.CTkLabel(
        pestana_ingreso, 
        text=f"Fecha del Registro: {fecha_actual} (Automática por el Sistema)", 
        font=("Arial", 13, "italic"), text_color="gray"
    ).grid(row=0, column=0, columnspan=4, pady=10, sticky="w", padx=20)

    # Llamamos a la función para pintar las cajas en la fila 1
    cajas = crear_interfaz_cajas(pestana_ingreso, 1)

    mensaje_guardado = ctk.CTkLabel(pestana_ingreso, text="", font=("Arial", 12))
    mensaje_guardado.grid(row=7, column=0, columnspan=4, pady=5)

    def llenar_cajas(caja_tot, caja_ven, tot, ven):
        caja_tot.configure(state="normal")
        caja_tot.delete(0, 'end')
        caja_tot.insert(0, str(tot))
        caja_tot.configure(state="readonly")
        
        caja_ven.configure(state="normal")
        caja_ven.delete(0, 'end')
        caja_ven.insert(0, str(ven))
        caja_ven.configure(state="readonly")

    def ejecutar_calculo():
        pulg_d = cajas["d_pulg"].get().strip() or "0"
        pulg_r = cajas["r_pulg"].get().strip() or "0"
        pulg_s = cajas["s_pulg"].get().strip() or "0"

        tot_d, ven_d = calculo_T.buscar_medida("DIESEL", pulg_d)
        tot_r, ven_r = calculo_T.buscar_medida("REGULAR", pulg_r)
        tot_s, ven_s = calculo_T.buscar_medida("SUPER", pulg_s)

        llenar_cajas(cajas["d_gls"], cajas["d_ven"], tot_d, ven_d)
        llenar_cajas(cajas["r_gls"], cajas["r_ven"], tot_r, ven_r)
        llenar_cajas(cajas["s_gls"], cajas["s_ven"], tot_s, ven_s)

        boton_guardar.grid(row=6, column=0, columnspan=4, pady=20)

    def guardar_en_bd():
        # Lógica de guardado (INSERT) aquí (para que tu botón funcione completamente)
        conn = conexion()
        if not conn:
            mensaje_guardado.configure(text="Error de conexión.", text_color="red")
            return
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO registros_medidas (fecha, diesel_pulg, diesel_gls, diesel_venta, regular_pulg, regular_gls, regular_venta, super_pulg, super_gls, super_venta) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                fecha_actual, 
                float(cajas["d_pulg"].get() or 0), float(cajas["d_gls"].get() or 0), float(cajas["d_ven"].get() or 0),
                float(cajas["r_pulg"].get() or 0), float(cajas["r_gls"].get() or 0), float(cajas["r_ven"].get() or 0),
                float(cajas["s_pulg"].get() or 0), float(cajas["s_gls"].get() or 0), float(cajas["s_ven"].get() or 0)
            ))
            conn.commit()
            mensaje_guardado.configure(text="¡Registro Guardado!", text_color="green")
            boton_guardar.grid_forget()
        except Exception as e:
            print("Error al insertar:", e)
            mensaje_guardado.configure(text="Error (¿El registro de hoy ya existe?)", text_color="red")
        finally:
            if conn: conn.close()

    boton_calcular = ctk.CTkButton(pestana_ingreso, text="CALCULAR MEDIDA", command=ejecutar_calculo)
    boton_calcular.grid(row=5, column=0, columnspan=4, pady=20)
    
    boton_guardar = ctk.CTkButton(pestana_ingreso, text="GUARDAR REGISTRO", fg_color="green", hover_color="darkgreen", command=guardar_en_bd)

def menu_buscar_medidas(pestana_buscar):
    import datetime
    
    ctk.CTkLabel(pestana_buscar, text="Buscar Registro por Fecha", font=("Arial", 16, "bold")).pack(pady=10)

    entrada_fecha = ctk.CTkEntry(pestana_buscar, placeholder_text="YYYY-MM-DD", width=150)
    entrada_fecha.pack(pady=10)

    resultado_label = ctk.CTkLabel(pestana_buscar, text="", font=("Arial", 12))
    resultado_label.pack(pady=10)

    def buscar():
        fecha = entrada_fecha.get().strip()

        if not fecha:
            resultado_label.configure(text="Ingresa una fecha", text_color="red")
            return

        try:
            datetime.datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            resultado_label.configure(text="Formato inválido (YYYY-MM-DD)", text_color="red")
            return

        conn = conexion()
        if not conn:
            resultado_label.configure(text="Error de conexión a Neon", text_color="red")
            return

        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT * FROM registros_medidas 
                WHERE fecha = %s::date;
            """, (fecha,))
            
            registro = cur.fetchone()

            if registro:
                texto = f"""
Fecha: {registro[1]}

DIESEL → Pulg: {registro[2]} | GLS: {registro[3]} | Venta: {registro[4]}
REGULAR → Pulg: {registro[5]} | GLS: {registro[6]} | Venta: {registro[7]}
SUPER → Pulg: {registro[8]} | GLS: {registro[9]} | Venta: {registro[10]}
"""
                resultado_label.configure(text=texto, text_color="green")
            else:
                resultado_label.configure(text="No existe registro para esa fecha", text_color="red")

        except Exception as e:
            print(e)
            resultado_label.configure(text="Error al consultar Neon", text_color="red")
        finally:
            conn.close()

    boton_buscar = ctk.CTkButton(pestana_buscar, text="BUSCAR", command=buscar)
    boton_buscar.pack(pady=10)

def menu_editar_medidas(pestana_editar):
    # 1. Buscador Superior
    marco_buscador = ctk.CTkFrame(pestana_editar)
    marco_buscador.grid(row=0, column=0, columnspan=4, pady=10, padx=20, sticky="w")
    
    ctk.CTkLabel(marco_buscador, text="Buscar Fecha (YYYY-MM-DD):", font=("Arial", 13, "bold")).grid(row=0, column=0, padx=10, pady=5)
    entrada_fecha = ctk.CTkEntry(marco_buscador, placeholder_text="Ej. 2023-10-25", width=120)
    entrada_fecha.grid(row=0, column=1, padx=10, pady=5)

    mensaje_editar = ctk.CTkLabel(pestana_editar, text="", font=("Arial", 12))
    
    # 2. Reciclar la interfaz visual en la fila 1
    cajas = crear_interfaz_cajas(pestana_editar, 1)

    def llenar_caja(caja, valor, es_lectura=False):
        caja.configure(state="normal")
        caja.delete(0, 'end')
        caja.insert(0, str(valor) if valor is not None else "0")
        if es_lectura:
            caja.configure(state="readonly")

    def buscar_registro():
        fecha = entrada_fecha.get().strip()
        if not fecha:
            mensaje_editar.configure(text="Por favor ingresa una fecha.", text_color="red")
            return
            
        registro = calculo_T.obtener_registro_por_fecha(fecha)
        if registro:
            mensaje_editar.configure(text="Registro encontrado. Modifica las pulgadas y recalcula.", text_color="green")
            
            # Suponiendo que el orden de BD es: id, fecha, d_pulg, d_gls, d_ven, r_pulg, r_gls...
            llenar_caja(cajas["d_pulg"], registro[2])
            llenar_caja(cajas["d_gls"], registro[3], True)
            llenar_caja(cajas["d_ven"], registro[4], True)
            
            llenar_caja(cajas["r_pulg"], registro[5])
            llenar_caja(cajas["r_gls"], registro[6], True)
            llenar_caja(cajas["r_ven"], registro[7], True)
            
            llenar_caja(cajas["s_pulg"], registro[8])
            llenar_caja(cajas["s_gls"], registro[9], True)
            llenar_caja(cajas["s_ven"], registro[10], True)
            
            boton_calcular.grid(row=5, column=0, columnspan=4, pady=10)
            boton_guardar.grid_forget()
        else:
            mensaje_editar.configure(text="No se encontró registro para esa fecha.", text_color="red")

    boton_buscar = ctk.CTkButton(marco_buscador, text="Buscar", command=buscar_registro)
    boton_buscar.grid(row=0, column=2, padx=10, pady=5)

    # 3. Recálculo
    def ejecutar_calculo():
        tot_d, ven_d = calculo_T.buscar_medida("DIESEL", cajas["d_pulg"].get().strip() or "0")
        tot_r, ven_r = calculo_T.buscar_medida("REGULAR", cajas["r_pulg"].get().strip() or "0")
        tot_s, ven_s = calculo_T.buscar_medida("SUPER", cajas["s_pulg"].get().strip() or "0")

        llenar_caja(cajas["d_gls"], tot_d, True)
        llenar_caja(cajas["d_ven"], ven_d, True)
        llenar_caja(cajas["r_gls"], tot_r, True)
        llenar_caja(cajas["r_ven"], ven_r, True)
        llenar_caja(cajas["s_gls"], tot_s, True)
        llenar_caja(cajas["s_ven"], ven_s, True)
        
        boton_guardar.grid(row=6, column=0, columnspan=4, pady=10)
        mensaje_editar.configure(text="Cálculo actualizado. Ahora puedes guardar.", text_color="orange")

    boton_calcular = ctk.CTkButton(pestana_editar, text="CALCULAR NUEVA MEDIDA", command=ejecutar_calculo)

    # 4. Actualizar Base de Datos (UPDATE)
    def guardar_cambios():
        fecha = entrada_fecha.get().strip()
        exito = calculo_T.actualizar_registro(
            fecha,
            float(cajas["d_pulg"].get() or 0), float(cajas["d_gls"].get() or 0), float(cajas["d_ven"].get() or 0),
            float(cajas["r_pulg"].get() or 0), float(cajas["r_gls"].get() or 0), float(cajas["r_ven"].get() or 0),
            float(cajas["s_pulg"].get() or 0), float(cajas["s_gls"].get() or 0), float(cajas["s_ven"].get() or 0)
        )
        
        if exito:
            mensaje_editar.configure(text="¡Registro Actualizado Exitosamente!", text_color="green")
            boton_guardar.grid_forget()
        else:
            mensaje_editar.configure(text="Error al actualizar.", text_color="red")

    boton_guardar = ctk.CTkButton(pestana_editar, text="GUARDAR CAMBIOS", fg_color="green", hover_color="darkgreen", command=guardar_cambios)
    mensaje_editar.grid(row=7, column=0, columnspan=4, pady=5)


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

    ventana_admin.protocol("WM_DELETE_WINDOW",cerrar_programa)
    
    ctk.CTkLabel(ventana_admin, text="⚙️ ADMINISTRADOR", font=("Arial", 20, "bold")).pack(pady=10)
    
    # Pestañas del Admin 
    tabs = ctk.CTkTabview(ventana_admin, width=750, height=400)
    tabs.pack(pady=10)
    
    tabs.add("Añadir")
    tabs.add("Historial")
    tabs.add("Buscar")
    menu_buscar_medidas(tabs.tab("Buscar"))
    tabs.add("Editar")
    tabs.add("Eliminar")

    # Inyectamos las funciones en sus pestañas
    menu_ingresar_medidas(tabs.tab("Añadir"))
    menu_editar_medidas(tabs.tab("Editar"))


# funcion para finalizar el programa
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

# titulo principal 
titulo = ctk.CTkLabel(ventana, text="LOGIN AL SISTEMA", font=("Arial",20,"bold"))
titulo.pack(pady=20)

# usuario
entrada_usuario = ctk.CTkEntry(ventana, placeholder_text="usuario", width=200)
entrada_usuario.pack(pady=10)

# contraseña
entrada_password = ctk.CTkEntry(ventana, placeholder_text="contraseña", show="*", width=200)
entrada_password.pack(pady=10)

# boton ingresar
boton_entrar = ctk.CTkButton(ventana, text="Ingresar", command=intentar_login)
boton_entrar.pack(pady=20)

mensaje_error = ctk.CTkLabel(ventana, text="", text_color="red")
mensaje_error.pack(pady=5)

ventana.mainloop()




