# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2023 Graz University of Technology.
# Copyright (C) 2024 Shared RDM.
#
# invenio-override is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""invenio module for sharedRDM theme."""

from flask_login import login_required
from flask_menu import current_menu
from invenio_i18n import lazy_gettext as _

try:
    from invenio_records_marc21.ui.theme import current_identity_can_view
except ImportError:
    current_identity_can_view = lambda: False

from . import config
from .views import blueprint, index, locked, require_authenticated


class InvenioOverride(object):
    """invenio-override extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        # https://flask.palletsprojects.com/en/1.1.x/api/#flask.Flask.add_url_rule
        app.add_url_rule("/", "index", index)
        self.init_config(app)
        app.register_error_handler(423, locked)
        app.config["THEME_LOGO"] = app.config.get("OVERRIDE_LOGO")
        app.extensions["invenio-override"] = self
        routes = app.config.get("OVERRIDE_ROUTES")
        blueprint.add_url_rule(routes["index"], view_func=index)

        @app.context_processor
        def inject_visibility():
            return {"can_view_marc21": current_identity_can_view()}

    def init_config(self, app):
        """Initialize configuration."""
        for k in dir(config):
            if k.startswith("INVENIO_OVERRIDE_") or k.startswith("OVERRIDE_"):
                app.config.setdefault(k, getattr(config, k))


def finalize_app(app):
    """Finalize app."""
    modify_user_dashboard(app)
    guard_view_functions(app)


def modify_user_dashboard(app):
    """Modify user dashboard.

    To modify the dashboard menu, access the user_dashboard_menu
    through root_menu.submenu("dashboard").
    """
    root_menu = app.extensions["menu"].root_node
    user_dashboard_menu = root_menu.submenu("dashboard")

    if "overview" not in user_dashboard_menu.children:
        user_dashboard_menu.submenu("overview").register(
            "invenio-override.overview",
            text=_("Overview"),
            order=0,
        )

    root_menu.submenu("actions.deposit").register(
        "invenio-override.overview",
        _("My dashboard"),
        order=1,
    )


def guard_view_functions(app):
    """Guard view functions against unauthenticated access."""
    endpoints_to_guard = [
        "invenio_app_rdm_users.communities",
        "invenio_app_rdm_users.requests",
        "invenio_app_rdm_users.uploads",
    ]

    for endpoint in endpoints_to_guard:
        view_func = app.view_functions.get(endpoint)
        if not view_func:
            continue

        view_func = login_required(require_authenticated(view_func))

        app.view_functions[endpoint] = view_func
