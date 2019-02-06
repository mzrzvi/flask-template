"""
All user models
"""

# pylint: disable=no-member,invalid-name,super-init-not-called,too-few-public-methods,too-many-instance-attributes


from enum import Enum

from datetime import datetime

from sqlalchemy.sql.expression import and_

from flask_security import UserMixin, RoleMixin
from flask_security.utils import hash_password, verify_password

from app_name.database import db

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
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


class User(db.Model, UserMixin):
    """
    User superclass to inherit auth token function
    """
    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(db.Text)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    phone_number = db.Column(db.Text, unique=True)
    image_url = db.Column(db.Text)

    active = db.Column(db.Boolean)
    is_admin = db.Column(db.Boolean)

    oauth_connections = db.relationship('OAuthConnection', backref='owner')

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime)
    confirmed_at = db.Column(db.DateTime)

    last_login_at = db.Column(db.DateTime)
    current_login_at = db.Column(db.DateTime)
    last_login_ip = db.Column(db.Text)
    current_login_ip = db.Column(db.Text)
    login_count = db.Column(db.Integer)

    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users'),
                            cascade="all,delete")

    def __init__(self, **data):
        self.full_name = data.get('full_name', '')
        self.first_name = data.get('first_name', '')
        self.last_name = data.get('last_name', '')
        self.email = data.get('email', '')
        self.password = hash_password(data.get('password', ''))
        self.phone_number = data.get('phone_number', '')
        self.image_url = data.get('image_url', '')

        self.active = data.get('is_active', True)
        self.is_admin = data.get('is_admin', False)

        self.oauth_connections = data.get('oauth_connections', [])

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
        }

    def public_dict(self):
        """
        Serialize user's data into dictionary to be exposed publicly
        :return:
        """
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
        }

    def get_oauth_dicts_for(self, provider):
        """
        Returns dict of info needed for async task that retrieves contacts
        :return: dict()
        """
        connections = self.get_my_oauth_connection_for(provider)

        return [connection.to_dict() for connection in connections]

    def get_my_oauth_connections_for(self, provider):
        """
        Returns the user's connection for the
        :param provider: Enum       # used the word "provider" cause "type" is a keyword in python
        :return: OAuthConnnection (db.Model)
        """
        assert type(provider) == OAuthConnectionType, \
            'Please send a OAuthConnectionType object as the "provider"'

        return [connection for connection in self.oauth_connections if connection.type == provider]

    @classmethod
    def get_user_by_attrs(cls, get_all=False, **attrs):
        """
        Filters users by provided attributes
        Provided attributes must be in User class
        :param get_all: bool
        :param attrs: dict
        :return: user
        """
        if not all(attr in cls.__dict__ for attr in attrs):
            return None

        filters = []
        for attr, value in attrs.items():
            filters.append(eval('{}.{}'.format(cls.__name__, attr)) == value)

        query = cls.query.filter(and_(*filters))

        return query.all() if get_all else query.first()


class OAuthConnectionType(Enum):
    """
    Types of OAuth that we support
    """
    FACEBOOK = 'facebook'
    GOOGLE = 'google'


class OAuthConnection(db.Model):
    """
    Class to create various connected accounts
    """
    __tablename__ = 'oauth_connection'

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    email_address = db.Column(db.Text)
    type = db.Column(db.Enum(OAuthConnectionType))

    ext_user_id = db.Column(db.Text)
    ext_access_token = db.Column(db.Text)
    ext_refresh_token = db.Column(db.Text)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime)

    def __init__(self, **data):
        self.owner_id = data.get('owner_id')

        self.email_address = data.get('email_address')
        self.type = data.get('type')

        self.ext_user_id = data.get('ext_user_id')
        self.ext_access_token = data.get('ext_access_token')
        self.ext_refresh_token = data.get('ext_refresh_token')

    def to_dict(self):
        """
        Serializes oauth connection
        :return: dict()
        """
        return {
            'type': self.type,
            'ext_access_token': self.ext_access_token,
            'ext_refresh_token': self.ext_refresh_token,
            'email_address': self.email_address,
        }

