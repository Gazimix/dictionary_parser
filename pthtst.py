import re

def win_path_from_wsl_path(lin_path):
    i = 0
    path_pieces = str(lin_path).split('/')
    regex = r"\/mnt\/[a-z]\/.*"
    cmp = re.compile(regex)
    if re.match(cmp, lin_path):
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

def wsl_path_from_win_path(win_path):
    i = 0
    path_pieces = str(win_path).split('\\')
    regex = r"[A-Z]:\\.*"
    cmp = re.compile(regex)
    if re.match(cmp, win_path):
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

def print_ln():
    print("__________________________________________")

print_ln()
win_path_from_wsl_path("/mnt/d/Google Drive/Documents/Linguistics/English III.docx")
print_ln()
win_path_from_wsl_path("D:\\Google Drive\\Documents\\Linguistics\\English III.docx")
print_ln()
wsl_path_from_win_path("/mnt/d/Google Drive/Documents/Linguistics/English III.docx")
print_ln()
wsl_path_from_win_path("D:\\Google Drive\\Documents\\Linguistics\\English III.docx")
print_ln()