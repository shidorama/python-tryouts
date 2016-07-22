def normalize_structure_cp(tree):
    """
    Method transforms convoluted dic-list mix that facebook returns into dict structure with lists or basic types
    as endpoints
    :param tree:
    :type tree: dict|list|string
    :return:
    """
    normalized_tree = {}
    if not isinstance(tree, (list, dict)):
        return tree
    elif isinstance(tree, list):
        pre_list = [normalize_structure(leaf) for leaf in tree]
        for l in pre_list:
            pre_result = {}
            if isinstance(l, dict):
                pre_result.update(l)
        if pre_result:
            return pre_result
        return pre_list
    elif isinstance(tree, dict):
        end_keys = ('name', 'value')
        for key in end_keys:
            if key in tree:
                return tree[key]
        pre_dict = {k: normalize_structure(v) for k, v in tree.iteritems()}
        normalized_tree.update(**pre_dict)

    return normalized_tree