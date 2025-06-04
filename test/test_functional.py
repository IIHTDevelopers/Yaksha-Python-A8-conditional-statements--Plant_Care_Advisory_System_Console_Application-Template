import unittest
import os
import importlib
import sys
import io
import contextlib
import re
import inspect
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

class TestPlantCareFunctional(unittest.TestCase):
    """Test class for functional testing of the Plant Care Advisory System."""
    
    def setUp(self):
        """Setup test data before each test method."""
        self.test_obj = TestUtils()
        self.module_obj = load_module_dynamically()
    
    def test_function_structure_and_implementation(self):
        """Test function structure patterns and implementation techniques"""
        try:
            # Check if module can be imported
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestFunctionStructureAndImplementation", False, "functional")
                print("TestFunctionStructureAndImplementation = Failed")
                return
            
            # Check if implementation is functional
            if not is_implementation_functional(self.module_obj):
                self.test_obj.yakshaAssert("TestFunctionStructureAndImplementation", False, "functional")
                print("TestFunctionStructureAndImplementation = Failed")
                return
            
            errors = []
            
            # === FUNCTION STRUCTURE TESTING ===
            
            # Check if all required functions exist
            functions_to_check = {
                'calculate_watering_schedule': r'if.*elif.*elif.*elif',
                'adjust_for_season': r'if.*elif.*else',
                'check_temperature': r'if.*elif.*else',
                'determine_humidity_needs': r'if.*elif.*else'
            }
            
            missing_functions = []
            for func_name in functions_to_check.keys():
                if not check_function_exists(self.module_obj, func_name):
                    missing_functions.append(func_name)
            
            if missing_functions:
                errors.append(f"Missing required functions: {', '.join(missing_functions)}")
                self.test_obj.yakshaAssert("TestFunctionStructureAndImplementation", False, "functional")
                print("TestFunctionStructureAndImplementation = Failed")
                return
            
            # Check function implementations for required conditional structures
            for func_name, pattern in functions_to_check.items():
                try:
                    if check_function_exists(self.module_obj, func_name):
                        func = getattr(self.module_obj, func_name)
                        code = inspect.getsource(func)
                        if not re.search(pattern, code.replace('\n', ' '), re.DOTALL):
                            errors.append(f"{func_name} missing {pattern} structure")
                    else:
                        errors.append(f"Function {func_name} not found")
                except Exception as e:
                    errors.append(f"Error inspecting {func_name}: {str(e)}")
            
            # === IMPLEMENTATION TECHNIQUES TESTING ===
            
            # Check implementation techniques using source code inspection
            implementation_checks = [
                ("calculate_watering_schedule", ["if", "elif"], "Should use if-elif structure for plant types"),
                ("adjust_for_season", ["if", "elif", "else"], "Should use if-elif-else structure for seasons"),
                ("check_temperature", ["if", "elif", "else"], "Should use if-elif-else structure for temperature ranges"),
                ("determine_humidity_needs", ["if", "elif", "else"], "Should use if-elif-else structure for humidity levels"),
                ("get_sunlight_requirement", ["if", "elif"], "Should use if-elif structure for plant types")
            ]
            
            for func_name, required_keywords, description in implementation_checks:
                try:
                    if check_function_exists(self.module_obj, func_name):
                        func = getattr(self.module_obj, func_name)
                        source = inspect.getsource(func)
                        source_lower = source.lower()
                        
                        missing_keywords = []
                        for keyword in required_keywords:
                            if keyword not in source_lower:
                                missing_keywords.append(keyword)
                        
                        if missing_keywords:
                            errors.append(f"{func_name} missing conditional keywords {missing_keywords}: {description}")
                            
                        # Check for proper conditional structure patterns
                        if func_name == "calculate_watering_schedule":
                            elif_count = source_lower.count("elif")
                            if elif_count < 2:
                                errors.append(f"{func_name} should have at least 3 elif statements for 4 plant types")
                        
                        elif func_name == "adjust_for_season":
                            if "else" not in source_lower:
                                errors.append(f"{func_name} should have else clause for default seasons")
                        
                        elif func_name in ["check_temperature", "determine_humidity_needs"]:
                            if source_lower.count("if") < 2:
                                errors.append(f"{func_name} should have multiple conditional checks")
                    
                except Exception as e:
                    errors.append(f"Error inspecting {func_name} implementation: {str(e)}")
            
            # Test logical flow and decision making
            logic_tests = [
                ("calculate_watering_schedule", [(1, 14), (2, 3), (3, 2), (4, 1)], "Should return different values for different plant types"),
                ("adjust_for_season", [(5, 1, 5), (5, 2, 4), (5, 3, 5), (5, 4, 6)], "Should adjust differently for each season"),
                ("check_temperature", [(5.0, "low"), (25.0, "optimal"), (35.0, "high")], "Should categorize temperatures correctly"),
                ("determine_humidity_needs", [(20, "Low"), (50, "Medium"), (80, "High")], "Should categorize humidity levels correctly"),
                ("get_sunlight_requirement", [(1, "sun"), (2, "indirect"), (3, "full"), (4, "direct")], "Should provide different requirements for each plant type")
            ]
            
            for func_name, test_cases, description in logic_tests:
                if check_function_exists(self.module_obj, func_name):
                    results = []
                    for test_case in test_cases:
                        if len(test_case) == 2:  # Single argument functions
                            arg, expected_substring = test_case
                            result = safely_call_function(self.module_obj, func_name, arg)
                        else:  # Multi-argument functions
                            args = test_case[:-1]
                            expected_substring = test_case[-1]
                            result = safely_call_function(self.module_obj, func_name, *args)
                        
                        if result is None:
                            errors.append(f"{func_name} returned None for test case {test_case}")
                        else:
                            results.append(result)
                            # Check if expected substring is in result (for string returns)
                            if isinstance(result, str) and expected_substring.lower() not in result.lower():
                                errors.append(f"{func_name} result '{result}' should contain '{expected_substring}' for input {test_case[:-1]}")
                            # Check exact match for integer returns
                            elif isinstance(result, int) and result != expected_substring:
                                errors.append(f"{func_name} returned {result}, expected {expected_substring} for input {test_case[:-1]}")
                            # Check tuple returns
                            elif isinstance(result, tuple) and len(result) >= 1 and expected_substring.lower() not in result[0].lower():
                                errors.append(f"{func_name} tuple result should contain '{expected_substring}' for input {test_case[:-1]}")
                    
                    # Check that function produces different outputs for different inputs (shows conditional logic)
                    unique_results = set(str(r) for r in results if r is not None)
                    if len(unique_results) < 2 and len(test_cases) > 2:
                        errors.append(f"{func_name} should produce different outputs for different inputs: {description}")
            
            # Final result checking
            if errors:
                self.test_obj.yakshaAssert("TestFunctionStructureAndImplementation", False, "functional")
                print("TestFunctionStructureAndImplementation = Failed")
            else:
                self.test_obj.yakshaAssert("TestFunctionStructureAndImplementation", True, "functional")
                print("TestFunctionStructureAndImplementation = Passed")
        
        except Exception as e:
            self.test_obj.yakshaAssert("TestFunctionStructureAndImplementation", False, "functional")
            print("TestFunctionStructureAndImplementation = Failed")

    def test_calculation_logic_and_return_types(self):
        """Test calculation logic and validate return types"""
        try:
            # Check if module can be imported
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestCalculationLogicAndReturnTypes", False, "functional")
                print("TestCalculationLogicAndReturnTypes = Failed")
                return
            
            # Check if implementation is functional
            if not is_implementation_functional(self.module_obj):
                self.test_obj.yakshaAssert("TestCalculationLogicAndReturnTypes", False, "functional")
                print("TestCalculationLogicAndReturnTypes = Failed")
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
                self.test_obj.yakshaAssert("TestCalculationLogicAndReturnTypes", False, "functional")
                print("TestCalculationLogicAndReturnTypes = Failed")
                return
            
            # === CALCULATION LOGIC TESTING ===
            
            # Test watering schedule calculations
            watering_tests = [
                (1, 14, "Succulent should be watered every 14 days"),
                (2, 3, "Tropical should be watered every 3 days"),
                (3, 2, "Flowering should be watered every 2 days"),
                (4, 1, "Herb should be watered every 1 day")
            ]
            
            for plant_type, expected, message in watering_tests:
                result = safely_call_function(self.module_obj, "calculate_watering_schedule", plant_type)
                if result is None:
                    errors.append(f"calculate_watering_schedule({plant_type}) returned None")
                elif not isinstance(result, int):
                    errors.append(f"calculate_watering_schedule({plant_type}) should return an integer, got {type(result)}")
                elif result != expected:
                    errors.append(f"calculate_watering_schedule({plant_type}) returned {result}, expected {expected}: {message}")
            
            # Test season adjustment
            season_tests = [
                (7, 1, 7, "Spring should not change watering days"),
                (7, 2, 6, "Summer should decrease watering days by 1"),
                (7, 3, 7, "Fall should not change watering days"),
                (7, 4, 8, "Winter should increase watering days by 1"),
                (1, 2, 1, "Summer adjustment should maintain minimum of 1 day"),
                (2, 2, 1, "Summer adjustment of 2 days should become 1"),
                (14, 4, 15, "Winter adjustment should add 1 day"),
                (10, 1, 10, "Spring adjustment should not change"),
                (5, 3, 5, "Fall adjustment should not change")
            ]
            
            for days, season, expected, message in season_tests:
                result = safely_call_function(self.module_obj, "adjust_for_season", days, season)
                if result is None:
                    errors.append(f"adjust_for_season({days}, {season}) returned None")
                elif not isinstance(result, int):
                    errors.append(f"adjust_for_season({days}, {season}) should return an integer, got {type(result)}")
                elif result != expected:
                    errors.append(f"adjust_for_season({days}, {season}) returned {result}, expected {expected}: {message}")
            
            # === RETURN TYPES TESTING ===
            
            # Test return types
            type_tests = [
                # (function_name, args, expected_type, description)
                ("calculate_watering_schedule", [1], int, "Should return integer for watering days"),
                ("calculate_watering_schedule", [4], int, "Should return integer for all plant types"),
                ("adjust_for_season", [7, 2], int, "Should return integer for adjusted days"),
                ("adjust_for_season", [1, 4], int, "Should return integer for all seasons"),
                ("check_temperature", [25.0], str, "Should return string for temperature status"),
                ("check_temperature", [35.0], str, "Should return string for all temperatures"),
                ("determine_humidity_needs", [50], tuple, "Should return tuple for humidity needs"),
                ("determine_humidity_needs", [80], tuple, "Should return tuple for all humidity levels"),
                ("get_sunlight_requirement", [1], str, "Should return string for sunlight requirements"),
                ("get_sunlight_requirement", [3], str, "Should return string for all plant types"),
                ("generate_care_instructions", [2, 1, 25.0, 50], str, "Should return string for care instructions")
            ]
            
            for func_name, args, expected_type, description in type_tests:
                result = safely_call_function(self.module_obj, func_name, *args)
                if result is None:
                    errors.append(f"{func_name} returned None when it should return {expected_type.__name__}: {description}")
                elif not isinstance(result, expected_type):
                    errors.append(f"{func_name} returned {type(result).__name__}, expected {expected_type.__name__}: {description}")
                
                # Special checks for tuple returns
                if expected_type == tuple and isinstance(result, tuple):
                    if len(result) != 2:
                        errors.append(f"{func_name} tuple should have exactly 2 elements, got {len(result)}")
                    elif not all(isinstance(item, str) for item in result):
                        errors.append(f"{func_name} tuple should contain only strings")
            
            # Test return value ranges and formats
            range_tests = [
                ("calculate_watering_schedule", [1], lambda x: 1 <= x <= 20, "Watering days should be reasonable (1-20)"),
                ("calculate_watering_schedule", [2], lambda x: 1 <= x <= 20, "All plant types should return reasonable days"),
                ("adjust_for_season", [5, 2], lambda x: x >= 1, "Adjusted days should be at least 1"),
                ("adjust_for_season", [1, 4], lambda x: x >= 1, "Minimum adjustment should maintain at least 1 day"),
                ("check_temperature", [25.0], lambda x: len(x) > 10, "Temperature status should be descriptive"),
                ("check_temperature", [35.0], lambda x: "temperature" in x.lower(), "Should mention temperature"),
                ("get_sunlight_requirement", [1], lambda x: len(x) > 5, "Sunlight requirement should be descriptive"),
                ("get_sunlight_requirement", [2], lambda x: "light" in x.lower(), "Should mention light"),
                ("generate_care_instructions", [1, 1, 25.0, 50], lambda x: len(x) > 100, "Care instructions should be comprehensive")
            ]
            
            for func_name, args, validator, description in range_tests:
                result = safely_call_function(self.module_obj, func_name, *args)
                if result is not None:
                    try:
                        if not validator(result):
                            errors.append(f"{func_name} result validation failed: {description}")
                    except Exception as e:
                        errors.append(f"{func_name} validation error: {str(e)}")
            
            # Test boundary behavior
            boundary_tests = [
                ("adjust_for_season", [1, 2], lambda x: x == 1, "Summer adjustment should respect minimum of 1 day"),
                ("adjust_for_season", [2, 2], lambda x: x == 1, "Summer adjustment should decrease but maintain minimum"),
                ("calculate_watering_schedule", [1], lambda x: x > 0, "Should return positive watering days"),
                ("calculate_watering_schedule", [4], lambda x: x > 0, "All plant types should return positive days")
            ]
            
            for func_name, args, validator, description in boundary_tests:
                if check_function_exists(self.module_obj, func_name):
                    result = safely_call_function(self.module_obj, func_name, *args)
                    if result is None:
                        errors.append(f"{func_name} returned None for boundary test: {description}")
                    elif not validator(result):
                        errors.append(f"{func_name} boundary test failed: {description}")
            
            # Final result checking
            if errors:
                self.test_obj.yakshaAssert("TestCalculationLogicAndReturnTypes", False, "functional")
                print("TestCalculationLogicAndReturnTypes = Failed")
            else:
                self.test_obj.yakshaAssert("TestCalculationLogicAndReturnTypes", True, "functional")
                print("TestCalculationLogicAndReturnTypes = Passed")
        
        except Exception as e:
            self.test_obj.yakshaAssert("TestCalculationLogicAndReturnTypes", False, "functional")
            print("TestCalculationLogicAndReturnTypes = Failed")

    def test_environmental_assessment(self):
        """Test if environmental assessment functions work correctly"""
        try:
            # Check if module can be imported
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestEnvironmentalAssessment", False, "functional")
                print("TestEnvironmentalAssessment = Failed")
                return
            
            # Check if implementation is functional
            if not is_implementation_functional(self.module_obj):
                self.test_obj.yakshaAssert("TestEnvironmentalAssessment", False, "functional")
                print("TestEnvironmentalAssessment = Failed")
                return
            
            errors = []
            
            # Test all required functions
            required_functions = [
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
                self.test_obj.yakshaAssert("TestEnvironmentalAssessment", False, "functional")
                print("TestEnvironmentalAssessment = Failed")
                return
            
            # Test temperature checks with comprehensive scenarios
            temp_tests = [
                (35.0, "high", "High temperature should warn about heat stress"),
                (5.0, "low", "Low temperature should warn about cold damage"),
                (20.0, "optimal", "Normal temperature should indicate optimal conditions"),
                (30.1, "high", "Just above threshold should be high"),
                (9.9, "low", "Just below threshold should be low"),
                (25.5, "optimal", "Room temperature should be optimal"),
                (50.0, "high", "Maximum allowed temperature should be high"),
                (-10.0, "low", "Minimum allowed temperature should be low")
            ]
            
            for temp, expected_text, message in temp_tests:
                result = safely_call_function(self.module_obj, "check_temperature", temp)
                if result is None:
                    errors.append(f"check_temperature({temp}) returned None")
                elif not isinstance(result, str):
                    errors.append(f"check_temperature({temp}) should return a string, got {type(result)}")
                elif expected_text.lower() not in result.lower():
                    errors.append(f"check_temperature({temp}) returned '{result}', expected to contain '{expected_text}': {message}")
            
            # Test humidity assessment with comprehensive scenarios
            humidity_tests = [
                (20, "Low", "mist", "Low humidity should suggest misting"),
                (45, "Medium", "optimal", "Medium humidity should indicate optimal conditions"),
                (70, "High", "fungal", "High humidity should warn about fungal growth"),
                (0, "Low", "mist", "Minimum humidity should be Low"),
                (29, "Low", "mist", "Just below medium should be Low"),
                (30, "Medium", "optimal", "Lower boundary of medium"),
                (60, "Medium", "optimal", "Upper boundary of medium"),
                (61, "High", "fungal", "Just above medium should be High"),
                (100, "High", "fungal", "Maximum humidity should be High")
            ]
            
            for humid, expected_level, expected_advice, message in humidity_tests:
                result = safely_call_function(self.module_obj, "determine_humidity_needs", humid)
                if result is None:
                    errors.append(f"determine_humidity_needs({humid}) returned None")
                elif not isinstance(result, tuple) or len(result) != 2:
                    errors.append(f"determine_humidity_needs({humid}) should return a tuple of 2 elements, got {type(result)}")
                else:
                    level, advice = result
                    if level != expected_level:
                        errors.append(f"determine_humidity_needs({humid}) returned level '{level}', expected '{expected_level}': {message}")
                    if expected_advice.lower() not in advice.lower():
                        errors.append(f"determine_humidity_needs({humid}) advice '{advice}' should contain '{expected_advice}': {message}")
            
            # Test sunlight requirements comprehensively
            sunlight_tests = [
                (1, ["sun", "shade"], "Succulent sunlight should mention both sun and shade"),
                (2, ["indirect"], "Tropical should need indirect light"),
                (3, ["full sun"], "Flowering should need full sun"),
                (4, ["direct", "hours"], "Herb should need direct sunlight with hours specified")
            ]
            
            for plant_type, expected_texts, message in sunlight_tests:
                result = safely_call_function(self.module_obj, "get_sunlight_requirement", plant_type)
                if result is None:
                    errors.append(f"get_sunlight_requirement({plant_type}) returned None")
                elif not isinstance(result, str):
                    errors.append(f"get_sunlight_requirement({plant_type}) should return a string, got {type(result)}")
                elif not all(text.lower() in result.lower() for text in expected_texts):
                    errors.append(f"get_sunlight_requirement({plant_type}) returned '{result}', expected to contain {expected_texts}: {message}")
            
            # Final result checking
            if errors:
                self.test_obj.yakshaAssert("TestEnvironmentalAssessment", False, "functional")
                print("TestEnvironmentalAssessment = Failed")
            else:
                self.test_obj.yakshaAssert("TestEnvironmentalAssessment", True, "functional")
                print("TestEnvironmentalAssessment = Passed")
        
        except Exception as e:
            self.test_obj.yakshaAssert("TestEnvironmentalAssessment", False, "functional")
            print("TestEnvironmentalAssessment = Failed")

    def test_care_instructions(self):
        """Test if care instructions are generated with all required components"""
        try:
            # Check if module can be imported
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestCareInstructions", False, "functional")
                print("TestCareInstructions = Failed")
                return
            
            # Check if implementation is functional
            if not is_implementation_functional(self.module_obj):
                self.test_obj.yakshaAssert("TestCareInstructions", False, "functional")
                print("TestCareInstructions = Failed")
                return
            
            errors = []
            
            # Test required function
            if not check_function_exists(self.module_obj, "generate_care_instructions"):
                self.test_obj.yakshaAssert("TestCareInstructions", False, "functional")
                print("TestCareInstructions = Failed")
                return
            
            # Plant-specific instruction tests
            plant_instructions = {
                1: "Avoid overwatering",               # Succulent
                2: "Maintain high humidity",           # Tropical
                3: "Remove dead flowers regularly",    # Flowering
                4: "Harvest regularly to promote growth"  # Herb
            }
            
            for plant_type, expected_care in plant_instructions.items():
                instructions = safely_call_function(self.module_obj, "generate_care_instructions", plant_type, 1, 25.0, 45)
                if instructions is None:
                    errors.append(f"generate_care_instructions returned None for plant type {plant_type}")
                elif not isinstance(instructions, str):
                    errors.append(f"generate_care_instructions should return a string for plant type {plant_type}, got {type(instructions)}")
                elif expected_care not in instructions:
                    errors.append(f"Plant type {plant_type} instructions missing '{expected_care}'")
            
            # Seasonal advice tests
            seasonal_advice = {
                2: "Increase watering frequency",  # Summer
                4: "Reduce watering frequency"     # Winter
            }
            
            for season, expected_advice in seasonal_advice.items():
                instructions = safely_call_function(self.module_obj, "generate_care_instructions", 1, season, 25.0, 45)
                if instructions is None:
                    errors.append(f"generate_care_instructions returned None for season {season}")
                elif not isinstance(instructions, str):
                    errors.append(f"generate_care_instructions should return a string for season {season}, got {type(instructions)}")
                elif expected_advice not in instructions:
                    errors.append(f"Season {season} advice missing '{expected_advice}'")
            
            # Required sections test
            required_sections = [
                "Watering Schedule: Every",
                "Sunlight Requirement:",
                "Temperature Status:",
                "Humidity Level:",
                "Special Care Instructions:"
            ]
            
            sample_instructions = safely_call_function(self.module_obj, "generate_care_instructions", 2, 1, 25.0, 45)
            if sample_instructions is None:
                errors.append("generate_care_instructions returned None for section test")
            elif not isinstance(sample_instructions, str):
                errors.append(f"generate_care_instructions should return a string for section test, got {type(sample_instructions)}")
            else:
                for section in required_sections:
                    if section not in sample_instructions:
                        errors.append(f"Instructions missing required section: '{section}'")
            
            # Environmental advice tests
            environmental_tests = [
                (35.0, "shade", "High temperature should suggest shade"),
                (5.0, "cold", "Low temperature should mention cold protection"),
                (20, "mist", "Low humidity should suggest misting"),
                (80, "fungal", "High humidity should warn about fungal growth")
            ]
            
            for condition_value, expected_keyword, description in environmental_tests:
                if "temperature" in description.lower():
                    instructions = safely_call_function(self.module_obj, "generate_care_instructions", 1, 1, condition_value, 45)
                else:  # humidity test
                    instructions = safely_call_function(self.module_obj, "generate_care_instructions", 1, 1, 25.0, condition_value)
                
                if instructions is None:
                    errors.append(f"generate_care_instructions returned None for {description}")
                elif not isinstance(instructions, str):
                    errors.append(f"generate_care_instructions should return a string for {description}, got {type(instructions)}")
                elif expected_keyword.lower() not in instructions.lower():
                    errors.append(f"Instructions should contain '{expected_keyword}' for {description}")
            
            # Final result checking
            if errors:
                self.test_obj.yakshaAssert("TestCareInstructions", False, "functional")
                print("TestCareInstructions = Failed")
            else:
                self.test_obj.yakshaAssert("TestCareInstructions", True, "functional")
                print("TestCareInstructions = Passed")
        
        except Exception as e:
            self.test_obj.yakshaAssert("TestCareInstructions", False, "functional")
            print("TestCareInstructions = Failed")

    def test_integration_workflow(self):
        """Test complete integration workflow of all functions working together"""
        try:
            # Check if module can be imported
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestIntegrationWorkflow", False, "functional")
                print("TestIntegrationWorkflow = Failed")
                return
            
            # Check if implementation is functional
            if not is_implementation_functional(self.module_obj):
                self.test_obj.yakshaAssert("TestIntegrationWorkflow", False, "functional")
                print("TestIntegrationWorkflow = Failed")
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
                self.test_obj.yakshaAssert("TestIntegrationWorkflow", False, "functional")
                print("TestIntegrationWorkflow = Failed")
                return
            
            # Test complete workflow scenarios
            workflow_tests = [
                # (plant_type, season, temperature, humidity, expected_components)
                (1, 2, 35.0, 20, {  # Succulent in summer, high temp, low humidity
                    "watering": ["Every", "13"],  # 14-1=13 for summer
                    "plant_advice": ["Avoid overwatering"],
                    "seasonal": ["Increase watering frequency"],
                    "environmental": ["shade", "mist"]
                }),
                (2, 4, 5.0, 80, {  # Tropical in winter, low temp, high humidity
                    "watering": ["Every", "4"],  # 3+1=4 for winter  
                    "plant_advice": ["Maintain high humidity"],
                    "seasonal": ["Reduce watering frequency"],
                    "environmental": ["cold", "fungal"]
                }),
                (3, 1, 20.0, 45, {  # Flowering in spring, optimal conditions
                    "watering": ["Every", "2"],  # No seasonal adjustment
                    "plant_advice": ["Remove dead flowers"],
                    "environmental": ["optimal"]
                }),
                (4, 3, 25.0, 55, {  # Herb in fall, optimal conditions
                    "watering": ["Every", "1"],  # No seasonal adjustment
                    "plant_advice": ["Harvest regularly"],
                    "environmental": ["optimal"]
                })
            ]
            
            for plant_type, season, temp, humidity, expected in workflow_tests:
                # Test individual functions first
                base_days = safely_call_function(self.module_obj, "calculate_watering_schedule", plant_type)
                if base_days is None:
                    errors.append(f"Workflow test failed: calculate_watering_schedule returned None for plant {plant_type}")
                    continue
                
                adjusted_days = safely_call_function(self.module_obj, "adjust_for_season", base_days, season)
                if adjusted_days is None:
                    errors.append(f"Workflow test failed: adjust_for_season returned None for plant {plant_type}")
                    continue
                
                temp_status = safely_call_function(self.module_obj, "check_temperature", temp)
                if temp_status is None:
                    errors.append(f"Workflow test failed: check_temperature returned None for plant {plant_type}")
                    continue
                
                humidity_result = safely_call_function(self.module_obj, "determine_humidity_needs", humidity)
                if humidity_result is None:
                    errors.append(f"Workflow test failed: determine_humidity_needs returned None for plant {plant_type}")
                    continue
                
                sunlight_req = safely_call_function(self.module_obj, "get_sunlight_requirement", plant_type)
                if sunlight_req is None:
                    errors.append(f"Workflow test failed: get_sunlight_requirement returned None for plant {plant_type}")
                    continue
                
                # Test complete integration
                full_instructions = safely_call_function(self.module_obj, "generate_care_instructions", plant_type, season, temp, humidity)
                if full_instructions is None:
                    errors.append(f"Workflow test failed: generate_care_instructions returned None for plant {plant_type}")
                    continue
                
                # Verify expected components are present
                for category, expected_items in expected.items():
                    for item in expected_items:
                        if item not in full_instructions:
                            errors.append(f"Workflow test failed: Missing '{item}' in instructions for plant {plant_type}, season {season}")
            
            # Test data consistency across functions
            consistency_tests = [
                (1, 1, 25.0, 50),  # Succulent, spring, optimal
                (2, 2, 30.0, 40),  # Tropical, summer, optimal
                (3, 3, 15.0, 60),  # Flowering, fall, optimal
                (4, 4, 10.0, 30)   # Herb, winter, optimal
            ]
            
            for plant_type, season, temp, humidity in consistency_tests:
                # Get individual results
                watering_days = safely_call_function(self.module_obj, "calculate_watering_schedule", plant_type)
                seasonal_days = safely_call_function(self.module_obj, "adjust_for_season", watering_days, season) if watering_days else None
                temp_check = safely_call_function(self.module_obj, "check_temperature", temp)
                humidity_check = safely_call_function(self.module_obj, "determine_humidity_needs", humidity)
                sunlight_check = safely_call_function(self.module_obj, "get_sunlight_requirement", plant_type)
                
                # Get integrated result
                integrated = safely_call_function(self.module_obj, "generate_care_instructions", plant_type, season, temp, humidity)
                
                if integrated and seasonal_days:
                    # Check if watering schedule matches
                    if f"Every {seasonal_days} days" not in integrated:
                        errors.append(f"Consistency error: Watering schedule mismatch for plant {plant_type}")
                
                if integrated and temp_check:
                    # Temperature status should be consistent
                    if "optimal" in temp_check.lower() and "optimal" not in integrated.lower():
                        errors.append(f"Consistency error: Temperature status mismatch for plant {plant_type}")
                
                if integrated and humidity_check and len(humidity_check) == 2:
                    # Humidity level should be consistent
                    humidity_level = humidity_check[0]
                    if humidity_level not in integrated:
                        errors.append(f"Consistency error: Humidity level mismatch for plant {plant_type}")
            
            # Test cross-functional integration scenarios
            integration_scenarios = [
                # Test that all functions work together for extreme but valid inputs
                (1, 2, 50.0, 0, "Succulent in summer with maximum temperature and minimum humidity"),
                (4, 4, -10.0, 100, "Herb in winter with minimum temperature and maximum humidity"),
                (2, 1, 30.0, 30, "Tropical in spring at temperature and humidity boundaries"),
                (3, 3, 10.0, 60, "Flowering in fall at temperature and humidity boundaries")
            ]
            
            for plant_type, season, temp, humidity, description in integration_scenarios:
                # Test that each function handles the scenario
                functions_to_test = [
                    ("calculate_watering_schedule", [plant_type]),
                    ("check_temperature", [temp]),
                    ("determine_humidity_needs", [humidity]),
                    ("get_sunlight_requirement", [plant_type])
                ]
                
                # Test individual functions
                for func_name, args in functions_to_test:
                    result = safely_call_function(self.module_obj, func_name, *args)
                    if result is None:
                        errors.append(f"Integration scenario failed: {func_name} returned None for {description}")
                
                # Test season adjustment if watering schedule works
                watering_result = safely_call_function(self.module_obj, "calculate_watering_schedule", plant_type)
                if watering_result is not None:
                    season_result = safely_call_function(self.module_obj, "adjust_for_season", watering_result, season)
                    if season_result is None:
                        errors.append(f"Integration scenario failed: adjust_for_season returned None for {description}")
                
                # Test full integration
                full_result = safely_call_function(self.module_obj, "generate_care_instructions", plant_type, season, temp, humidity)
                if full_result is None:
                    errors.append(f"Integration scenario failed: generate_care_instructions returned None for {description}")
                elif not isinstance(full_result, str):
                    errors.append(f"Integration scenario failed: generate_care_instructions should return string for {description}")
                elif len(full_result) < 50:
                    errors.append(f"Integration scenario failed: generate_care_instructions returned insufficient content for {description}")
            
            # Final result checking
            if errors:
                self.test_obj.yakshaAssert("TestIntegrationWorkflow", False, "functional")
                print("TestIntegrationWorkflow = Failed")
            else:
                self.test_obj.yakshaAssert("TestIntegrationWorkflow", True, "functional")
                print("TestIntegrationWorkflow = Passed")
        
        except Exception as e:
            self.test_obj.yakshaAssert("TestIntegrationWorkflow", False, "functional")
            print("TestIntegrationWorkflow = Failed")

if __name__ == '__main__':
    unittest.main()