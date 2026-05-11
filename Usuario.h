#ifndef USUARIO_H
#define USUARIO_H

#include <string>

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

#endif