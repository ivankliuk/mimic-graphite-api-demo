==================
Mimic Graphite API
==================

This project is a proof of concept, per se. Its purpose to mimic Graphite API behaviour to be consumed by `Grafana <http://grafana.org/>`_.

Workflow
--------

`Mimic Graphite API <https://github.com/ivankliuk/mimic-graphite-api-demo>`_ behaves as `Graphite API <https://github.com/brutasse/graphite-api>`_ service from Grafana's perspective. So you can shove it to Grafana and it will behave exactly as Graphite API. After the mimic is added to Grafana as a data source, there will be four metrics available:

* Temperature in Kyiv
* Temperature in Odesa
* Absolute temperature in Kyiv
* Absolute temperature in Odesa

Those reveal temperature data for Jan-Feb 2016.

Installation
------------

Installation instruction presumes you're using ``virtualenv`` and ``pip`` for managing Python packages. The project works on Python 2.7+ and Python 3.4.

#. Download project from GitHub:

   .. code :: bash

      git clone https://github.com/ivankliuk/mimic-graphite-api-demo.git

#. Change current directory:

   .. code :: bash

      cd mimic-graphite-api-demo/

#. Create Python ``virtualenv``:

   .. code :: bash

      mkvirtualenv mimic

#. Install project's requirements:

   .. code :: bash

      pip install -r requirements.txt

Execution
---------

Run following command from the project's directory:

.. code :: bash

   python main.py <HOST> <PORT>

where ``HOST`` and ``PORT`` are IP address and port where the server will be listening.
