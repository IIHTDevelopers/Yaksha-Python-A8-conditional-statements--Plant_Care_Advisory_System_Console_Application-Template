import pytest
from test.TestUtils import TestUtils
from plant_care_advisor import *

test_obj = TestUtils()

def test_input_range_exceptions():
    """Test input range validation across all functions"""
    try:
        # Plant type range validation
        with pytest.raises(ValueError):
            calculate_watering_schedule(0)    # Too low
        with pytest.raises(ValueError):
            calculate_watering_schedule(5)    # Too high
            
        # Season range validation
        with pytest.raises(ValueError):
            adjust_for_season(7, 0)    # Season too low
        with pytest.raises(ValueError):
            adjust_for_season(7, 5)    # Season too high
            
        # Temperature range validation
        with pytest.raises(ValueError):
            check_temperature(-10.1)   # Too cold
        with pytest.raises(ValueError):
            check_temperature(50.1)    # Too hot
            
        # Humidity range validation
        with pytest.raises(ValueError):
            determine_humidity_needs(-1)    # Negative humidity
        with pytest.raises(ValueError):
            determine_humidity_needs(101)   # Humidity too high
        
        test_obj.yakshaAssert("TestInputRangeExceptions", True, "exception")
    except Exception as e:
        test_obj.yakshaAssert("TestInputRangeExceptions", False, "exception")

def test_input_type_exceptions():
    """Test input type validation across functions"""
    try:
        # Test type validation in various functions
        with pytest.raises(ValueError):
            calculate_watering_schedule("succulent")  # String instead of int
            
        with pytest.raises(ValueError):
            adjust_for_season("weekly", 2)  # String instead of int
            
        with pytest.raises(ValueError):
            check_temperature("hot")  # String instead of float
            
        with pytest.raises(ValueError):
            determine_humidity_needs("humid")  # String instead of int
            
        test_obj.yakshaAssert("TestInputTypeExceptions", True, "exception")
    except Exception as e:
        test_obj.yakshaAssert("TestInputTypeExceptions", False, "exception")