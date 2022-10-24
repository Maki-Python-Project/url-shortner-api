def conver_fetch_to_dict(values):
    list_of_values_from_fetch = []
    most_popular_dict = {}

    for idx in range(len(values)):
        list_of_values_from_fetch.append({'longurl': values[idx][0], 'shorturl': values[idx][1]})

    most_popular_dict['most_popular'] = list_of_values_from_fetch

    return most_popular_dict
