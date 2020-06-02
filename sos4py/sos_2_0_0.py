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
from owslib.util import testXMLValue, nspath_eval, openURL
from owslib.swe.observation.sos200 import SosCapabilitiesReader
from owslib.swe.observation.sos200 import SensorObservationService_2_0_0
from owslib.etree import etree
from owslib import ows
import pandas as pd
import inspect
from .util import get_namespaces, nspv, TimePeriod, parseGDAReferencedElement, gda_member, check_list_param

      
class sos_2_0_0(object):
    """
        Abstraction for OGC Sensor Observation Service (SOS).
        Implements sos4py.
    """
    def __new__(self, url, version, xml=None, username=None, password=None):
        """overridden __new__ method"""
        obj = object.__new__(self)
        obj.__init__(url, version, xml, username, password)
        return obj
    
    def __init__(self, url, version, xml=None, username=None, password=None):
        """Initialize."""
        self.url = url
        self.username = username
        self.password = password
        self.version = version
        self._capabilities = None
        
        reader = SosCapabilitiesReader(
            version="2.0.0", url=self.url, username=self.username, password=self.password
        )
        if xml:  # read from stored xml
            self._capabilities = reader.read_string(xml)
        else:  # read from server
            self._capabilities = reader.read(self.url)
            
        SensorObservationService_2_0_0._build_metadata(self)

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
        namespaces = get_namespaces()
        for op in self._capabilities.findall(nspath_eval('sos:contents/sos:Contents/swes:offering/sos:ObservationOffering/swes:observableProperty', namespaces)):
            observed_prop = testXMLValue(op)
            test_observed_properties.append(observed_prop)
        test_observed_properties = sorted(set(test_observed_properties))
        return(test_observed_properties)
       
    # Get data availability function
    def get_data_availability(self, procedures=None, observedProperties=None, featuresOfInterest=None, offerings=None, method=None, **kwargs):
        """Construction function for "GetDataAvailability" operation"""
        namespaces = get_namespaces()
        method = method or 'Get'
        try:
            base_url = next((m.get('url') for m in SensorObservationService_2_0_0.getOperationByName(self,'GetDataAvailability').methods
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