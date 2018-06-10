import json


def extract(filename):
    ''' (str) -> list of object
    Given the filename of a JSON file in the current directory, extract and return
    its data.
    :param filename: name of the JSON file:
    :return data: data extracted from the JSON file:
    '''
    file = open(filename, 'r')
    json_decode = json.load(file)
    data = []
    for item in json_decode:
        data.append(item)
    return data
