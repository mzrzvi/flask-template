"""
All user models
"""

# pylint: disable=no-member,invalid-name,super-init-not-called,too-few-public-methods,too-many-instance-attributes

import uuid
from datetime import datetime

from flask_security import UserMixin, RoleMixin
from flask_security.utils import hash_password, verify_password

from app.database import db

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Text, db.ForeignKey('base_user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)


class Role(db.Model, RoleMixin):
    """
    Roles used for AdminUsers
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True)
    description = db.Column(db.Text)

    def __str__(self):
        return self.name


class BaseUser(db.Model, UserMixin):
    """
    User superclass to inherit auth token function
    """
    id = db.Column(db.Text, primary_key=True)
    type = db.Column(db.Text)

    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    phone_number = db.Column(db.Text, unique=True)

    active = db.Column(db.Boolean)
    facebook_user_id = db.Column(db.Text)
    facebook_access_token = db.Column(db.Text)

    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    confirmed_at = db.Column(db.DateTime)

    last_login_at = db.Column(db.DateTime)
    current_login_at = db.Column(db.DateTime)
    last_login_ip = db.Column(db.Text)
    current_login_ip = db.Column(db.Text)
    login_count = db.Column(db.Integer)

    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users'),
                            cascade="all,delete")

    __mapper_args__ = {
        'polymorphic_identity': 'base_user',
        'polymorphic_on': type
    }

    def __init__(self, **data):
        self.id = str(uuid.uuid4())
        self.first_name = data.get('first_name', '')
        self.last_name = data.get('last_name', '')
        self.active = data.get('is_active', True)
        self.email = data.get('email', '')
        self.password = hash_password(data.get('password', ''))

        self.facebook_user_id = data.get('facebook_user_id')
        self.facebook_access_token = data.get('facebook_access_token')

        self.created_at = datetime.now()

    def change_password(self, old_password, new_password):
        """
        Changes the user's password, hashes, saves and returns True
        If old password is incorrect returns False
        :return: True if password was successfully changed else False
        """
        if not verify_password(old_password, self.password):
            return False

        self.password = hash_password(new_password)

        db.session.commit()

        return True

    def to_dict(self):
        """
        Serializes user's data into dictionary for API response
        :return:
        """
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone_number': self.phone_number,
            'type': self.type
        }

    def public_dict(self):
        """
        Serialize user's data into dictionary to be exposed publicly
        :return:
        """
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'type': self.type
        }


class AdminUser(BaseUser):
    """
    For users of the admin dashboard
    """
    id = db.Column(db.Text, db.ForeignKey('base_user.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'admin',
    }

    def __str__(self):
        return 'Admin: {first_name} {last_name}'.format(first_name=self.first_name,
                                                        last_name=self.last_name)


class ExampleUser(BaseUser):
    """
    Example user inheriting from BaseUser class above
    Owns many Resource A's while a Resource A is only associated with one ExampleUser
    """
    id = db.Column(db.Text, db.ForeignKey('base_user.id'), primary_key=True)

    resource_a_set = db.relationship('ResourceA', backref='owner', lazy=True)

    __mapper_args__ = {
        'polymorphic_identity': 'example_user',
    }

    def __init__(self, **data):
        super(ExampleUser, self).__init__(**data)

    def __str__(self):
        return 'Example User: {first_name} {last_name}'.format(first_name=self.first_name,
                                                               last_name=self.last_name)
