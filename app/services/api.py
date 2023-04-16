import requests 


def create_crew(crew_name: str) -> dict:
    request = f"htpps://starship.com/create_crew/{crew_name}"
    #response = requests.get(request).json
    response = {"token": "oGmeLokYjCxJk-0ztVipcv5pmomkmLXbvkC-lrTarK0", 
                "status": 0, 
                "linked_users": []}
    return response
