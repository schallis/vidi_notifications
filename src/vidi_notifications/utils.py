def from_vidi_format(orig_dict):
    """Convert Vidi json format to sensible python compatible version"""
    new_dict = {}
    for field in orig_dict['field']:
        new_dict[field['key']] = field['value']
    return new_dict


def to_vidi_format(orig_dict):
    """Convert sensible json to verbose Vidi format"""
    new_dict = {'field': []}
    for key, value in orig_dict.items():
        new_dict['field'].append({
            'key': key,
            'value': value,
        })
    return new_dict


class JobObject(object):
    """
        Provides direct dictionary style item access to the wrapped json
    """

    def __init__(self, data):
        self.data = data

    def __getattr__(self, item):
        return self.data[item]

    def __getitem__(self, item):
        return self.data[item]

    def __contains__(self, item):
        return item in self.data.keys()
