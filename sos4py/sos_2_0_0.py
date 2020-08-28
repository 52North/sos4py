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
from owslib.etree import etree
from owslib import ows
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
        """Construction function for "GetDataAvailability" operation"""
        method = method or 'Get'
        try:
            base_url = next((m.get('url') for m in self.getOperationByName(self,'GetDataAvailability').methods
                            if m.get('type').lower() == method.lower()))
        except StopIteration:
            base_url = self.url

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

        request_gda = openURL(base_url, request, method, username=self.username, password=self.password, **url_kwargs).read()
        gda = etree.fromstring(request_gda)

        if gda.tag == nspath_eval("ows:ExceptionReport", namespaces):
            raise ows.ExceptionReport(gda)

        gdaMembers = gda.findall(nspath_eval("gda:dataAvailabilityMember", namespaces))
        final = list(map(gda_member, gdaMembers))
        return(final)

    def get_feature_of_interest(self, featureOfInterest=None, observedProperty=None, procedure=None, responseFormat=None,method=None, **kwargs):
        """Performs "GetFeatureOfInterest" request

        Parameters
        ----------
        featureOfInterest : str, optional
           feature of interest
        observedProperty: str, optional
           observed property
        procedure: str, optional
           procedure
        responseFormat : str
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

        request = {'service': 'SOS', 'version': self.version, 'request': 'GetFeatureOfInterest'}

        # Optional Fields
        if featureOfInterest is not None:
            request['featureOfInterest'] = featureOfInterest

        if observedProperty is not None:
            request['observedProperty'] = observedProperty

        if procedure is not None:
            request['procedure'] = procedure

        if responseFormat is not None:
            request['responseFormat'] = responseFormat

        url_kwargs = {}
        if 'timeout' in kwargs:
            url_kwargs['timeout'] = kwargs.pop('timeout')  # Client specified timeout value

        if kwargs:
            for kw in kwargs:
                request[kw] = kwargs[kw]

        response = openURL(base_url, request, method,
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
            fois.append(foi.name)
            points.append(Point(foi.get_geometry()[1],foi.get_geometry()[0])) # Point expects (x, y)

        crs = pyproj.CRS.from_user_input(int(parsed_response.features[0].get_srs().split("/")[-1]))
        sites = gpd.GeoDataFrame({'site_name': fois, 'geometry': gpd.GeoSeries(points)},  crs=crs)

        # Add columns to GeoDataFrame indicating whether or not a specific phenomenon is available for a specific foi
        if include_phenomena==True:
            for phenomenon in self.sosPhenomena():
                response = self.get_feature_of_interest(observedProperty=phenomenon)
                xml_tree = etree.fromstring(response)
                parsed_response = SOSGetFeatureOfInterestResponse(xml_tree)
                fois = [foi.name for foi in parsed_response.features]
                sites_sub = pd.DataFrame({'site_name': fois, phenomenon: True})
                sites = sites.join(sites_sub.set_index('site_name'), on='site_name')

            sites = sites.fillna(False)

        return sites


class SOSGetFeatureOfInterestResponse(object):
    """ The base response type from SOS2.0. Container for OM_Observation
    objects.
    """
    def __init__(self, element):
        feature_data = element.findall(
            nspath_eval("sos:featureMember/wml2:MonitoringPoint", namespaces))
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
            y, x = testXMLValue(self.shape.find(nspv("ns:Point/ns:pos"))).split(" ")
            try:
                x = float(x)
                y = float(y)
            except Exception:
                raise ValueError("Error parsing coordinates value")
            self.geometry = tuple((float(y),float(x)))

            # TODO: write parsers for different geometry types
