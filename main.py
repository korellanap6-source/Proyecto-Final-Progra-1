import customtkinter as ctk 
from tkinter import ttk, messagebox
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

# --- FUNCIONES DE LÓGICA ---

def consultar_historial(tabla_treeview):
    conn = conexion()
    if not conn: return
    try:
        cursor = conn.cursor()
        # Traemos los datos de la tabla registros_medidas
        cursor.execute("SELECT id, diesel_pulg, diesel_gls, diesel_venta, fecha FROM registros_medidas ORDER BY id DESC")
        filas = cursor.fetchall()

        for item in tabla_treeview.get_children():
            tabla_treeview.delete(item)

        for fila in filas:
            tabla_treeview.insert("", "end", values=fila)
    except Exception as e:
        print(f"Error al cargar historial: {e}")
    finally:
        conn.close()

def eliminar_registro(id_eliminar, lbl_msj, tabla):
    id_e = id_eliminar.get().strip()
    if not id_e:
        lbl_msj.configure(text="❌ Por favor, ingrese un ID", text_color="orange")
        return
    
    if messagebox.askyesno("Confirmar", f"¿Estás seguro de eliminar el registro {id_e}?"):
        conn = conexion()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM registros_medidas WHERE id = %s", (id_e,))
            conn.commit()
            if cursor.rowcount > 0:
                lbl_msj.configure(text=f"✅ Registro {id_e} eliminado exitosamente", text_color="green")
                consultar_historial(tabla) # Refresca la tabla automáticamente
                id_eliminar.delete(0, 'end')
            else:
                lbl_msj.configure(text="❌ El ID no existe en la base de datos", text_color="red")
        except Exception as e:
            lbl_msj.configure(text=f"❌ Error técnico: {e}", text_color="red")
        finally:
            conn.close()

# --- CONFIGURACIÓN DE APARIENCIA ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

ventana = ctk.CTk()
ventana.geometry("450x450")
ventana.title("Sistema de Medición de Tanques - Irvyn")

# --- INTERFACES DE LAS PESTAÑAS ---

def menu_editar_registro(pestana_editar):
    ctk.CTkLabel(pestana_editar, text="✏️ EDITAR REGISTRO EXISTENTE", font=("Arial", 18, "bold")).pack(pady=15)
    
    ent_id = ctk.CTkEntry(pestana_editar, placeholder_text="ID del Registro (Ej: 3)", width=280)
    ent_id.pack(pady=8)
    
    ent_nom = ctk.CTkEntry(pestana_editar, placeholder_text="Escribe: DIESEL", width=280)
    ent_nom.pack(pady=8)
    
    ent_pulg = ctk.CTkEntry(pestana_editar, placeholder_text="Nuevas Pulgadas", width=280)
    ent_pulg.pack(pady=8)
    
    ent_fec = ctk.CTkEntry(pestana_editar, placeholder_text="Nueva Fecha (AAAA-MM-DD)", width=280)
    ent_fec.pack(pady=8)

    lbl_resultado = ctk.CTkLabel(pestana_editar, text="", font=("Arial", 12))
    lbl_resultado.pack(pady=10)

    def confirmar_edicion():
        exito = calculo_T.actualizar_registro_completo(ent_id.get(), ent_nom.get(), ent_pulg.get(), ent_fec.get())
        if exito:
            lbl_resultado.configure(text="✅ Actualizado en Neon con éxito", text_color="green")
        else:
            lbl_resultado.configure(text="❌ No se pudo actualizar. Revisa el ID.", text_color="red")

    ctk.CTkButton(pestana_editar, text="GUARDAR CAMBIOS", fg_color="#1f538d", font=("Arial", 14, "bold"), command=confirmar_edicion).pack(pady=20)

def menu_ingresar_medidas(pestana_ingreso): 
    fecha_actual = datetime.date.today().strftime("%Y-%m-%d")
    ctk.CTkLabel(pestana_ingreso, text=f"Fecha del Registro: {fecha_actual}", font=("Arial", 13, "italic"), text_color="gray").grid(row=0, column=0, columnspan=4, pady=15, sticky="w", padx=20)

    # Encabezados con diseño original
    headers = ["Combustible", "Pulgadas (PULG)", "Galones (GLS)", "Venta Disponible"]
    for i, h in enumerate(headers):
        ctk.CTkLabel(pestana_ingreso, text=h, font=("Arial", 14, "bold")).grid(row=1, column=i, padx=15, pady=10)
    
    # FILA DIESEL
    ctk.CTkLabel(pestana_ingreso, text="⛽ DIESEL:", font=("Arial", 14)).grid(row=2, column=0, padx=20, pady=10, sticky="w")
    e_d_p = ctk.CTkEntry(pestana_ingreso, width=100); e_d_p.grid(row=2, column=1)
    e_d_g = ctk.CTkEntry(pestana_ingreso, width=100, state="readonly"); e_d_g.grid(row=2, column=2)
    e_d_v = ctk.CTkEntry(pestana_ingreso, width=100, state="readonly"); e_d_v.grid(row=2, column=3)
    
    # FILA REGULAR
    ctk.CTkLabel(pestana_ingreso, text="⛽ REGULAR:", font=("Arial", 14)).grid(row=3, column=0, padx=20, pady=10, sticky="w")
    e_r_p = ctk.CTkEntry(pestana_ingreso, width=100); e_r_p.grid(row=3, column=1)
    e_r_g = ctk.CTkEntry(pestana_ingreso, width=100, state="readonly"); e_r_g.grid(row=3, column=2)
    e_r_v = ctk.CTkEntry(pestana_ingreso, width=100, state="readonly"); e_r_v.grid(row=3, column=3)

    # FILA SÚPER
    ctk.CTkLabel(pestana_ingreso, text="⛽ SÚPER:", font=("Arial", 14)).grid(row=4, column=0, padx=20, pady=10, sticky="w")
    e_s_p = ctk.CTkEntry(pestana_ingreso, width=100); e_s_p.grid(row=4, column=1)
    e_s_g = ctk.CTkEntry(pestana_ingreso, width=100, state="readonly"); e_s_g.grid(row=4, column=2)
    e_s_v = ctk.CTkEntry(pestana_ingreso, width=100, state="readonly"); e_s_v.grid(row=4, column=3)

    def ejecutar_calculo():
        td, vd = calculo_T.buscar_medida("DIESEL", e_d_p.get())
        tr, vr = calculo_T.buscar_medida("REGULAR", e_r_p.get())
        ts, vs = calculo_T.buscar_medida("SUPER", e_s_p.get())

        def actualizar(c_g, c_v, g, v):
            c_g.configure(state="normal"); c_g.delete(0, 'end'); c_g.insert(0, str(g)); c_g.configure(state="readonly")
            c_v.configure(state="normal"); c_v.delete(0, 'end'); c_v.insert(0, str(v)); c_v.configure(state="readonly")

        actualizar(e_d_g, e_d_v, td, vd)
        actualizar(e_r_g, e_r_v, tr, vr)
        actualizar(e_s_g, e_s_v, ts, vs)

    ctk.CTkButton(pestana_ingreso, text="CALCULAR MEDIDA", font=("Arial", 14, "bold"), command=ejecutar_calculo).grid(row=5, column=0, columnspan=4, pady=25)

# --- VENTANA DE ADMINISTRADOR ---

def abrir_ventana_admin():
    ventana.withdraw() 
    v_admin = ctk.CTkToplevel()
    v_admin.geometry("950x700")
    v_admin.title("Panel de Administración - Gasolinera")
    
    ctk.CTkLabel(v_admin, text="⚙️ PANEL DE CONTROL ADMINISTRATIVO", font=("Arial", 22, "bold")).pack(pady=15)
    
    tabs = ctk.CTkTabview(v_admin, width=900, height=600)
    tabs.pack(pady=10)
    
    tabs.add("Añadir"); tabs.add("Historial"); tabs.add("Editar"); tabs.add("Eliminar")

    # --- LÓGICA ELIMINAR ---
    p_eliminar = tabs.tab("Eliminar")
    ctk.CTkLabel(p_eliminar, text="🗑️ ELIMINAR REGISTRO PERMANENTEMENTE", font=("Arial", 18, "bold"), text_color="red").pack(pady=20)
    ent_id_del = ctk.CTkEntry(p_eliminar, placeholder_text="Ingrese el ID a eliminar", width=300)
    ent_id_del.pack(pady=15)
    lbl_msg_del = ctk.CTkLabel(p_eliminar, text="")
    lbl_msg_del.pack()

    # --- LÓGICA HISTORIAL ---
    p_historial = tabs.tab("Historial")
    columnas = ("ID", "Pulgadas", "Galones", "Venta", "Fecha")
    tabla = ttk.Treeview(p_historial, columns=columnas, show="headings", height=15)
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=130, anchor="center")
    tabla.pack(pady=10, fill="both", expand=True)
    
    ctk.CTkButton(p_historial, text="🔄 REFRESCAR DATOS", command=lambda: consultar_historial(tabla)).pack(pady=10)

    # Botón Eliminar (conectado al historial para refrescar)
    ctk.CTkButton(p_eliminar, text="ELIMINAR REGISTRO", fg_color="#922b21", hover_color="#641e16", 
                  command=lambda: eliminar_registro(ent_id_del, lbl_msg_del, tabla)).pack(pady=20)

    # Cargar contenido
    menu_ingresar_medidas(tabs.tab("Añadir"))
    menu_editar_registro(tabs.tab("Editar"))
    consultar_historial(tabla)

def intentar_login():
    if entrada_usuario.get().strip() == "admin" and entrada_password.get().strip() == "1234":
        abrir_ventana_admin()
    else:
        mensaje_error.configure(text="❌ Credenciales incorrectas")

# --- UI LOGIN ---
ctk.CTkLabel(ventana, text="SISTEMA DE CONTROL ⛽", font=("Arial", 22, "bold")).pack(pady=30)
entrada_usuario = ctk.CTkEntry(ventana, placeholder_text="Usuario", width=220)
entrada_usuario.pack(pady=12)
entrada_password = ctk.CTkEntry(ventana, placeholder_text="Contraseña", show="*", width=220)
entrada_password.pack(pady=12)
ctk.CTkButton(ventana, text="ENTRAR", font=("Arial", 14, "bold"), command=intentar_login).pack(pady=25)
mensaje_error = ctk.CTkLabel(ventana, text="", text_color="red")
mensaje_error.pack()

ventana.mainloop()