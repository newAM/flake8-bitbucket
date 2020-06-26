flake8-bitbucket
################
|Python Version| |Build Status| |Black| |PyPi Version|

A flake8 plugin for `bitbucket code insights`_.

DISCLAIMER
**********
Updates to this package will be **very** slow.

Bitbucket requires license keys to use their product,
and this makes system testing needlessly difficult.

Installation
************
Tested with Python 3.8.

.. code:: bash

    python3.8 -m pip install flake8-bitbucket

Usage
*****
``flake8-bitbucket`` adds these CLI options to ``flake8``.
These options can be provided via the CLI or a ``.flake8`` configuration file.

::

    flake8-bitbucket:
    --bitbucket-api-token BITBUCKET_API_TOKEN
                            Bitbucket API token for authentication, or a path to a file containing the token. Setting this option will automatically enable flake8-bitbucket as the formatter.
    --bitbucket-url BITBUCKET_URL
                            Bitbucket server URL, such as http://localhost:8090.
    --bitbucket-project-key BITBUCKET_PROJECT_KEY
                            Bitbucket project key.
    --bitbucket-repository-slug BITBUCKET_REPOSITORY_SLUG
                            Bitbucket respository slug.
    --bitbucket-suppress  Exit with code 0 on bitbucket HTTP failures.
    --bitbucket-verify BITBUCKET_VERIFY
                            Path to SSL certificate (.pem) for HTTPS bitbucket connections.
    --bitbucket-delete    Delete the report and exit.

For example::

    flake8 . \
        --bitbucket-api-token MTA2MDg0MzcwODU4Okhh8vnnicQGd4immIB6LbB+mopl \
        --bitbucket-url http://localhost:7990/ \
        --bitbucket-project-key TEST \
        --bitbucket-repository-slug smellyrepo


.. image:: https://raw.githubusercontent.com/newAM/flake8-bitbucket/master/smelly_code.png

.. _bitbucket code insights: https://confluence.atlassian.com/bitbucketserver/code-insights-966660485.html

.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
.. |Build Status| image:: https://api.travis-ci.com/newAM/flake8-bitbucket.svg?branch=master
   :target: https://travis-ci.com/newAM/flake8-bitbucket
.. |PyPi Version| image:: https://img.shields.io/pypi/v/flake8-bitbucket
    :target: https://pypi.org/project/flake8-bitbucket/
.. |Python Version| image:: https://img.shields.io/pypi/pyversions/flake8-bitbucket
