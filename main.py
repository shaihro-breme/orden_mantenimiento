import csv, os, datetime

def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")

def generar_codigo_orden():
    if not os.path.exists("datos/ordenes.csv"):
        return "OM-001"
    with open("datos/ordenes.csv", "r", encoding="utf-8") as archivo:
        filas = list(csv.reader(archivo))
        numero = len(filas)
        return "OM-" + str(numero).zfill(3)

def ver_orden():
    if not os.path.exists("datos/ordenes.csv"):
        print("No hay ordenes todavia")
        return
    with open("datos/ordenes.csv", "r", encoding="utf-8") as archivo:
        reader = csv.DictReader(archivo)
        for fila in reader:
            print(fila["codigo_orden"], "|", fila["nombre_orden"], "|", fila["fecha_creacion"])

def abrir_orden():
    if not os.path.exists("datos/ordenes.csv"):
        print("No hay ordenes todavia")
        return
    with open("datos/ordenes.csv", "r", encoding="utf-8") as archivo:
        reader = csv.DictReader(archivo)
        ordenes = list(reader)
    for i, fila in enumerate(ordenes):
        print(i + 1, "|", fila["codigo_orden"], "|", fila["nombre_orden"], "|", fila["fecha_creacion"])
    while True:
        try:
            eleccion = int(input("Numero de la orden que desee selecionar:\n"))
            if 1 <= eleccion <=len(ordenes):
                break
            else:
                print("Numero fuera de rango")
        except ValueError:
            print("Ingrese un numero valido")
    orden = ordenes[eleccion - 1]
    print("Codigo de orden: ",orden["codigo_orden"])
    print("nombre: ",orden["nombre_orden"])
    print("Prioridad: ",orden["prioridad"])
    print("Fecha de creacion: ",orden["fecha_creacion"])
    print("Cuenta: ",orden["cuenta"])
    print("Requerido por: ",orden["requerido_por"])
    print("Aprobado Por: ",orden["aprobado_por"])
    print("Fecha de aprobacion: ",orden["fecha_aprobacion"])
    print("Equipo: ",orden["equipo"])
    print("Codigo del equipo: ",orden["codigo_equipo"])
    print("Tipo de mantenimiento: ",orden["tipo_mantenimiento"])
    print("Descripcion: ",orden["descripcion"])
    print("Fecha de inicio: ",orden["fecha_inicio"])
    print("Fecha de finalizacion: ",orden["fecha_finalizacion"])
    print("Fecha de realizacion: ",orden["fecha_realizacion"])
    print("Cuadrilla: ",orden["cuadrilla"])
    print("Personal asignado: ",orden["personal_asignado"])
    print("Supervisor: ",orden["supervisor"])
    print("Seccion: ",orden["seccion"])
    print("Insumo: ",orden["insumo"])
    print("Codigo del insumo: ",orden["codigo_insumo"])
    print("EPP: ",orden["epp"])
    print("AST: ",orden["ast"])
    print("Responsable: ",orden["responsable"])
    print("Autorizacion: ",orden["autorizacion"])
    print("Comentarios: ",orden["comentarios"])

def crear_orden():
    nombre_orden = input("Introduzca el nombre de la orden:\n")
    codigo_orden = generar_codigo_orden()
    prioridad = input("Introduzca la prioridad:\n")
    fecha_creacion = datetime.date.today()
    cuenta = input("Introduzca la cuenta:\n")
    requerido_por = input("Requerido por:\n")
    aprobado_por = input("Aprovado por:\n")
    fecha_aprobacion = input("Fecha de aprovacion:\n")
    equipo = input("Introduzca el equipo:\n")
    codigo_equipo = input("Introduzca el codigo del equipo:\n")
    tipo_mantenimiento = input("Tipo de mantenimiento:\n")
    descripcion = input("Introduzca la descripcion:\n")
    fecha_inicio = input("Introduzca la fecha de inicio:\n")
    fecha_finalizacion = input("Introduzca la fecha de finalizcion:\n")
    fecha_realizacion = input("Introduzca fecha de realizacion:\n")
    cuadrilla = input("Introduzca cuadrilla:\n")
    personal_asignado = input("Introduzca el personal asignado:\n")
    supervisor = input("Introduzca el supervisor:\n")
    seccion = input("Introduzca la seccion:\n")
    insumo = input("Introduzca el insumo:\n")
    codigo_insumo = input("Introduzca el codigo del insumo:\n")
    epp = input("Introduzca el EPP:\n")
    ast = input("AST:SI/NO:\n")
    responsable = input("Introduzca al responsable:\n")
    autorizacion = input("Introduzca la autorizacion:\n")
    comentarios = input("Comentarios:\n")

    archivo_existe = os.path.exists("datos/ordenes.csv")
    with open("datos/ordenes.csv", "a", newline="", encoding="utf-8") as archivo:
        write = csv.writer(archivo)
        if not archivo_existe:
            write.writerow(["codigo_orden", "nombre_orden", "prioridad", "fecha_creacion", "cuenta", "requerido_por", "aprobado_por", "fecha_aprobacion",
                    "equipo", "codigo_equipo", "tipo_mantenimiento", "descripcion", "fecha_inicio", "fecha_finalizacion", "fecha_realizacion",
                    "cuadrilla", "personal_asignado", "supervisor", "seccion", "insumo", "codigo_insumo", "epp", "ast", "responsable", "autorizacion",
                    "comentarios"])
        write.writerow([codigo_orden, nombre_orden, prioridad, fecha_creacion, cuenta, requerido_por, aprobado_por, fecha_aprobacion,
                    equipo, codigo_equipo, tipo_mantenimiento, descripcion, fecha_inicio, fecha_finalizacion, fecha_realizacion,
                    cuadrilla, personal_asignado, supervisor, seccion, insumo, codigo_insumo, epp, ast, responsable, autorizacion,
                    comentarios])
    print(f"Orden {codigo_orden} creada correctamente")

def inicio():
    while True:
        limpiar_pantalla()
        selector = input("Selector\n"
              "[c] Crear Nueva Orden\n"
              "[v] Ver Todas Las Ordenes\n"
              "[a] Abrir Orden Existente\n"
              "[s] Salir\n")

        if selector == "c":
            crear_orden()
        elif selector == "v":
            ver_orden()
        elif selector == "a":
            abrir_orden()
        elif selector == "s":
            exit()

def main():
    os.makedirs("datos", exist_ok=True)
    inicio()

if __name__ == "__main__":
    main()