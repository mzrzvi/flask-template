"""
Initializes database
"""

# pylint: disable=invalid-name,no-member

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app_name import app

db = SQLAlchemy(app)

migrate = Migrate(app, db)


def clean_db():
    """
    Initializes clean database
    """
    from app_name.users.models import Role, AdminUser, ExampleUser        # pylint: disable=cyclic-import

    db.reflect()
    db.drop_all()
    db.create_all()

    with app.app_context():
        user_role = Role.query.filter_by(name='user').first()
        if not user_role:
            user_role = Role(name='user')
            db.session.add(user_role)
            db.session.commit()

        super_user_role = Role.query.filter_by(name='superuser').first()
        if not super_user_role:
            super_user_role = Role(name='superuser')
            db.session.add(super_user_role)
            db.session.commit()

        super_user = AdminUser.query.filter_by(email=app.config['SUPERUSER_EMAIL']).first()
        if not super_user:
            super_user = AdminUser(
                first_name='Admin',
                last_name='User',
                email=app.config['SUPERUSER_EMAIL'],
                password=app.config['SUPERUSER_PASSWORD'],
                roles=[user_role, super_user_role],
                is_active=True
            )

            db.session.add(super_user)
            db.session.commit()

        example_user = ExampleUser(
            first_name='John',
            last_name='Smith',
            email='john.smith@example.com',
            password='password',
            roles=[user_role],
            is_active=True
        )

        db.session.add(example_user)
        db.session.commit()
