from flask import Flask

from routes.forms import forms_bp
from routes.patients import patients_bp
from routes.practitioners import practitioners_bp
from routes.search import search_bp
from routes.files import files_bp
from routes.analytics import analytics_bp
from routes.settings_acc import settings_bp
from routes.profile import profile_bp
from routes.logout import logout_bp

# New ones
from routes.count import count_bp
from routes.current import current_bp
from routes.all_routes import all_routes_bp

app = Flask(__name__)

# Register all blueprints
app.register_blueprint(forms_bp)
app.register_blueprint(patients_bp)
app.register_blueprint(practitioners_bp)
app.register_blueprint(search_bp)
app.register_blueprint(files_bp)
app.register_blueprint(analytics_bp)
app.register_blueprint(settings_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(logout_bp)
app.register_blueprint(count_bp)
app.register_blueprint(current_bp)
app.register_blueprint(all_routes_bp)

if __name__ == '__main__':
    app.run(debug=True)
