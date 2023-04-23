import config
import requests


def create_crew(crew_name: str) -> dict:
    request = f"{config.SERVER}/api/crew"
    response = requests.post(request, params={"name": crew_name})
    #response = api_response_example.CREATE_CREW
    return response.json()


def get_ship(API_TOKEN: str) -> dict:
    request = f"{config.SERVER}/api/ship"
    response = requests.get(request, params={"token": API_TOKEN})
    #response = api_response_example.GET_SHIP
    return response.json()


def get_crew(API_TOKEN: str) -> dict:
    request = f"{config.SERVER}/api/crew"
    response = requests.get(request, params={"token": API_TOKEN})
    #response = api_response_example.GET_CREW
    return response.json()


def get_garage(API_TOKEN: str) -> dict:
    request = f"{config.SERVER}/api/garage"
    response = requests.get(request, params={"token": API_TOKEN})
    #response = api_response_example.GARAGE
    return response.json()


def get_detail_copy(API_TOKEN: str, detail_id: int) -> dict:
    request = f"{config.SERVER}/api/detail_copy"
    response = requests.get(request, params={"token": API_TOKEN, 
                                             "id": detail_id})
    return response.json()


def get_detail_type(API_TOKEN: str, detail_type_id: str) -> dict:
    request = f"{config.SERVER}/api/detail"
    response = requests.get(request, params={"token": API_TOKEN, 
                                             "id": detail_type_id})
    return response.json()


def detail_put_off(API_TOKEN: str, detail_id: int) -> None:
    request = f"{config.SERVER}/api/detail_copy"
    response = requests.put(request, params={"token": API_TOKEN, 
                                             "id": detail_id, 
                                             "action": "put_off"})


def detail_put_on(API_TOKEN: str, detail_id: int) -> None:
    request = f"{config.SERVER}/api/detail_copy"
    response = requests.put(request, params={"token": API_TOKEN, 
                                             "id": detail_id, 
                                             "action": "put_on"})


def upgrade_detail(API_TOKEN: str, detail_id: int) -> None:
    request = f"{config.SERVER}/api/detail_copy"
    response = requests.put(request, params={"token": API_TOKEN, 
                                             "id": detail_id, 
                                             "action": "upgrade"})

def get_store() -> dict:
    request = f"{config.SERVER}/api/store"
    response = requests.get(request)
    #response = api_response_example.GET_SHOP
    return response.json()


def buy_detail(API_TOKEN: str, detail_id: int) -> None:
    requset = f"{config.SERVER}/api/detail"
    response = requests.post(requset, params={"token": API_TOKEN, 
                                             "id": detail_id})
