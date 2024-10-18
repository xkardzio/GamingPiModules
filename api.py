from modules import Service, KeyBinderService, get_function_result
from flask import Flask, request, jsonify, render_template

apiService = Service(base_url="/launcher-api", template="base.html")
kb = KeyBinderService()

app = Flask(__name__)

@app.route(f'{apiService.base_url}/{kb.base_url}', methods=["GET"])
def KeyBinder_page():
    return render_template(f'{kb.base_url}/{kb.template}')

@app.route(f"{apiService.base_url}/{kb.base_url}/config", methods=["POST"])
def load_config():
    config = request.json
    return get_function_result(kb.load_config(config))

@app.route(f"{apiService.base_url}/{kb.base_url}/config", methods=["GET"])
def get_config():
    config = kb.get_config()
    return get_function_result(kb.get_config())

@app.route(f"{apiService.base_url}/{kb.base_url}/profile", methods=["POST"])
def change_profile():
    kb.profile = request.json
    return get_function_result(kb.profile)

@app.route(f"{apiService.base_url}/{kb.base_url}/profile", methods=["GET"])
def get_profile():
    return get_function_result(kb.profile)

@app.route(f"{apiService.base_url}/", methods=["GET"])
@app.route(f"/", methods=["GET"])
def API_page():
    return render_template(apiService.template)



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
