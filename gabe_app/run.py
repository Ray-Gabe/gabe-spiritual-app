from flask import Flask
from gabe_app.routes.auth_routes import auth_bp
from gabe_app.routes.main_routes import main_bp

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Register routes
app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
