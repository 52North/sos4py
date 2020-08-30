======
sos4py
======


.. image:: https://img.shields.io/pypi/v/sos4py.svg
        :target: https://pypi.python.org/pypi/sos4py


sos4py is a convenience layer for Python environment to access services, extract data, and allow querying from SOS instances.


* Free software: Apache Software License 2.0


Features
--------
*   Allows connection to an SOS service using OWSLib.

*   Explore and summarize service capabilities, sensor metadata, offerings, observed properties, available phenomena and features of interest.

*   Query requests to an SOS service for Get Data Availability.

*   Query requests to an SOS service for getting observation data.

*   Query requests to an SOS service for getting observation site data.

Usage
-----

**EXAMPLES OF THE PACKAGE CAN BE SEEN:**: https://github.com/52North/sos4py/tree/master/examples

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

**Get capabilities functions (summaries):**
 *Description*
  Construction class sos_2_0_0. Implements the the return of the function *connection_sos()* as input. The methods of the class can be used for metadata retrieval of sensors, and observation data queries.

 *Usage*
     ``class sos_2_0_0(self, url, version, xml=None, username=None, password=None):``

 *Methods*
  ``sosServiceIdentification()`` The identification section of a SOS v2.0 capabilities document. This function queries the identification metadata available and returns the data as a pandas Series dataframe. 

  ``sosProvider()`` The provider section of an SOS v2.0 capabilities document. This function queries the provider metadata available and returns the data as a pandas Series dataframe.     

  ``sosOperationsMetadata()`` Elements in an OperationsMetadata object.This function queries the operations available of a SOS v2.0 capabilities document and returns the data as a pandas Series dataframe.  

  ``sosOfferings()`` Explore offerings section of an SOS v2.0 capabilities document. This function queries the offerings and returns the data as a pandas Series dataframe. 

  ``sosPhenomena()`` Queries a SOS v2.0 for all its phenomena. Returns a list of the phenomena ids.
  
  ``sosFeaturesOfInterest()`` Queries a SOS v2.0 for all its features of interest. Returns a list of the feature of interest ids.

 *Examples*

    ``from sos4py.main import connection_sos``
    
    ``service = connection_sos('http://sensorweb.demo.52north.org/52n-sos-webapp/sos/kvp')``

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
      Xml file path.

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



**Get sites function:**        
 *Description*
  Method to retrieve sites from an SOS. The result is a GeoDataFrame.

 *Usage*

 ``def get_sites(self, include_phenomena=False)``
      
 *Parameters*

    include_phenomena : boolean, optional
      Whether or not flags for the existance of phenomenona (e.g. water temperature) should be included (default is False)


 *Examples*

      ``service.get_sites()``
      
      ``service.get_sites(include_phenomena = True)``
      

**Get data function:**        
 *Description*
  Method to get observation data from an SOS. The result is a DataFrame.

 *Usage*

 ``def get_data(self, sites=None, phenomena=None, procedures=None, begin=None, end=None)``
      
 *Parameters*

    sites : non-empty list of str, optional
       observation sites/sensor locations
       
    phenomena : non-empty list of str, optional
       phenomena, e.g. water temperature
       
    procedures : non-empty list of str, optional
       measurement procedures of the observation, e.g. measurements in 2 m water depth
       
    begin : str, optional if end is not provided
       begin of time period in the form 'YYYY-MM-DDThh:mm:ssZ', e.g. '2020-01-01T10:00:00Z'
       
    end : str, optional if begin is not provided
       end of time period in the form 'YYYY-MM-DDThh:mm:ssZ', e.g. '2020-01-02T10:00:00Z'  

  It is recommended to provide at least one of sites, phenomena or procedures. Otherwise the request may take very long.

 *Examples*

      ``service.get_data()``
      
      ``service.get_data(sites=['Sensor location 1'],phenomena=['water temperature','salinity'])``
      
      

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
