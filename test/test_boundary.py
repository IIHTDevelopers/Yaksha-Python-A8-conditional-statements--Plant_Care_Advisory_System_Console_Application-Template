import unittest
import os
import importlib
import sys
import io
import contextlib
from test.TestUtils import TestUtils

def check_file_exists(filename):
    """Check if a file exists in the current directory."""
    return os.path.exists(filename)

def safely_import_module(module_name):
    """Safely import a module, returning None if import fails."""
    try:
        return importlib.import_module(module_name)
    except ImportError:
        return None

def check_function_exists(module, function_name):
    """Check if a function exists in a module."""
    return hasattr(module, function_name) and callable(getattr(module, function_name))

def safely_call_function(module, function_name, *args, **kwargs):
    """Safely call a function, returning None if it fails."""
    if not check_function_exists(module, function_name):
        return None
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            return getattr(module, function_name)(*args, **kwargs)
    except Exception:
        return None

def load_module_dynamically():
    """Load the student's module for testing"""
    module_obj = safely_import_module("skeleton")
    if module_obj is None:
        module_obj = safely_import_module("solution")
    return module_obj

def is_implementation_functional(module_obj):
    """Check if the implementation is functional by testing basic operations"""
    if module_obj is None:
        return False
    
    try:
        # Test basic functionality of each required function
        functions_to_test = [
            ("calculate_watering_schedule", [1]),
            ("adjust_for_season", [7, 1]),
            ("check_temperature", [25.0]),
            ("determine_humidity_needs", [50]),
            ("get_sunlight_requirement", [1])
        ]
        
        for func_name, args in functions_to_test:
            result = safely_call_function(module_obj, func_name, *args)
            if result is None:
                return False
        
        return True
    except Exception:
        return False

class TestPlantCareBoundary(unittest.TestCase):
    """Test class for boundary value testing of the Plant Care Advisory System."""
    
    def setUp(self):
        """Setup test data before each test method."""
        self.test_obj = TestUtils()
        self.module_obj = load_module_dynamically()
    
    def test_comprehensive_boundary_scenarios(self):
        """Comprehensive test for all boundary scenarios across all functions"""
        try:
            # Check if module can be imported
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestComprehensiveBoundaryScenarios", False, "boundary")
                print("TestComprehensiveBoundaryScenarios = Failed")
                return
            
            # Check if implementation is functional
            if not is_implementation_functional(self.module_obj):
                self.test_obj.yakshaAssert("TestComprehensiveBoundaryScenarios", False, "boundary")
                print("TestComprehensiveBoundaryScenarios = Failed")
                return
            
            errors = []
            
            # Test all required functions exist
            required_functions = [
                "calculate_watering_schedule",
                "adjust_for_season",
                "check_temperature",
                "determine_humidity_needs",
                "get_sunlight_requirement"
            ]
            
            missing_functions = []
            for func_name in required_functions:
                if not check_function_exists(self.module_obj, func_name):
                    missing_functions.append(func_name)
            
            if missing_functions:
                errors.append(f"Missing required functions: {', '.join(missing_functions)}")
                self.test_obj.yakshaAssert("TestComprehensiveBoundaryScenarios", False, "boundary")
                print("TestComprehensiveBoundaryScenarios = Failed")
                return
            
            # === WATERING SCHEDULE BOUNDARIES ===
            
            if check_function_exists(self.module_obj, "calculate_watering_schedule"):
                watering_boundary_tests = [
                    (1, 14, "Succulent (minimum plant type) should return 14 days"),
                    (4, 1, "Herb (maximum plant type) should return 1 day"),
                    (2, 3, "Tropical (middle value) should return 3 days"),
                    (3, 2, "Flowering (middle value) should return 2 days")
                ]
                
                for plant_type, expected, message in watering_boundary_tests:
                    result = safely_call_function(self.module_obj, "calculate_watering_schedule", plant_type)
                    if result is None:
                        errors.append(f"calculate_watering_schedule({plant_type}) returned None")
                    elif not isinstance(result, int):
                        errors.append(f"calculate_watering_schedule({plant_type}) should return an integer, got {type(result)}")
                    elif result != expected:
                        errors.append(f"calculate_watering_schedule({plant_type}) returned {result}, expected {expected}: {message}")
            else:
                errors.append("calculate_watering_schedule function not found")
            
            # === SEASON ADJUSTMENT BOUNDARIES ===
            
            if check_function_exists(self.module_obj, "adjust_for_season"):
                season_boundary_tests = [
                    # (days, season, expected, description)
                    (1, 2, 1, "Summer adjustment should maintain minimum of 1 day"),
                    (2, 2, 1, "Summer adjustment should decrease by 1"),
                    (14, 2, 13, "Summer adjustment of large value"),
                    (1, 4, 2, "Winter adjustment should increase by 1"),
                    (14, 4, 15, "Winter adjustment of large value"),
                    (7, 1, 7, "Spring should not change watering days"),
                    (7, 3, 7, "Fall should not change watering days"),
                    (1, 1, 1, "Spring with minimum days"),
                    (1, 3, 1, "Fall with minimum days"),
                    (3, 2, 2, "Summer adjustment maintaining reasonable minimum"),
                    (10, 4, 11, "Winter adjustment for moderate days"),
                    (5, 1, 5, "Spring adjustment maintaining original"),
                    (8, 3, 8, "Fall adjustment maintaining original")
                ]
                
                for days, season, expected, description in season_boundary_tests:
                    result = safely_call_function(self.module_obj, "adjust_for_season", days, season)
                    if result is None:
                        errors.append(f"adjust_for_season({days}, {season}) returned None")
                    elif not isinstance(result, int):
                        errors.append(f"adjust_for_season({days}, {season}) should return an integer, got {type(result)}")
                    elif result != expected:
                        errors.append(f"adjust_for_season({days}, {season}) returned {result}, expected {expected}: {description}")
            else:
                errors.append("adjust_for_season function not found")
            
            # === TEMPERATURE BOUNDARIES ===
            
            if check_function_exists(self.module_obj, "check_temperature"):
                temperature_boundary_tests = [
                    # (temperature, expected_keyword, description)
                    (30.1, "too high", "Just above optimal upper bound should be too high"),
                    (30.0, "optimal", "Exact upper boundary should be optimal"),
                    (10.0, "optimal", "Exact lower boundary should be optimal"),
                    (9.9, "too low", "Just below optimal lower bound should be too low"),
                    (50.0, "too high", "Maximum allowed temperature should be too high"),
                    (-10.0, "too low", "Minimum allowed temperature should be too low"),
                    (20.0, "optimal", "Middle temperature should be optimal"),
                    (25.5, "optimal", "Typical room temperature should be optimal"),
                    (35.0, "too high", "High summer temperature should be too high"),
                    (5.0, "too low", "Cold winter temperature should be too low"),
                    (15.0, "optimal", "Cool but optimal temperature"),
                    (28.0, "optimal", "Warm but optimal temperature")
                ]
                
                for temperature, expected_keyword, description in temperature_boundary_tests:
                    result = safely_call_function(self.module_obj, "check_temperature", temperature)
                    if result is None:
                        errors.append(f"check_temperature({temperature}) returned None")
                    elif not isinstance(result, str):
                        errors.append(f"check_temperature({temperature}) should return a string, got {type(result)}")
                    elif expected_keyword.lower() not in result.lower():
                        errors.append(f"check_temperature({temperature}) returned '{result}', expected to contain '{expected_keyword}': {description}")
            else:
                errors.append("check_temperature function not found")
            
            # === HUMIDITY BOUNDARIES ===
            
            if check_function_exists(self.module_obj, "determine_humidity_needs"):
                humidity_boundary_tests = [
                    # (humidity, expected_level, expected_advice_keyword, description)
                    (0, "Low", "misting", "Minimum humidity should be Low with misting advice"),
                    (29, "Low", "misting", "Just below medium threshold should be Low"),
                    (30, "Medium", "optimal", "Lower boundary of medium should be Medium"),
                    (60, "Medium", "optimal", "Upper boundary of medium should be Medium"),
                    (61, "High", "fungal", "Just above medium threshold should be High"),
                    (100, "High", "fungal", "Maximum humidity should be High with fungal warning"),
                    (45, "Medium", "optimal", "Middle humidity should be Medium"),
                    (15, "Low", "misting", "Very low humidity should be Low"),
                    (85, "High", "fungal", "Very high humidity should be High"),
                    (1, "Low", "misting", "Very minimum humidity should be Low"),
                    (28, "Low", "misting", "Edge case just below medium"),
                    (31, "Medium", "optimal", "Just above low threshold"),
                    (59, "Medium", "optimal", "Just below high threshold"),
                    (62, "High", "fungal", "Just above medium threshold"),
                    (99, "High", "fungal", "Near maximum humidity")
                ]
                
                for humidity, expected_level, expected_advice, description in humidity_boundary_tests:
                    result = safely_call_function(self.module_obj, "determine_humidity_needs", humidity)
                    if result is None:
                        errors.append(f"determine_humidity_needs({humidity}) returned None")
                    elif not isinstance(result, tuple) or len(result) != 2:
                        errors.append(f"determine_humidity_needs({humidity}) should return a tuple of 2 elements, got {type(result)}")
                    else:
                        level, advice = result
                        if not isinstance(level, str):
                            errors.append(f"determine_humidity_needs({humidity}) level should be a string, got {type(level)}")
                        elif level != expected_level:
                            errors.append(f"determine_humidity_needs({humidity}) returned level '{level}', expected '{expected_level}': {description}")
                        
                        if not isinstance(advice, str):
                            errors.append(f"determine_humidity_needs({humidity}) advice should be a string, got {type(advice)}")
                        elif expected_advice.lower() not in advice.lower():
                            errors.append(f"determine_humidity_needs({humidity}) advice '{advice}' should contain '{expected_advice}': {description}")
            else:
                errors.append("determine_humidity_needs function not found")
            
            # === SUNLIGHT REQUIREMENT BOUNDARIES ===
            
            if check_function_exists(self.module_obj, "get_sunlight_requirement"):
                sunlight_boundary_tests = [
                    (1, ["sun", "shade"], "Succulent (minimum plant type) should mention both sun and shade"),
                    (4, ["direct", "hours"], "Herb (maximum plant type) should need direct sunlight with hours"),
                    (2, ["indirect"], "Tropical (middle value) should need indirect light"),
                    (3, ["full sun"], "Flowering (middle value) should need full sun")
                ]
                
                for plant_type, expected_keywords, description in sunlight_boundary_tests:
                    result = safely_call_function(self.module_obj, "get_sunlight_requirement", plant_type)
                    if result is None:
                        errors.append(f"get_sunlight_requirement({plant_type}) returned None")
                    elif not isinstance(result, str):
                        errors.append(f"get_sunlight_requirement({plant_type}) should return a string, got {type(result)}")
                    elif not all(keyword.lower() in result.lower() for keyword in expected_keywords):
                        errors.append(f"get_sunlight_requirement({plant_type}) returned '{result}', expected to contain {expected_keywords}: {description}")
            else:
                errors.append("get_sunlight_requirement function not found")
            
            # === INTEGRATION BOUNDARY TESTING ===
            
            # Test boundary combinations that should work together
            if all(check_function_exists(self.module_obj, func) for func in required_functions):
                integration_boundary_tests = [
                    # (plant_type, season, temp, humidity, expected_watering_days, description)
                    (1, 2, 30.0, 30, 13, "Succulent in summer at boundary temperature and humidity"),
                    (4, 4, 10.0, 60, 2, "Herb in winter at boundary temperature and humidity"),
                    (2, 1, -10.0, 0, 3, "Tropical in spring at minimum boundaries"),
                    (3, 3, 50.0, 100, 2, "Flowering in fall at maximum boundaries")
                ]
                
                for plant_type, season, temp, humidity, expected_days, description in integration_boundary_tests:
                    # Test individual functions
                    base_days = safely_call_function(self.module_obj, "calculate_watering_schedule", plant_type)
                    if base_days is None:
                        errors.append(f"Integration boundary test failed: calculate_watering_schedule returned None for {description}")
                        continue
                    
                    adjusted_days = safely_call_function(self.module_obj, "adjust_for_season", base_days, season)
                    if adjusted_days is None:
                        errors.append(f"Integration boundary test failed: adjust_for_season returned None for {description}")
                        continue
                    elif adjusted_days != expected_days:
                        errors.append(f"Integration boundary test failed: Expected {expected_days} days but got {adjusted_days} for {description}")
                    
                    temp_result = safely_call_function(self.module_obj, "check_temperature", temp)
                    if temp_result is None:
                        errors.append(f"Integration boundary test failed: check_temperature returned None for {description}")
                    
                    humidity_result = safely_call_function(self.module_obj, "determine_humidity_needs", humidity)
                    if humidity_result is None:
                        errors.append(f"Integration boundary test failed: determine_humidity_needs returned None for {description}")
                    
                    sunlight_result = safely_call_function(self.module_obj, "get_sunlight_requirement", plant_type)
                    if sunlight_result is None:
                        errors.append(f"Integration boundary test failed: get_sunlight_requirement returned None for {description}")
            
            # Final result checking
            if errors:
                self.test_obj.yakshaAssert("TestComprehensiveBoundaryScenarios", False, "boundary")
                print("TestComprehensiveBoundaryScenarios = Failed")
            else:
                self.test_obj.yakshaAssert("TestComprehensiveBoundaryScenarios", True, "boundary")
                print("TestComprehensiveBoundaryScenarios = Passed")
                
        except Exception as e:
            self.test_obj.yakshaAssert("TestComprehensiveBoundaryScenarios", False, "boundary")
            print("TestComprehensiveBoundaryScenarios = Failed")

if __name__ == '__main__':
    unittest.main()