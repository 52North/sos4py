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
from owslib.etree import etree

PHENOMENON_TIME_ID = 'PhenomenonTimeId'
PHENOMENON_TIME = 'PhenomenonTime'
START_TIME = 'StartTime'
END_TIME = 'EndTime'

def get_namespaces():
    n = Namespaces()
    ns = n.get_namespaces(["fes", "gml32", "ogc", "om20", "sa", "sml", "swe20", "swes", "wml2", "xlink", "xsi"])
    ns["ns"] = "http://www.opengis.net/gml/3.2"
    ns["ows"] = n.get_namespace("ows110")
    ns["sams"] = "http://www.opengis.net/samplingSpatial/2.0"
    ns["sf"] = "http://www.opengis.net/sampling/2.0"
    ns["sos"] = n.get_namespace("sos20")
    ns["gda"] = 'http://www.opengis.net/sosgda/1.0'
    ns["gda2"] = 'http://www.opengis.net/sosgda/2.0'
    return ns

def nspv(path):
    ''' Apply the nspath_eval function to a path '''
    return nspath_eval(path, get_namespaces())

def TimePeriod(start, end):
    ''' gml TimePeriod construction '''
    return ("start: " + str(start) + " " + "end: " + str(end))

def parseGDAReferencedElement(gdaMember, elementName):
    """Function to parse an element of a "GetDataAvailability" member"""
    element = testXMLAttribute(gdaMember.find(nspv(elementName)), nspv("xlink:href"))
    return(element)

def gda2_member(gdaMember):
    return gda_member(gdaMember, 'gda2')

def gda_member(gdaMember, gdaPrefix='gda'):
    """Function to parse each "GetDataAvailability" member"""
    #Prefixes
    gdaProcedureName = gdaPrefix + ":procedure"
    gdaObservedPropertyName = gdaPrefix + ":observedProperty"
    gdaFeatureOfInterestName = gdaPrefix + ":featureOfInterest"
    gdaOfferingName = gdaPrefix + ":offering"
    gdaPhenomenonTime = gdaPrefix + ":phenomenonTime"
    gdaResultTime = gdaPrefix + ":resultTime"

    #Applying a parsing function to the elements
    procedure_gda = parseGDAReferencedElement(gdaMember, gdaProcedureName)
    observedProperty_gda = parseGDAReferencedElement(gdaMember, gdaObservedPropertyName)
    featureOfInterest_gda = parseGDAReferencedElement(gdaMember, gdaFeatureOfInterestName)
    offering_gda = parseGDAReferencedElement(gdaMember, gdaOfferingName)

    ''' Determine if phenomenonTime is instant or period. This
    depend on the type of observation '''
    pt_gml_id = parseGDAReferencedElement(gdaMember, gdaPhenomenonTime)
    if pt_gml_id is not None:
        phenomenonTime_gda = None
        resultTime_gda = None
        start = None
        end = None
    else:
        instant_element = gdaMember.find(nspv(
            gdaPhenomenonTime + "/gml32:TimeInstant"))
        if instant_element is not None:
            pt_gml_id = testXMLAttribute(instant_element, nspv("gml32:id"))
            phenomenonTime_gda = extract_time(instant_element)
        else:
            period_element = gdaMember.find(nspv(gdaPhenomenonTime + "/gml32:TimePeriod"))
            pt_gml_id = testXMLAttribute(period_element, nspv("gml32:id"))
            start = extract_time(period_element.find(nspv("gml32:beginPosition")))
            end = extract_time(period_element.find(nspv("gml32:endPosition")))
            phenomenonTime_gda = TimePeriod(start, end)
            resultTime_gda = extract_time(gdaMember.find(nspv(gdaResultTime + "/gml32:TimeInstant/gml32:timePosition")))

    #Constructing the results
    gda_values = [procedure_gda, observedProperty_gda, featureOfInterest_gda, offering_gda, pt_gml_id, phenomenonTime_gda, start, end, resultTime_gda]
    gda_index = ['Procedure', 'ObservedProperty','FeatureOfInterest', 'Offering', PHENOMENON_TIME_ID, PHENOMENON_TIME, START_TIME, END_TIME, 'ResultTime']
    a = pd.Series(gda_values, index=gda_index, name="gda_member")
    return(a)

def _get_gda_for_id(id, gdaMembers):
    validId = id.replace('#', '')
    for gdaMember in gdaMembers:
        if gdaMember.get(PHENOMENON_TIME_ID) == validId:
            return gdaMember
    return None

def check_gda_references(gdaMembers):
    for gdaMember in gdaMembers:
            if gdaMember.get(PHENOMENON_TIME_ID).startswith('#'):
                data = _get_gda_for_id(gdaMember.get(PHENOMENON_TIME_ID), gdaMembers)
                if data is not None:
                    gdaMember.at[PHENOMENON_TIME_ID] = None
                    gdaMember.at[PHENOMENON_TIME] = data.get(PHENOMENON_TIME)
                    gdaMember.at[START_TIME] = data.get(START_TIME)
                    gdaMember.at[END_TIME] = data.get(END_TIME)
    return gdaMembers

def check_list_param(list_param):
    ''' Check parameters conditions and if the condition is not satisfied the program will stop and give an assertion error '''
    correctness = (isinstance(list_param, list) and \
    len(list_param) > 0 and \
    map(lambda x: isinstance(x, str), list_param))
    assert (correctness),("A non-empty list of strings is expected!")
