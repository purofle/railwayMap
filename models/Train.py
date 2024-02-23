from pydantic import BaseModel


class Train(BaseModel):
    date: str
    from_station: str
    station_train_code: str
    to_station: str
    total_num: int
    train_no: str


class TrainLeftTicket(BaseModel):
    arrive_time: str
    arrive_day_str: str
    running_time: str
    start_time: str

    station_name: str
    station_no: str
