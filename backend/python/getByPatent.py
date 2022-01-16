def getByPatent(patente, cur, conn):
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
