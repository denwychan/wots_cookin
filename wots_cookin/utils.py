import os

def get_path(file_path, abs_path = os.path.abspath(__file__)):
    abs_path = abs_path.split('/')
    new_path = ''
    check = 0

    for dir in abs_path[1:]:
        if dir == 'wots_cookin':
            check = 1
        if check == 0:
            new_path += f'/{dir}'

    new_path += file_path
    return new_path
