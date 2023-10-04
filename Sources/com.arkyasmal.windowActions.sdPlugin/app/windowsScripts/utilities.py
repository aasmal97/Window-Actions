def one_indexed(num): 
    return int(num) - 1
def get_window_id(cmd_args): 
    win_id = cmd_args[cmd_args.index("--winId") + 1]
    win_id_type = cmd_args[cmd_args.index("--winIdType") + 1]
    return (win_id, win_id_type)