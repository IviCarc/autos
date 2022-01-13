#!/usr/bin/env python3

import sqlite3
import pandas as pd
import sys
import re
from help_functions import *

conn = sqlite3.connect("/home/ivan/Documents/programacion/autos/db_autos")
cur = conn.cursor()

def getByClient(client):
    cur.execute("""SELECT id FROM Cliente WHERE cliente = (?)""", (client,))

    client_id = cur.fetchone()[0]

    print('ID DEL CLIENTE',client_id)

    cur.execute("""
    SELECT id, auto_id ,patente
    FROM Auto_Cliente 
    WHERE cliente_id = (?)
    """, (client_id,))

    autosCliente = cur.fetchall()

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
            fila = f'{client} | {modelo} | {trabajo} | {km} Km | {fecha} | {patente}'
            print(fila)


def listClients():
    cur.execute("""
        SELECT *
        FROM Cliente
    """)
    clients = cur.fetchall()
    for client in clients: print(f'{client[0]}, {client[1]}')

def regexp(expr, item):
    reg = re.compile(expr)
    return reg.search(item) is not None

conn.create_function("REGEXP", 2, regexp)

def searchClients(regex):
    
    cur.execute("""
        SELECT *
        FROM Cliente
        WHERE cliente REGEXP (?)
    """, (regex, ))
    clients = cur.fetchall()
    if not clients: print('No matches')
    else:
        for client in clients: print(f'{client[0]}, {client[1]}')


def getByPatent(patente):
    cur.execute("""
        SELECT *
        FROM Auto_Cliente
        WHERE patente = (?)
    """, (patente, ))
    auto = cur.fetchall()[0]

    print(auto)

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

    for reparacion in reparaciones:
        fecha = reparacion[0]
        km = reparacion[1]
        trabajo = reparacion[2]

        fila = f'{cliente} | {modelo} | {trabajo} | {km}Km | {fecha} | {patente}'

        print(fila)

def newRecord(cliente, modelo, trabajo, km, fecha, patente):
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
            print("Revise los valores ingresados como 'patente', 'cliente' y 'modelo'")
            return
        conn.commit()
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
    print("Operación realizada exitosamente")
    


args = sys.argv

for i in range(len(args)):
    if args[i] == args[0]:
        continue
    if args[i] == '--cliente' or args[i] == '-c':
        if args[i + 1] == '--help':
            client_help()
            break
        getByClient(args[i + 1])
    if args[i] == '-l' or args[i] == '--lista':
        try:
            if args[i + 1] == '--help':
                list_help()
                break
        except:
            listClients()
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