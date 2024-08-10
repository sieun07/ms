from datetime import datetime

def current_time():
    now = datetime.now()
    time_string = now.strftime("%Y년 %m월 %d %H시 %M분 %S초")
    return(f"현재시간: {time_string}")

if __name__ == '__main__':
    print(current_time())