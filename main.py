import sqlite3, numpy
import re
import pandas as pd

# Abrir el csv y eliminar una columna bug
df = pd.read_csv("autos.csv", usecols=["Cliente", "Auto", "Trabajo", "Kilometraje", "Fecha", "Patente"])


# Dar formato a la fecha


# Dar formato al kilometraje

df.loc[pd.isnull(df["Kilometraje"]), "Kilometraje"] = "0" # Transforma los valores nulos o vacíos en el csv, a "0"

for i in range(len(df["Kilometraje"])): # Este bucle itera por todos los valores de la columna de Kilometraje, utilizando regex,
    if df["Kilometraje"][i] == "0": continue # elimina los "." y el string "km" y sus variaciones
    df["Kilometraje"][i] = re.sub("\.|KM|km|Km|\?", "", df["Kilometraje"][i])

df["Kilometraje"] = pd.to_numeric(df["Kilometraje"]) # Transformar la columna al tipo int

# Dar formato al auto
df.loc[pd.isnull(df["Auto"]), "Auto"] = "Desconocido"

# Dar formato al cliente
df.loc[pd.isnull(df["Cliente"]), "Cliente"] = "Desconocido"

# Dar formato al trabajo
df.loc[pd.isnull(df["Trabajo"]), "Trabajo"] = "Desconocido"

# Dar formato a la patente
df.loc[pd.isnull(df["Patente"]), "Patente"] = "Desconocida"

print(type(df["Fecha"][0]))



# Conexión a la base de datos
# conn = sqlite3.connect("autos")
# cur = conn.cursor()
# cur.execute("DELETE FROM clientes WHERE true")
# conn.commit()
# cur.close()