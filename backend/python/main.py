import sqlite3
import re
import pandas as pd
pd.options.mode.chained_assignment = None

# Conexión a la base de datos

conn = sqlite3.connect("db_autos")
cur = conn.cursor()
cur.executescript("""
    DROP TABLE IF EXISTS Cliente;
    DROP TABLE IF EXISTS Auto;
    DROP TABLE IF EXISTS Auto_Cliente;
    DROP TABLE IF EXISTS Reparacion;

    CREATE TABLE Cliente (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        cliente TEXT UNIQUE
    );
    CREATE TABLE Auto (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        modelo TEXT NOT NULL UNIQUE
    )
""")
cur.executescript("""
    DROP TABLE IF EXISTS Auto_Cliente;
    CREATE TABLE Auto_Cliente (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        cliente_id INTEGER,
        auto_id INTEGER,
        patente TEXT,
        UNIQUE (cliente_id, auto_id, patente)
    );
    CREATE TABLE Reparacion(
        auto_cliente_id INTEGER,
        fecha TEXT,
        kilometraje INTEGER,
        trabajo TEXT,
        UNIQUE (auto_cliente_id, fecha, kilometraje, trabajo)
    );
""")
conn.commit()

# Abrir el csv y eliminar una columna bug
df = pd.read_csv("Autos - Hoja 1.csv", usecols=["Cliente", "Auto", "Trabajo", "Kilometraje", "Fecha", "Patente"])

# Dar formato a la fecha ????

# REVISA ESTO PAPA QUE ONDA CON EL VALOR TRUCHO DE LA FECHA MEDIA PILA 
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

df.loc[df["Fecha"].str.contains("\?|Km", na=False).values, "Fecha"] = "desconocida"
df.loc[pd.isnull(df["Fecha"]), "Fecha"] = "desconocida"
# df["Fecha"] = pd.to_datetime(df["Fecha"], dayfirst=True)

# Dar formato al kilometraje
df.loc[pd.isnull(df["Kilometraje"]), "Kilometraje"] = "0" # Transforma los valores nulos o vacíos en el csv, a "0"

# Dar formato a la patente
df.loc[pd.isnull(df["Patente"]), "Patente"] = "desconocida"
df["Patente"] = df["Patente"].str.lower()


# Dar formato al auto
df.loc[pd.isnull(df["Auto"]), "Auto"] = "desconocido"
df["Auto"] = df["Auto"].str.lower()


# Dar formato al cliente
df.loc[pd.isnull(df["Cliente"]), "Cliente"] = "desconocido"
df["Cliente"] = df["Cliente"].str.lower()

# Dar formato al trabajo
df.loc[pd.isnull(df["Trabajo"]), "Trabajo"] = "desconocido"

# Iteramos por el frame, elimina el string "km" y sus variaciones
# Reemplaza los espacios " " en las patente por "-"

def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
        (" ", "-"),
    )
    s = s.strip()
    for a, b in replacements:
        s = s.replace(a, b)
    return s

for i in range(len(df)): 
    if df["Kilometraje"][i] != "0":
        df["Kilometraje"][i] = re.sub("\.|KM|km|Km|\?", "", df["Kilometraje"][i])
    if df["Patente"][i] != "desconocida":
        df["Patente"][i] = df["Patente"][i].replace(" ", "-")
    if df["Cliente"][i] != "desconocido":
        df["Cliente"][i] = normalize(df["Cliente"][i])
    if df["Auto"][i] != "desconocido":
        df["Auto"][i] = normalize(df["Auto"][i])



df["Kilometraje"] = pd.to_numeric(df["Kilometraje"]) # Transformar la columna al tipo int

# for i in range(len(df)): 
#     if df["Kilometraje"][i] == "0": continue # elimina los "." y el string "km" y sus variaciones
#     df["Kilometraje"][i] = re.sub("\.|KM|km|Km|\?", "", df["Kilometraje"][i])
#     if df["Patente"][i] == "desconocida" : continue
#     df["Patente"][i] = df["Patente"][i].replace(" ", "-")



conn.commit()

for i in range(len(df)):
    # Si el cliente o el auto no existen los inserta
    cur.execute("""INSERT OR IGNORE INTO Cliente (cliente) VALUES (?)""", (df["Cliente"][i],))
    cur.execute("""INSERT OR IGNORE INTO Auto (modelo) VALUES (?)""", (df["Auto"][i],))
    auto_cliente = df["Auto"][i]
    nombre_cliente = df["Cliente"][i]
    cur.execute("""SELECT Auto.id, Cliente.id FROM Auto, Cliente WHERE Auto.modelo = (?) and Cliente.cliente = (?)""", (auto_cliente, nombre_cliente))
    fila = cur.fetchone()

    cur.execute("INSERT OR IGNORE INTO Auto_Cliente (patente, auto_id, cliente_id) VALUES (?, ?, ?)", (df["Patente"][i], fila[0], fila[1]))

conn.commit()


for i in range(len(df)):
    fecha = str(df["Fecha"][i])
    km = int(df["Kilometraje"][i])
    trabajo = df["Trabajo"][i]
    patente = df["Patente"][i]

    auto_cliente = df["Auto"][i]
    nombre_cliente = df["Cliente"][i]
    cur.execute("""SELECT Auto.id, Cliente.id FROM Auto, Cliente 
    WHERE Auto.modelo = (?) and Cliente.cliente = (?)""", (auto_cliente, nombre_cliente))

    [auto_id, cliente_id] = cur.fetchone()

    cur.execute("""SELECT id FROM Auto_Cliente 
    WHERE patente = (?) AND auto_id = (?) AND cliente_id = (?)""", (patente, auto_id, cliente_id))

    auto_cliente_id = cur.fetchone()[0]

    cur.execute("""INSERT OR IGNORE INTO Reparacion (auto_cliente_id, fecha, kilometraje, trabajo) VALUES (?,?,?,?)""", (auto_cliente_id, fecha, km, trabajo))

conn.commit()
cur.close()