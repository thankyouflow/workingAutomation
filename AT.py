import os

file_path = '/Users/tyflow/Downloads/AT47회/AT47회'
file_names = os.listdir(file_path)

for name in file_names:
    print(name)
    src = os.path.join(file_path, name)
    filename = os.path.splitext(name)
    dst = os.path.join(file_path, filename[0] + '.txt')
    os.rename(src, dst)
    r = open(dst, mode='rt', encoding='utf-8')
    x = r.read()
    target = x.split('try')[1].split('catch')[0].split('\n')
    for t in target:
        change = ''
        if t.find('DS_') >= 0:
            tableName = t.split('DS_')[1].split('.')[0]
            print(tableName)
            print(x.count(tableName))
            if x.count(tableName) <= 3:
                if t.strip()[:2] != '//':
                    change = '//' + t.strip()
            else:
                if t.strip()[:2] == '//':
                    change = t.strip()[2:]
        if change:
            print(change)
            x = x.replace(t.strip(), change)
    # w = open(dst, mode='wt', encoding='utf-8')
    # w.write(x)
    # w.close()
    break