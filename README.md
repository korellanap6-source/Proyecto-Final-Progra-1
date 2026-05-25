Administrador:
usuario: admin  
contraseña: 1234

empleado:
usuario: gas  
contraseña: 5678

### 1. Instalar Python (El Motor)
1. Descarga Python desde la página oficial: [python.org](https://www.python.org/downloads/)
2. **MUY IMPORTANTE:** Al abrir el instalador, en la primera pantalla, busca en la parte inferior una casilla que dice **"Add Python to PATH"** (o "Add python.exe to PATH") y **márcala** antes de darle a instalar. 

### 2. Visual Studio Code
1. Abre Visual Studio Code.
2. Ve al apartado de **Extensiones** .
3. Busca **"Python"** y dale a **Instalar**.

### 3. Instalar la Librería Visual (CustomTkinter)
El diseño de nuestra interfaz requiere una librería especial.
1. Abre la terminal dentro de VS Code  `Terminal` -> `New Terminal`
2. Escribe el siguiente comando y presiona Enter:

   pip install customtkinter

Abre la terminal de tu Visual Studio Code (asegúrate de estar en tu rama de pruebas) y ejecuta este comando. Esto instala la librería que permite a Python hablar con PostgreSQL:
   pip install psycopg2-binary

Antes de ejecutarlo, recuerda instalar la librería para leer el archivo .env ejecutando en tu terminal: 

   pip install python-dotenv