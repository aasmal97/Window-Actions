import os


def empty_obj(curr_dict):
    return curr_dict is None or len(curr_dict.keys()) <= 0


def merge(a: dict, b: dict, path=[]):
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] != b[key]:
                raise Exception('Conflict at ' + '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a


def merge_all(dictionaries: list[dict]):
    result: dict = {}
    for dictionary in dictionaries:
        result = merge(result, dictionary)
    return result


def get_directory_tree(path: str):
    parts = path.split(os.path.sep)
    tree: dict[str, dict] = {
        parts[0]: {}
    }
    curr_tree = tree
    for i in range(len(parts)-1):
        prev_path = parts[i]
        curr_path = parts[i+1]
        curr_tree = curr_tree[prev_path]
        curr_tree[curr_path] = {}
    return tree


def relative_to_top(path: str):
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    new_path = os.path.normpath(os.path.abspath(
        os.path.join(curr_dir, fr'..\{path}')))
    return get_directory_tree(new_path)


dir_to_ignore = merge_all([
    relative_to_top(
        r'Sources\com.arkyasmal.windowactions.sdPlugin\app\buildFiles'),
    relative_to_top(r'Sources\com.arkyasmal.windowactions.sdPlugin\app\dll'),
    relative_to_top(
        r'Sources\com.arkyasmal.windowactions.sdPlugin\app\windowsScripts'),
    relative_to_top(r'Sources\com.arkyasmal.windowactions.sdPlugin\test'),
])


def files_to_ignore(dir, files):
    curr_path = os.path.normpath(os.path.abspath(os.path.join(dir)))
    val = files
    parts = curr_path.split(os.path.sep)
    curr_tree = dir_to_ignore
    for i in parts:
        # means we are in an excluded dir
        if empty_obj(curr_tree):
            return val
        elif i in curr_tree:
            curr_tree = curr_tree[i]
        # if we never exit it not excluded
        else:
            return []
    return val if empty_obj(curr_tree) else []
