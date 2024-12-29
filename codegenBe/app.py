from flask import Flask
from flask_cors import CORS
from routes import generate_code_route, run_code_route

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for the app (allow all domains by default)
CORS(app)

# Register routes
app.register_blueprint(generate_code_route)
app.register_blueprint(run_code_route)

if __name__ == '__main__':
    app.run(debug=True)
