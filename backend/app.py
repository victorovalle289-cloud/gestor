from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql
import bcrypt
from flasgger import Swagger

app = Flask(__name__)
CORS(app)
swagger = Swagger(app)

# Configuración centralizada de la base de datos
DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = "NuevaClave_2026!"  # Tu contraseña de MySQL actualizada
DB_NAME = "gestor_contrasena"


def conectar():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        charset="utf8mb4",
    )


@app.route("/", methods=["GET"])
def consulta_general():
    try:
        conn = conectar()
        cur = conn.cursor()
        cur.execute("SELECT * FROM baul")
        datos = cur.fetchall()
        data = []
        for row in datos:
            data.append(
                {
                    "id_baul": row[0],
                    "Plataforma": row[1],
                    "usuario": row[2],
                    "clave": row[3],
                }
            )
        cur.close()
        conn.close()
        return jsonify({"baul": data, "mensaje": "Baúl de contraseñas"})
    except Exception as ex:
        print("Error en consulta_general:", ex)
        return jsonify({"mensaje": "Error de conexión a la base de datos"}), 500


@app.route("/consulta_individual/<codigo>", methods=["GET"])
def consulta_individual(codigo):
    try:
        conn = conectar()
        cur = conn.cursor()
        cur.execute("SELECT * FROM baul WHERE id_baul = %s", (codigo,))
        datos = cur.fetchone()
        cur.close()
        conn.close()
        if datos:
            dato = {
                "id_baul": datos[0],
                "Plataforma": datos[1],
                "usuario": datos[2],
                "clave": datos[3],
            }
            return jsonify({"baul": dato, "mensaje": "Registro encontrado"})
        return jsonify({"mensaje": "Registro no encontrado"}), 404
    except Exception as ex:
        print("Error en consulta_individual:", ex)
        return jsonify({"mensaje": "Error"}), 500


@app.route("/registro/", methods=["POST"])
def registro():
    try:
        if request.is_json:
            data = request.get_json() or {}
        else:
            data = request.form

        plataforma = data.get("plataforma")
        usuario = data.get("usuario")
        clave_raw = data.get("clave")

        if not plataforma or not usuario or not clave_raw:
            return jsonify({"mensaje": "Faltan campos obligatorios"}), 400

        clave = bcrypt.hashpw(clave_raw.encode("utf-8"), bcrypt.gensalt()).decode(
            "utf-8"
        )

        conn = conectar()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO baul (plataforma, usuario, clave) VALUES (%s, %s, %s)",
            (plataforma, usuario, clave),
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"mensaje": "Registro agregado"})
    except Exception as ex:
        print("Error en registro:", ex)
        return jsonify({"mensaje": "Error"}), 500


@app.route("/eliminar/<codigo>", methods=["DELETE"])
def eliminar(codigo):
    try:
        conn = conectar()
        cur = conn.cursor()
        cur.execute("DELETE FROM baul WHERE id_baul = %s", (codigo,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"mensaje": "Eliminado"})
    except Exception as ex:
        print("Error en eliminar:", ex)
        return jsonify({"mensaje": "Error"}), 500


@app.route("/actualizar/<codigo>", methods=["PUT", "POST"])
def actualizar(codigo):
    try:
        if request.is_json:
            data = request.get_json() or {}
        else:
            data = request.form

        plataforma = data.get("plataforma")
        usuario = data.get("usuario")
        clave_raw = data.get("clave")

        if not plataforma or not usuario or not clave_raw:
            return jsonify({"mensaje": "Faltan campos obligatorios"}), 400

        clave = bcrypt.hashpw(clave_raw.encode("utf-8"), bcrypt.gensalt()).decode(
            "utf-8"
        )

        conn = conectar()
        cur = conn.cursor()
        cur.execute(
            "UPDATE baul SET plataforma = %s, usuario = %s, clave = %s WHERE id_baul = %s",
            (plataforma, usuario, clave, codigo),
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"mensaje": "Registro actualizado"})
    except Exception as ex:
        print("Error en actualizar:", ex)
        return jsonify({"mensaje": "Error"}), 500


if __name__ == "__main__":
    app.run(debug=True)