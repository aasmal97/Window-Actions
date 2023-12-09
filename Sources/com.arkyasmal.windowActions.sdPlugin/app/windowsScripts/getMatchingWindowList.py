import re
from determineActiveWindows import get_active_windows
def test_regex(pattern, testStr):
    result = re.search(pattern, testStr)
    return result
def get_matching_windows_list(win_id_type, win_id):
    id_type = "title" if win_id_type == 'win_title' or win_id_type == 'win_ititle' else win_id_type
    is_partial_str = win_id_type == 'win_ititle'
    all_windows = get_active_windows()
    matching_windows_itr = filter(lambda window: test_regex(win_id, window[id_type]) if is_partial_str else window[id_type] == win_id, all_windows)
    matching_windows = list(matching_windows_itr)
    return matching_windows