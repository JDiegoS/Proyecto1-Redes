#Proyecto 1 Redes
#Juan Diego Solorzano 18151

import sys
import asyncio
import logging
from getpass import getpass
from slixmpp.xmlstream.asyncio import asyncio

import slixmpp

#Referencia https://slixmpp.readthedocs.io/en/slix-1.6.0/getting_started/echobot.html

class Client(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.add_event_handler('session_start', self.start)

        #Al recibir mensaje
        #self.add_event_handler('message', self.message)

    async def getUsers(self):
        try:
            self.get_roster()
        except:
            print("Error al obtener roster")
        
        self.send_presence()
        print('Waiting for presence updates...\n')
        #self.presences_received.wait(5)
        await asyncio.sleep(5)
        print("\nLista de usuarios:")
        
        groups = self.client_roster.groups()
        for group in groups:
            for jid in groups[group]:
                sub = self.client_roster[jid]['subscription']
                name = self.client_roster[jid]['name']
                if self.client_roster[jid]['name']:
                    print(' %s (%s) [%s]' % (name, jid, sub))
                else:
                    print(' %s [%s]' % (jid, sub))

                connections = self.client_roster.presence(jid)
                for res, pres in connections.items():
                    show = 'available'
                    if pres['show']:
                        show = pres['show']
                    print('   - %s (%s)' % (res, show))
                    if pres['status']:
                        print('       %s' % pres['status'])
    async def start(self, event):
        self.send_presence()
        self.get_roster()

        print("\nBienvenido al programa " + self.jid)
        sigue = True
        while sigue == True:
            opc2 =  int(input("\nIngrese una opcion:\n1. Mostrar Usuarios \n2. Agregar Contacto \n3. Mostrar Usuario \n4. Mensaje de Presencia \n5. Mensaje Privado \n6. Mensaje Grupal\n7. Log out \n"))
            if opc2 == 1:
                #Mostrar Usuarios
                await self.getUsers()
            elif opc2 == 2:
                pass
            elif opc2 == 3:
                pass
            elif opc2 == 4:
                pass
            elif opc2 == 5:
                pass
            elif opc2 == 6:
                pass
            elif opc2 == 7:
                print("Hasta luego!")
                self.disconnect()
                sigue = False
    
    def message(self, msg):
        if msg['type'] in ('normal', 'chat'):
            msg.reply("Thanks for sending:\n%s" % msg['body']).send()
    
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