from datetime import datetime
from typing import List

import aiohttp
import pydantic

from models.Train import Train, TrainLeftTicket


async def get_train_list(keyword: str, date: str = "") -> List[Train]:
    if not date:
        date = datetime.today().strftime("%Y%m%d")
    url = 'https://search.12306.cn/search/v1/train/search'
    async with aiohttp.request("GET", url, params={"keyword": keyword, "date": date}) as r:
        return pydantic.TypeAdapter(List[Train]).validate_python((await r.json())["data"])


async def get_train_left_ticket(train_id: str, date: str = "") -> List[TrainLeftTicket]:
    if not date:
        date = datetime.today().strftime("%Y-%m-%d")
    url = "https://kyfw.12306.cn/otn/queryTrainInfo/query"
    async with aiohttp.request("GET", url, params={
        "leftTicketDTO.train_no": train_id,
        "leftTicketDTO.train_date": date,
        "rand_code": "",
    }) as r:
        result = (await r.json())["data"]["data"]
        return [TrainLeftTicket(
            arrive_time=t["arrive_time"],
            arrive_day_str=t["arrive_day_str"],
            running_time=t["running_time"],
            start_time=t["start_time"],

            station_name=t["station_name"],
            station_no=t["station_no"],
        ) for t in result]
