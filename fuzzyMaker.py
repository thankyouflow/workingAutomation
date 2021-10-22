target = input("채점 cs 파일의 경로와 파일명을 입력해주세요.")

f = open(target, 'r')

fuzzy2 = []
fuzzy3 = []

check = False
while True:
    line = f.readline()
    if not line: break
    if "채점프로그램 환경 구조체" in line:
      check = True

    elif "}" in line:
      check = False

    if check:
      if "DS" in line and "//" not in line:
        data = line.split("+")[1].split(".")[0].replace("\"", "").strip()
        if 'A' in data.split("_")[0] or 'B' in data.split("_")[0]:
          fuzzy2.append(data)
        else:
          fuzzy3.append(data)

path = input("파일을 만들 경로를 입력해주세요.")
fileName = input("급수를 입력해주세요.")

with open(path + "/FUZZY2_" + fileName + ".txt", "w") as wf:
  for text in fuzzy2:
    wf.write(text + ";\n")

with open(path + "/FUZZY3_" + fileName + ".txt", "w") as wf:
  for text in fuzzy3:
    wf.write(text + ";\n")

f.close()