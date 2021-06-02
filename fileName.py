import os

file_path = '/Users/tyflow/Downloads/answerData'
file_names = os.listdir(file_path)

for name in file_names:
    src = os.path.join(file_path, name)
    dst = name.split('_')[1]
    dst = os.path.join(file_path, dst)
    os.rename(src, dst)