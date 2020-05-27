flake8-bitbucket
################
A flake8 plugin for `bitbucket code insights`_.

DISCLAIMER
**********
I will **not** be maintaining this beyond my own use cases.

Bitbucket requires license keys to use their product,
and this makes system testing needlessly difficult.

Installation
************
Requires python3.8, might work on newer version.

.. code:: bash

    pip install git+https://github.com/newAM/flake8-bitbucket.git

Installing from Repository
==========================
.. code:: bash

    python3.8 -m pip uninstall -y flake8-bitbucket
    python3.8 setup.py install

Usage
*****
``flake8-bitbucket`` adds these CLI options to ``flake8``.
These options can be provided via the CLI or a ``.flake8`` configuration file.

::

    flake8-bitbucket:
    --bitbucket-api-token BITBUCKET_API_TOKEN
                            Bitbucket API token for authentication. Setting this option will automatically enable flake8-bitbucket as the formatter.
    --bitbucket-url BITBUCKET_URL
                            Bitbucket server URL, such as http://localhost:8090.
    --bitbucket-project-key BITBUCKET_PROJECT_KEY
                            Bitbucket project key.
    --bitbucket-repository-slug BITBUCKET_REPOSITORY_SLUG
                            Bitbucket respository slug.
    --bitbucket-suppress  Exit with code 0 on bitbucket HTTP failures.
    --bitbucket-verify BITBUCKET_VERIFY
                            Path to SSL certificate (.pem) for HTTPS bitbucket connections.

For example::

    flake8 . \
        --bitbucket-api-token MTA2MDg0MzcwODU4Okhh8vnnicQGd4immIB6LbB+mopl \
        --bitbucket-url http://localhost:7990/ \
        --bitbucket-project-key TEST \
        --bitbucket-repository-slug smellyrepo

.. image:: https://raw.githubusercontent.com/newAM/flake8-bitbucket/master/smelly_code.png

.. bitbucket code insights: https://confluence.atlassian.com/bitbucketserver/code-insights-966660485.html
