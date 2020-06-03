======
sos4py
======


.. image:: https://img.shields.io/pypi/v/sos4py.svg
        :target: https://pypi.python.org/pypi/sos4py


sos4py is a convenience layer for Python environment to access services, extract data, and allow querying from SOS instances.


* Free software: Apache Software License 2.0
* Documentation: https://sos4py.readthedocs.io.


Features
--------
*   Allows connection to an SOS service using OWSLib.

    * These indentation requirements are the same for sub-list items
          (but apply to their symbol or number, not their item text).

    *   A.

        + If you *do* use them (for items with sub-lists or extra
          paragraphs) put blank lines between *all* items at that level.

* TODO

Installation
------------
#. `pip install project-name`
#. Add `'project_name.middleware.ProjectNameMiddleware'` to `MIDDLEWARE_CLASSES` (if necessary)
#. Add `'project_name'` to `INSTALLED_APPS` (if necessary)
#. Run `syncdb` (if necessary)


Usage
-----

**Connecting to an SOS service:**
 *Description*
  Base class of a connection to a Sensor Observation Service. The result is class object SensorObservationService_2_0_0(object) of the OWSLib (<https://github.com/geopython/OWSLib/blob/master/owslib/swe/observation/sos200.py>)
 *Usage*
     ``def connection_sos(url,
     xml=None,
     username=None,
     password=None,):``

 *Parameters*

    xml : str
      Xml file path.

    username : str
      Username to access the SOS service.

    password : str
      User password to access the SOS service.

 *Example*

    ``from sos4py.main import connection_sos``
    
    ``service = sos4py('http://sensorweb.demo.52north.org/52n-sos-webapp/sos/kvp')``

**Get capabilities functions(summaries):**
 *Description*
  Construction class sos_2_0_0. Implements the the return of the function *connection_sos()* as inpu. The methods of the class can be used for metadata retrieval of sensors, and observation data queries.

 *Usage*
     ``class sos_2_0_0(self, url, version, xml=None, username=None, password=None):``

 *Methods*
  ``sosServiceIdentification()`` The identification section of a SOS v2.0 capabilities document. This function queries the identification metadata available and returns the data as a pandas Series dataframe. 

  ``sosProvider()`` The provider section of an SOS v2.0 capabilities document. This function queries the provider metadata available and returns the data as a pandas Series dataframe.     

  ``sosOperationsMetadata()`` Elements in an OperationsMetadata object.This function queries the operations available of a SOS v2.0 capabilities document and returns the data as a pandas Series dataframe.  

  ``sosOfferings()`` Explore offerings section of an SOS v2.0 capabilities document. This function queries the offerings and returns the data as a pandas Series dataframe. 

  ``sosPhenomena()`` Queries a SOS v2.0 for all its phenomena. Returns a list of the phenomena ids.

 *Examples*

    ``from sos4py.main import connection_sos``
    
    ``service = sos4py('http://sensorweb.demo.52north.org/52n-sos-webapp/sos/kvp')``

    ``service.sosServiceIdentification()``

    ``service.sosProvider()``

    ``service.sosOperationsMetadata()``

    ``service.sosOfferings()``

    ``service.phenomena()``


**Get Data Availability function:**        
 *Description*
  Base class of a connection to a Sensor Observation Service. The result is class object SensorObservationService_2_0_0(object) of the OWSLib (<https://github.com/geopython/OWSLib/blob/master/owslib/swe/observation/sos200.py>)

 *Usage*

 ``def get_data_availability(object, procedures=None, observedProperties=None, featuresOfInterest=None, offerings=None, method=None, **kwargs)``
      
 *Parameters*

    object : str
      Object of type sos_2_0_0.

    procedures : list of str
      Query the data based on the availability of the indicated procedures.

    observedProperties: list of str
      Query the data based on the availability of the indicated observed properties.

    featuresOfInterest : list of str
      Query the data based on the availability of the indicated features of interest.

    offerings : list of str
      Query the data based on the availability of the indicated offerings.

    method : str
      'Get' or 'Post' request parameter.


 *Examples*

      ``service.get_data_availability()``



      ``service.get_data_availability(procedures=['http://www.52north.org/test/procedure/6'], 
      featuresOfInterest=['http://www.52north.org/test/featureOfInterest/6'])``


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
