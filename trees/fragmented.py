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
