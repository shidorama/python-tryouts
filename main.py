# -*- coding: latin-1 -*-
from twisted.internet import reactor
from twisted.protocols.basic import LineReceiver

def main():
    pass


class DataParser(object):
    skip_fields = ['geo_locations', 'flexible_specs']
    def __init__(self):
        pass
        # self.data = data
        # x = self._parse_targeting_data(self.data)
        # return x

    def _parse_targeting_data(self, fb_obj):
        targeting = fb_obj.get('targeting')

        for field in targeting:
            if field not in self.skip_fields:
                self._auto_parse(targeting[field])

        if targeting.get('geo_locations'):
            fb_obj.update(self._get_countries(targeting.get('geo_locations')))

        flexible_specs = fb_obj.get('flexible_specs')
        if flexible_specs:
            fb_obj['audiences'] = list(self._get_audiences(flexible_specs))

        return fb_obj

    def _auto_parse(self, obj):
        if isinstance(obj, (basestring, int, float)):
            return obj


    @classmethod
    def _get_countries(cls, geo_locations):
        """
        Method iterates through geo_data and forms 3 distinct datasets: cities, regions and countries
        :type geo_locations: list
        :param geo_locations: data from facebook
        :return: resulting dictionary with up to 3 keys: cities, regions, countries
        :rtype dict
        """
        geo_data = {}
        countries = set()
        cities = set()
        regions = set()
        if isinstance(geo_locations.get('cities'), list):
            cities.update([c['name'] for c in geo_locations['cities']])
            regions.update([c['region'] for c in geo_locations['cities']])
            countries.update([c['country'] for c in geo_locations['cities']])
        if isinstance(geo_locations.get('regions'), list):
            regions.update([c['name'] for c in geo_locations['regions']])
            countries.update([c['country'] for c in geo_locations['regions']])
        if isinstance(geo_locations.get('countries'), list):
            countries.update(geo_locations['countries'])

        if countries:
            geo_data['countries'] = list(countries)
        if regions:
            geo_data['regions'] = list(regions)
        if cities:
            geo_data['cities'] = list(cities)

        return geo_data

    def _get_audiences(self, audiences):
        audiences_result = {}
        if not isinstance(audiences, (list, dict)):
            return audiences
        elif isinstance(audiences, list):
            pre_list = [self._get_audiences(audience) for audience in audiences]
            for l in pre_list:
                pre_result = {}
                if isinstance(l, dict):
                    pre_result.update(l)
            if pre_result:
                return pre_result
            return pre_list
        elif isinstance(audiences, dict):
            end_keys = ('name', 'value')
            for key in end_keys:
                if key in audiences:
                    return audiences[key]
            pre_dict = {k:self._get_audiences(v) for k, v in audiences.iteritems()}
            audiences_result.update(**pre_dict)

        return audiences_result




dt = {
    "targeting": {
        "age_max": 45,
        "age_min": 18,
        "flexible_spec": [
            {
                "interests": [
                    {
                        "id": "6002971095994",
                        "name": "Action games"
                    },
                    {
                        "id": "6003020622093",
                        "name": "Taylor Swift"
                    }
                ],
                "user_adclusters": [
                    {
                        "id": "6008588203383",
                        "name": "Fast Food"
                    }
                ],
                "behaviors": [
                    {
                        "id": "6006289261825",
                        "name": "Crossover"
                    },
                    {
                        "id": "6006289262825",
                        "name": "Luxury SUV"
                    },
                    {
                        "id": "6006371352132",
                        "name": "Farmers"
                    },
                    {
                        "id": "6015559470583",
                        "name": "Expats (All)"
                    }
                ],
                "life_events": [
                    {
                        "id": "6005149512172",
                        "name": "New job"
                    }
                ]
            }
        ],
        "friends_of_connections": [
            {
                "id": "1728780934030988",
                "name": "My Favorit Product"
            }
        ],
        "geo_locations": {
            "regions": [
                {
                    "key": "3849",
                    "name": "Connecticut",
                    "country": "US"
                },
                {
                    "key": "3854",
                    "name": "Hawaii",
                    "country": "US"
                },
                {
                    "key": "3864",
                    "name": "Massachusetts",
                    "country": "US"
                },
                {
                    "key": "3875",
                    "name": "New York",
                    "country": "US"
                }
            ],
            "countries": [
                "US"
            ],
            "cities": [
                {
                    "country": "ES",
                    "distance_unit": "mile",
                    "key": "673453",
                    "name": "Barcelona",
                    "radius": 25,
                    "region": u"Cataluña",
                    "region_id": "1029"
                }
            ],
            "location_types": [
                "home",
                "recent"
            ]
        },
        "locales": [
            23,
            44,
            9
        ],
        "user_os": [
            "Android_ver_5.1_and_above"
        ]
    },
    "id": "6052531977602"
}

# y = DataParser(dt)

class LEVELS():
    CATALOG = list


def _dynamic_auto_parsing(data, levels=1, from_level=None):
    current_level = type(data)
    end_data = {basestring, int, float, str, unicode}
    types = set()
    subtypes = set()
    if current_level in end_data:
        return [data], levels, current_level, True

    result = []
    for entry in data:
        if current_level == dict:
            prep_data = data[entry]
        elif current_level == list:
            prep_data = entry

        types.add(type(entry))
        if len(types) > 1 and not types.issubset(end_data):
            return [], levels, current_level, True

        new_data, new_levels, lower_level, unpack = _dynamic_auto_parsing(prep_data, levels, current_level)
        subtypes.add(lower_level)
        if new_levels == 0 and unpack:
            result.extend(new_data)
        elif current_level == dict:
            result.append([entry, new_data])
        else:
            result.append([None, new_data])

    if current_level == dict and subtypes.issubset(end_data): #Data needs extraction; we don't need everything from dict
        for entry in result:
            if entry[0] in ('name', 'value'):
                return entry[1], levels, current_level, True
        return [], new_levels, current_level, True

    if new_levels > 0 and from_level is not None:
        newres = []
        for x in result:
            newres.extend(x[1])
        new_levels -= 1
        return newres, new_levels, current_level, False

    if from_level is None:
        newres = {}
        for entry in result:
            newres[entry[0]] = entry[1]
        return newres

    return result, new_levels, current_level, True


def _dynamic_auto_parsing_2(dt):
    pass


def normalize_structure(dt):
    if type(dt) not in (list, dict):
        return dt
    if isinstance(dt, dict):
        return parse_dict(dt)
    return parse_list(dt)


def parse_list(lst):
    interrupt = False
    for x in lst:
        if isinstance(x, (dict, list)):
            interrupt = True
            break
    if interrupt:
        result = flatten_list([normalize_structure(x) for x in lst])
        return result

    return lst


def flatten_list(lst):
    result = {}
    for x in lst:
        if isinstance(x, dict):
            result.update(x)
            continue
        return lst
    return result


def parse_dict(dct):
    end_keys = ('name', 'value')
    for key in end_keys:
        if key in dct:
            return dct[key]
    return {x:normalize_structure(dct[x]) for x in dct if isinstance(dct[x], (list, dict))}


# wow = _dynamic_auto_parsing(dt, 1)
woe = normalize_structure(dt)
www = DataParser()
wowww = www._get_audiences(dt)
print wow
