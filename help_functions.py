def helper():
    print("Uso: 'script <operacion> [argumentos]'")
    print("Operaciones:\n  {-h --help}\n  {-c --client}\n  {-n --new}\n  {-s --search}" )
    print("Para información más específica vea 'script <operacion> --help'")

def newRecord_help():
    print("Uso: 'script {-n --nuevo} [cliente modelo trabajo km fecha patente]'")
    print("Todos los argumentos deben estar presentes, de no conocerse, ingrese 'desconocido'")
    print("Cada argumento debe estar separado por un espacio\nEn caso de que un argumento colleve mas de una palabra, encerrarlo dentro de comillas")
    print("Argumentos:")
    print("  cliente: nombre del cliente, todo en minusculas")
    print("  modelo: modelo del auto, todo en minusculas")
    print("  trabajo: trabajo realizado al auto")
    print("  km: kilometraje del auto, numero entero positivo sin espacios entre digitos ni letras")
    print("  fecha: fecha de realizado el trabajo en formato DIA/MES/AÑO, ej 10/9/2021")
    print("  patente: patente del auto, se ingresa entre comillas respetando los espacios, sea del tipo 'LL NNN LLL' o 'LLL NNN'")

def client_help():
    print("Uso: 'script {-c --cliente} [cliente]'")
    print("Devuelve todas las reparaciones del cliente ingresado")
    print("Si el cliente lleva mas de una palabra, ingresarlo entre comillas")

def list_help():
    print("Uso: 'script {-l --lista}'")
    print("Devuelve todos los clientes con su ID")

def getByPatent_help():
    print("Uso: 'script {-p --patente} [patente]'")
    print("Devuelve todas las reparaciones del auto con la patente ingresada")
    print("La patente se ingresara entre comillas respetando los espacios")

def search_help():
    print("Uso:'script {-b --buscar} [expresion]'")
    print("Devuelve todas las coincidencias de clientes con respecto a la expresion")
    print("La expresion es una regex cualquiera, debe ingresarse sin espacios o entre comillas")
