from flask import Flask, jsonify
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1)

    with app.app_context():
        from app.index import bp as index_bp
        from app.routes import bp as routes_bp

        app.register_blueprint(index_bp, url_prefix="/")
        app.register_blueprint(routes_bp, url_prefix="/api")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)