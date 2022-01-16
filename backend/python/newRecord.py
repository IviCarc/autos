def newRecord(cliente, modelo, trabajo, km, fecha, patente, cur, conn):
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