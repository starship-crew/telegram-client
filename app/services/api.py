import requests 


def create_crew(crew_name: str) -> dict:
    request = f"https://starship.com/create_crew/{crew_name}"
    #response = requests.get(request).json
    response = {
                "token": "oGmeLokYjCxJk-0ztVipcv5pmomkmLXbvkC-lrTarK0", 
                "status": 0, 
                "linked_users": []
               }
    return response


def get_ship(API_TOKEN: str) -> dict:
    request = f"https://starship.com/crew/{API_TOKEN}/ship"
    #response = requests.get(request).json
    response = {
                "shame": "luzer",  
                "details": [], 
                "health": 200, 
                "maneuverability": 50, 
                "damage_absorption": 75, 
                "damage": 100, 
                "stability": 80, 
                "power_generation": 150, 
                "power_consumption": 140, 
                "accel_factor": 300, 
                "detail_limit": 5, 
               }
    return response
