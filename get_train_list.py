import asyncio
import os
from typing import Dict

import pydantic_core
from aiohttp import ContentTypeError
from pydantic import TypeAdapter

from api import api
from models.Train import Train

TrainListType = TypeAdapter(Dict[str, Train])
train_list: Dict[str, Train] = {}
head = "G"
file_name = f"train_list_{head}.json"


def add_train_list(train: Train):
    train_list[train.station_train_code] = train
    print("added train", train.station_train_code)


def check_train_list(train_code: str) -> bool:
    return train_code in train_list.keys()


async def main():
    # 判断文件是否存在
    if not os.path.exists(file_name):
        with open(file_name, "w") as f:
            f.write("{}")
    # load data
    with open(file_name, "r") as f:
        global train_list
        train_list = TrainListType.validate_json(f.read())

    print(f"已有{len(train_list.keys())}条数据")

    try:
        for i in range(1, 10000):
            if check_train_list(f"{head}{i}"):
                print(f"已经有了{head}{i}")
                continue
            remote_train_list = await api.get_train_list(f"{head}{i}")
            for remote_train in remote_train_list:
                if check_train_list(remote_train.station_train_code):
                    print(f"已经有了{remote_train.station_train_code}")
                    continue
                add_train_list(remote_train)
    except ContentTypeError:
        print(f"被12306制裁了，已经爬到了{len(train_list)}条{head}头车辆数据")
        train_list_dict = pydantic_core.to_json(train_list)
        with open(file_name, "wb") as f:
            f.write(train_list_dict)


if __name__ == "__main__":
    asyncio.run(main())
