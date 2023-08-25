import googlemaps
import requests
import urllib.parse
import logging

def run(budget, location, distance):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    logger = logging.getLogger("list_operations")

    file_handler = logging.FileHandler("list_operations.log")
    logger.addHandler(file_handler)

    gmaps = googlemaps.Client(key='AIzaSyCALAR7kXuPaSVuGjZhdaiypWb3UL4RDhU')

    geocode_result = gmaps.geocode(location)

    latitude = geocode_result[0]['geometry']['location']['lat']
    longitude = geocode_result[0]['geometry']['location']['lng']

    #print(f"Latitude: {latitude}")
    #print(f"Longitude: {longitude}")

    # Geocoding an address
    location = (latitude, longitude)
    radius = distance
    budget = budget

    # Perform the nearby search
    nearby_places = gmaps.places_nearby(
        location=location,
        radius=radius,
        type='restaurant'  # Specify the type of place you're looking for
    )

    # Extract relevant information from the API response
    nearby_restaurants = []
    for place in nearby_places['results']:
        name = place['name']
        address = place['vicinity']
        nearby_restaurants.append({'name': name, 'address': address})

    nr_name = []
    nr_address = []
    for i in nearby_restaurants:
        nr_name.append(i['name'])
        nr_address.append(i['address'])
    nr_price = []
    nr_log = []
    f_name = []
    f_add = []
    f_price = []
    # Print the list of nearby restaurants
    for restaurant in nearby_restaurants:
        # Extracting restaurant name and preparing the URL for Swiggy API
        restaurant_name = restaurant['name']
        restaurant_name_encoded = urllib.parse.quote(restaurant_name)
        swiggy_url = f'https://www.swiggy.com/dapi/restaurants/search/v3?lat={latitude}&lng={longitude}&str={restaurant_name_encoded}&trackingId=undefined&submitAction=SUGGESTION'

        # Fetching and parsing Swiggy API response
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        swiggy_resp = requests.get(swiggy_url, headers=headers).json()
        def find_key_occurrence(json_string, target_key):
            data = json_string

            def recursive_search(item):
                if isinstance(item, dict):
                    if target_key in item:
                        return item[target_key]
                    for key, value in item.items():
                        result1 = recursive_search(value)
                        if result1 is not None:
                            return result1
                elif isinstance(item, list):
                    for element in item:
                        result1 = recursive_search(element)
                        if result1 is not None:
                            return result1

            return recursive_search(data)

        # Extracting the cost for two people from Swiggy API response

        try:
            target_key = 'costForTwo'
            cost_for_two = find_key_occurrence(swiggy_resp, target_key)
            cost_for_two_in_rupees = int(cost_for_two) / 100

        except None:
            continue

        if cost_for_two_in_rupees <= budget:
            print(f"Name: {restaurant['name']}")
            print(f"Address: {restaurant['address']}")
            print(f"Cost for Two: {cost_for_two_in_rupees} INR")
            logger.info("Restaurant: %s, Address: %s, Cost for Two: %s INR", restaurant_name, restaurant['address'],
                        cost_for_two_in_rupees)


            f_name.append(restaurant_name)
            f_add.append(restaurant['address'])
            f_price.append(cost_for_two_in_rupees)

    with open('textfile1.txt','w') as txt:
        for i in range(len(f_name)):
            txt.write('Name: ')
            txt.write(f_name[i])
            txt.write('\nAddress: ')
            txt.write(f_add[i])
            txt.write('\nPrice: ')
            txt.write(str(f_price[i]))
            txt.write(';\n\n')

