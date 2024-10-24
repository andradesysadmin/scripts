from flask import Flask, request, jsonify
import subprocess


'''

API que ultilizo para desligar remotamente computadores windows


'''


app = Flask(__name__)

@app.route('/shutdown', methods=['POST'])
def shutdown():
    try:
        # Comando para desligar a máquina Windows
        subprocess.run(['shutdown', '/s', '/t', '0'], check=True)
        return jsonify({"status": "success", "message": "Shutdown initiated"}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/restart', methods=['POST'])
def restart():
    try:
        # Comando para reiniciar a máquina Windows
        subprocess.run(['shutdown', '/r', '/t', '0'], check=True)
        return jsonify({"status": "success", "message": "Restart initiated"}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9050)
