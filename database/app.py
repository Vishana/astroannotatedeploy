from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import logging

app = Flask(__name__)
CORS(app)

DATABASE = 'astroannotate.db'

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_db_connection():
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        logger.error(f"Database connection failed: {e}")
        return None

@app.route('/api/labels', methods=['GET'])
def get_labels():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    labels = conn.execute('SELECT * FROM image_labels').fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in labels])

@app.route('/api/labels', methods=['POST'])
def add_label():
    try:
        new_label = request.get_json()
    except Exception:
        return jsonify({"error": "Invalid JSON"}), 400

    # Validate input
    required_fields = ['image_url', 'ai_label']
    if not all(field in new_label for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        conn.execute('INSERT INTO image_labels (image_url, ai_label, human_1_score, human_2_score, human_3_score, human_1_comment, human_2_comment, human_3_comment, ai_accuracy) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                     (new_label['image_url'], new_label['ai_label'], new_label['human_1_score'], new_label['human_2_score'], new_label['human_3_score'], new_label['human_1_comment'], new_label['human_2_comment'], new_label['human_3_comment'], new_label['ai_accuracy']))
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Error inserting data: {e}")
        return jsonify({"error": "Failed to insert data"}), 500
    finally:
        conn.close()

    return jsonify(new_label), 201

@app.route('/api/labels/<int:id>', methods=['PUT'])
def update_label(id):
    try:
        updated_label = request.get_json()
    except Exception:
        return jsonify({"error": "Invalid JSON"}), 400

    # Validate input
    required_fields = ['image_url', 'ai_label']
    if not all(field in updated_label for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        conn.execute('UPDATE image_labels SET image_url = ?, ai_label = ?, human_1_score = ?, human_2_score = ?, human_3_score = ?, human_1_comment = ?, human_2_comment = ?, human_3_comment = ?, ai_accuracy = ? WHERE image_id = ?',
                     (updated_label['image_url'], updated_label['ai_label'], updated_label['human_1_score'], updated_label['human_2_score'], updated_label['human_3_score'], updated_label['human_1_comment'], updated_label['human_2_comment'], updated_label['human_3_comment'], updated_label['ai_accuracy'], id))
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Error updating data: {e}")
        return jsonify({"error": "Failed to update data"}), 500
    finally:
        conn.close()

    return jsonify(updated_label)

@app.route('/api/labels/<int:id>', methods=['DELETE'])
def delete_label(id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        conn.execute('DELETE FROM image_labels WHERE image_id = ?', (id,))
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Error deleting data: {e}")
        return jsonify({"error": "Failed to delete data"}), 500
    finally:
        conn.close()

    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
