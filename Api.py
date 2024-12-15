from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

def conectar_db():
    conn = sqlite3.connect('recipes.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recetas', methods=['GET'])
def ver_recetas():
    conn = conectar_db()
    c = conn.cursor()
    c.execute("SELECT * FROM recipes")
    recetas = c.fetchall()
    conn.close()
    return jsonify([dict(receta) for receta in recetas])

@app.route('/recetas', methods=['POST'])
def agregar_receta():
    data = request.get_json()
    conn = conectar_db()
    c = conn.cursor()
    c.execute("INSERT INTO recipes (title, ingredients, steps) VALUES (?, ?, ?)",
              (data['title'], data['ingredients'], data['steps']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Receta agregada exitosamente"}), 201

@app.route('/recetas/<int:receta_id>', methods=['PUT'])
def actualizar_receta(receta_id):
    data = request.get_json()
    conn = conectar_db()
    c = conn.cursor()
    c.execute("UPDATE recipes SET title = ?, ingredients = ?, steps = ? WHERE id = ?",
              (data['title'], data['ingredients'], data['steps'], receta_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Receta actualizada exitosamente"})

@app.route('/recetas/<int:receta_id>', methods=['DELETE'])
def eliminar_receta(receta_id):
    conn = conectar_db()
    c = conn.cursor()
    c.execute("DELETE FROM recipes WHERE id = ?", (receta_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Receta eliminada exitosamente"})

@app.route('/recetas/<int:receta_id>', methods=['GET'])
def buscar_receta(receta_id):
    conn = conectar_db()
    c = conn.cursor()
    c.execute("SELECT * FROM recipes WHERE id = ?", (receta_id,))
    receta = c.fetchone()
    conn.close()
    if receta:
        return jsonify(dict(receta))
    return jsonify({"error": "Receta no encontrada"}), 404

if __name__ == '__main__':
    app.run(debug=True)