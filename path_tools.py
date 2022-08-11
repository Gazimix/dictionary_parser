import platform
import re

SYSTEM = platform.system()

def win_path_from_linux_path(lin_path):
    i = 0
    path_pieces = str(lin_path).split('/')
    is_param_linux_path = is_wsl_path(lin_path)
    if is_param_linux_path:
        win_pth = ""
        for piece in path_pieces:
            if i == 0 or i == 1:
                pass
            elif i == 2:
                win_pth += piece.upper() + ":\\"
            elif i < len(path_pieces) - 1:
                win_pth += piece + "\\"
            elif i == len(path_pieces) - 1:
                win_pth += piece
            i += 1
        # print(win_pth)
        return win_pth
    else:
        # print(lin_path)
        return lin_path

def is_wsl_path(lin_path):
    regex = r"\/mnt\/[a-z]\/.*"
    cmp = re.compile(regex)
    is_param_linux_path = re.match(cmp, lin_path)
    return is_param_linux_path

def wsl_path_from_win_path(win_path):
    i = 0
    path_pieces = str(win_path).split('\\')
    is_param_win_path = is_win_path(win_path)
    if is_param_win_path:
        lin_path = "/mnt/"
        for piece in path_pieces:
            if i == 0:
                lin_path += piece[0].lower() + "/"
            elif i < len(path_pieces) - 1:
                lin_path += piece + "/"
            elif i == len(path_pieces) - 1:
                lin_path += piece
            i += 1
        # print(lin_path)
        return lin_path
    else:
        # print(win_path)
        return win_path

def is_win_path(win_path):
    regex = r"[A-Z]:\\.*"
    cmp = re.compile(regex)
    is_param_win_path = re.match(cmp, win_path)
    return is_param_win_path


def extract_os_path_from_normalized_path(path):
    if SYSTEM == 'Linux':
        return path
    elif SYSTEM == 'Windows':
        return win_path_from_linux_path(path)
