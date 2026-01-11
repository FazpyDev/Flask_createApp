def register_routes(app):
    @app.route("/")
    def home():
        return "home"