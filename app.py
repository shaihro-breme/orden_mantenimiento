import csv, os
from flask import Flask, render_template, request, jsonify, send_file
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import openpyxl
from datetime import date
import io

app = Flask(__name__)
ARCHIVO_CSV = "datos/ordenes.csv"
CAMPOS = ["codigo_orden", "nombre_orden", "prioridad", "fecha_creacion", "requerido_por",
          "fecha_aprobacion", "equipo", "codigo_equipo", "tipo_mantenimiento", "descripcion",
          "fecha_inicio", "fecha_finalizacion", "cuadrilla", "personal_asignado", "supervisor",
          "insumo", "codigo_insumo", "epp", "ast", "responsable", "autorizacion", "comentarios"]

def generar_codigo_orden():
    if not os.path.exists(ARCHIVO_CSV):
        return "OM-001"
    with open(ARCHIVO_CSV, "r", encoding="utf-8") as f:
        filas = list(csv.reader(f))
        return "OM-" + str(len(filas)).zfill(3)

def leer_ordenes():
    if not os.path.exists(ARCHIVO_CSV):
        return []
    with open(ARCHIVO_CSV, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/ordenes", methods=["GET"])
def get_ordenes():
    ordenes = leer_ordenes()
    busqueda = request.args.get("busqueda", "").lower()
    if busqueda:
        ordenes = [o for o in ordenes if busqueda in o["codigo_orden"].lower() or busqueda in o["nombre_orden"].lower()]
    return jsonify(ordenes)

@app.route("/api/ordenes", methods=["POST"])
def crear_orden():
    datos = request.json
    datos["codigo_orden"] = generar_codigo_orden()
    datos["fecha_creacion"] = str(date.today())
    archivo_existe = os.path.exists(ARCHIVO_CSV)
    with open(ARCHIVO_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CAMPOS)
        if not archivo_existe:
            writer.writeheader()
        writer.writerow(datos)
    return jsonify({"mensaje": f"Orden {datos['codigo_orden']} creada correctamente", "codigo": datos["codigo_orden"]})

@app.route("/api/ordenes/<codigo>", methods=["PUT"])
def editar_orden(codigo):
    ordenes = leer_ordenes()
    datos = request.json
    for i, o in enumerate(ordenes):
        if o["codigo_orden"] == codigo:
            datos["codigo_orden"] = codigo
            datos["fecha_creacion"] = o["fecha_creacion"]
            ordenes[i] = datos
            break
    with open(ARCHIVO_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CAMPOS)
        writer.writeheader()
        writer.writerows(ordenes)
    return jsonify({"mensaje": "Orden actualizada correctamente"})

@app.route("/api/ordenes/<codigo>", methods=["DELETE"])
def eliminar_orden(codigo):
    ordenes = leer_ordenes()
    ordenes = [o for o in ordenes if o["codigo_orden"] != codigo]
    with open(ARCHIVO_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CAMPOS)
        writer.writeheader()
        writer.writerows(ordenes)
    return jsonify({"mensaje": "Orden eliminada correctamente"})

@app.route("/api/exportar/excel")
def exportar_excel():
    ordenes = leer_ordenes()
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Ordenes"
    if ordenes:
        ws.append(list(ordenes[0].keys()))
        for o in ordenes:
            ws.append(list(o.values()))
    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return send_file(buf, download_name="ordenes.xlsx", as_attachment=True, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

@app.route("/api/exportar/pdf/<codigo>")
def exportar_pdf(codigo):
    ordenes = leer_ordenes()
    orden = next((o for o in ordenes if o["codigo_orden"] == codigo), None)
    if not orden:
        return "Orden no encontrada", 404
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    ancho, alto = A4
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, alto - 50, f"Orden de Trabajo - {orden['codigo_orden']}")
    c.setFont("Helvetica", 11)
    etiquetas = {
        "nombre_orden": "Nombre", "prioridad": "Prioridad", "fecha_creacion": "Fecha de Creacion",
        "requerido_por": "Requerido por", "fecha_aprobacion": "Fecha de Aprobacion",
        "equipo": "Equipo", "codigo_equipo": "Codigo del Equipo", "tipo_mantenimiento": "Tipo de Mantenimiento",
        "descripcion": "Descripcion", "fecha_inicio": "Fecha de Inicio", "fecha_finalizacion": "Fecha de Finalizacion",
        "cuadrilla": "Cuadrilla", "personal_asignado": "Personal Asignado", "supervisor": "Supervisor",
        "insumo": "Insumo", "codigo_insumo": "Codigo del Insumo", "epp": "EPP", "ast": "AST",
        "responsable": "Responsable", "autorizacion": "Autorizacion", "comentarios": "Comentarios"
    }
    y = alto - 90
    for campo, etiqueta in etiquetas.items():
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, f"{etiqueta}:")
        c.setFont("Helvetica", 10)
        c.drawString(200, y, str(orden.get(campo, "")))
        y -= 22
        if y < 50:
            c.showPage()
            y = alto - 50
    c.save()
    buf.seek(0)
    return send_file(buf, download_name=f"orden_{codigo}.pdf", as_attachment=True, mimetype="application/pdf")

PLAN_CSV = "datos/plan_anual_de_mantenimiento_plantilla.csv"

@app.route("/api/plan", methods=["GET"])
def get_plan():
    if not os.path.exists(PLAN_CSV):
        return jsonify({"encabezado1": [], "encabezado2": [], "filas": []})
    with open(PLAN_CSV, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        filas = list(reader)
    return jsonify({
        "encabezado1": filas[0] if len(filas) > 0 else [],
        "encabezado2": filas[1] if len(filas) > 1 else [],
        "filas": filas[2:] if len(filas) > 2 else []
    })

@app.route("/api/plan", methods=["POST"])
def guardar_plan():
    datos = request.json
    encabezado1 = datos.get("encabezado1", [])
    encabezado2 = datos.get("encabezado2", [])
    filas = datos.get("filas", [])
    os.makedirs("datos", exist_ok=True)
    with open(PLAN_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(encabezado1)
        writer.writerow(encabezado2)
        writer.writerows(filas)
    return jsonify({"mensaje": "Plan guardado correctamente"})

@app.route("/api/plan/equipos")
def get_equipos():
    if not os.path.exists(PLAN_CSV):
        return jsonify([])
    with open(PLAN_CSV, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # salta encabezado 1
        next(reader)  # salta encabezado 2
        equipos = []
        for fila in reader:
            if fila and fila[0].strip():
                equipos.append(fila[0].strip())
    return jsonify(equipos)

@app.route("/api/plan/tarea")
def get_tarea():
    equipo = request.args.get("equipo", "")
    frecuencia = request.args.get("frecuencia", "")
    frecuencias = {
        "Semanal": 1,
        "Mensual": 2,
        "Trimestral": 4,
        "Semestral": 6,
        "Anual": 8
    }
    col = frecuencias.get(frecuencia)
    if not col:
        return jsonify({"descripcion": "", "tipo": ""})
    if not os.path.exists(PLAN_CSV):
        return jsonify({"descripcion": "", "tipo": ""})
    with open(PLAN_CSV, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        next(reader)
        for fila in reader:
            if fila and fila[0].strip() == equipo:
                descripcion = fila[col] if len(fila) > col else ""
                tipo = fila[col + 1] if len(fila) > col + 1 else ""
                return jsonify({"descripcion": descripcion, "tipo": tipo})
    return jsonify({"descripcion": "", "tipo": ""})

if __name__ == "__main__":
    os.makedirs("datos", exist_ok=True)
    app.run(host="0.0.0.0", port=6969, debug=True)