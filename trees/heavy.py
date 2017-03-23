class basestring(str):
    pass

class unicode(str, basestring):
    pass

def _dynamic_auto_parsing(data, levels=1, from_level=None):
    """
    All in one method, normalizes structure and flattens resulting struct
    :param data: data for processing
    :type data: dict|list|int|string|float
    :param levels: flattening level, 1 is default
    :type levels: int
    :param from_level:
    :type from_level: type
    :return:
    :rtype dict|list|string
    :rtype int
    :rtype type
    :rtype bool
    """
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

    if current_level == dict and subtypes.issubset(
            end_data):  # Data needs extraction; we don't need everything from dict
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
        return newres, new_levels, current_level, True

    return result, new_levels, current_level, True
