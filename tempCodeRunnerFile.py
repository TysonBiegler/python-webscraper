    result_json = response.json()
    high_level = result_json['data']
    home_search = high_level['home_search']
    result_items = home_search['results']