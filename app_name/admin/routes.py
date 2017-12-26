"""
Routes for admin dashboard
"""

from flask import redirect, render_template

from app_name import app
from app_name.util.exceptions import protect_500


@app.route('/')
@protect_500
def index():
    """
    Redirects user to admin panel
    :return:
    """
    return redirect('admin/')


@app.route('/admin')
@protect_500
def admin():
    """
    Renders admin view
    :return:
    """
    return render_template('admin/index.html')
