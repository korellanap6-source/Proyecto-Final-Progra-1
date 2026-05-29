# Sistema de Control y Medición de Tanques de Combustible

Este sistema fue diseñado para facilitar la gestión, el cálculo y el almacenamiento del inventario diario de combustible (Diésel, Regular y Súper) en una estación de servicio. La aplicación automatiza la conversión de medidas físicas (pulgadas) a galones y mantiene un registro histórico centralizado y seguro.

# Requisitos Previos (Instalación)

Antes de ejecutar el sistema por primera vez, es indispensable instalar los complementos de interfaz gráfica, conexión a base de datos y variables de entorno. 

Abra su terminal o línea de comandos y ejecute el siguiente comando:

pip install customtkinter psycopg2 python-dotenv

Adicional a esto tambien es necesario que cree un archivo llamado .env, en el cual se va a colocar la conexion a la base de datos, ya sea local o en la nube (no se agrego al repositorio por temas de seguridad de informacion)

# Perfiles de Acceso

Para proteger los datos, el sistema cuenta con dos niveles de acceso:

* **Administrador:** Tiene control total de la plataforma. Puede ingresar nuevas medidas, visualizar el historial completo, buscar registros específicos, y editar o eliminar datos de días anteriores.

* **Empleado:** Tiene acceso operativo. Únicamente está autorizado para registrar las medidas del día actual y consultar la tabla del historial.

## Manual de Uso e Inicio Rápido

##1. Iniciar la Aplicación
Asegúrese de estar ubicado en la carpeta del proyecto. Abra su terminal o línea de comandos y ejecute el sistema con el siguiente comando:

python main.py

**"El programa requiere conexion a internet ya que el sistema guarda la información de forma segura en la nube"**

## 2. Inicio de Sesión

Al ejecutarse el programa, aparecerá la pantalla de acceso. Ingrese una de las siguientes credenciales de prueba, dependiendo de las funciones que desee evaluar:

Para ingresar como Administrador:

Usuario: admin
Contraseña: 1234

Para ingresar como Empleado:

Usuario: Kevin
Contraseña: 1234

## 3. Uso de las Herramientas del Sistema

Una vez dentro de la plataforma, podrá navegar utilizando las pestañas superiores. Cada una cumple una función específica:

**Añadir / Ingresar Medida**: Ingrese las pulgadas de combustible que marca la regla física en cada tanque. Al hacer clic en "Calcular Medida", el sistema deducirá la reserva de seguridad y le mostrará los galones disponibles para la venta. Finalmente, haga clic en "Guardar Registro".

**Historial:** Muestra una tabla con todos los registros almacenados en el sistema ordenados por fecha. Incluye un botón para actualizar la tabla y ver los datos más recientes.

**Buscar(Exclusivo Administrador):** Permite consultar cómo estaban los tanques en un día específico. Solo debe ingresar la fecha en formato numérico (por ejemplo: 2023-10-25) y presionar el botón de búsqueda.

**Editar(Exclusivo Administrador):** Si se cometió un error al ingresar los datos de un día anterior, utilice esta pestaña. Busque la fecha, corrija las pulgadas, vuelva a calcular el total y presione "Guardar Cambios" para actualizar la base de datos.

**Eliminar(Exclusivo Administrador):** En caso de existir un registro duplicado o inválido, ingrese la fecha correspondiente para borrarlo permanentemente del sistema.