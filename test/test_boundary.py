import pytest
from test.TestUtils import TestUtils
from plant_care_advisor import *

test_obj = TestUtils()

def test_watering_and_season_boundary():
    """Test watering schedule and season adjustment with boundary values"""
    try:
        # Watering schedule boundaries
        watering_max = calculate_watering_schedule(1) == 14
        watering_min = calculate_watering_schedule(4) == 1
        
        # Season adjustment boundaries
        season_min = adjust_for_season(1, 2) == 1     # Minimum days (summer)
        season_max = adjust_for_season(14, 4) == 15   # Maximum days (winter)
        
        test_obj.yakshaAssert("TestWateringAndSeasonBoundary", 
                            watering_max and watering_min and season_min and season_max, 
                            "boundary")
    except Exception as e:
        test_obj.yakshaAssert("TestWateringAndSeasonBoundary", False, "boundary")

def test_environment_boundary():
    """Test temperature and humidity with boundary values"""
    try:
        # Temperature boundaries
        temp_high = "too high" in check_temperature(30.1).lower()
        temp_low = "too low" in check_temperature(9.9).lower()
        temp_upper = "optimal" in check_temperature(30.0).lower()
        temp_lower = "optimal" in check_temperature(10.0).lower()
        
        # Humidity boundaries
        level1, _ = determine_humidity_needs(0)    # Minimum humidity
        level2, _ = determine_humidity_needs(100)  # Maximum humidity
        level3, _ = determine_humidity_needs(30)   # Low-Medium boundary
        level4, _ = determine_humidity_needs(60)   # Medium-High boundary
        humidity_correct = (level1 == "Low" and level2 == "High" and 
                          level3 == "Medium" and level4 == "Medium")
        
        test_obj.yakshaAssert("TestEnvironmentBoundary", 
                            temp_high and temp_low and temp_upper and temp_lower and humidity_correct, 
                            "boundary")
    except Exception as e:
        test_obj.yakshaAssert("TestEnvironmentBoundary", False, "boundary")