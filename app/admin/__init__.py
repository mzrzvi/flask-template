"""
Admin panel initialization
"""

# pylint: disable=no-member,invalid-name, too-many-locals
from flask_admin import Admin

from app import app
from app.admin.views import (
    AuthModelView,
    AuthBaseView,
    CustomModelView
)

from app.database import db


def configure_admin(_app):
    """
    Configures admin dashboard
    :param _app:
    :return: Flask Admin instance
    """
    from app.users.models import (
        AdminUser,
        ExampleUser
    )

    from app.resources.models import (
        ResourceA,
        ResourceB
    )

    # Create admin
    _admin = Admin(
        _app,
        'Admin',
        base_template='my_master.html',
        template_mode='bootstrap3'
    )

    _admin.add_view(AuthModelView(AdminUser, db.session))
    _admin.add_view(CustomModelView(ExampleUser, db.session))

    _admin.add_view(AuthModelView(ResourceA, db.session))
    _admin.add_view(AuthModelView(ResourceB, db.session))

    return _admin


admin = configure_admin(app)
