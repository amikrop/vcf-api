vcf-api
=======

.. image:: https://github.com/amikrop/vcf-api/actions/workflows/main.yml/badge.svg
   :target: https://github.com/amikrop/vcf-api/actions/
   :alt: Workflows

This is a demo backend providing basic `VCF <https://en.wikipedia.org/wiki/Variant_Call_Format>`_ records management, made using Django REST Framework.

It is tested for Python versions 3.8 - 3.12.

Usage
-----

A VCF file must be present for the app to run. The default path is ``data/variants.vcf``,
but this can be changed, as shown `below <https://github.com/amikrop/vcf-api?tab=readme-ov-file#settings>`_.

Locally
*******

1. Change into the ``app/`` directory:

.. code-block:: bash

   cd app

2. Install dependencies (preferably in a `virtual environment <https://docs.python.org/3/tutorial/venv.html>`_):

.. code-block:: bash

   pip install -r requirements.txt

Serve application
~~~~~~~~~~~~~~~~~

Launch the development server:

.. code-block:: bash

   python manage.py runserver

Unit tests
~~~~~~~~~~

* Run the tests for the current Python version:

.. code-block:: bash

   pytest

* Run the tests for all supported Python versions found in your system, using `tox <https://tox.wiki/>`_:

.. code-block:: bash

   tox

Docker
******

Serve application
~~~~~~~~~~~~~~~~~

Build and run the Docker container with `Docker Compose <https://docs.docker.com/compose/>`_:

* Linux/macOS:

.. code-block:: bash

   ./docker-start.sh

* Windows:

.. code-block:: bash

   docker-start.bat

Unit tests
~~~~~~~~~~

Once you have started the Docker app, you can run the tests for the containerized deployment:

.. code-block:: bash

   docker compose run web pytest

Settings
--------

Settings are resolved in the following order (highest priority first):

1. Explicit values in ``settings.py``

2. Environment variables

3. Defaults

Environment variables can be read from a ``.env`` file, if present.

Application settings
********************

* ``VCF_FILE_BASENAME``: Basename of the VCF file to be used. Will be looked for in the ``data/`` directory.
* ``VCF_FILE_PATH``: Alternatively, if you want to specify a custom path for the VCF file, set this instead.
* ``WRITE_TOKEN``: Token required to perform write operations (create, update, delete).
* ``REST_FRAMEWORK["PAGE_SIZE"]``: Default page size for paginated results.

=============================== ====================== ===========================================
Name                            Environment variable   Default
=============================== ====================== ===========================================
``VCF_FILE_BASENAME``           ``VCF_FILE_BASENAME``  ``"variants.vcf"``
``VCF_FILE_PATH``               ``VCF_FILE_PATH``      ``{PROJECT_ROOT}/data/{VCF_FILE_BASENAME}``
``WRITE_TOKEN``                 ``DJANGO_WRITE_TOKEN`` ``"secret-token"``
``REST_FRAMEWORK["PAGE_SIZE"]`` ``DJANGO_PAGE_SIZE``   ``100``
=============================== ====================== ===========================================

Infrastructure settings
***********************

Deployment-related settings, that should be changed in production:

================= ======================== ================
Name              Environment variable     Default
================= ======================== ================
``SECRET_KEY``    ``SECRET_KEY``           ``"secret-key"``
``DEBUG``         ``DEBUG``                ``True``
``ALLOWED_HOSTS`` ``DJANGO_ALLOWED_HOSTS`` ``[]``
================= ======================== ================

Endpoints
---------

The following endpoints are available:

* ``GET /``: List VCF records, paginated.

  * Optional query parameters:

    * ``id``: Filter by record ID.
    * ``limit``: Number of records per page (default: as per ``REST_FRAMEWORK["PAGE_SIZE"]`` setting).
    * ``offset``: Offset for pagination (default: 0).

  * Can take the HTTP ``Accept`` header for content negotiation (``application/json`` or ``application/xml``).
  * Supports caching with the ``ETag``/``If-None-Match`` HTTP headers.

* ``POST /``: Create a new VCF record.
* ``PUT /?id=<record-id>``: Update existing VCF records.
* ``DELETE /?id=<record-id>``: Delete VCF records.

The ``POST``, ``PUT`` and ``DELETE`` endpoints require the HTTP ``Authorization`` header to be set to ``Bearer <WRITE_TOKEN>``,
where ``<WRITE_TOKEN>`` is configured from settings.

The ``POST`` and ``PUT`` endpoints expect the request body to contain a VCF record, similar to:

.. code-block:: json

   {"CHROM": "chr1", "POS": 1000, "ALT": "A", "REF": "G", "ID": "rs123"}

Input validation is performed, using the following rules:

* `CHROM`: ``chr``, then a number from ``1`` to ``22`` or one of ``X``, ``Y``, ``M``
* `POS`: positive integer
* `ID`: ``rs``, then a positive integer
* `ALT`, `REF`: one of ``A``, ``C``, ``G``, ``T``, ``.``
