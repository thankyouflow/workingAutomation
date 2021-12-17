import os

def makedirs(path):
  try:
    os.makedirs(path)
  except OSError:
    if not os.path.isdir(path):
      raise

while True:
  target = input("채점 cs 파일의 경로와 파일명을 입력해주세요. (파일을 끌어서 넣어주세요)\n종료 - ctrl + c\n").replace(' ', '')
  f = open(target, 'r')

  fuzzy2 = []
  fuzzy3 = []

  check = False
  while True:
      line = f.readline().replace(' ', '')
      if not line: break
      if "채점프로그램환경구조체" in line:
        check = True

      elif '{}' not in line and "}" in line:
        break

      if check:
        if line[:2] == "DS":
          data = line.split("+")[1].split(".")[0].replace("\"", "").strip()
          if 'A' in data.split("_")[0] or 'B' in data.split("_")[0]:
            fuzzy2.append(data)
          else:
            fuzzy3.append(data)

  path = os.getcwd() + '/Downloads/fuzzyText'
  makedirs(path)

  fileName = input("급수를 입력해주세요.").replace(' ', '')

  with open(path + "/FUZZY2_" + fileName + ".txt", "w") as wf:
    for text in fuzzy2:
      wf.write(text + ";\n")

  with open(path + "/FUZZY3_" + fileName + ".txt", "w") as wf:
    for text in fuzzy3:
      wf.write(text + ";\n")

  f.close()

  print("파일 생성 위치 : " + path + "\n")
