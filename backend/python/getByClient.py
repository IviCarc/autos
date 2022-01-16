def getByClient(client, cur, conn):

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