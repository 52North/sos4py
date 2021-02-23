# sos4py
        
<a target="_blank" href="https://pypi.python.org/pypi/sos4py/"><img alt="version" src="https://img.shields.io/pypi/v/sos4py.svg"/></a>

sos4py is a convenience layer for Python environment to access services, extract data, and allow querying from SOS instances.


* Free software: Apache Software License 2.0


Features
--------
*   Allows connection to an SOS service using OWSLib.

*   Explore and summarize service capabilities, sensor metadata, offerings, observed properties, available phenomena and features of interest.

*   Query requests to an SOS service for getting Data Availability.

*   Query requests to an SOS service for getting observation data.

*   Query requests to an SOS service for getting observation site data.

Usage
-----

**EXAMPLES OF THE PACKAGE CAN BE SEEN:**: https://github.com/52North/sos4py/tree/master/examples

**Connecting to an SOS service:**

 *Description*
 
  Method to connect to a Sensor Observation Service. The result is an instance of sos_2_0_0 which inherits from SensorObservationService_2_0_0 of OWSLib (<https://github.com/geopython/OWSLib/blob/master/owslib/swe/observation/sos200.py>)
  
 *Usage*
 
     ``def connection_sos(url,
     xml=None,
     username=None,
     password=None,):``

 *Parameters*
 
    url : str
      url of the SOS.

    xml : str
      Xml file path.

    username : str
      Username to access the SOS service.

    password : str
      User password to access the SOS service.

 *Example*

    ``from sos4py.main import connection_sos``
    
    ``service = connection_sos('http://sensorweb.demo.52north.org/52n-sos-webapp/sos/kvp')``

**Get capabilities functions (summaries):**

 *Description*
 
  Summary methods to retrieve metadata of sensors.

 *Usage*
 
  ``def sosServiceIdentification():`` The identification section of a SOS v2.0 capabilities document. This function queries the identification metadata available and returns the data as a pandas Series dataframe. 

  ``def sosProvider():`` The provider section of an SOS v2.0 capabilities document. This function queries the provider metadata available and returns the data as a pandas Series dataframe.     

  ``def sosOperationsMetadata():`` Elements in an OperationsMetadata object.This function queries the operations available of a SOS v2.0 capabilities document and returns the data as a pandas Series dataframe.  

  ``def sosOfferings():`` Explore offerings section of an SOS v2.0 capabilities document. This function queries the offerings and returns the data as a pandas Series dataframe. 

  ``def sosPhenomena():`` Queries a SOS v2.0 for all its phenomena. Returns a list of the phenomena ids.
  
  ``def sosFeaturesOfInterest():`` Queries a SOS v2.0 for all its features of interest. Returns a list of the feature of interest ids.

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
 
  Method to get information on data availability.

 *Usage*

 ``def get_data_availability(object, procedures=None, observedProperties=None, featuresOfInterest=None, offerings=None, method=None, **kwargs):``
      
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

  It is recommended to provide at least one of sites, phenomena or procedures. Otherwise, the request may take very long.

 *Examples*

      ``service.get_data()``
      
      ``service.get_data(sites=['Sensor location 1'],phenomena=['water temperature','salinity'])``
      
Funding organizations/projects
-------

The development of sos4py was supported by several organizations and projects. Among other, we would like to thank the following organisations and project

| Project/Logo | Description |
| :-------------: | :------------- |
| <a target="_blank" href="https://www.bmvi.de/"><img alt="BMVI" align="middle" width="100" src="https://raw.githubusercontent.com/52North/sos/develop/spring/views/src/main/webapp/static/images/funding/bmvi-logo-en.png"/></a><a target="_blank" href="https://www.bmvi.de/DE/Themen/Digitales/mFund/Ueberblick/ueberblick.html"><img alt="mFund" align="middle" width="100" src="https://raw.githubusercontent.com/52North/sos/develop/spring/views/src/main/webapp/static/images/funding/mFund.jpg"/></a><a target="_blank" href="http://wacodis.fbg-hsbo.de/"><img alt="WaCoDis - Water management Copernicus services for the determination of substance inputs into waters and dams within the framework of environmental monitoring" align="middle" width="126" src="https://raw.githubusercontent.com/52North/sos/develop/spring/views/src/main/webapp/static/images/funding/wacodis-logo.png"/></a> | The development of this version of sos4py was supported by the <a target="_blank" href="https://www.bmvi.de/"> German Federal Ministry of of Transport and Digital Infrastructure</a> research project <a target="_blank" href="http://wacodis.fbg-hsbo.de/">WaCoDis</a> (co-funded by the German Federal Ministry of Transport and Digital Infrastructure, programme mFund) |
| <a target="_blank" href="https://bmbf.de/"><img alt="BMBF" align="middle" width="100" src="https://raw.githubusercontent.com/52North/sos/develop/spring/views/src/main/webapp/static/images/funding/bmbf_logo_neu_eng.png"/></a><a target="_blank" href="https://www.fona.de/"><img alt="FONA" align="middle" width="100" src="https://raw.githubusercontent.com/52North/sos/develop/spring/views/src/main/webapp/static/images/funding/fona.png"/></a><a target="_blank" href="http://www.mudak-wrm.kit.edu/"><img alt="Multidisciplinary data acquisition as the key for a globally applicable water resource management (MuDak-WRM)" align="middle" width="100" src="https://raw.githubusercontent.com/52North/sos/develop/spring/views/src/main/webapp/static/images/funding/mudak_wrm_logo.png"/></a> | The development of this version of sos4py was supported by the <a target="_blank" href="https://www.bmbf.de/"> German Federal Ministry of Education and Research</a> research project <a target="_blank" href="http://www.mudak-wrm.kit.edu/">MuDak-WRM</a> (co-funded by the German Federal Ministry of Education and Research, programme FONA) |

Credits
-------

This package was created with <a target="_blank" href="https://github.com/audreyr/cookiecutter">Cookiecutter</a> and the <a target="_blank" href="https://github.com/audreyr/cookiecutter-pypackage">audreyr/cookiecutter-pypackage</a> project template. 
