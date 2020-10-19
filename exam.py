with open("/home/pi/coding/git_rasp/telegram_bot/ppom_max_num.txt", "r") as f:
    max_num = int(f.readline().replace("'",""))
    print(max_num)
# 뽐뿌 최신 게시글 번호 불러오기
def update_ppom_max_num():
    with open("/home/pi/coding/git_rasp/telegram_bot/ppom_max_num.txt", "w") as f:
        f.write(str(max_num))