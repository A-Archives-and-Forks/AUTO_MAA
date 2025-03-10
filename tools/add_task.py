import uuid

import requests

server_url = "http://localhost:5000"


def add_quick_task(task_type, task_id=None, params=None):
    if not task_id:
        task_id = str(uuid.uuid4())

    task = {"id": task_id, "type": task_type}
    if params:
        task["params"] = params

    response = requests.post(f"{server_url}/maa/addTask", json=task)
    print("Add Task Response:", response.json())
    return response.json()


def get_tasks():
    response = requests.post(f"{server_url}/maa/getTask", json={"user": "test", "device": "test_device"})
    print("Get Tasks Response:", response.json())
    return response.json()


if __name__ == "__main__":
    valid_task_types = {
        "LinkStart-Base",  # 这个不知道干啥的，我估计是连接adb的
        "LinkStart-WakeUp",  # 开始唤醒
        "LinkStart-Combat",  # 刷理智
        "LinkStart-Recruiting", # 自动公招
        "LinkStart-Mall", # 获取信用及购物
        "LinkStart-Mission", # 领取奖励
        "LinkStart-AutoRoguelike", # 自动肉鸽
        "LinkStart-ReclamationAlgorithm", # 盐酸
        "CaptureImage", # 截图
        "LinkStart", # 一键长草
        "Toolbox-GachaOnce", # 抽卡一次
        "Settings-ConnectionAddress", # 修改设置-连接地址；Settings-[SettingsName] 型的任务的 type 的可选值为 Settings-ConnectionAddress, Settings-Stage1
        "CaptureImageNow", # 立刻截图任务，和上面的截图任务是基本一样的，唯一的区别是这个任务会立刻被运行，而不会等待其他任务。
        "StopTask" , # 停止任务
        "HeartBeat" # 心跳任务，该任务会立即返回，并且将当前“顺序执行的任务”队列中正在执行的任务的Id作为Payload返回，如果当前没有任务执行，返回空字符串。
    }
    add_quick_task("LinkStart-WakeUp")
    add_quick_task("CaptureImage")
    add_quick_task("LinkStart-Recruiting")
    add_quick_task("CaptureImage")
    add_quick_task("LinkStart-Mall")
    add_quick_task("CaptureImage")
    add_quick_task("LinkStart-Mission")
    add_quick_task("CaptureImage")
