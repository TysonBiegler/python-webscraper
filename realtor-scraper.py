from audioop import add
from numpy import full
import requests
import pandas as pd
from torch import are_deterministic_algorithms_enabled
import re

# print('What city would you like to search in?')
# city = input('>')
# print("What state?")
# state = input(">").upper()
# print(f'Searching for houses in {city}, {state}')

city = input("What city would you like to search in?: ")
if not re.match('^[A-Za-z]*$', city):
    print('Error! Only letters a-z allowed.')
        
state = input(f'what state is {city} in?: ')
if not re.match('^[A-Za-z]*$', state):
    print('Error! Only letters a-z allowed.')
elif len(state)>2:
    print('Error! Only 2 Characters allowed!')
print(f'Looking for houses in {city}, {state}.')

#curl command from realtor that was translated into PYTHON
headers = {
    'authority': 'www.realtor.com',
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.9',
    # Already added when you pass json=
    # 'content-type': 'application/json',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'split=n; split_tcv=112; __vst=1ae3a798-c7a2-4fd6-bc2a-b84aec36420f; __ssn=2be76bf7-9bec-41d5-80fe-ad5dccd95956; __ssnstarttime=1656371226; threshold_value=14; automation=false; clstr=; clstr_tcv=; __edwssnstarttime=1656371227; __split=54; bcc=false; bcvariation=SRPBCRR%3Av1%3Adesktop; s_ecid=MCMID%7C60448848225504571971823027342865190689; G_ENABLED_IDPS=google; AMCVS_8853394255142B6A0A4C98A4%40AdobeOrg=1; _fbp=fb.1.1656371230679.1994552756; pxcts=e080b0a3-f66d-11ec-a314-77496f485a55; _pxvid=e080a595-f66d-11ec-a314-77496f485a55; __fp=837a8a8aee2ccdcf813605eddb237b99; g_state={"i_t":1656457634099,"i_l":0}; user_activity=return; userStatus=return_user; _rdc-next_session=ZWwvZkpxOFhhMnFZN3lKT1NvaTY2VFNGeUk4S0hNR3M2MWVTWlorMmhSaGZOOWZERTAxU2p1MExvMkZHY1k3MElMMzhrTnJ1V0xaUjVDSXN1U2Mvcy9OSkgweEpFTGFxL1VEMTM5eEFGdC8xRjk2ZXJQVzZFalFLWmdPUksxSzhTTjVWbGxFZEJsZjB5VVc3ckNLUnEwV1p1Zjl0OUF3eHNQaVpSa0RkUmlnRFgwdzZpa1ZjdEJaem9QcnlVY0p0dW9SYWVRZVNDbDUyeGx5N2ZmaFNUa3VLZVlMSTRHUlIveFo1MWZNYjR3NUt6anZwU1U0UU1nQ1dUZDNQd2NCQy0tU2lUWHhEbUFRSWxpaUI1NWpkV1FGUT09--6ef7522c91ac8ee16cc587cffaef24d12c41ddcc; srchID=f8838c24f07b4dafa02bd1435eaac82a; criteria=pg%3D1%26sprefix%3D%252Frealestateandhomes-search%26area_type%3Dcity%26search_type%3Dcity%26city%3DBeaverton%26state_code%3DOR%26state_id%3DOR%26lat%3D45.477764%26long%3D-122.8168974%26county_fips%3D41067%26county_fips_multi%3D41067%26loc%3DBeaverton%252C%2520OR%26locSlug%3DBeaverton_OR%26county_needed_for_uniq%3Dfalse; last_ran=-1; AMCV_8853394255142B6A0A4C98A4%40AdobeOrg=-1124106680%7CMCIDTS%7C19171%7CMCMID%7C60448848225504571971823027342865190689%7CMCAID%7CNONE%7CMCOPTOUT-1656457737s%7CNONE%7CvVersion%7C5.2.0; _px3=bff4a4fe793afeab79ba705576d7a30c8d203a9fd74de0f0b6e68cf6a56e776a:K4y4T/AZ9X3DsF2yMR0ZgMn4YqZyVWl+p9uW/uSEsSffWD/OiCutdLR+P3Cs1sCrjKATMcyaANB5/N9RF+wirw==:1000:dN+xBAPNb3QeS4gUCqNmWgmH04dKl0XFJFQjFWHbkYYcEJFP6Ni/sU8wP1gc96sUNEvSNiOdIZjmAK3h/CHzFMsGmdi7mBBMmvbJLQ8ed1kV2F35oXjhdZU16G2NNSquagQn9SJzTZ9iKf0gq83igbOtibasU3mKl6gGtwo4ouRxcMbVHAsfTpRuORtNSme08aqySOxwE3E9ZPAqkSzsdw==; last_ran_threshold=1656450679799',
    'origin': 'https://www.realtor.com',
    'referer': (f'https://www.realtor.com/realestateandhomes-search/{city}_{state}'),
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36',
}

params = {
    'client_id': 'rdc-x',
    'schema': 'vesta',
}

json_data = {
    'query': '\n\nquery ConsumerSearchMainQuery($query: HomeSearchCriteria!, $limit: Int, $offset: Int, $sort: [SearchAPISort], $sort_type: SearchSortType, $client_data: JSON, $bucket: SearchAPIBucket)\n{\n  home_search: home_search(query: $query,\n    sort: $sort,\n    limit: $limit,\n    offset: $offset,\n    sort_type: $sort_type,\n    client_data: $client_data,\n    bucket: $bucket,\n  ){\n    count\n    total\n    results {\n      property_id\n      list_price\n      primary_photo (https: true){\n        href\n      }\n      source {\n        id\n        agents{\n          office_name\n        }\n        type\n        spec_id\n        plan_id\n      }\n      community {\n        property_id\n        description {\n          name\n        }\n        advertisers{\n          office{\n            hours\n            phones {\n              type\n              number\n            }\n          }\n          builder {\n            fulfillment_id\n          }\n        }\n      }\n      products {\n        brand_name\n        products\n      }\n      listing_id\n      matterport\n      virtual_tours{\n        href\n        type\n      }\n      status\n      permalink\n      price_reduced_amount\n      other_listings{rdc {\n      listing_id\n      status\n      listing_key\n      primary\n    }}\n      description{\n        beds\n        baths\n        baths_full\n        baths_half\n        baths_1qtr\n        baths_3qtr\n        garage\n        stories\n        type\n        sub_type\n        lot_sqft\n        sqft\n        year_built\n        sold_price\n        sold_date\n        name\n      }\n      location{\n        street_view_url\n        address{\n          line\n          postal_code\n          state\n          state_code\n          city\n          coordinate {\n            lat\n            lon\n          }\n        }\n        county {\n          name\n          fips_code\n        }\n      }\n      tax_record {\n        public_record_id\n      }\n      lead_attributes {\n        show_contact_an_agent\n        opcity_lead_attributes {\n          cashback_enabled\n          flip_the_market_enabled\n        }\n        lead_type\n        ready_connect_mortgage {\n          show_contact_a_lender\n          show_veterans_united\n        }\n      }\n      open_houses {\n        start_date\n        end_date\n        description\n        methods\n        time_zone\n        dst\n      }\n      flags{\n        is_coming_soon\n        is_pending\n        is_foreclosure\n        is_contingent\n        is_new_construction\n        is_new_listing (days: 14)\n        is_price_reduced (days: 30)\n        is_plan\n        is_subdivision\n      }\n      list_date\n      last_update_date\n      coming_soon_date\n      photos(limit: 2, https: true){\n        href\n      }\n      tags\n      branding {\n        type\n        photo\n        name\n      }\n    }\n  }\n}',
    'variables': {
        'query': {
            'status': [
                'for_sale',
                'ready_to_build',
            ],
            'primary': True,
            'search_location': {
                'location': (f'{city}, {state}'),
            },
        },
        'client_data': {
            'device_data': {
                'device_type': 'web',
            },
            'user_data': {
                'last_view_timestamp': -1,
            },
        },
        'limit':41,
        'offset': 0,
        'zohoQuery': {
            'silo': 'search_result_page',
            'location': (f'{city}'),
            'property_status': 'for_sale',
            'filters': {},
            'page_index': '1',
        },
        'geoSupportedSlug': (f'{city}_{state}'),
        'sort': [
            {
                'field': 'list_date',
                'direction': 'desc',
            },
            {
                'field': 'photo_count',
                'direction': 'desc',
            },
        ],
        'by_prop_type': [
            'home',
        ],
    },
    'operationName': 'ConsumerSearchMainQuery',
    'callfrom': 'SRP',
    'nrQueryType': 'MAIN_SRP',
    'visitor_id': '1ae3a798-c7a2-4fd6-bc2a-b84aec36420f',
    'isClient': True,
    'seoPayload': {
        'asPath': (f'/realestateandhomes-search/{city}_{state}/sby-6'), #need to add page number to the end of this so I can use a for loop to iterate through every page
        'pageType': {
            'silo': 'search_result_page',
            'status': 'for_sale',
        },
        'county_needed_for_uniq': False,
    },
}

response = requests.post('https://www.realtor.com/api/v1/hulk_main_srp', params=params, headers=headers, json=json_data)

result_json = response.json()
high_level = result_json['data']
home_search = high_level['home_search']
result_items = home_search['results']


#----------------------Address info
#street_address
result_items[0]['location']['address']['line']
#city
result_items[0]['location']['address']['city']
#state eg: OR
result_items[0]['location']['address']['state_code']
#zip_code
result_items[0]['location']['address']['postal_code']

#home_type
result_items[0]['description']['type']
#year_built
result_items[0]['description']['year_built']
#bedrooms
result_items[0]['description']['beds']
#bathrooms
result_items[0]['description']['baths']
#sq_foot
result_items[0]['description']['lot_sqft']
#price
result_items[0]['list_price']

# address = (f'{street_address} {city} {state}, {zip_code}')
# print(address)

home_type = []
year_built = []
address = []
bedrooms = []
bathrooms = []
sq_foot = []
price = []

for result in result_items:
    try:
        home_type.append(result['description']['type'])
    except:
        home_type.append('')
    try:
        year_built.append(result['description']['year_built'])
    except:
        year_built.append('')
    try:
        address.append(result['location']['address']['line'])
    except:
        address.append('')
    try:
        bedrooms.append(result['description']['beds'])
    except:
        bedrooms.append('')
    try:
        bathrooms.append(result['description']['baths'])
    except:
        bathrooms.append('')
    try:
        sq_foot.append(result['description']['lot_sqft'])
    except:
        sq_foot.append('')
    try:
        price.append(result['list_price'])
    except:
        price.append('')

df_realtor = pd.DataFrame({'Home Type': home_type, 'Year Built': year_built, 'Address': address, 'Bedrooms': bedrooms, 'Bathrooms': bathrooms, 'Square Feet': sq_foot, 'Price': price})

df_realtor.to_csv(r'C:\Users\tyson\Documents\Webdev Portfolio\Python\webscraper\csv\realtor_data.csv', header=True)
