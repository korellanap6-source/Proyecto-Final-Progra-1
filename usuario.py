class usuario:
    def __init__(self,username,password):
        self.username= username
        self.username= password


    def validar (self,u,p):
        return  (self.username== u and  self.password == p)