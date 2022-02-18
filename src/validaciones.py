# Validar el código (si es numérico,mayor a 0 y menor a 6 caracteres).
def validar_codigo(codigo: str) -> bool:
    return (codigo.isnumeric() and len(codigo) >= 1 and len(codigo) <= 6)

#Validar el nombre (si es un texto sin espacios en blanco de entre 1 y 100 caracteres).
def validar_nombre(nombre: str) -> bool:
    nombre = nombre.strip()
    return (len(nombre) > 0 and len(nombre) <= 30)

# Validar que los créditos estén entre 1 y 20.
def validar_creditos(creditos: str) -> bool:
    creditos_texto = str(creditos)
    if creditos_texto.isnumeric():
        return (creditos >= 1 and creditos <= 20)
    else:
        return False

    
#Validar el nombre del profesor (si es un texto sin espacios en blanco de entre 1 y 50 caracteres).
def validar_profesor(nombre: str) -> bool:
    nombre = nombre.strip()
    return (len(nombre) > 0 and len(nombre) <= 50)


#Validar el paralelo (si es un texto sin espacios en blanco de entre 0 y 1 caracteres).
def validar_paralelo(nombre: str) -> bool:
    nombre = nombre.strip()
    return (len(nombre) > 0 and len(nombre) <= 1)

#Validar el estado del curso (si es un texto sin espacios en blanco de entre 1 y 30 caracteres).
def validar_estado(nombre: str) -> bool:
    nombre = nombre.strip()
    return (len(nombre) > 0 and len(nombre) <= 30)