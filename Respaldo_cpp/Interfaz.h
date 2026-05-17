#ifndef INTERFAZ_H
#define INTERFAZ_H

#include <iostream>
#include <windows.h>

// Definiciones para el marco
#define arrizq 219				
#define arrder 219				
#define abajizq 219				
#define abajder 219				
#define vert 178				
#define horiz 178				

using namespace std;

#define PR(x) cout<<char(x);

class Interfaz {
public:
    static void gotoxy(int x, int y){
        HANDLE hCon = GetStdHandle(STD_OUTPUT_HANDLE); 
        COORD dwPos; 
        dwPos.X = x; 
        dwPos.Y = y;
        SetConsoleCursorPosition(hCon,dwPos); 
    }

    static void marco(int a, int b, int c, int d){
        int i;							
        gotoxy(a-1,b-1);				
        PR(arrizq);						
        for (i=a; i<=c; i++) { PR(horiz); }
        PR(arrder);
        for (i=b; i<=d; i++){ gotoxy (c+1,i); PR(vert); }
        gotoxy(a-1,d+1);
        PR(abajizq);					
        for (i=a; i<=c; i++) { PR(horiz); }
        PR(abajder);			
        for (i=b; i<=d; i++){ gotoxy (a-1,i); PR(vert); }
    }

    static bool AjustarVentana_menu(int Ancho, int Alto){
        _COORD Coordenada;
        Coordenada.X = Ancho;
        Coordenada.Y = Alto;
        _SMALL_RECT Rect;
        Rect.Top = 0; Rect.Left = 0; Rect.Right = Ancho - 1; Rect.Bottom = Alto - 1;
        HANDLE hConsola = GetStdHandle(STD_OUTPUT_HANDLE);
        SetConsoleScreenBufferSize(hConsola, Coordenada);
        SetConsoleWindowInfo(hConsola, TRUE, &Rect);
        return TRUE;
    }
};

#endif