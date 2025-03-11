def calculate_watering_schedule(plant_type: int) -> int:
    """Calculate watering frequency in days based on plant type."""
    if not isinstance(plant_type, int):
        raise ValueError("Plant type must be an integer.")
    if not 1 <= plant_type <= 4:
        raise ValueError("Invalid plant type. Must be between 1 and 4.")
        
    # TODO: Implement if-elif-else logic to return the correct watering schedule
    # plant_type 1 (Succulent): return 14 days
    # plant_type 2 (Tropical): return 3 days
    # plant_type 3 (Flowering): return 2 days
    # plant_type 4 (Herb): return 1 day
    pass

def adjust_for_season(days: int, season: int) -> int:
    """Adjust watering schedule based on season."""
    if not isinstance(season, int):
        raise ValueError("Season must be an integer.")
    if not 1 <= season <= 4:
        raise ValueError("Invalid season. Must be between 1 and 4.")
    if not isinstance(days, int):
        raise ValueError("Days must be an integer.")
    if days < 0:
        raise ValueError("Base schedule cannot be negative.")
        
    # TODO: Implement if-else logic to adjust watering days based on season
    # season 2 (Summer): decrease days by 1 (minimum 1 day)
    # season 4 (Winter): increase days by 1
    # season 1/3 (Spring/Fall): no change
    pass

def check_temperature(temperature: float) -> str:
    """Check if temperature is within optimal range."""
    if not isinstance(temperature, (int, float)):
        raise ValueError("Temperature must be a number.")
    if not -10.0 <= temperature <= 50.0:
        raise ValueError("Temperature must be between -10.0 and 50.0 Celsius.")
        
    # TODO: Implement if-elif-else logic to check temperature conditions
    # temperature > 30.0: return "Temperature too high - Risk of heat stress"
    # temperature < 10.0: return "Temperature too low - Risk of cold damage"
    # otherwise: return "Temperature optimal for plant growth"
    pass

def determine_humidity_needs(humidity: int) -> tuple[str, str]:
    """Determine humidity level and provide advice."""
    if not isinstance(humidity, int):
        raise ValueError("Humidity must be an integer.")
    if not 0 <= humidity <= 100:
        raise ValueError("Humidity must be between 0 and 100 percent.")
        
    # TODO: Implement if-elif-else logic to determine humidity level and advice
    # humidity < 30: return ("Low", "Increase humidity with misting")
    # humidity > 60: return ("High", "Monitor for fungal growth")
    # otherwise: return ("Medium", "Humidity is optimal")
    pass

def generate_care_instructions(plant_type: int, season: int, temperature: float, humidity: int) -> str:
    """Generate specific care instructions based on all plant parameters."""
    # Input validation
    if not isinstance(plant_type, int):
        raise ValueError("Plant type must be an integer.")
    if not 1 <= plant_type <= 4:
        raise ValueError("Invalid plant type")
    if not isinstance(season, int):
        raise ValueError("Season must be an integer.")
    if not 1 <= season <= 4:
        raise ValueError("Invalid season")
    if not isinstance(temperature, (int, float)):
        raise ValueError("Temperature must be a number.")
    if not -10.0 <= temperature <= 50.0:
        raise ValueError("Invalid temperature")
    if not isinstance(humidity, int):
        raise ValueError("Humidity must be an integer.")
    if not 0 <= humidity <= 100:
        raise ValueError("Invalid humidity")

    # TODO: Implement logic to generate care instructions
    # 1. Calculate base watering days and adjust for season
    # 2. Get temperature status, humidity needs, and sunlight requirements
    # 3. Build plant-specific instructions using if-elif-else
    # 4. Add seasonal and environmental advice using if-else
    # 5. Format and return the complete care instructions
    pass

def get_sunlight_requirement(plant_type: int) -> str:
    """Helper function to determine sunlight requirements."""
    if not isinstance(plant_type, int):
        raise ValueError("Plant type must be an integer.")
    if not 1 <= plant_type <= 4:
        raise ValueError("Invalid plant type. Must be between 1 and 4.")
        
    # TODO: Implement if-elif-else logic to return sunlight requirements
    # plant_type 1 (Succulent): return "Full sun to partial shade"
    # plant_type 2 (Tropical): return "Bright indirect light"
    # plant_type 3 (Flowering): return "Full sun"
    # plant_type 4 (Herb): return "At least 6 hours of direct sunlight"
    pass

def main():
    """Main function to run the plant care advisory system."""
    # TODO: Implement the main program flow
    # 1. Display welcome message
    # 2. Get user input for plant type, season, temperature, and humidity
    # 3. Generate and display care instructions
    # 4. Handle potential errors with try-except
    pass

if __name__ == "__main__":
    main()