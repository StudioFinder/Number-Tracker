
import phonenumbers
from phonenumbers import geocoder as pn_geocoder
from opencage.geocoder import OpenCageGeocode
import folium

# Your OpenCage API key
API_KEY = "insert API key here" #create a opencage geocode account and generate API key

def track_phone_number(number):
    try:
        # Parse and validate U.S. phone number
        parsed_number = phonenumbers.parse(number, "US")
        
        if not (phonenumbers.is_valid_number(parsed_number) and 
                phonenumbers.region_code_for_number(parsed_number) == "US"):
            raise ValueError("The phone number is not a valid U.S. number.")
        
        # Get location description (city, state) from `phonenumbers`
        location_description = pn_geocoder.description_for_number(parsed_number, "en")
        if not location_description:
            raise ValueError("Unable to determine location from the phone number.")

        # Initialize the OpenCage Geocoder and geocode the location description
        geocoder = OpenCageGeocode(API_KEY)
        geocode_result = geocoder.geocode(location_description)
        if not geocode_result:
            raise ValueError("Unable to retrieve coordinates for the given location.")

        # Extract latitude and longitude from geocode results
        lat = geocode_result[0]["geometry"]["lat"]
        lng = geocode_result[0]["geometry"]["lng"]

        # Create a map centered at the location and add a marker
        m = folium.Map(location=[lat, lng], zoom_start=10)
        folium.Marker([lat, lng], popup=f"{parsed_number}\n{location_description}").add_to(m)

        # Save the map as an HTML file
        map_filename = "phone_location_map.html"
        m.save(map_filename)
        print(f"Map has been saved as {map_filename}")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    phone_number = input("Enter a U.S. phone number: ")
    track_phone_number(phone_number)
