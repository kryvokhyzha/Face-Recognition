from flask import render_template
from app import app


@app.errorhandler(404)
def not_found_error(error):
    return render_template('/errors/404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    # db.session.rollback()
    return render_template('/errors/500.html'), 500


app.register_error_handler(404, not_found_error)
app.register_error_handler(500, internal_error)
