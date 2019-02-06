"""
Admin dashboard views
"""

# pylint: disable=invalid-name,
import logging

from flask import (
    url_for,
    redirect,
    abort,
    flash,
    request
)

from flask_admin import BaseView
from flask_admin.babel import gettext
from flask_admin.contrib.sqla import ModelView

from flask_security import current_user

from wtforms.compat import iteritems


# Set up logger
log = logging.getLogger("flask-admin.sqla")

RESOURCE_PAGE_SIZE = 100


# Create customized model view class
class AuthModelView(ModelView):
    """
    Super class for model views requiring auth
    """
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))

    def _get_list_extra_args(self):
        args = super()._get_list_extra_args()

        args.extra_args['max'] = RESOURCE_PAGE_SIZE
        self.page_size = RESOURCE_PAGE_SIZE

        return args


class SearchableModelView(AuthModelView):
    """
    Endorsements page searchable
    """
    def __init__(self, *args, searchable_attrs, **kwargs):
        self.column_searchable_list = searchable_attrs
        super(SearchableModelView, self).__init__(*args, **kwargs)


class CustomModelView(AuthModelView):
    """
    Custom model view class for avoiding errors with polymorphic flask-sqlalchemy tables
    """
    def __init__(self, *args, form_excluded_columns=None, **kwargs):
        if form_excluded_columns is None:
            form_excluded_columns = []

        self.form_excluded_columns = form_excluded_columns
        super(CustomModelView, self).__init__(*args, **kwargs)

    def create_model(self, form):
        """
            Original Flask comment: Create model from form.

            Parent object must be AuthModelView so that only admin users have access to
            the admin panel

            This method is taking from the original flask ModelView
            code but is modified to work with Joined Table Inheritance
            models.

            :param form:
                Form instance
        """
        try:
            # Secret sauce..
            # The model was being being instantiated without being passed the
            # data dict to initialize values. Creating the dict and then passing
            # it to the model
            data = {name: field.data for name, field in iteritems(form._fields)}

            model = self.model(**data)
            self.session.add(model)
            self._on_model_change(form, model, True)
            self.session.commit()
        except Exception as ex:                                       # pylint: disable=broad-except
            if not self.handle_view_exception(ex):
                flash(gettext('Failed to create record. %(error)s', error=str(ex)), 'error')
                log.exception('Failed to create record.')

            self.session.rollback()

            return False
        else:
            self.after_model_change(form, model, True)

        return model


class AuthBaseView(BaseView):
    """
    Super class for views requiring auth
    """
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))
