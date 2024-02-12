from flask import Flask, request, jsonify
from flask_cors import CORS
from routing import Routing_conditionals
import traceback  # Import the traceback module for logging

app = Flask(__name__)
CORS(app, origins="*")


@app.route("/process_data", methods=['POST'])
def process_data():
    try:
        data = request.get_json()

        conditions = data['json_input1']
        task = data['json_input2']
        # n = data['bool_input']

        r = Routing_conditionals(0)

        # 0 - это все действия суперюзера
        # 1 - первое действие
        # 2 - последнее

        return jsonify(r.run(conditions=conditions, task=task))

    except Exception as e:
        # Log the traceback for debugging
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
