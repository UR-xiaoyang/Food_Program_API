from datetime import datetime

def 输出日志(操作, IP, 操作人):
    # 获取当前时间
    current_time = datetime.now()
    print(f"[{current_time.strftime('%Y-%m-%d|%H:%M:%S')}] {IP} --> {操作人} {操作}")
def debug():
    输出日志("测试", "127.0.0.1", "DEBUG")
# debug()
