__author__ = "Kirill Cherkasov"
import random
import string
import os
import subprocess
import hashlib
import re


def create_file(namef, dir_name, size):
    if not size.isdigit():
        if size.endswith('KB'):
            s1 = size.split('KB')
            size1 = int(s1[0]) * 1024
            token = ''.join(random.choice(
                string.ascii_uppercase + string.ascii_lowercase +
                string.digits) for x in range(size1))
        if size.endswith('MB'):
            s1 = size.split('MB')
            size1 = int(s1[0]) * 1048576
            token = ''.join(random.choice(
                string.ascii_uppercase + string.ascii_lowercase +
                string.digits) for x in range(size1))
        if size.endswith('GB'):
            s1 = size.split('GB')
            size1 = int(s1[0]) * 1073741824
            token = ''.join(random.choice(
                string.ascii_uppercase + string.ascii_lowercase +
                string.digits) for x in range(size1))
    else:
        token = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(int(size)))
    try:
        token
    except NameError:
        token = 's'
    if not os.path.exists(os.path.join(os.getcwd(), dir_name)):
        os.mkdir(dir_name)
    file = open(dir_name + namef, "w")
    file.write(token)
    file.close()
    return os.path.getsize(os.path.join(os.getcwd(), dir_name, namef[1:]))


def glue_files(files_dir, hash_file, outfile):
    '''
    склеивает файлы из директории files_dir выбирая за основу
    hash_file, склеивает всё в outfile
    :param files_dir:
    :param hash_file:
    :param outfile:
    :return:
    '''
    result = {}
    hash_list = []
    with open(os.path.join(files_dir,hash_file), 'r', encoding='utf-8') as hash_file_stream:
        for line in hash_file_stream:
            hash_list.append(line[:-1])
    for file_name in os.listdir(files_dir):
        with open(os.path.join(files_dir, file_name), 'rb') as file:
            text = hashlib.md5(file.read()).hexdigest()
            if text in hash_list:
                result[hash_list.index(text)] = file_name
    with open(outfile, 'wb') as out:
        for file_name in result.values():
            with open(os.path.join(files_dir, file_name), 'rb') as file:
                out.write(file.read())
    raw_string = subprocess.check_output(['file', outfile]).decode('utf-8')
    os.rename(outfile, '.'.join((outfile, get_file_extension(raw_string))))
    return len(result)


def get_file_extension(raw_string):
    '''
    с помощью утилиты file (Unix) опрелеляет тип файла
    и возвращает его расширение, выбирая из вывода утилиты при
    помощи регулярного выражения нужные символы
    :param raw_string:
    :return:
    '''
    pattern = r'[a-z]*: ([A-Z]*)'
    return re.findall(pattern, raw_string)[0].lower()


def part_file(file_name, piece_size, destination_folder='parted'):
    count = 0
    with open(file_name, 'rb') as source_file:
        while True:
            tmp = source_file.read(piece_size)
            if tmp == b'':
                break
            parted_file_name = hashlib.md5(tmp).hexdigest()
            with open(os.path.join(destination_folder, parted_file_name), 'wb') as parted_file:
                parted_file.write(tmp)
            count += 1
    return count


def main():
    if __name__ == '__main__':
        glue_files('files/file2/', 'parts.md5', 'file2')
        glue_files('files/file1/', 'parts.md5', 'file1')
        print(create_file("/test1.txt", ".", '10KB'))
        print(create_file("/test2.txt", ".", '1024'))
        print(create_file("/test11.txt", ".", '2MB'))
        print(create_file("/test21.txt", ".", '1B'))
        part_file('file1.jpeg', 1024)
        print()
main()
