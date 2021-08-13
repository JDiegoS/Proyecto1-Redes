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
        self.add_event_handler("message", self.message)
        self.add_event_handler("groupchat_message", self.muc_message)

    async def getSpecificUser(self):
        uName = input("Ingrese el usuario: ")
        try:
            self.get_roster()
        except:
            print("Error al obtener lista")
        
        self.send_presence()
        print('Buscando contactos...\n')
        #self.presences_received.wait(5)
        await asyncio.sleep(2)
        
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
        print('Buscando contactos...\n')
        #self.presences_received.wait(5)
        await asyncio.sleep(3)
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
    
    async def addContact(self):
        addName = input("Ingrese el usuario: ")
        addNick = input("Ingrese el apodo para el contacto: ")
        try:
            self.send_presence_subscription(pfrom=self.boundjid.bare, pto=addName, ptype="subscribe", pnick=addNick)
            print("Solicitud enviada correctamente")
            self.get_roster()
            await asyncio.sleep(1)
        except:
            print("Error al agregar contacto")
        

    async def presenceMessage(self):
        show = input("Nuevo show: ")
        status = input("Nuevo status: ")
        self.send_presence(show, status)
        self.get_roster()
        await asyncio.sleep(1)

    async def privateChat(self):
        uName = input("Ingrese el nombre del recipiente: ")
        mssg = input("Ingrese el mensaje: ")
        try:
            self.send_message(mto=uName, mbody=mssg, mtype='chat')
            self.get_roster()
            await asyncio.sleep(1)
            print("Mensaje enviado")
        except:
            print("Error al mandar mensaje")
    
    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            print("\nMensaje recibido de %s:\n   %s\n" % (msg['from'], msg['body']))
    
    async def groupChat(self):
        self.register_plugin('xep_0045') # Multi-User Chat
        self.register_plugin('xep_0199') # XMPP Ping
        opc3 = int(input("\nIngrese una opcion:\n1. Crear chat\n2. Unirse a chat\n"))
        addr = input("Direccion del grupo (ejemplo@conference.alumchat.xyz): ")
        name = input("Nickname: ")
        self.plugin['xep_0045'].join_muc(room=addr, nick=name, pstatus='open', pfrom=self.boundjid.full)
        if opc3 == 1:
            await self.plugin['xep_0045'].set_affiliation(addr, jid = self.boundjid.full, affiliation = 'owner')
            print('\nGrupo creado\n')
        elif opc3 == 2:
            print("Se unio correctamente")
        self.send_presence()
        self.get_roster()
        await asyncio.sleep(1)

    async def sendGroup(self):
        addr = input("Direccion del grupo (ejemplo@conference.alumchat.xyz): ")
        mssg = input("Ingrese el mensaje: ")
        try:
            self.send_message(mto=addr, mbody=mssg, mtype='groupchat')
            self.send_presence()
            self.get_roster()
            await asyncio.sleep(1)
            print("Mensaje enviado")
        except:
            print("Error al mandar mensaje")

    def muc_message(self, msg):
        if msg['type'] == 'groupchat':
            print("\nMensaje recibido del grupo %s\n %s:\n    %s\n" % (msg['mucroom'], msg['mucnick'], msg['body']))

    async def start(self, event):
        self.send_presence()
        self.get_roster()
        await asyncio.sleep(1)

        print("\nBienvenido al programa, " + self.jid)
        sigue = True
        while sigue == True:
            opc2 =  int(input("\nIngrese una opcion:\n1. Mostrar Usuarios \n2. Agregar Contacto \n3. Mostrar Usuario Especifico \n4. Mensaje de Presencia \n5. Enviar Mensaje Privado \n6. Enviar Mensaje Grupal\n7. Crear/Unirse a chat grupal\n8. Log out \n0. Notificaciones (mensajes recibidos, etc)\n"))
            if opc2 == 1:
                #Mostrar Usuarios
                await self.getUsers()
            elif opc2 == 2:
                #Agregar Contacto
                await self.addContact()
            elif opc2 == 3:
                #Mostrar contacto especifico
                await self.getSpecificUser()
            elif opc2 == 4:
                #Mensaje de presencia
                await self.presenceMessage()
            elif opc2 == 5:
                #Mensaje privado
                await self.privateChat()
            elif opc2 == 6:
                await self.sendGroup()
            elif opc2 == 7:
                await self.groupChat()
            elif opc2 == 8:
                print("Hasta luego!")
                self.disconnect()
                sigue = False
            elif opc2 == 0:
                self.send_presence()
                self.get_roster()
                await asyncio.sleep(1)
