# pywintypes import is required or else .exe won't build properly
import functools
import pywintypes
from win32api import EnumDisplayMonitors, GetMonitorInfo, EnumDisplayDevices
from win32com.client import GetObject
from difflib import SequenceMatcher


def convert_unit16_to_str(arr):
    chr_list = [chr(x) for x in arr]
    filtered_list = list(filter(lambda char: len(char) <= 1, chr_list))
    new_str = functools.reduce(lambda a, b: a+b, filtered_list)
    return new_str.rstrip('\x00')


def extract_keys(obj, parent_key=''):
    keys = []

    if isinstance(obj, dict):  # Check if the object is a dictionary
        for k, v in obj.items():
            full_key = f"{parent_key}.{k}" if parent_key else k
            keys.append(str(full_key))  # Convert key to string and add to list
            keys.extend(extract_keys(v, full_key))  # Recursively extract keys
    elif isinstance(obj, list):  # If the object is a list, check each item
        for i, item in enumerate(obj):
            keys.extend(extract_keys(item, f"{parent_key}[{i}]"))

    return keys


def get_monitor_name(monitor: dict[str, str | None]):
    name: str
    if monitor["user_name"] != None:
        name = convert_unit16_to_str(monitor["user_name"])
    elif monitor['code'] != None and monitor['man_name'] != None:
        name = f'{convert_unit16_to_str(monitor["man_name"])} - {
            convert_unit16_to_str(monitor["code"])}'
    else:
        name = f'Generic PnP Monitor - {str(monitor['idx'])}'
    return name


def get_monitor_names():
    names = [GetMonitorInfo(x[0])["Device"] for x in EnumDisplayMonitors()]
    monitor_ids = [EnumDisplayDevices(names[x], 0, 1).DeviceID.replace(
        "#", "\\") for x in range(len(names))]
    obj_wmi = GetObject('winmgmts:\\\\.\\root\\WMI').InstancesOf(
        'WmiMonitorID')  # WmiMonitorConnectionParams
    instance_names = [dict(instance_name=item.InstanceName,
                           man_name=item.ManufacturerName, code=item.ProductCodeID, user_name=item.UserFriendlyName, idx=i + 1) for i, item in enumerate(obj_wmi)]
    for instance in instance_names:
        highest_match = {"match": "", "idx": 0}
        for idx in range(len(monitor_ids)):
            pattern = instance['instance_name'].replace("\\", " ")
            test_str = monitor_ids[idx].replace("\\", " ")
            sequence = SequenceMatcher(None, pattern, test_str).find_longest_match(
                0, len(pattern), 0, len(test_str))
            matching_str = test_str[sequence.a:sequence.a + sequence.size]
            if len(matching_str) > len(highest_match['match']):
                highest_match.update({'match': matching_str, "idx": idx})
        # we want the idx to be 1-indexed
        instance.update({"idx": highest_match["idx"] + 1})
    instance_names = [
        {**item, "name": get_monitor_name(item)} for item in instance_names]
    return instance_names
