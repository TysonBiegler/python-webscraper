from audioop import add
from xml.sax.handler import property_lexical_handler
from numpy import full
import requests
import pandas as pd
from torch import are_deterministic_algorithms_enabled
import re


city = input("City?: ")
if not re.match('^[A-Za-z]*$', city):
    print('Error! Only letters a-z allowed.')   
state = input(f'Two Character State?: ')
if not re.match('^[A-Za-z]*$', state):
    print('Error! Only letters a-z allowed.')
elif len(state)>2:
    print('Error! Only 2 Characters allowed!')
print(f'Looking for houses in {city}, {state}.')

#cURL start from realtor.com
headers = {
    'authority': 'www.realtor.com',
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.9',
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
        'limit':200,
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
#cURL end from realtor.com


result_items = response.json()['data']['home_search']
print(f'count: {result_items["count"]}')
print(f'total: {result_items["total"]}')
result_items = result_items['results']

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
#print(df_realtor)
#df_realtor.to_csv(r'C:\Users\tyson\Documents\Webdev Portfolio\Python\webscraper\csv\realtor_data.csv', header=True)


#looping through the other pages -start-
home_type = []
year_built = []
address = []
bedrooms = []
bathrooms = []
sq_foot = []
price = []
#cURL start from realtor.com
for i in range(1,51):
    page_increment = (f'/pg-{str(i)}')
    headers = {
        'authority': 'www.realtor.com',
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9',
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
            'limit':200,
            'offset': 0,
            'zohoQuery': {
                'silo': 'search_result_page',
                'location': (f'{city}'),
                'property_status': 'for_sale',
                'filters': {},
                'page_index': str(i),
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
            'asPath': (f'/realestateandhomes-search/{city}_{state}/sby-6{page_increment}'),
            'pageType': {
                'silo': 'search_result_page',
                'status': 'for_sale',
            },
            'county_needed_for_uniq': False,
        },
    }
    #response
    response = requests.post('https://www.realtor.com/api/v1/hulk_main_srp', params=params, headers=headers, json=json_data)
    #cURL end from realtor.com

    #json object
    result_items = response.json()['data']['home_search']
    #result items
    result_items = result_items['results']

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
#print(df_realtor)
df_realtor.to_csv(r'C:\Users\tyson\Documents\Webdev Portfolio\Python\webscraper\csv\realtor_data.csv', header=True)
