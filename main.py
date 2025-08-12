import Util

print("데이터 경로를 입력하세요> ")
path = input().strip()

datas = Util.read_files(path)

Util.get_all_match_data(datas)
