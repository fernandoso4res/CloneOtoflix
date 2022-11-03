from flask import Flask


def create_app():
    from ext import auth, database, swagger, cors
    
    from routes.auth_route import bp as auth_bp
    from routes.subscriptions_route import bp as subscriptions_bp
    from routes.flashcards_route import bp as flashcards_bp
    from routes.users_route import bp as users_bp
    from routes.benefits_club_route import bp as benefits_club_bp
    from routes.certificates_route import bp as certificates_bp
    from routes.questions_route import bp as questions_bp
    from routes.simulated_route import bp as simulated_bp
    from routes.decks_route import bp as decks_bp
    from routes.rankings_route import bp as rankings_bp
    from routes.students_route import bp as students_bp
    from routes.courses_route import bp as courses_bp
    from routes.modules_route import bp as modules_bp

    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    auth.init_app(app)
    database.init_app(app)
    swagger.init_app(app)
    cors.init_app(app)
        

    app.register_blueprint(auth_bp, url_prefix=app.config['URL_PREFIX']+'/auth')
    app.register_blueprint(subscriptions_bp, url_prefix=app.config['URL_PREFIX']+'/subscriptions')
    app.register_blueprint(flashcards_bp, url_prefix=app.config['URL_PREFIX']+'/flashcards')
    app.register_blueprint(users_bp, url_prefix=app.config['URL_PREFIX']+'/users')
    app.register_blueprint(benefits_club_bp, url_prefix=app.config['URL_PREFIX']+'/benefits-club')
    app.register_blueprint(certificates_bp, url_prefix=app.config['URL_PREFIX']+'/certificates')
    app.register_blueprint(questions_bp, url_prefix=app.config['URL_PREFIX']+'/questions')
    app.register_blueprint(simulated_bp, url_prefix=app.config['URL_PREFIX']+'/simulated')
    app.register_blueprint(decks_bp, url_prefix=app.config['URL_PREFIX']+'/decks')
    app.register_blueprint(rankings_bp, url_prefix=app.config['URL_PREFIX']+'/rankings')
    app.register_blueprint(students_bp, url_prefix=app.config['URL_PREFIX']+'/students')
    app.register_blueprint(courses_bp, url_prefix=app.config['URL_PREFIX']+'/courses')
    app.register_blueprint(modules_bp, url_prefix=app.config['URL_PREFIX']+'/modules')

    # print(app.config)
    return app