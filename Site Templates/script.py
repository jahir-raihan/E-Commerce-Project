import os
file_name = os.listdir('html')

for file in file_name:
    lines = open('html/'+file, 'r').readlines()

    file_new = open('html/'+file, 'w')
    for idx, line in enumerate(lines):
        if line.strip().startswith('<link'):
            l = line.split('href')
            l = l[0] + 'href' + l[1][0:2] + '..' + l[1][2:]
            lines[idx] = l

        if line.strip().startswith('<img'):
            l = line.split('src')
            l = l[0] + 'src' + l[1][0:2] + '..' + l[1][2:]
            lines[idx] = l

    file_new.writelines(lines)
