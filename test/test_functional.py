import pytest
import re
import inspect
from test.TestUtils import TestUtils
from plant_care_advisor import *

test_obj = TestUtils()

def test_function_structure():
    """Test if required functions use proper conditional structures"""
    try:
        # Check function definitions with if-else structures
        functions_to_check = {
            'calculate_watering_schedule': r'if.*elif.*elif.*elif',
            'adjust_for_season': r'if.*elif.*else',
            'check_temperature': r'if.*elif.*else',
            'determine_humidity_needs': r'if.*elif.*else'
        }
        
        for func_name, func in [(n, globals()[n]) for n in functions_to_check]:
            code = inspect.getsource(func)
            pattern = functions_to_check[func_name]
            assert re.search(pattern, code.replace('\n', ' '), re.DOTALL), f"{func_name} missing required conditional structure"
        
        test_obj.yakshaAssert("TestFunctionStructure", True, "functional")
    except Exception:
        test_obj.yakshaAssert("TestFunctionStructure", False, "functional")

def test_calculation_logic():
    """Test if calculation logic is implemented correctly"""
    try:
        # Test watering schedule calculations
        watering_correct = (
            calculate_watering_schedule(1) == 14 and  # Succulent
            calculate_watering_schedule(2) == 3 and   # Tropical
            calculate_watering_schedule(3) == 2 and   # Flowering
            calculate_watering_schedule(4) == 1       # Herb
        )
        
        # Test season adjustment
        season_correct = (
            adjust_for_season(7, 1) == 7 and  # Spring - no change
            adjust_for_season(7, 2) == 6 and  # Summer - decrease
            adjust_for_season(7, 3) == 7 and  # Fall - no change
            adjust_for_season(7, 4) == 8      # Winter - increase
        )
        
        # Test minimum adjustment for summer
        summer_min_correct = adjust_for_season(1, 2) == 1  # Minimum of 1 day
        
        test_obj.yakshaAssert("TestCalculationLogic", 
                            watering_correct and season_correct and summer_min_correct, 
                            "functional")
    except Exception:
        test_obj.yakshaAssert("TestCalculationLogic", False, "functional")

def test_environmental_assessment():
    """Test if environmental assessment functions work correctly"""
    try:
        # Test temperature checks
        temperature_correct = (
            check_temperature(35.0) == "Temperature too high - Risk of heat stress" and
            check_temperature(5.0) == "Temperature too low - Risk of cold damage" and
            check_temperature(20.0) == "Temperature optimal for plant growth"
        )
        
        # Test humidity assessment
        humidity_low, advice_low = determine_humidity_needs(20)
        humidity_med, advice_med = determine_humidity_needs(45)
        humidity_high, advice_high = determine_humidity_needs(70)
        
        humidity_correct = (
            humidity_low == "Low" and advice_low == "Increase humidity with misting" and
            humidity_med == "Medium" and advice_med == "Humidity is optimal" and
            humidity_high == "High" and advice_high == "Monitor for fungal growth"
        )
        
        # Test sunlight requirements
        sunlight_correct = (
            get_sunlight_requirement(1) == "Full sun to partial shade" and
            get_sunlight_requirement(2) == "Bright indirect light" and
            get_sunlight_requirement(3) == "Full sun" and
            get_sunlight_requirement(4) == "At least 6 hours of direct sunlight"
        )
        
        test_obj.yakshaAssert("TestEnvironmentalAssessment", 
                            temperature_correct and humidity_correct and sunlight_correct, 
                            "functional")
    except Exception:
        test_obj.yakshaAssert("TestEnvironmentalAssessment", False, "functional")

def test_care_instructions():
    """Test if care instructions are generated with all required components"""
    try:
        # Test each plant type's specific care instruction
        plant_instructions = {
            1: "Avoid overwatering",               # Succulent
            2: "Maintain high humidity",           # Tropical
            3: "Remove dead flowers regularly",    # Flowering
            4: "Harvest regularly to promote growth"  # Herb
        }
        
        # Test seasonal advice
        seasonal_advice = {
            2: "Increase watering frequency",  # Summer
            4: "Reduce watering frequency"     # Winter
        }
        
        all_correct = True
        
        # Check all plant types
        for plant_type, expected_care in plant_instructions.items():
            instructions = generate_care_instructions(plant_type, 1, 25.0, 45)
            if expected_care not in instructions:
                all_correct = False
                break
        
        # Check seasonal advice
        for season, expected_advice in seasonal_advice.items():
            instructions = generate_care_instructions(1, season, 25.0, 45)
            if expected_advice not in instructions:
                all_correct = False
                break
        
        # Check required sections
        required_sections = [
            "Watering Schedule: Every",
            "Sunlight Requirement:",
            "Temperature Status:",
            "Humidity Level:",
            "Special Care Instructions:"
        ]
        
        sample_instructions = generate_care_instructions(2, 1, 25.0, 45)
        for section in required_sections:
            if section not in sample_instructions:
                all_correct = False
                break
        
        test_obj.yakshaAssert("TestCareInstructions", all_correct, "functional")
    except Exception:
        test_obj.yakshaAssert("TestCareInstructions", False, "functional")