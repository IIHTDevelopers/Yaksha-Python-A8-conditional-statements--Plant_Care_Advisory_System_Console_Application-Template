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

def check_raises_exception(func, args, expected_exception=ValueError):
    """Check if a function raises the expected exception type."""
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            func(*args)
        return False  # No exception was raised
    except expected_exception:
        return True  # Expected exception was raised
    except Exception:
        return False  # Different exception was raised

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

class TestPlantCareException(unittest.TestCase):
    """Test class for exception handling in the Plant Care Advisory System."""
    
    def setUp(self):
        """Setup test data before each test method."""
        self.test_obj = TestUtils()
        self.module_obj = load_module_dynamically()
    
    def test_comprehensive_exception_handling(self):
        """Comprehensive test for all exception scenarios across all functions"""
        try:
            # Check if module can be imported
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestComprehensiveExceptionHandling", False, "exception")
                print("TestComprehensiveExceptionHandling = Failed")
                return
            
            # Check if implementation is functional
            if not is_implementation_functional(self.module_obj):
                self.test_obj.yakshaAssert("TestComprehensiveExceptionHandling", False, "exception")
                print("TestComprehensiveExceptionHandling = Failed")
                return
            
            errors = []
            
            # Test all required functions exist
            required_functions = [
                "calculate_watering_schedule",
                "adjust_for_season", 
                "check_temperature",
                "determine_humidity_needs",
                "get_sunlight_requirement",
                "generate_care_instructions"
            ]
            
            missing_functions = []
            for func_name in required_functions:
                if not check_function_exists(self.module_obj, func_name):
                    missing_functions.append(func_name)
            
            if missing_functions:
                errors.append(f"Missing required functions: {', '.join(missing_functions)}")
                self.test_obj.yakshaAssert("TestComprehensiveExceptionHandling", False, "exception")
                print("TestComprehensiveExceptionHandling = Failed")
                return
            
            # === INPUT RANGE VALIDATION TESTS ===
            
            # Plant type range validation for calculate_watering_schedule and get_sunlight_requirement
            plant_functions = ["calculate_watering_schedule", "get_sunlight_requirement"]
            plant_range_tests = [
                (0, "Plant type 0 should raise ValueError (too low)"),
                (5, "Plant type 5 should raise ValueError (too high)"),
                (-1, "Plant type -1 should raise ValueError (negative)"),
                (10, "Plant type 10 should raise ValueError (way too high)")
            ]
            
            for func_name in plant_functions:
                if check_function_exists(self.module_obj, func_name):
                    for plant_type, description in plant_range_tests:
                        if not check_raises_exception(getattr(self.module_obj, func_name), [plant_type], ValueError):
                            errors.append(f"{func_name} does not raise ValueError for plant type {plant_type}: {description}")
                else:
                    errors.append(f"{func_name} function not found")
            
            # Season range validation for adjust_for_season
            if check_function_exists(self.module_obj, "adjust_for_season"):
                season_range_tests = [
                    (7, 0, "Season 0 should raise ValueError (too low)"),
                    (7, 5, "Season 5 should raise ValueError (too high)"),
                    (7, -1, "Season -1 should raise ValueError (negative)"),
                    (7, 10, "Season 10 should raise ValueError (way too high)")
                ]
                
                for days, season, description in season_range_tests:
                    if not check_raises_exception(self.module_obj.adjust_for_season, [days, season], ValueError):
                        errors.append(f"adjust_for_season does not raise ValueError for season {season}: {description}")
                
                # Test negative days
                if not check_raises_exception(self.module_obj.adjust_for_season, [-1, 2], ValueError):
                    errors.append("adjust_for_season does not raise ValueError for negative days")
            else:
                errors.append("adjust_for_season function not found")
            
            # Temperature range validation
            if check_function_exists(self.module_obj, "check_temperature"):
                temp_range_tests = [
                    (-10.1, "Temperature -10.1 should raise ValueError (too cold)"),
                    (50.1, "Temperature 50.1 should raise ValueError (too hot)"),
                    (-100.0, "Temperature -100.0 should raise ValueError (extremely cold)"),
                    (100.0, "Temperature 100.0 should raise ValueError (extremely hot)")
                ]
                
                for temperature, description in temp_range_tests:
                    if not check_raises_exception(self.module_obj.check_temperature, [temperature], ValueError):
                        errors.append(f"check_temperature does not raise ValueError for temperature {temperature}: {description}")
            else:
                errors.append("check_temperature function not found")
            
            # Humidity range validation
            if check_function_exists(self.module_obj, "determine_humidity_needs"):
                humidity_range_tests = [
                    (-1, "Humidity -1 should raise ValueError (negative)"),
                    (101, "Humidity 101 should raise ValueError (too high)"),
                    (-10, "Humidity -10 should raise ValueError (very negative)"),
                    (200, "Humidity 200 should raise ValueError (way too high)")
                ]
                
                for humidity, description in humidity_range_tests:
                    if not check_raises_exception(self.module_obj.determine_humidity_needs, [humidity], ValueError):
                        errors.append(f"determine_humidity_needs does not raise ValueError for humidity {humidity}: {description}")
            else:
                errors.append("determine_humidity_needs function not found")
            
            # === INPUT TYPE VALIDATION TESTS ===
            
            # Test invalid types for all functions
            invalid_types = [
                ("string", "String input should raise ValueError"),
                (2.5, "Float input should raise ValueError"),
                (None, "None input should raise ValueError"),
                ([], "List input should raise ValueError"),
                ({}, "Dictionary input should raise ValueError"),
                (True, "Boolean input should raise ValueError")
            ]
            
            # Plant type validation for calculate_watering_schedule and get_sunlight_requirement
            for func_name in plant_functions:
                if check_function_exists(self.module_obj, func_name):
                    for invalid_input, description in invalid_types:
                        if not check_raises_exception(getattr(self.module_obj, func_name), [invalid_input], ValueError):
                            errors.append(f"{func_name} does not raise ValueError for {type(invalid_input).__name__} input: {description}")
                else:
                    errors.append(f"{func_name} function not found")
            
            # Season and days validation for adjust_for_season
            if check_function_exists(self.module_obj, "adjust_for_season"):
                # Test invalid days types
                for invalid_input, description in invalid_types:
                    if not check_raises_exception(self.module_obj.adjust_for_season, [invalid_input, 2], ValueError):
                        errors.append(f"adjust_for_season does not raise ValueError for {type(invalid_input).__name__} days: {description}")
                
                # Test invalid season types
                for invalid_input, description in invalid_types:
                    if not check_raises_exception(self.module_obj.adjust_for_season, [7, invalid_input], ValueError):
                        errors.append(f"adjust_for_season does not raise ValueError for {type(invalid_input).__name__} season: {description}")
            else:
                errors.append("adjust_for_season function not found")
            
            # Temperature validation
            if check_function_exists(self.module_obj, "check_temperature"):
                temp_invalid_types = [
                    ("hot", "String temperature should raise ValueError"),
                    (None, "None temperature should raise ValueError"),
                    ([], "List temperature should raise ValueError"),
                    ({}, "Dictionary temperature should raise ValueError"),
                    ("25.0", "String number should raise ValueError"),
                    (True, "Boolean temperature should raise ValueError")
                ]
                
                for invalid_temp, description in temp_invalid_types:
                    if not check_raises_exception(self.module_obj.check_temperature, [invalid_temp], ValueError):
                        errors.append(f"check_temperature does not raise ValueError for {type(invalid_temp).__name__} input: {description}")
            else:
                errors.append("check_temperature function not found")
            
            # Humidity validation
            if check_function_exists(self.module_obj, "determine_humidity_needs"):
                for invalid_input, description in invalid_types:
                    if not check_raises_exception(self.module_obj.determine_humidity_needs, [invalid_input], ValueError):
                        errors.append(f"determine_humidity_needs does not raise ValueError for {type(invalid_input).__name__} input: {description}")
            else:
                errors.append("determine_humidity_needs function not found")
            
            # === GENERATE_CARE_INSTRUCTIONS COMPREHENSIVE TESTING ===
            
            if check_function_exists(self.module_obj, "generate_care_instructions"):
                # Test invalid plant types
                plant_type_tests = [
                    (0, 1, 25.0, 50, "Plant type 0 should raise ValueError"),
                    (5, 1, 25.0, 50, "Plant type 5 should raise ValueError"),
                    ("tropical", 1, 25.0, 50, "String plant type should raise ValueError"),
                    (None, 1, 25.0, 50, "None plant type should raise ValueError"),
                    (2.5, 1, 25.0, 50, "Float plant type should raise ValueError"),
                    ([], 1, 25.0, 50, "List plant type should raise ValueError"),
                    (True, 1, 25.0, 50, "Boolean plant type should raise ValueError")
                ]
                
                for plant_type, season, temp, humidity, description in plant_type_tests:
                    if not check_raises_exception(self.module_obj.generate_care_instructions, [plant_type, season, temp, humidity], ValueError):
                        errors.append(f"generate_care_instructions does not raise ValueError: {description}")
                
                # Test invalid seasons
                season_tests = [
                    (1, 0, 25.0, 50, "Season 0 should raise ValueError"),
                    (1, 5, 25.0, 50, "Season 5 should raise ValueError"),
                    (1, "summer", 25.0, 50, "String season should raise ValueError"),
                    (1, None, 25.0, 50, "None season should raise ValueError"),
                    (1, 2.5, 25.0, 50, "Float season should raise ValueError"),
                    (1, [], 25.0, 50, "List season should raise ValueError"),
                    (1, True, 25.0, 50, "Boolean season should raise ValueError")
                ]
                
                for plant_type, season, temp, humidity, description in season_tests:
                    if not check_raises_exception(self.module_obj.generate_care_instructions, [plant_type, season, temp, humidity], ValueError):
                        errors.append(f"generate_care_instructions does not raise ValueError: {description}")
                
                # Test invalid temperatures
                temp_tests = [
                    (1, 1, -11.0, 50, "Temperature -11.0 should raise ValueError"),
                    (1, 1, 51.0, 50, "Temperature 51.0 should raise ValueError"),
                    (1, 1, "hot", 50, "String temperature should raise ValueError"),
                    (1, 1, None, 50, "None temperature should raise ValueError"),
                    (1, 1, [], 50, "List temperature should raise ValueError"),
                    (1, 1, {}, 50, "Dict temperature should raise ValueError"),
                    (1, 1, True, 50, "Boolean temperature should raise ValueError")
                ]
                
                for plant_type, season, temp, humidity, description in temp_tests:
                    if not check_raises_exception(self.module_obj.generate_care_instructions, [plant_type, season, temp, humidity], ValueError):
                        errors.append(f"generate_care_instructions does not raise ValueError: {description}")
                
                # Test invalid humidity
                humidity_tests = [
                    (1, 1, 25.0, -1, "Humidity -1 should raise ValueError"),
                    (1, 1, 25.0, 101, "Humidity 101 should raise ValueError"),
                    (1, 1, 25.0, "humid", "String humidity should raise ValueError"),
                    (1, 1, 25.0, None, "None humidity should raise ValueError"),
                    (1, 1, 25.0, 45.5, "Float humidity should raise ValueError"),
                    (1, 1, 25.0, [], "List humidity should raise ValueError"),
                    (1, 1, 25.0, True, "Boolean humidity should raise ValueError")
                ]
                
                for plant_type, season, temp, humidity, description in humidity_tests:
                    if not check_raises_exception(self.module_obj.generate_care_instructions, [plant_type, season, temp, humidity], ValueError):
                        errors.append(f"generate_care_instructions does not raise ValueError: {description}")
            else:
                errors.append("generate_care_instructions function not found")
            
            # === EDGE CASES - VALID BOUNDARIES SHOULD NOT RAISE EXCEPTIONS ===
            
            # Test boundary values that should NOT raise exceptions (valid edge cases)
            valid_edge_cases = [
                # (function_name, args, description)
                ("calculate_watering_schedule", [1], "Plant type 1 should be valid"),
                ("calculate_watering_schedule", [4], "Plant type 4 should be valid"),
                ("adjust_for_season", [1, 1], "Minimum days and season should be valid"),
                ("adjust_for_season", [20, 4], "Large days and season 4 should be valid"),
                ("check_temperature", [-10.0], "Minimum temperature should be valid"),
                ("check_temperature", [50.0], "Maximum temperature should be valid"),
                ("determine_humidity_needs", [0], "Minimum humidity should be valid"),
                ("determine_humidity_needs", [100], "Maximum humidity should be valid"),
                ("get_sunlight_requirement", [1], "Plant type 1 should be valid for sunlight"),
                ("get_sunlight_requirement", [4], "Plant type 4 should be valid for sunlight"),
                ("generate_care_instructions", [1, 1, -10.0, 0], "Minimum boundary values should be valid"),
                ("generate_care_instructions", [4, 4, 50.0, 100], "Maximum boundary values should be valid")
            ]
            
            for func_name, args, description in valid_edge_cases:
                if check_function_exists(self.module_obj, func_name):
                    try:
                        result = safely_call_function(self.module_obj, func_name, *args)
                        if result is None:
                            errors.append(f"{func_name} returned None for valid edge case: {description}")
                    except Exception as e:
                        errors.append(f"{func_name} raised unexpected exception for valid edge case {description}: {str(e)}")
                else:
                    errors.append(f"Function {func_name} not found")
            
            # === ADDITIONAL BOOLEAN INPUT VALIDATION ===
            
            # Test specific boolean input scenarios that should be caught
            boolean_tests = [
                # Test boolean inputs that might pass isinstance(x, int) check
                ("calculate_watering_schedule", [True], "Boolean True should raise ValueError"),
                ("calculate_watering_schedule", [False], "Boolean False should raise ValueError"),
                ("get_sunlight_requirement", [True], "Boolean True should raise ValueError"),
                ("get_sunlight_requirement", [False], "Boolean False should raise ValueError"),
                ("adjust_for_season", [True, 1], "Boolean days should raise ValueError"),
                ("adjust_for_season", [1, True], "Boolean season should raise ValueError"),
                ("adjust_for_season", [False, 1], "Boolean False days should raise ValueError"),
                ("adjust_for_season", [1, False], "Boolean False season should raise ValueError"),
                ("determine_humidity_needs", [True], "Boolean True humidity should raise ValueError"),
                ("determine_humidity_needs", [False], "Boolean False humidity should raise ValueError"),
                ("check_temperature", [True], "Boolean True temperature should raise ValueError"),
                ("check_temperature", [False], "Boolean False temperature should raise ValueError")
            ]
            
            for func_name, args, description in boolean_tests:
                if check_function_exists(self.module_obj, func_name):
                    if not check_raises_exception(getattr(self.module_obj, func_name), args, ValueError):
                        errors.append(f"{func_name} does not raise ValueError: {description}")
                else:
                    errors.append(f"Function {func_name} not found for boolean test")
            
            # === COMPREHENSIVE GENERATE_CARE_INSTRUCTIONS BOOLEAN TESTS ===
            
            if check_function_exists(self.module_obj, "generate_care_instructions"):
                comprehensive_boolean_tests = [
                    (True, 1, 25.0, 50, "Boolean True plant type should raise ValueError"),
                    (False, 1, 25.0, 50, "Boolean False plant type should raise ValueError"),
                    (1, True, 25.0, 50, "Boolean True season should raise ValueError"),
                    (1, False, 25.0, 50, "Boolean False season should raise ValueError"),
                    (1, 1, True, 50, "Boolean True temperature should raise ValueError"),
                    (1, 1, False, 50, "Boolean False temperature should raise ValueError"),
                    (1, 1, 25.0, True, "Boolean True humidity should raise ValueError"),
                    (1, 1, 25.0, False, "Boolean False humidity should raise ValueError")
                ]
                
                for plant_type, season, temp, humidity, description in comprehensive_boolean_tests:
                    if not check_raises_exception(self.module_obj.generate_care_instructions, [plant_type, season, temp, humidity], ValueError):
                        errors.append(f"generate_care_instructions does not raise ValueError: {description}")
            
            # === EXTREME VALUE TESTS ===
            
            # Test extreme values that should definitely raise exceptions
            extreme_tests = [
                ("calculate_watering_schedule", [-999], "Extreme negative plant type should raise ValueError"),
                ("calculate_watering_schedule", [999], "Extreme positive plant type should raise ValueError"),
                ("adjust_for_season", [1, -999], "Extreme negative season should raise ValueError"),
                ("adjust_for_season", [1, 999], "Extreme positive season should raise ValueError"),
                ("adjust_for_season", [-999, 1], "Extreme negative days should raise ValueError"),
                ("check_temperature", [-999.0], "Extreme cold temperature should raise ValueError"),
                ("check_temperature", [999.0], "Extreme hot temperature should raise ValueError"),
                ("determine_humidity_needs", [-999], "Extreme negative humidity should raise ValueError"),
                ("determine_humidity_needs", [999], "Extreme positive humidity should raise ValueError"),
                ("get_sunlight_requirement", [-999], "Extreme negative plant type should raise ValueError"),
                ("get_sunlight_requirement", [999], "Extreme positive plant type should raise ValueError")
            ]
            
            for func_name, args, description in extreme_tests:
                if check_function_exists(self.module_obj, func_name):
                    if not check_raises_exception(getattr(self.module_obj, func_name), args, ValueError):
                        errors.append(f"{func_name} does not raise ValueError: {description}")
                else:
                    errors.append(f"Function {func_name} not found for extreme test")
            
            # Final result checking
            if errors:
                self.test_obj.yakshaAssert("TestComprehensiveExceptionHandling", False, "exception")
                print("TestComprehensiveExceptionHandling = Failed")
            else:
                self.test_obj.yakshaAssert("TestComprehensiveExceptionHandling", True, "exception")
                print("TestComprehensiveExceptionHandling = Passed")
                
        except Exception as e:
            self.test_obj.yakshaAssert("TestComprehensiveExceptionHandling", False, "exception")
            print("TestComprehensiveExceptionHandling = Failed")

if __name__ == '__main__':
    unittest.main()