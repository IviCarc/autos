#!/usr/bin/env python

import sqlite3
import pandas as pd
import sys
import re

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
    patente = patente.upper()
    cur.execute("""
        SELECT *
        FROM Auto_Cliente
        WHERE patente = (?)
    """, (patente, ))
    auto = cur.fetchall()[0]

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

    # print(auto)
    # print(cliente)
    # print(modelo)
    # print(fecha, km,trabajo)


args = sys.argv

for i in range(len(args)):
    if args[i] == args[0]:
        continue
    if args[i] == '--client':
        getByClient(args[i + 1])
    if args[i] == '-l':
        listClients()
    if args[i] == '--search':
        searchClients(args[i + 1])
    if args[i] == '--patent':
        getByPatent(args[i + 1])
