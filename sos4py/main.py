# -*- coding: utf-8 -*-
############################################################################## #
#                                                                              #
# Author: Alfredo Chavarria (a.h.chavarriavargas@utwente.student.nl)           #
# Created: 2020-05-28                                                          #
# Project: sos4py - https://github.com/52North/sos4py                          #
#                                                                              #
############################################################################## #

"""Main module."""

# Import functions from other libraries
from owslib.util import clean_ows_url
from .sos_2_0_0 import sos_2_0_0

def connection_sos(url,
             xml=None,
             username=None,
             password=None,):
    """
    SOS GetDataAvailability function
    :param url: url of capabilities document
    :param xml: elementtree object
    :param username: username allowed to handle with SOS
    :param password: password for the username
    :return: a sos_2_0_0 object
    """
    clean_url = clean_ows_url(url) # Clean an OWS URL of basic service elements
    version = "2.0.0"
    return sos_2_0_0.__new__(sos_2_0_0, clean_url, version, xml, username, password)


