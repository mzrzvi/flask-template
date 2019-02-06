"""
Example models for an example resource group
"""

import uuid
from datetime import datetime

from app_name.database import db


class ResourceA(db.Model):
    """
    Example resource to build model and routes around
    Owns many Resource B's while a Resource B is only associated with 1 Resource A
    All Resource A's can be viewed by anyone -- signed-in user or not
    Only resources you own can be edited by you, however
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)

    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    resource_b_set = db.relationship('ResourceB', backref='resourceA')

    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self, **data):
        self.id = str(uuid.uuid4())
        self.name = data.get('name')

        self.created_at = datetime.now()

    def __str__(self):
        return 'Resource A: {name}'.format(name=self.name)

    def to_dict(self):
        """
        Serialize data into publicly exposable dictionary
        :return:
        """
        return {
            'id': self.id,
            'name': self.name
        }


class ResourceB(db.Model):
    """
    Example resource used to demonstrate one-to-many relationships
    Associated with one Resource A and does not own any resources
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)

    resource_a_id = db.Column(db.Integer, db.ForeignKey('resourceA.id'), nullable=False)

    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self, **data):
        self.id = str(uuid.uuid4())
        self.name = data.get('name')

        self.created_at = datetime.now()

    def __str__(self):
        return 'Resource B: {name}'.format(name=self.name)
