from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

SERVICES = {
    "restaurant": "http://localhost:5001",
    "order": "http://localhost:5002",
    "payment": "http://localhost:5004",
    "feedback": "http://localhost:5005"
}

@app.route('/api/<service_name>/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def gateway(service_name, path):
    if service_name not in SERVICES:
        return jsonify({"error": "Service not found"}), 404
        
    url = f"{SERVICES[service_name]}/{path}"
    
    try:
        resp = requests.request(
            method=request.method,
            url=url,
            headers={key: value for (key, value) in request.headers if key != 'Host'},
            json=request.get_json() if request.is_json else None,
            params=request.args
        )
        
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items()
                   if name.lower() not in excluded_headers]
                   
        return (resp.content, resp.status_code, headers)
    except requests.exceptions.ConnectionError:
        return jsonify({"error": f"{service_name} service is down"}), 503

if __name__ == '__main__':
    app.run(port=5000, debug=True)
