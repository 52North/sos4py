from sos4py.main import connection_sos
from sos4py.sos_2_0_0 import SOSGetFeatureOfInterestResponse

BOM_URL = "http://www.bom.gov.au/waterdata/services"

def test_create_sos():
    bom_sos = connection_sos(BOM_URL)
    assert bom_sos is not None

def test_ident_service():
    bom_sos = connection_sos(BOM_URL)
    provider = bom_sos.sosProvider()
    assert provider is not None
    ops = bom_sos.sosOperationsMetadata()
    assert ops is not None
    expected_verbs = ["GetCapabilities",
                      "GetDataAvailability",
                      "GetFeatureOfInterest",
                      "GetObservation",
                      "DescribeSensor"]
    for op in ops:
        assert op.name in expected_verbs

def test_get_feature_of_interest():
    bom_sos = connection_sos(BOM_URL)
    include_phenomena = False
    bom_sites = bom_sos.get_sites(include_phenomena)
    assert bom_sites is not None
    assert len(bom_sites) > 0

def test_get_data_availability():
    bom_sos = connection_sos(BOM_URL)
    data_avail = bom_sos.get_data_availability(procedures=["http://bom.gov.au/waterdata/services/tstypes/Pat4_C_B_1_DailyMean"])
    assert data_avail is not None
    assert len(data_avail) > 0

def test_get_observation():
    bom_sos = connection_sos(BOM_URL)
    obs = bom_sos.get_observation(procedure="http://bom.gov.au/waterdata/services/tstypes/Pat4_C_B_1_DailyMean",
                                   feature_of_interest="http://bom.gov.au/waterdata/services/stations/105107A",
                                   observed_property="http://bom.gov.au/waterdata/services/parameters/Water Course Discharge",
                                   response_format="application/x-kvp")
    assert obs is not None
    assert len(obs) > 0
