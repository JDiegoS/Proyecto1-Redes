#Proyecto 1 Redes
#Juan Diego Solorzano 18151


from getpass import getpass
from client import Client

import slixmpp

class Register(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        super().__init__(jid, password)

        self.add_event_handler("session_start", self.start)
        self.add_event_handler('register', self.register)

    def start(self, event):
        self.send_presence()
        self.get_roster()

    def register(self, event):
        resp = self.Iq()
        resp['type'] = 'set'
        resp['register']['username'] = self.boundjid.user
        resp['register']['password'] = self.password

        try:
            resp.send()
            print("Registrado correctamente")
            self.disconnect()
        except:
            print("Error al registrarse")
            self.disconnect()

termino = False
print("\nBienvenido")
while termino != True:
    opc1 = int(input("\nIngrese una opcion:\n1. Iniciar sesion \n2. Registrar nuevo usuario \n3. Salir\n"))
    if opc1 == 1:
        #Iniciar sesion
        userName = input("Ingrese el usuario: ")
        password = getpass("Ingrese la contrasena: ")

        currentC = Client(userName, password)
        currentC.connect()
        currentC.process(forever=False)

    elif opc1 == 2:
        #Registrar
        newUser = input("Ingrese el usuario: ")
        newPass = getpass("Ingrese la contrasena: ")

        registerU = Register(newUser, newPass)
        registerU.register_plugin('xep_0004') ### Data Forms
        registerU.register_plugin('xep_0030') ### Service Discovery
        registerU.register_plugin('xep_0066') ### Band Data
        registerU.register_plugin('xep_0077') ### Band Registration
        registerU.connect()
        registerU.process(forever=False)

    elif opc1 == 3:
        print("Gracias por utilizar el programa")
        termino = True
    else:
        print("Esa no es una opcion")