#!/usr/bin/env python3

import sqlite3
import sys
import re
from help_functions import *
import json


# !!!! IMPORTANTE !!!!
# EN CASO DE HABER UN ERROR, SE ENVIARÁ UN CÓDIGO, SU SIGNIFICADO ESTARÁ INDICADO EN LA FUNCIÓN


conn = sqlite3.connect("/home/ivan/Documents/programacion/autos/backend/python/db_autos")
cur = conn.cursor()

def getByClient(client):

    # App nos indica si estamos llamando al script desde terminal o desde la app
    # La diferencia radica en el formato del print, cuando llamemos desde la app necesitamos un JSON

    app = False
    try:
        app = args[3]
    except:
        pass
    cur.execute("""SELECT id FROM Cliente WHERE cliente = (?)""", (client,))

    try:
        client_id = cur.fetchone()[0]
    except:
        if not app:
            print(f"'{client[0].upper() + client[1:]}' no existe")
        else:
            print('0') #'0' indica que el cliente no existe
        return

    cur.execute("""
    SELECT id, auto_id ,patente
    FROM Auto_Cliente 
    WHERE cliente_id = (?)
    """, (client_id,))

    autosCliente = cur.fetchall()

    repArray = []

    for auto in autosCliente:
        patente = auto[2]

        # Conseguir el modelo del auto
        auto_id = auto[1]

        cur.execute("""
            SELECT modelo 
            FROM Auto
            WHERE id = (?)
        """, (auto_id,))

        modelo = cur.fetchone()[0]

        cur.execute("""
            SELECT *
            FROM Reparacion 
            WHERE auto_cliente_id = (?)
        """, (auto[0],)) #id del auto

        reparaciones = cur.fetchall()

        for reparacion in reparaciones:
            fecha = reparacion[1]
            km = reparacion[2]
            trabajo = reparacion[3]

            if not app:
                # Formato para terminal
                fila = f'{client} | {modelo} | {trabajo} | {km} Km | {fecha} | {patente}' 
                print(fila)
            else:
                # JSON usado por la app
                repArray.append({"cliente":client,"modelo":modelo, "trabajo":trabajo,
                "km": km, "fecha": fecha, "patente":patente})
    if app:
        jsonData = json.dumps(repArray)
        print(jsonData)



def listClients():
    app = False
    try:
        app = args[2]
    except:
        pass
    
    cur.execute("""
        SELECT *
        FROM Cliente
    """)
    clients = cur.fetchall()

    clientsArr = []

    for client in clients: 
        if not app:
            print(f'{client[0]}, {client[1]}')
        else:
            clientsArr.append({"Cliente" : client[1]})
    if app: print(json.dumps(clientsArr))

def listPatents():
    app = False
    try:
        app = args[2]
    except:
        pass
    
    cur.execute("""
        SELECT patente
        FROM Auto_Cliente
    """)
    
    patentes = cur.fetchall()

    patentsArr = []

    for patente in patentes: 
        if not app:
            print(f'{patente[0]}')
        else:
            patentsArr.append({"patente" : patente[0]})
    if app: print(json.dumps(patentsArr))




def regexp(expr, item):
    reg = re.compile(expr)
    return reg.search(item) is not None

conn.create_function("REGEXP", 2, regexp)

def searchClients(regex):
    # App nos indica si estamos llamando al script desde terminal o desde la app
    # La diferencia radica en el formato del print, cuando llamemos desde la app necesitamos un JSON

    app = False
    try:
        app = args[3]
    except:
        pass


    cur.execute("""
        SELECT *
        FROM Cliente
        WHERE cliente REGEXP (?)
    """, (regex, ))

    clients = cur.fetchall()
    clientsArr = []
    
    if not clieFnts: 
        if not app:
            print('No matches')
        else:
            print('0')
        return
    else:
        for client in clients: 
            if not app:
                print(f'{client[0]}, {client[1]}')
            else: clientsArr.append({"id": client[0], "cliente": client[1]})
    if app:
        print(json.dumps(clientsArr))


def getByPatent(patente):
    # App nos indica si estamos llamando al script desde terminal o desde la app
    # La diferencia radica en el formato del print, cuando llamemos desde la app necesitamos un JSON

    app = False
    try:
        app = args[3]
    except:
        pass

    cur.execute("""
        SELECT *
        FROM Auto_Cliente
        WHERE patente = (?)
    """, (patente, ))
    try:
        auto = cur.fetchall()[0]
    except:
        if not app:
            print(f"'{patente}' no existe")
        else:
            print('0')
        return
    auto_cliente_id = auto[0]
    client_id = auto[1]
    auto_id = auto[2]

    cur.execute("""
        SELECT cliente
        FROM Cliente
        WHERE id = (?);
    """, (client_id, ))

    cliente = cur.fetchone()[0]

    cur.execute("""
        SELECT modelo
        FROM Auto
        WHERE id = (?)
    """, (auto_id, ))

    modelo = cur.fetchone()[0]

    cur.execute("""
        SELECT fecha, kilometraje, trabajo
        FROM Reparacion
        WHERE auto_cliente_id = (?)
    """, (auto_cliente_id, ))

    reparaciones = cur.fetchall()

    repArray = []

    for reparacion in reparaciones:
        fecha = reparacion[0]
        km = reparacion[1]
        trabajo = reparacion[2]

        if not app:
            fila = f'{cliente} | {modelo} | {trabajo} | {km}Km | {fecha} | {patente}'
            print(fila)
        else:
            repArray.append({"cliente":cliente,"modelo":modelo, "trabajo":trabajo,
                "km": km, "fecha": fecha, "patente":patente})
    if app: print(json.dumps(repArray))

def newRecord(cliente, modelo, trabajo, km, fecha, patente):
    app = False
    try:
        app = args[3]
    except:
        pass

    if km.lower() == 'desconocido':
        km = 0
    try:
        km = int(km)
        if km < 0: raise Exception()
    except:
        print('Kilometraje ingresado no válido')
        return
    patente = patente.upper()
    cliente = cliente.lower()
    modelo = modelo.lower()


    # Si el cliente o el modelo del auto no existen en la base de datos, los agregamos
    cur.execute("""
        INSERT OR IGNORE INTO Cliente (cliente) VALUES (?)
    """, (cliente, ))
    cur.execute("""
        INSERT OR IGNORE INTO Auto (modelo) VALUES (?)
    """, (modelo, ))
    conn.commit()

    # Seleccionamos el id del cliente y del modelo del auto
    cur.execute("""
        SELECT Cliente.id, Auto.id
        FROM Cliente, Auto
        WHERE Cliente.cliente = (?) AND Auto.modelo = (?)
    """, (cliente, modelo,))
    [cliente_id, auto_id] = cur.fetchone()

    # Insertamos en la tabla "Auto_Cliente" el los ids previos con su patente.
    # Si los datos son incorrectos, por ejemplo, que la patente se repita con un id distinto 
    # no se agregará

    # Chequeamos si el auto del cliente existe

    cur.execute("""
        SELECT id
        FROM Auto_Cliente
        WHERE cliente_id = (?) 
        AND auto_id = (?) 
        AND patente = (?)
    """, (cliente_id, auto_id, patente))

    auto_cliente_id = cur.fetchone()

    # Esto sucede si el auto no existe
    if not auto_cliente_id:
        # Se crea el auto execpto si los datos son erróneos, ej si se ingresa una patente con un auto al que no le corresponde o ya existe
        try:
            cur.execute("""
            INSERT INTO Auto_Cliente (cliente_id, auto_id, patente)
            VALUES (?, ?, ?)
        """, (cliente_id, auto_id, patente))
        except sqlite3.IntegrityError:

            if not app:
                print("Revise los valores ingresados como 'patente', 'cliente' y 'modelo'")
            else:
                print("1") # 1 CODIGO ERROR
            return
        conn.commit()

        if not app:
            print("Nuevo auto del cliente ingresado en la base de datos")

        cur.execute("""
            SELECT id
            FROM Auto_Cliente
            WHERE cliente_id = (?) 
            AND auto_id = (?) 
            AND patente = (?)
        """, (cliente_id, auto_id, patente))

        auto_cliente_id = cur.fetchone()[0]

    # Insertamos la reparación en la tabla, si la reparación es duplicada, retornamos
    try:
        cur.execute("""
            INSERT  INTO Reparacion (auto_cliente_id, fecha, kilometraje, trabajo)
            VALUES (?, ?, ?, ?)
        """, (auto_cliente_id, fecha, km, trabajo))
        conn.commit()
    except:
        print('Este registro ya existe, revise los datos')
        return
    if not app:
        print("Operación realizada exitosamente")
    else:
        print("0") # EXITO

args = sys.argv

for i in range(len(args)):
    if args[i] == args[0]:
        continue
    if args[i] == '--cliente' or args[i] == '-c':
        if args[i + 1] == '--help':
            client_help()
            break
        getByClient(args[i + 1])
    if args[i] == '-lc' or args[i] == '--lista-clientes':
        try:
            args[i +1]
        except:
            listClients()
            break
        if args[i + 1] == '--help': list_help()
        elif args[i + 1] == 'true': listClients()

    if args[i] == '-lp' or args[i] == '--lista-patentes':
        try:
            args[i +1]
        except:
            listPatents()
            break
        if args[i + 1] == '--help': list_help()
        elif args[i + 1] == 'true': listPatents()

    if args[i] == '--buscar' or args[i] == '-b':
        if args[i + 1] == '--help':
            search_help()
            break
        searchClients(args[i + 1])
    if args[i] == '--patente' or args[i] == '-p':
        if args[i + 1] == '--help':
            getByPatent_help()
            break
        getByPatent(args[i + 1])
    if args[i] == '--nuevo' or args[i] == '-n':
        if args[i + 1] == '--help':
            newRecord_help()
            break
        try:
            newRecord(args[i +1], args[i +2], args[i +3], args[i +4], args[i +5], args[i +6])
        except:
            print("Argumentos inválidos. Escriba '--nuevo --help' para ver la ayuda de esta función")
    if args[i] == '--help':
        helper()
conn.close()