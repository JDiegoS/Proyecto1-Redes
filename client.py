import sys
import asyncio
import logging
from getpass import getpass
from slixmpp.xmlstream.asyncio import asyncio

import slixmpp

#Referencias:
# https://slixmpp.readthedocs.io/en/slix-1.6.0/getting_started/echobot.html
# https://github.com/fritzy/SleekXMPP/tree/develop/examples

class Client(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.add_event_handler('session_start', self.start)

    async def getSpecificUser(self):
        uName = input("Ingrese el usuario: ")
        try:
            self.get_roster()
        except:
            print("Error al obtener lista")
        
        self.send_presence()
        print('Waiting for presence updates...\n')
        #self.presences_received.wait(5)
        await asyncio.sleep(5)
        
        found = False
        groups = self.client_roster.groups()
        for group in groups:
            for jid in groups[group]:
                if jid == uName:
                    found = True
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
                    break
            else:
                continue
            break
        if found == False:
            print("No se encontro el usuario en los contactos")
    async def getUsers(self):
        try:
            self.get_roster()
        except:
            print("Error al obtener lista")
        
        self.send_presence()
        print('Waiting for presence updates...\n')
        #self.presences_received.wait(5)
        await asyncio.sleep(5)
        print("\nLista de usuarios:")
        
        groups = self.client_roster.groups()
        for group in groups:
            print('\n%s' % group)
            print('-' * 50)
            for jid in groups[group]:
                sub = self.client_roster[jid]['subscription']
                name = self.client_roster[jid]['name']
                if self.client_roster[jid]['name']:
                    print('  %s (%s) [%s]' % (name, jid, sub))
                else:
                    print('  %s [%s]' % (jid, sub))

                connections = self.client_roster.presence(jid)
                for res, pres in connections.items():
                    show = 'available'
                    if pres['show']:
                        show = pres['show']
                    print('    - %s (%s)' % (res, show))
                    if pres['status']:
                        print('        %s' % pres['status'])
    
    def addContact(self):
        addName = input("Ingrese el usuario: ")
        addNick = input("Ingrese el apodo para el contacto: ")
        try:
            self.send_presence_subscription(pfrom=self.boundjid.bare, pto=addName, ptype="subscribe", pnick=addNick)
            print("Solicitud enviada correctamente")
        except:
            print("Error al agregar contacto")

    def mensajePresencia():
        pass

    def chatPersonal():
        pass

    def chatGrupal():
        pass

    async def start(self, event):
        self.send_presence()
        self.get_roster()

        print("\nBienvenido al programa, " + self.jid)
        sigue = True
        while sigue == True:
            opc2 =  int(input("\nIngrese una opcion:\n1. Mostrar Usuarios \n2. Agregar Contacto \n3. Mostrar Usuario Especifico \n4. Mensaje de Presencia \n5. Mensaje Privado \n6. Mensaje Grupal\n7. Log out \n"))
            if opc2 == 1:
                #Mostrar Usuarios
                await self.getUsers()
            elif opc2 == 2:
                #Agregar Contacto
                self.addContact()
            elif opc2 == 3:
                #Mostrar contacto especifico
                await self.getSpecificUser()
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
