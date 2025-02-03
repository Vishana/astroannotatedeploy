from flask import Flask, request, jsonify
from ai_labeling import generate_label  # Import the function from generate_label.py

app = Flask(__name__)

@app.route('/generate_image_label', methods=['POST'])
def generate_image_label():
    try:
        # Get image file path from the request
        image_path = request.json.get("image_path")

        if not image_path:
            return jsonify({"error": "No image path provided"}), 400

        # Call the generate_label function
        label = generate_label(image_path)

        return jsonify({"label": label})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)