#Proyecto 1 Redes
#Juan Diego Solorzano 18151

def mostrarUsuarios():
    pass

def agregarContacto():
    pass

def mostrarContacto():
    pass

def mensajePresencia():
    pass

def chatPersonal():
    pass

def chatGrupal():
    pass


termino = False
print("Bienvenido \n")
while termino != True:
    opc1 = input("Ingrese una opcion:\n1. Iniciar sesion \n2. Registrar nuevo usuario \n3. Salir\n")
    if opc1 == 1:
        #Iniciar sesion
        userName = input("Ingrese el usuario: ")
        password = input("Ingrese la contrasena: ")
    elif opc1 == 2:
        #Registrar
        newUser = input("Ingrese el usuario: ")
        newPass = input("Ingrese la contrasena: ")
    elif opc1 == 3:
        print("Gracias por utilizar el programa")
        termino = True
    else:
        print("Esa no es una opcion")