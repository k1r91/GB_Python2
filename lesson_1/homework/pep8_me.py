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
            size1 = int(s1[0])*1024
            token = ''.join(random.choice(
                string.ascii_uppercase + string.ascii_lowercase +
                string.digits) for x in range(size1))
        if size.endswith('MB'):
            s1 = size.split('MB')
            size1 = int(s1[0])*1048567
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
    file = open(dir_name + namef, "w")
    file.write(token)


def glue_together(files_dir, hash_file, outfile):
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
    os.rename(outfile, '.'.join((outfile,get_file_extension(outfile))))
    return len(result)


def get_file_extension(file):
    '''
    с помощью утилиты file (Unix) опрелеляет тип файла
    и возвращает его расширение, выбирая из вывода утилиты при
    помощи регулярного выражения нужные символы
    :param file:
    :return:
    '''
    pattern = r'{0}: ([A-Z]*)'.format(file)
    raw_string = subprocess.check_output(['file', file]).decode('utf-8')
    print(raw_string)
    return re.findall(pattern, raw_string)[0]


def split_file(file_name, split_size):
    pass


def main():
    if __name__ == '__main__':
        glue_together('files/file2/', 'parts.md5', 'file2')
        glue_together('files/file1/', 'parts.md5', 'file1')
        create_file("/test1.txt", ".", '10KB')
        create_file("/test2.txt", ".", '1024')
        create_file("/test11.txt", ".", '2MB')
        create_file("/test21.txt", ".", '1B')

main()
