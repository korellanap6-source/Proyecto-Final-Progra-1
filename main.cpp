#include <iostream>
#include <stdlib.h>	
#include <conio.h> 
#include <windows.h> 
#include <string>
#include "Usuario.h"
#include "Interfaz.h"

void menuTrabajador();
void menuAdmin();

using namespace std;

bool realizarLogin(string rolEsperado) {
    string userIn, passIn;
    
    Interfaz::AjustarVentana_menu(50, 20);
    system("cls");
    Interfaz::marco(5, 5, 44, 15);
    
    Interfaz::gotoxy(15, 6); cout << "LOGIN: " << rolEsperado;
    Interfaz::gotoxy(10, 8);  cout << "Usuario: "; cin >> userIn;
    Interfaz::gotoxy(10, 10); cout << "Password: "; cin >> passIn;

    
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
        Interfaz::AjustarVentana_menu(50, 20); 	
        system("cls"); 									
        Interfaz::marco(3, 3, 46, 17);							
        system("color 0B"); 			
        
        Interfaz::gotoxy(6, 5); cout << "SISTEMA DE MEDICION DE TANQUES -";
        Interfaz::gotoxy(21, 7); cout << "LOGIN";
        Interfaz::gotoxy(12, 8); cout << "--------------------------";
        Interfaz::gotoxy(10, 10); cout << "[1] Ingresar como Trabajador";
        Interfaz::gotoxy(10, 11); cout << "[2] Ingresar como Administrador";
        Interfaz::gotoxy(10, 13); cout << "[3] Salir del Sistema";
        Interfaz::gotoxy(10, 15); cout << "Seleccione su rol: ";

        opcion = getch();

        switch (opcion) {
            case '1':
                if (realizarLogin("TRABAJADOR")){
                    menuTrabajador();
                }else {
                    Interfaz::gotoxy(12, 17); cout << "Error: Datos incorrectos.";
                    Sleep(1500);
                }
                break;
            case '2':
                if (realizarLogin("ADMIN")){
                    menuAdmin();
                }else {
                    Interfaz::gotoxy(12, 17); cout << "Error: Datos incorrectos.";
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
    Interfaz::AjustarVentana_menu(55, 20); 
    system("cls"); 
    Interfaz::marco(3, 3, 52, 17);
    system("color 0A"); 

    Interfaz::gotoxy(15, 5); cout << "PANEL DE TRABAJADOR";
    Interfaz::gotoxy(10, 7); cout << "-------------------------------";
    Interfaz::gotoxy(10, 9); cout << "[1] Registrar medida del dia";
    Interfaz::gotoxy(10, 11); cout << "[2] Cerrar Sesion";

    char op;
    do{
        op=getch();
        if(op == '1'){
            Interfaz::gotoxy(10, 14); cout << "Abriendo modulo de registro...  ";
            Sleep(1000);
            break;
        }
    }while(op != '2');
}

void menuAdmin(){
    Interfaz::AjustarVentana_menu(60, 25); 
    system("cls"); 
    Interfaz::marco(3, 3, 56, 22);
    system("color 0E"); 

    Interfaz::gotoxy(18, 5); cout << "PANEL DE ADMINISTRADOR";
    Interfaz::gotoxy(12, 7); cout << "---------------------------------";
    Interfaz::gotoxy(12, 9); cout << "[1] Registrar nueva medida";
    Interfaz::gotoxy(12, 10); cout << "[2] Buscar medida por fecha";
    Interfaz::gotoxy(12, 11); cout << "[3] Ver historial de medidas";
    Interfaz::gotoxy(12, 12); cout << "[4] Modificar un registro";
    Interfaz::gotoxy(12, 13); cout << "[5] Eliminar un registro";
    Interfaz::gotoxy(12, 15); cout << "[6] Cerrar Sesion";

    char op;
    do{
        op = getch();
        if(op >='1' && op<='5'){
            Interfaz::gotoxy(12, 18); cout << "Opcion " << op << " seleccionada...     ";
            Sleep(1000);
            break;
        }
    }while(op != '6');
}