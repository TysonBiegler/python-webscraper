import requests
import pandas as pd
import json



# city = input("City?: ")
# if not re.match('^[A-Za-z]*$', city):
#     print('Error! Only letters a-z allowed.')   
# state = input(f'Two Character State?: ')
# if not re.match('^[A-Za-z]*$', state):
#     print('Error! Only letters a-z allowed.')
# elif len(state)>2:
#     print('Error! Only 2 Characters allowed!')
# print(f'Looking for houses in {city}, {state}.')

city = 'Beaverton'
state = 'OR'
print(f'Looking for houses in {city}, {state}.')

page_number = 1
page_index = (f'/pg-')

headers = {
    
    'accept': 'application/json',
    'origin': 'https://www.realtor.com',
    'referer': 'https://www.realtor.com/realestateandhomes-search/Beaverton_OR/pg-1',
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
            'limit': 42,
            'offset': 0,
            'zohoQuery': {
                'silo': 'search_result_page',
                'location': (f'{city}, {state}'),
                'property_status': 'for_sale',
                'filters': {},
            },
            'sort_type': 'relevant',
            'geoSupportedSlug': (f'{city}_{state}'),
            'bucket': {
                'sort': 'modelF',
                'rerank': 'earth_fix',
            },
            'resetMap': '2022-07-01T21:26:26.636Z0.044973431329219604',
            'by_prop_type': [
                'home',
            ],
        },
        'operationName': 'ConsumerSearchMainQuery',
        'callfrom': 'SRP',
        'nrQueryType': 'MAIN_SRP',
        'user_id': '5d5caca34e1e060093e5b2ec',
        'isClient': True,
        'seoPayload': {
            'asPath': (f'/realestateandhomes-search/{city}_{state}/sby-6'),
            'pageType': {
                'silo': 'search_result_page',
                'status': 'for_sale',
            },
            'county_needed_for_uniq': False,
        },
    }

response = requests.post('https://www.realtor.com/api/v1/hulk_main_srp', params=params, headers=headers, json=json_data)


result_items = response.json()['data']['home_search']
count = result_items["count"]
total = result_items["total"]
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

while page_number < 14:
    page_number += 1
    page_url = response.json()['data']['zoho']['meta_data']['canonical_url']

    full_url = (f'full_url: {page_url}{page_index}{page_number}')

    headers = {
        
        'accept': 'application/json',
        'origin': 'https://www.realtor.com',
        'referer': 'https://www.realtor.com/realestateandhomes-search/Beaverton_OR/pg-1',
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
                'limit': 42,
                'offset': 0,
                'zohoQuery': {
                    'silo': 'search_result_page',
                    'location': (f'{city}, {state}'),
                    'property_status': 'for_sale',
                    'filters': {},
                },
                'sort_type': 'relevant',
                'geoSupportedSlug': (f'{city}_{state}'),
                'bucket': {
                    'sort': 'modelF',
                    'rerank': 'earth_fix',
                },
                'resetMap': '2022-07-01T21:26:26.636Z0.044973431329219604',
                'by_prop_type': [
                    'home',
                ],
            },
            'operationName': 'ConsumerSearchMainQuery',
            'callfrom': 'SRP',
            'nrQueryType': 'MAIN_SRP',
            'user_id': '5d5caca34e1e060093e5b2ec',
            'isClient': True,
            'seoPayload': {
                'asPath': (f'{full_url}'),
                'pageType': {
                    'silo': 'search_result_page',
                    'status': 'for_sale',
                },
                'county_needed_for_uniq': False,
            },
        }
    response = requests.post('https://www.realtor.com/api/v1/hulk_main_srp', params=params, headers=headers, json=json_data)

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
# print(df_realtor)
df_realtor.to_csv(r'C:\Users\tyson\Documents\Webdev Portfolio\Python\webscraper\csv\realtor_data.csv', header=True)