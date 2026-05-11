#include <iostream>
#include <stdlib.h>	
#include <conio.h> 
#include <windows.h> 
#include <string>

// Definiciones para el marco
#define arrizq 219				
#define arrder 219				
#define abajizq 219				
#define abajder 219				
#define vert 178				
#define horiz 178				
#define PR(x) cout<<char (x);	// Intercambiar el cout

void marco(int,int,int,int);
void gotoxy(int x, int y);
bool AjustarVentana_menu(int Ancho, int Alto); 
void menuTrabajador();
void menuAdmin();

using namespace std;

// --- CAPA DE DATOS (POO) ---
class Usuario {
private:
    string username;
    string password;
public:
    // Constructor
    Usuario(string u, string p) : username(u), password(p) {}
    
    // Método para validar
    bool validar(string u, string p) {
        return (username == u && password == p);
    }
};

bool realizarLogin(string rolEsperado) {
    string userIn, passIn;
    
    AjustarVentana_menu(50, 20);
    system("cls");
    marco(5, 5, 44, 15);
    
    gotoxy(15, 6); cout << "LOGIN: " << rolEsperado;
    
    gotoxy(10, 8);  cout << "Usuario: "; 
    cin >> userIn;
    
    gotoxy(10, 10); cout << "Password: ";
    cin >> passIn; 

    
    if (rolEsperado == "ADMIN") {
        Usuario admin("admin", "1234");
        return admin.validar(userIn, passIn);
    } else {
        Usuario trab("gas", "5678");
        return trab.validar(userIn, passIn);
    }
}


int main (){
    char opcion;

    do{
        AjustarVentana_menu(50, 20); 	
        system("cls"); 									
        marco(3, 3, 46, 17);							
        system("color 0B"); 			
        
        gotoxy(12, 5); cout << "SISTEMA DE INVENTARIO - DIESEL";
        gotoxy(21, 7); cout << "LOGIN";
        gotoxy(12, 8); cout << "--------------------------";
        gotoxy(10, 10); cout << "[1] Ingresar como Trabajador";
        gotoxy(10, 11); cout << "[2] Ingresar como Administrador";
        gotoxy(10, 13); cout << "[3] Salir del Sistema";
        gotoxy(10, 15); cout << "Seleccione su rol: ";

        opcion = getch();

        switch (opcion) {
            case '1':
                if (realizarLogin("TRABAJADOR")){
                    menuTrabajador();
                }else {
                    gotoxy(12, 17); cout << "Error: Datos incorrectos.";
                    Sleep(1500);
                }
                break;
            case '2':
                if (realizarLogin("ADMIN")){
                    menuAdmin();
                }else {
                    gotoxy(12, 17); cout << "Error: Datos incorrectos.";
                    Sleep(1500);
                }
                break;
            case '3':
                exit(0);
                break;
        }
    }while(true);
    return 0;
}

void menuTrabajador(){
    AjustarVentana_menu(55, 20); 
    system("cls"); 
    marco(3, 3, 52, 17);
    system("color 0A"); // Color verde para trabajador

    gotoxy(15, 5); cout << "PANEL DE TRABAJADOR";
    gotoxy(10, 7); cout << "-------------------------------";
    gotoxy(10, 9); cout << "[1] Registrar medida del dia";
    gotoxy(10, 11); cout << "[2] Cerrar Sesion";

    char op;
    do{
        op=getch();
        if(op == '1'){
            gotoxy(10, 14); cout << "Abriendo modulo de registro...  ";
            Sleep(1000);
            break;
        }
    }while(op != '2');
}

void menuAdmin(){
    AjustarVentana_menu(60, 25); 
    system("cls"); 
    marco(3, 3, 56, 22);
    system("color 0E"); // Color amarillo para admin

    gotoxy(18, 5); cout << "PANEL DE ADMINISTRADOR";
    gotoxy(12, 7); cout << "---------------------------------";
    gotoxy(12, 9); cout << "[1] Registrar nueva medida";
    gotoxy(12, 10); cout << "[2] Buscar medida por fecha";
    gotoxy(12, 11); cout << "[3] Ver historial de medidas";
    gotoxy(12, 12); cout << "[4] Modificar un registro";
    gotoxy(12, 13); cout << "[5] Eliminar un registro";
    gotoxy(12, 15); cout << "[6] Cerrar Sesion";

    char op;
    do{
        op = getch();
        if(op >='1' && op<='5'){
            gotoxy(12, 18); cout << "Opcion " << op << " seleccionada...     ";
            Sleep(1000);
            break;
        }
    }while(op != '6');
}

// Funcion gotoxy 
void gotoxy(int x, int y){
	HANDLE hCon; 
	hCon = GetStdHandle(STD_OUTPUT_HANDLE); 
	
	COORD dwPos; 
	dwPos.X = x; 
	dwPos.Y = y;
	SetConsoleCursorPosition(hCon,dwPos); 
}

// Funcion para el marco
void marco(int a, int b, int c, int d){
	
	int i;							
	gotoxy (a-1,b-1);				
	PR(arrizq);						
	
	for (i=a; i<=c; i++)			
		PR(horiz);
		PR(arrder);
		
		for (i=b; i<=d; i++){		
			gotoxy (c+1,i);
			PR(vert);
		}
	
	gotoxy (a-1,d+1);
	PR(abajizq);					
	
		for (i=a; i<=c; i++)		
			PR(horiz);
			PR(abajder);			
			
		for (i=b; i<=d; i++){
			gotoxy (a-1,i);
			PR(vert);
		}
}

// Funcion para la ventana
bool AjustarVentana_menu(int Ancho, int Alto){
	
	_COORD Coordenada;
	Coordenada.X = Ancho;
	Coordenada.Y = Alto;
	
	_SMALL_RECT Rect;
	Rect.Top = 0;
	Rect.Left = 0;
	Rect.Right = Ancho - 1;
	Rect.Bottom = Alto - 1;
	
	
	HANDLE hConsola = GetStdHandle(STD_OUTPUT_HANDLE);
	
	
	SetConsoleScreenBufferSize(hConsola, Coordenada);
	
	
	SetConsoleWindowInfo(hConsola, TRUE, &Rect);
	return TRUE;
}
