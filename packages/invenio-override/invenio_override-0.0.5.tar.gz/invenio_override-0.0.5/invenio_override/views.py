# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2023 Graz University of Technology.
# Copyright (C) 2024 Shared RDM.
#
# invenio-override is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""invenio module for sharedRDM theme."""

from functools import wraps
from typing import Dict, Optional

from flask import Blueprint, current_app, g, redirect, render_template, url_for
from flask_login import current_user, login_required
from invenio_rdm_records.proxies import current_rdm_records
from invenio_rdm_records.resources.serializers import UIJSONSerializer
from invenio_records_global_search.resources.serializers import (
    GlobalSearchJSONSerializer,
)
from invenio_users_resources.proxies import current_user_resources
from opensearch_dsl.utils import AttrDict

from .search import FrontpageRecordsSearch

blueprint = Blueprint(
    "invenio-override",
    __name__,
    template_folder="templates",
    static_folder="static",
)


@blueprint.route("/me/overview")
@login_required
def overview():
    """Render the user overview dashboard."""
    url = current_user_resources.users_service.links_item_tpl.expand(
        g.identity, current_user
    )["avatar"]
    is_authenticated = current_identity_is_authenticated()

    return render_template(
        "invenio_override/overview.html",
        is_authenticated=is_authenticated,
        user_avatar=url,
    )


def records_serializer(records=None) -> list:
    """
    Serialize a list of records.

    :param records: List of records to serialize.
    :returns: Serialized records as a list of dictionaries.
    """
    serializer = GlobalSearchJSONSerializer()
    return [serializer.dump_obj(r.to_dict()) for r in records]


def index():
    """
    Render the frontpage.

    Fetches the most recent records and renders the frontpage template.
    """
    records = FrontpageRecordsSearch()[:5].sort("-created").execute()

    return render_template(
        "invenio_override/frontpage.html", records=records_serializer(records)
    )


def default_error_handler(e: Exception) -> tuple:
    """
    Handle unhandled errors.

    :param e: Exception raised.
    :returns: Rendered error page with HTTP 500 status.
    """
    return render_template(current_app.config["THEME_500_TEMPLATE"]), 500


@blueprint.app_template_filter("make_dict_like")
def make_dict_like(value: str, key: str) -> Dict[str, str]:
    """
    Convert a value to a dict-like structure.

    :param value: The value to include in the dictionary.
    :param key: The key associated with the value.
    :returns: A dictionary with the given key-value pair.
    """
    return {key: value}


@blueprint.app_template_filter("cast_to_dict")
def cast_to_dict(attr_dict: AttrDict) -> dict:
    """
    Convert an AttrDict to a regular dictionary.

    :param attr_dict: The AttrDict to convert.
    :returns: The converted dictionary.
    """
    return AttrDict.to_dict(attr_dict)


def comingsoon() -> str:
    """
    Render the coming soon page.

    :returns: Rendered HTML for the coming soon page.
    """
    return render_template("invenio_override/comingsoon.html")


def locked(e) -> str:
    """
    Render the locked error page.

    :param e: Exception raised for a locked resource.
    :returns: Rendered HTML for the locked error page.
    """
    return render_template("invenio_override/423.html")


@blueprint.route("/records/search")
def records_search():
    """
    Render the search page UI.

    Adds a new endpoint at repository.tugraz.at/records/search,
    serving as the dedicated search page for RDM records.
    """
    return render_template("invenio_app_rdm/records/search.html")


def current_identity_is_authenticated() -> bool:
    """Check whether the current identity is authenticated via remote auth."""
    rdm_service = current_rdm_records.records_service
    return rdm_service.check_permission(g.identity, "authenticated")


def require_authenticated(view_func):
    """Decorator to guard views against unauthenticated users."""

    @wraps(view_func)
    def decorated_view(*args, **kwargs):
        if not current_identity_is_authenticated():
            return redirect(url_for("invenio-override.overview"))
        return view_func(*args, **kwargs)

    return decorated_view
