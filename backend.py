from app.create_app import create_app
from app.routes import socketio
from flask_cors import CORS

app = create_app()
# need to allow for cross origins so that godot can interact with the backend
CORS(app, resources={r"/*": {"origins": "*"}}) # this allows any origin to connect to the rest API, this should be changed if we ever do production

if __name__=='__main__':
    socketio.run(app, host='0.0.0.0', debug=True)  # this automatically handles socket api requests and REST api requests
    