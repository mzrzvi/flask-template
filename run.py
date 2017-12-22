"""
Run script for application
"""

from app import get_app
from app.database import clean_db

if __name__ == '__main__':
    app = get_app()

    if app.config.get('TESTING') or app.config.get('LOCAL'):
        clean_db()

    app.run(debug=True, host='0.0.0.0', port=app.config.get('PORT'))
