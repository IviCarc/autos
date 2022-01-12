import sqlite3
import pandas as pd
import sys

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

args = sys.argv
print(args)

for i in range(len(args)):
    if args[i] == args[0]:
        continue
    if args[i] == '--client':
        getByClient(args[i + 1])
