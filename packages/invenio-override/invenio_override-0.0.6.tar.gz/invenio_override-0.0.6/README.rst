..
    Copyright (C) 2020-2023 Graz University of Technology.
    Copyright (C) 2024 Shared RDM.

    invenio-override is free software; you can redistribute it and/or
    modify it under the terms of the MIT License; see LICENSE file for more
    details.

======================
 invenio-override
======================

.. image:: https://github.com/sharedRDM/invenio-override/workflows/CI/badge.svg
        :target: https://github.com/sharedRDM/invenio-override/actions

.. image:: https://img.shields.io/pypi/dm/invenio-override.svg
        :target: https://pypi.python.org/pypi/invenio-override

.. image:: https://img.shields.io/github/tag/sharedRDM/invenio-override.svg
        :target: https://github.com/sharedRDM/invenio-override/releases

.. image:: https://img.shields.io/github/license/sharedRDM/invenio-override.svg
        :target: https://github.com/sharedRDM/invenio-override/blob/master/LICENSE

.. image:: https://readthedocs.org/projects/invenio-override/badge/?version=latest
        :target: https://invenio-override.readthedocs.io/en/latest/?badge=latest

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

Override invenioRDM theme.

Features:

* Custom header template.
* Custom footer template.
* Custom login/signup templates.
* Custom frontpage template.
* Custom contact template.
* Overriden theme.

Configuration fields with the **default** values available to enable/disable these package's feature on a custom instance:

* Global search

.. code-block:: python

    # Publications - Enable or disable the publication global search feature.
    OVERRIDE_SHOW_PUBLICATIONS_SEARCH = False

    # OER - Enable or disable the educational resources global search feature.
    OVERRIDE_SHOW_EDUCATIONAL_RESOURCES = False


**Note**: by default invenio-override does not requiere **OER** or **Publications** packages. To install one or both, specify them as extras:
    
.. code-block::

    pip install invenio-override[lom, marc21]


or just

.. code-block::

    pip install invenio-override[marc21]


Enabling the OVERRIDE configurations without their respective library might lead to unexpected errors. More details about working with global-search packages here: https://github.com/tu-graz-library/invenio-global-search


* Frontpage and its right section

.. code-block:: python

    # Enable or disable a section on the frontpage that adds shortcuts to search and uploads
    OVERRIDE_RESOURCE_OVERVIEW = False

    # Enable or disable the right section of the frontpage (Contact us, Benefits)
    OVERRIDE_FRONTPAGE_RIGHT = False

    # If section Benefits is displayed, option to click on More and go to Statistics page for more info
    OVERRIDE_RIGHT_SECTION_TITLE = True

    # Contact Email for the Contact us feature in the right section
    OVERRIDE_SHOW_RIGHT_CONTACT_EMAIL = True

    # Contact email displayed in the right section
    OVERRIDE_RIGHT_SECTION_CONTACT_EMAIL = "support@example.com"

    # feedback form used in right section
    OVERRIDE_CONTACT_FORM = False

* Branding and UI

.. code-block:: python

    # Icon and Logo displayed on the webiste
    # list of available options: ["icon_use.png", "TUG.png", "KFU.svg", "MUG.svg", "invenio-override-default.svg", "sharedRDM.png"]
    OVERRIDE_ICON = "images/icon_use.png"

    OVERRIDE_LOGO = "images/inveniordm-tail.svg"

    # favicon for shortcuts
    # list of available options: ["kfu.ico", "mug.ico", "tug.ico"]
    OVERRIDE_FAVICON = "favicon.ico"

    # Override the Uploads menu title
    USER_DASHBOARD_MENU_OVERRIDES = {
      "uploads": {
        "text": _("Research Results"),
      },
    }


* Differentiate between production and testing instance

.. code-block:: python

    # Production environment. Can also be set in .env as 'INVENIO_OVERRIDE_PRODUCTION'
    OVERRIDE_PRODUCTION = False


Further documentation is available on
https://invenio-override.readthedocs.io/
