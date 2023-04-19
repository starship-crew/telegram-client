import requests 
from services import api_response_example


def create_crew(crew_name: str) -> dict:
    request = f"https://starship.com/create_crew/{crew_name}"
    #response = requests.get(request).json
    response = api_response_example.CREATE_CREW
    return response


def get_ship(API_TOKEN: str) -> dict:
    request = f"https://starship.com/crew/{API_TOKEN}/ship"
    #response = requests.get(request).json
    response = api_response_example.GET_SHIP
    return response


def get_crew(API_TOKEN: str) -> dict:
    request = f"https://starship.com/crew/{API_TOKEN}/crew"
    #response = requests.get(request).json
    response = api_response_example.GET_CREW
    return response


def get_garage(API_TOKEN: str) -> dict:
    request = f"https://starship.com/crew/{API_TOKEN}/garage"
    #response = requests.get(request).json
    response = api_response_example.GARAGE
    return response
