from flask import Flask

from routes.menuPrincipal_routes import menu_principal
from routes.learning_routes import learning
from routes.progress_routes import progress
from routes.profile_routes import profile
from routes.contact_routes import contact
app = Flask(__name__)
app.register_blueprint(menu_principal)
app.register_blueprint(learning)
app.register_blueprint(progress)
app.register_blueprint(profile)
app.register_blueprint(contact)
if __name__ == '__main__':
    app.run(debug=True)
