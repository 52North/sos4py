# -*- coding: utf-8 -*-
############################################################################## #
#                                                                              #
# Author: Alfredo Chavarria (a.h.chavarriavargas@utwente.student.nl)           #
# Created: 2020-05-28                                                          #
# Project: sos4py - https://github.com/52North/sos4py                          #
#                                                                              #
############################################################################## #

#Class function
# Import functions from other libraries
from owslib.util import testXMLValue, testXMLAttribute, nspath_eval, openURL
from owslib.swe.observation.sos200 import SensorObservationService_2_0_0
from owslib.swe.observation.sos200 import SOSGetObservationResponse
from owslib.swe.observation.waterml2 import MeasurementTimeseriesObservation
from owslib.swe.observation.om import MeasurementObservation
from owslib.etree import etree
from owslib import ows
from urllib.parse import urlencode, urlparse
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import pyproj
import inspect
from .util import get_namespaces, nspv, TimePeriod, parseGDAReferencedElement, gda_member, check_list_param

namespaces = get_namespaces()

class sos_2_0_0(SensorObservationService_2_0_0):
    """
        Abstraction for OGC Sensor Observation Service (SOS).
        Implements sos4py.
    """

    def __init__(self, url, version, xml=None, username=None, password=None):
        """Initialize."""

        super().__init__(url=url, version="2.0.0", xml=xml, username=username, password=password)

    # Summary functions
    def sosServiceIdentification(self):
        return(pd.Series((inspect.getmembers(self.identification)[2][1]), name='ServiceIdentification'))

    def sosProvider(self):
        return(pd.Series((inspect.getmembers(self.provider.contact)[2][1]), name='ProviderData'))

    def sosOperationsMetadata(self):
        sum_opme = []
        for i in self.operations:
            a = {"Name":i.name,
            "FormatOptions":i.formatOptions,
            "Parameters":i.parameters,
            "Methods":i.methods,
            "Constraints":i.constraints}
            a = pd.Series(a, name=i.name)
            sum_opme.append(a)
        return(sum_opme)

    def sosOfferings(self):
        sum_offer=[]
        for offering in self.offerings:
            a = pd.Series(inspect.getmembers(offering)[2][1], name=offering.id)
            sum_offer.append(a)
        return(sum_offer)

    def sosPhenomena(self):
        test_observed_properties = []
        for op in self._capabilities.findall(nspath_eval('sos:contents/sos:Contents/swes:offering/sos:ObservationOffering/swes:observableProperty', namespaces)):
            observed_prop = testXMLValue(op)
            test_observed_properties.append(observed_prop)
        test_observed_properties = sorted(set(test_observed_properties))
        return(test_observed_properties)

    def sosFeaturesOfInterest(self):
        get_foi = self.get_operation_by_name('GetFeatureOfInterest')
        fois = []
        for foi in sorted(get_foi.parameters['featureOfInterest']['values']):
            fois.append(foi)
        return fois

    # Get data availability function
    def get_data_availability(self, procedures=None, observedProperties=None, featuresOfInterest=None, offerings=None, method=None, **kwargs):
        """Performs "GetDataAvailability" request

        Parameters
        ----------
        procedures: non-empty list of str, optional
           request only specific procedures
        observedProperties: non-empty list of str, optional
           request only specific observed properties
        featuresOfInterest : non-empty list of str, optional
           request only specific features of interest
        offerings : non-empty list of str, optional
            request only specific offerings
        method: str, optional
           http method (default is "Get")

        Returns
        -------
        list of GetDataAvailability members
        """

        method = method or 'Get'
        try:
            base_url = next((m.get('url') for m in self.getOperationByName('GetDataAvailability').methods
                            if m.get('type').lower() == method.lower()))
        except StopIteration:
            base_url = self.url

        base_url = self._fix_url_base(base_url)

        #Mandatory request parameters
        request = {'service': 'SOS', 'version':"2.0.0", 'request': 'GetDataAvailability'}

        # Optional Fields
        if procedures is not None:
            check_list_param(procedures)
            procedure = ','.join(procedures)
            request['procedure'] = procedure

        if observedProperties is not None:
            check_list_param(observedProperties)
            observedProperty = ','.join(observedProperties)
            request['observedProperty'] = observedProperty

        if featuresOfInterest is not None:
            check_list_param(featuresOfInterest)
            featureOfInterest = ','.join(featuresOfInterest)
            request['featureOfInterest'] = featureOfInterest

        if offerings is not None:
            check_list_param(offerings)
            offering = ','.join(offerings)
            request['offering'] = offering

        url_kwargs = {}
        if 'timeout' in kwargs:
            url_kwargs['timeout'] = kwargs.pop('timeout')  # Client specified timeout value


        if kwargs:
            for kw in kwargs:
                request[kw] = kwargs[kw]

        data = urlencode(request)
        request_gda = openURL(base_url, data, method, username=self.username, password=self.password, **url_kwargs).read()
        gda = etree.fromstring(request_gda)

        if gda.tag == nspath_eval("ows:ExceptionReport", namespaces):
            raise ows.ExceptionReport(gda)

        gdaMembers = gda.findall(nspath_eval("gda:dataAvailabilityMember", namespaces))
        final = list(map(gda_member, gdaMembers))
        return(final)

    def get_feature_of_interest(self, featuresOfInterest=None, observedProperties=None, procedures=None, responseFormat=None, method=None, **kwargs):
        """Performs "GetFeatureOfInterest" request

        Parameters
        ----------
        featuresOfInterest : non-empty list of str, optional
           request only specific features of interest
        observedProperties: non-empty list of str, optional
           request only specific observed properties
        procedures: non-empty list of str, optional
           request only specific procedures
        responseFormat : str, optional
            response format
        method: str, optional
           http method (default is "Get")

        Returns
        -------
        response of the request as <class 'bytes'>
        """

        method = method or 'Get'
        methods = self.get_operation_by_name('GetFeatureOfInterest').methods
        base_url = [m['url'] for m in methods if m['type'] == method][0]

        base_url = self._fix_url_base(base_url)

        request = {'service': 'SOS', 'version': self.version, 'request': 'GetFeatureOfInterest'}

        # Optional Fields
        if featuresOfInterest is not None:
            check_list_param(featuresOfInterest)
            featureOfInterest = ','.join(featuresOfInterest)
            request['featureOfInterest'] = featureOfInterest

        if observedProperties is not None:
            check_list_param(observedProperties)
            observedProperty = ','.join(observedProperties)
            request['observedProperty'] = observedProperty

        if procedures is not None:
            check_list_param(procedures)
            procedure = ','.join(procedures)
            request['procedure'] = procedure

        if responseFormat is not None:
            request['responseFormat'] = responseFormat

        url_kwargs = {}
        if 'timeout' in kwargs:
            url_kwargs['timeout'] = kwargs.pop('timeout')  # Client specified timeout value

        if kwargs:
            for kw in kwargs:
                request[kw] = kwargs[kw]

        data = urlencode(request)
        response = openURL(base_url, data, method,
                               username=self.username, password=self.password, **url_kwargs).read()
        try:
            tr = etree.fromstring(response)
            if tr.tag == nspath_eval("ows:ExceptionReport", namespaces):
                raise ows.ExceptionReport(tr)
            else:
                return response
        except ows.ExceptionReport:
            raise
        except BaseException:
            return response

    def get_sites(self, include_phenomena=False):
        """Gets the registered sites of the SOS

        Parameters
        ----------
        include_phenomena : boolean, optional
           whether or not flags for the existance of phenomenona (e.g. water temperature) should be included (default is False)

        Returns
        -------
        sites as GeoDataFrame
        """

        # Get and parse response
        response = self.get_feature_of_interest()
        xml_tree = etree.fromstring(response)
        parsed_response = SOSGetFeatureOfInterestResponse(xml_tree)

        # Save features of interest with their geometry in a GeoDataFrame
        fois = []
        points = []
        for foi in parsed_response.features:
            if foi.get_geometry() is not None:
                fois.append(foi.name if foi.name is not None else foi.id)
                points.append(Point(foi.get_geometry()[1],foi.get_geometry()[0])) # Point expects (x, y)

        crs = pyproj.CRS.from_user_input(int(parsed_response.features[0].get_srs().split("/")[-1]))
        sites = gpd.GeoDataFrame({'site_name': fois, 'geometry': gpd.GeoSeries(points)},  crs=crs)

        # Add columns to GeoDataFrame indicating whether or not a specific phenomenon is available for a specific foi
        if include_phenomena==True:
            for phenomenon in self.sosPhenomena():
                response = self.get_feature_of_interest(observedProperties=[phenomenon])
                xml_tree = etree.fromstring(response)
                parsed_response = SOSGetFeatureOfInterestResponse(xml_tree)
                fois = [foi.name for foi in parsed_response.features]
                sites_sub = pd.DataFrame({'site_name': fois, phenomenon: True})
                sites = sites.join(sites_sub.set_index('site_name'), on='site_name')

            sites = sites.fillna(False)

        return sites

    def get_observation(self, responseFormat=None, offerings=None, observedProperties=None, featuresOfInterest=None, procedures=None, eventTime=None, method=None, **kwargs):
        """Overrides parent function get_observation()
        Performs "GetObservation" request

        Parameters
        ----------
        responseFormat : str
           response format, e.g. 'http://www.opengis.net/om/2.0'
        offerings : non-empty list of str, optional
           request only specific offerings
        observedProperties: non-empty list of str, optional
           request only specific observed properties
        featuresOfInterest : non-empty list of str, optional
           request only specific features of interest
        procedures: non-empty list of str, optional
           request only specific procedures
        eventTime: str, optional
           event time as om:resultTime, e.g. 'om:resultTime,2019-01-01T12:00:00Z/2019-01-02T12:00:00Z'
        method: str, optional
           http method (default is "Get")
        **kwargs : extra arguments
           anything else e.g. vendor specific parameters

        It is recommended to provide at least one of featuresOfInterest, observedProperties, offerings or procedures. Otherwise the request may take very long.

        Returns
        -------
        response of the request as <class 'bytes'>
        """

        method = method or 'Get'
        # Pluck out the get observation URL for HTTP method - methods is an
        # array of dicts
        methods = self.get_operation_by_name('GetObservation').methods
        base_url = [m['url'] for m in methods if m['type'] == method][0]

        base_url = self._fix_url_base(base_url)

        request = {'service': 'SOS', 'version': self.version, 'request': 'GetObservation'}

        if responseFormat is not None:
            request['responseFormat'] = responseFormat

        if offerings is not None:
            check_list_param(offerings)
            offering = ','.join(offerings)
            request['offering'] = offering

        if observedProperties is not None:
            check_list_param(observedProperties)
            observedProperty = ','.join(observedProperties)
            request['observedProperty'] = observedProperty

        if featuresOfInterest is not None:
            check_list_param(featuresOfInterest)
            featureOfInterest = ','.join(featuresOfInterest)
            request['featureOfInterest'] = featureOfInterest

        if procedures is not None:
            check_list_param(procedures)
            procedure = ','.join(procedures)
            request['procedure'] = procedure

        if eventTime is not None:
            request['temporalFilter'] = eventTime

        url_kwargs = {}
        if 'timeout' in kwargs:
            url_kwargs['timeout'] = kwargs.pop('timeout')  # Client specified timeout value

        if kwargs:
            for kw in kwargs:
                request[kw] = kwargs[kw]

        data = urlencode(request)
        response = openURL(base_url, data, method, username=self.username, password=self.password, **url_kwargs).read()

        try:
            tr = etree.fromstring(response)
            if tr.tag == nspath_eval("ows:ExceptionReport", namespaces):
                raise ows.ExceptionReport(tr)
            else:
                return response
        except ows.ExceptionReport:
            raise
        except BaseException:
            return response

    def get_data(self, sites=None, phenomena=None, procedures=None, begin=None, end=None):
        """Gets the observations of the SOS

        Parameters
        ----------
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

        Returns
        -------
        observations as DataFrame
        """

        # Set event time
        # TODO: Improve (check format, support different formats, support using only end or begin)
        assert ((begin is not None) and (end is not None) or (begin is None) and (end is None)),("If begin/end is provided, end/begin has to be provided as well!")
        if (begin is not None) and (end is not None):
            eventTime = 'om:resultTime,' + begin + '/' + end
        else:
            eventTime = None

        # Get and parse response
        response = self.get_observation(featuresOfInterest=sites, observedProperties=phenomena, procedures=procedures, eventTime=eventTime)
        xml_tree = etree.fromstring(response)
        parsed_response = SOSGetObservationResponse(xml_tree)

        # Check response format
        # TODO: Check if different observations can have different response formats. If yes, the format needs to be checked for each observation...
        if isinstance(parsed_response.observations[0], MeasurementObservation):
            response_format = 'http://www.opengis.net/om/2.0'
        elif isinstance(parsed_response.observations[0], MeasurementTimeseriesObservation):
            response_format = 'http://www.opengis.net/waterml/2.0'

        return self._create_obs_data_frame(parsed_response, response_format)

    def _fix_url_base(self, base_url):
        parsed_url = urlparse(base_url)
        self_parsed_url = urlparse(self.url)

        if parsed_url.netloc != self_parsed_url.netloc:
            base_url = parsed_url._replace(netloc=self_parsed_url.netloc).geturl()
        
        return base_url

    def _create_obs_data_frame(self, parsed_response=None, response_format=None):

        assert (response_format is not None),("Unknown response format.")
        if response_format == 'http://www.opengis.net/om/2.0':
            return self._create_df_om(parsed_response)
        elif response_format == 'http://www.opengis.net/waterml/2.0':
            return self._create_df_waterml(parsed_response)

    def _create_df_om(self, parsed_response):
        """
        Save observation data in a DataFrame using response format http://www.opengis.net/om/2.0
        """

        fois = []
        procedures = []
        phenomena = []
        phenomenon_times = []
        result_times = []
        values = []
        uoms = []

        for mo in parsed_response.observations:
            fois.append(mo.featureOfInterest)
            procedures.append(mo.procedure)
            phenomena.append(mo.observedProperty)
            phenomenon_times.append(mo.phenomenonTime)
            result_times.append(mo.resultTime)
            values.append(mo.get_result().value)
            uoms.append(mo.get_result().uom)

        return pd.DataFrame({'site': fois, 'procedure': procedures, 'phenomenon' : phenomena, 'phenomenon_time': phenomenon_times, 'result_time': result_times, 'value': values, 'unit': uoms})

    def _create_df_waterml(self, parsed_response):
        """
        Save observation data in a DataFrame using response format http://www.opengis.net/waterml/2.0
        """

        fois = []
        procedures = []
        phenomena = []
        time_stamps = []
        values = []
        uoms = []

        for mo in parsed_response.observations:
            for point in mo.get_result().points:
                fois.append(mo.featureOfInterest)
                procedures.append(mo.procedure)
                phenomena.append(mo.observedProperty)
                time_stamps.append(point.datetime)
                values.append(point.value)
                uoms.append(mo.get_result().defaultTVPMetadata.uom)

        return pd.DataFrame({'site': fois, 'procedure': procedures, 'phenomenon' : phenomena, 'time_stamp': time_stamps, 'value': values, 'unit': uoms})

class SOSGetFeatureOfInterestResponse(object):

    def __init__(self, element):
        feature_data = []
        # add WaterML MonitoringPoints
        mp = element.findall(nspath_eval("sos:featureMember/wml2:MonitoringPoint", namespaces))
        if mp is not None:
            feature_data.extend(mp)
         # add SamplingFeature SpatialSamplingFeature
        ssf = element.findall( nspath_eval("sos:featureMember/sams:SF_SpatialSamplingFeature", namespaces))
        if ssf is not None:
            feature_data.extend(ssf)
        self.features = []
        for feature in feature_data:
            parsed_feature = FeatureOfInterest(feature)
            self.features.append(parsed_feature)

class FeatureOfInterest(object):
    ''' Specialised feature of interest type '''

    def __init__(self, element):

        self.id = testXMLValue(element.find(nspv("gml32:identifier"))) # what is really the id? (gml:id attr or gml:identifier element)

        self.name = testXMLValue(element.find(nspv("gml32:name")))

        self.sampledFeature = testXMLAttribute(element.find(nspv("sf:sampledFeature")), nspv("xlink:href"))

        self.shape = element.find(nspv("sams:shape"))

        self._parse_geometry()

    def get_geometry(self):
        ''' Get geometry of feature of interest.
            Axis order is (y, x) or (latitude, longitude), respectively.
        '''
        return self.geometry

    def get_srs(self):
        ''' Get spatial reference system of feature of interest.
        '''
        return self.srs


    def _parse_geometry(self):
        ''' Parse the geometry '''

        if self.shape is not None:
            self.srs = testXMLAttribute(self.shape.find(nspv("ns:Point/ns:pos")), "srsName")
            # Coordinates are saved as <ns:pos srsName="">y x</ns:pos> or <ns:pos srsName="">latitude longitude</ns:pos>, respectively
            geom_node = testXMLValue(self.shape.find(nspv("ns:Point/ns:pos")))
            if geom_node is None:
                self.geometry = None
                return
            y, x = geom_node.split(" ")
            try:
                x = float(x)
                y = float(y)
            except Exception:
                raise ValueError("Error parsing coordinates value")
            self.geometry = tuple((float(y),float(x)))
        else:
            self.geometry = None
            # TODO: write parsers for different geometry types
