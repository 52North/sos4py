# -*- coding: utf-8 -*-
############################################################################## #
#                                                                              #
# Author: Alfredo Chavarria (a.h.chavarriavargas@utwente.student.nl)           #
# Created: 2020-05-28                                                          #
# Project: sos4py - https://github.com/52North/sos4py                          #
#                                                                              #
############################################################################## #

"""
Utility functions
"""

from owslib.util import nspath_eval, testXMLAttribute, extract_time
from owslib.namespaces import Namespaces
import pandas as pd


def get_namespaces():
    n = Namespaces()
    ns = n.get_namespaces(["fes", "gml32", "ogc", "om20", "sa", "sml", "swe20", "swes", "wml2", "xlink", "xsi"])
    ns["gda"] = 'http://www.opengis.net/sosgda/1.0'
    ns["ns"] = "http://www.opengis.net/gml/3.2"
    ns["ows"] = n.get_namespace("ows110")
    ns["sams"] = "http://www.opengis.net/samplingSpatial/2.0"
    ns["sf"] = "http://www.opengis.net/sampling/2.0"
    ns["sos"] = n.get_namespace("sos20")
    return ns

def nspv(path):
    ''' Apply the nspath_eval function to a path '''
    return nspath_eval(path, get_namespaces())

def TimePeriod(start, end):
    ''' gml TimePeriod construction '''
    return ("start: " + str(start) + " " + "end: " + str(end))

def parseGDAReferencedElement(gdaMembers, elementName):
    """Function to parse an element of a "GetDataAvailability" member"""
    element = testXMLAttribute(gdaMembers.find(nspv(elementName)), nspv("xlink:href"))
    return(element)

def gda_member(gdaMembers):
    """Function to parse each "GetDataAvailability" member"""
    #Prefixes
    gdaPrefix = "gda"
    gdaProcedureName = gdaPrefix + ":procedure"
    gdaObservedPropertyName = gdaPrefix + ":observedProperty"
    gdaFeatureOfInterestName = gdaPrefix + ":featureOfInterest"

    #Applying a parsing function to the elements
    procedure_gda = parseGDAReferencedElement(gdaMembers, gdaProcedureName)
    observedProperty_gda = parseGDAReferencedElement(gdaMembers, gdaObservedPropertyName)
    featureOfInterest_gda = parseGDAReferencedElement(gdaMembers, gdaFeatureOfInterestName)

    ''' Determine if phenomenonTime is instant or period. This
    depend on the type of observation '''
    instant_element = gdaMembers.find(nspv(
        "gda:phenomenonTime/gml32:TimeInstant"))

    if instant_element is not None:
        phenomenonTime_gda = extract_time(instant_element)
    else:
        start = extract_time(gdaMembers.find(nspv(
            "gda:phenomenonTime/gml32:TimePeriod/gml32:beginPosition")))
        end = extract_time(gdaMembers.find(nspv(
            "gda:phenomenonTime/gml32:TimePeriod/gml32:endPosition")))
        phenomenonTime_gda = TimePeriod(start, end)
        resultTime_gda = extract_time(gdaMembers.find(nspv(
        "gda:resultTime/gml32:TimeInstant/gml32:timePosition")))

    #Constructing the results
    gda_values = [procedure_gda, observedProperty_gda, featureOfInterest_gda, phenomenonTime_gda, start, end, resultTime_gda]
    gda_index = ['Procedure', 'ObservedProperty','FeatureOfInterest', 'PhenomenonTime', 'StartTime', 'EndTime', 'ResultTime']
    a = pd.Series(gda_values, index=gda_index, name="gda_member")
    return(a)

def check_list_param(list_param):
    ''' Check parameters conditions and if the condition is not satisfied the program will stop and give an assertion error '''
    correctness = (isinstance(list_param, list) and \
    len(list_param) > 0 and \
    map(lambda x: isinstance(x, str), list_param))
    assert (correctness)
