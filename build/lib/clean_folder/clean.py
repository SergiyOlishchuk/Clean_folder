import os
import sys
from string import punctuation
import zipfile

def normalize(name: str) -> str:
    letters = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k',
        'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'ts',
        'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya', 'і': 'i', ' ' : ' '
    }

    result = ''
    for letter in ''.join(name.split('.')[:-1]):
        if letter in punctuation:
            result += '_'
        elif not letter.isdigit():
            if letter.lower() in letters.keys():
                result += letters[letter.lower()] if letter.islower() else letters[letter.lower()].upper()
            else:
                result += letter

    return result + '.' + name.split('.')[-1]

def archive_processing(path_to_file: str, folder_path: str):
    folder = os.path.join(folder_path, normalize(path_to_file.split('\\')[-1]))
    os.mkdir(folder)
    with zipfile.ZipFile(path_to_file) as archive:
        archive.extractall(folder)
    
    os.remove(path_to_file)

def sorting(path: str, service_folders: dict) -> list:
    unknown_files = []

    for item in os.listdir(path):
        new_path = os.path.join(path, item)
        if new_path in [i['path'] for i in service_folders.values()]:
            continue

        if os.path.isdir(new_path):
            unknown_files.extend(sorting(new_path, service_folders=service_folders))
            try:
                os.rmdir(new_path)
            except OSError:
                pass
        else:
            if new_path.endswith(service_folders['images']['extentions']):
                os.replace(src=new_path, dst=os.path.join(service_folders['images']['path'], normalize(item)))
            elif new_path.endswith(service_folders['video']['extentions']):
                os.replace(src=new_path, dst=os.path.join(service_folders['video']['path'], normalize(name=item)))
            elif new_path.endswith(service_folders['docs']['extentions']):
                os.replace(src=new_path, dst=os.path.join(service_folders['docs']['path'], normalize(name=item)))
            elif new_path.endswith(service_folders['audio']['extentions']):
                os.replace(src=new_path, dst=os.path.join(service_folders['audio']['path'], normalize(name=item)))
            elif new_path.endswith(service_folders['archives']['extentions']):
                archive_processing(new_path, service_folders['archives']['path'])
            else:
                unknown_files.append(new_path)
            
    return unknown_files


def main():
    if not len(sys.argv) == 2:
        print('Invalid count of arguments')
        quit()
        
    path = sys.argv[1]
    
    service_folders = {
        'images' : {
            'path' : os.path.join(path, 'images'),
            'extentions' : ('.jpeg', '.png', '.jpg', '.svg')
        },
        'video' : {
            'path' : os.path.join(path, 'video'),
            'extentions' : ('.avi', '.mp4', '.mov', '.mkv')
        },
        'docs' : {
            'path' : os.path.join(path, 'documents'),
            'extentions' : ('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx')
        },
        'audio' : {
            'path' : os.path.join(path, 'audio'),
            'extentions' : ('.mp3', '.ogg', '.wav', '.amr')
        },
        'archives' : {
            'path' : os.path.join(path, 'archives'),
            'extentions' : ('.zip', '.gz', '.tar')
        }
    }

    for item in service_folders.values():
        if not os.path.exists(item['path']):
            os.mkdir(item['path'])

    print(sorting(path, service_folders))

        

if __name__ == '__main__':
    main()