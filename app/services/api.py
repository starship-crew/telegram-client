import config
import requests 
from services import api_response_example


def create_crew(crew_name: str) -> dict:
    request = f"{config.SERVER}/api/crew"
    #response = requests.post(request, params={"name": crew_name})
    response = api_response_example.CREATE_CREW
    return response#.json()


def get_ship(API_TOKEN: str) -> dict:
    request = f"{config.SERVER}/api/crew/ship"
    #response = requests.get(request, params={"token": API_TOKEN})
    response = api_response_example.GET_SHIP
    return response#.json()


def get_crew(API_TOKEN: str) -> dict:
    request = f"{config.SERVER}/api/crew"
    #response = requests.get(request, params={"token": API_TOKEN})
    response = api_response_example.GET_CREW
    return response#.json()


def get_garage(API_TOKEN: str) -> dict:
    request = f"{config.SERVER}/api/crew/garage"
    #response = requests.get(request, params={"token": API_TOKEN})
    response = api_response_example.GARAGE
    return response#.json()


def detail_put_off(API_TOKEN: str, detail_id: int) -> None:
    request = f"{config.SERVER}/api/crew/detail_copy/put_off"
    response = requests.get(request, params={"token": API_TOKEN, 
                                             "id": detail_id})


def detail_put_on(API_TOKEN: str, detail_id: int) -> None:
    request = f"{config.SERVER}/api/crew/detail_copy/put_on"
    response = requests.get(request, params={"token": API_TOKEN, 
                                             "id": detail_id})


def upgrade_detail(API_TOKEN: str, detail_id: int) -> None:
    request = f"{config.SERVER}/api/crew/detail_copy/upgrade"
    response = requests.get(request, params={"token": API_TOKEN, 
                                             "id": detail_id})



