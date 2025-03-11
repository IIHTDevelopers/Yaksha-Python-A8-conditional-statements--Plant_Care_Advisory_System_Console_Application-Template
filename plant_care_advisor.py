def calculate_watering_schedule(plant_type: int) -> int:
    """Calculate watering frequency in days based on plant type."""
    if not isinstance(plant_type, int):
        raise ValueError("Plant type must be an integer.")
    if not 1 <= plant_type <= 4:
        raise ValueError("Invalid plant type. Must be between 1 and 4.")
        
    if plant_type == 1:  # Succulent
        return 14
    elif plant_type == 2:  # Tropical
        return 3
    elif plant_type == 3:  # Flowering
        return 2
    elif plant_type == 4:  # Herb
        return 1

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
        
    if season == 2:  # Summer
        return max(1, days - 1)  # Ensure at least 1 day
    elif season == 4:  # Winter
        return days + 1
    else:  # Spring or Fall
        return days

def check_temperature(temperature: float) -> str:
    """Check if temperature is within optimal range."""
    if not isinstance(temperature, (int, float)):
        raise ValueError("Temperature must be a number.")
    if not -10.0 <= temperature <= 50.0:
        raise ValueError("Temperature must be between -10.0 and 50.0 Celsius.")
        
    if temperature > 30.0:
        return "Temperature too high - Risk of heat stress"
    elif temperature < 10.0:
        return "Temperature too low - Risk of cold damage"
    else:
        return "Temperature optimal for plant growth"

def determine_humidity_needs(humidity: int) -> tuple[str, str]:
    """Determine humidity level and provide advice."""
    if not isinstance(humidity, int):
        raise ValueError("Humidity must be an integer.")
    if not 0 <= humidity <= 100:
        raise ValueError("Humidity must be between 0 and 100 percent.")
        
    if humidity < 30:
        return ("Low", "Increase humidity with misting")
    elif humidity > 60:
        return ("High", "Monitor for fungal growth")
    else:
        return ("Medium", "Humidity is optimal")

def generate_care_instructions(plant_type: int, season: int, temperature: float, humidity: int) -> str:
    """Generate specific care instructions based on all plant parameters."""
    # Validate inputs
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

    # Calculate base watering days and adjust for season
    base_days = calculate_watering_schedule(plant_type)
    adjusted_days = adjust_for_season(base_days, season)
    
    # Get status messages
    temp_status = check_temperature(temperature)
    humidity_level, humidity_advice = determine_humidity_needs(humidity)
    sunlight = get_sunlight_requirement(plant_type)
    
    # Build care instructions
    instructions = []
    
    # Plant-specific instructions
    if plant_type == 1:  # Succulent
        instructions.append("Avoid overwatering")
    elif plant_type == 2:  # Tropical
        instructions.append("Maintain high humidity")
    elif plant_type == 3:  # Flowering
        instructions.append("Remove dead flowers regularly")
    elif plant_type == 4:  # Herb
        instructions.append("Harvest regularly to promote growth")

    # Add seasonal advice
    if season == 2:  # Summer
        instructions.append("Increase watering frequency")
    elif season == 4:  # Winter
        instructions.append("Reduce watering frequency")

    # Add environmental advice
    if temperature > 30.0:
        instructions.append("Provide shade and increase watering")
    elif temperature < 10.0:
        instructions.append("Protect from cold and reduce watering")

    instructions.append(humidity_advice)

    return "\n".join([
        f"Watering Schedule: Every {adjusted_days} days",
        f"Sunlight Requirement: {sunlight}",
        f"Temperature Status: {temp_status}",
        f"Humidity Level: {humidity_level}",
        "Special Care Instructions:",
        *instructions
    ])

def get_sunlight_requirement(plant_type: int) -> str:
    """Helper function to determine sunlight requirements."""
    if not isinstance(plant_type, int):
        raise ValueError("Plant type must be an integer.")
    if not 1 <= plant_type <= 4:
        raise ValueError("Invalid plant type. Must be between 1 and 4.")
        
    if plant_type == 1:
        return "Full sun to partial shade"
    elif plant_type == 2:
        return "Bright indirect light"
    elif plant_type == 3:
        return "Full sun"
    else:  # Herb
        return "At least 6 hours of direct sunlight"

def main():
    """Main function to run the plant care advisory system."""
    try:
        print("\nPlant Care Advisory System")
        print("-------------------------")
        print("Plant Types: 1-Succulent, 2-Tropical, 3-Flowering, 4-Herb")
        plant_type = int(input("Enter plant type (1-4): "))
        
        print("\nSeasons: 1-Spring, 2-Summer, 3-Fall, 4-Winter")
        season = int(input("Enter current season (1-4): "))
        
        temperature = float(input("\nEnter temperature (-10.0 to 50.0 °C): "))
        humidity = int(input("Enter humidity (0-100%): "))
        
        print("\nPlant Care Report")
        print("----------------")
        print(generate_care_instructions(plant_type, season, temperature, humidity))
        
    except ValueError as e:
        print(f"\nError: {str(e)}")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()