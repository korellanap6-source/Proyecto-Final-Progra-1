
class usuario:
    # Constructor
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    # Método para validar
    def validar(self, u, p):
        # ¡La palabra 'return' aquí es obligatoria!
        return (self.username == u and self.password == p)