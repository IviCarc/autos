def helper():
    print("Uso: 'autos.py <operacion> [argumentos]'")
    print("Operaciones:\n  {-h --help}\n  {-c --client}\n  {-n --new}\n  {-s --search}" )
    print("Para información más específica vea 'autos.py <operacion> --help'")

def newRecord_help():
    print("Uso: 'autos.py {-n --nuevo} [cliente modelo trabajo km fecha patente]'")
    print("Todos los argumentos deben estar presentes, de no conocerse, ingrese 'desconocido'")
    print("Cada argumento debe estar separado por un espacio")
    print("Cuando un argumento requiera mas de una palabra, estas deben separarse por '-'")
    print("Argumentos:")
    print("  cliente: minusculas sin tildes => 'guillermo-garcia'")
    print("  modelo: minusculas sin tildes => 'ford-fiesta'")
    print("  trabajo: entre comillas, formato libre => '\"Distribucion completa con bomba de agua\"'")
    print("  km: numero entero positivo sin espacios entre digitos sin letras => '243640'")
    print("  fecha: DIA/MES/AÑO => '10/9/2021'")
    print("  patente: minusculas => 'jfx-403' => 'ab 203 cb'")

def client_help():
    print("Uso: 'autos.py {-c --cliente} [cliente]'")
    print("Devuelve todas las reparaciones del cliente ingresado")
    print("Si el cliente lleva mas de una palabra, ingresarlo entre comillas")

def list_help():
    print("Uso: 'autos.py {-l --lista}'")
    print("Devuelve todos los clientes con su ID")

def getByPatent_help():
    print("Uso: 'autos.py {-p --patente} [patente]'")
    print("Devuelve todas las reparaciones del auto con la patente ingresada")
    print("La patente se ingresara entre comillas con guiones '-' donde va cada espacio")
    print("Ej => 'autos.py -p jde-001'")

def search_help():
    print("Uso:'autos.py {-b --buscar} [expresion]'")
    print("Devuelve todas las coincidencias de clientes con respecto a la expresion")
    print("La expresion es una regex cualquiera, debe ingresarse sin espacios o entre comillas")
