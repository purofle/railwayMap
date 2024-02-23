import asyncio
import os
from typing import Dict

import pydantic_core

from api.api import get_train_left_ticket
from get_train_list import TrainListType
from models.Train import Train

head = "G"
list_file_name = f"train_list_{head}.json"
train_list: Dict[str, Train] = {}


async def main():
    with open(list_file_name, "r") as f:
        global train_list
        train_list = TrainListType.validate_json(f.read())

    done_trains = os.listdir("trains")
    count = len(done_trains)

    for t in train_list.values():
        if f"{t.station_train_code}.json" in done_trains:
            print(f"Skip {t.station_train_code}")
            continue
        with open(f"trains/{t.station_train_code}.json", "wb") as f:
            count += 1
            print(f"获取 {t.station_train_code}，已经有 {count} 个")
            f.write(pydantic_core.to_json(await get_train_left_ticket(t.train_no)))


if __name__ == "__main__":
    asyncio.run(main())
