import os
import shutil

file_path = '/Users/tyflow/Downloads/test/FAT1_answer'
file_names = os.listdir(file_path)


"""
폴더 안에 있는 파일명 변경
"""
a = 0
for name in file_names:
    src = os.path.join(file_path, name)
    filename = name.split('_')[1] + 'DB'
    if name != '.DS_Store':
      target_name = os.listdir(src)
      # 파일형식 잘못된 부분 걸러내는 부분
      if 'rar' not in target_name[0]:
        print(name)
      target_src = os.path.join(src, target_name[0])
      os.rename(target_src, os.path.join(src, filename + '.rar'))


    # 파일이동
    src = os.path.join(file_path, name)
    if name != '.DS_Store':
      target_name = os.listdir(src)
      target_src = os.path.join(src, target_name[0])
      to_ = '/Users/tyflow/Downloads/FAT1_result'
      shutil.move(target_src, to_)