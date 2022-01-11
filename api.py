import json
import requests
import os
from requests_toolbelt.multipart.encoder import MultipartEncoder


class PetFriends:
    """апи библиотека к веб приложению Pet Friends"""

    def __init__(self):
        self.base_url = "https://petfriends1.herokuapp.com/"

    # GET api/key
    def get_api_key(self, email: str, passwd: str) -> json:
        '''Метод отправляет get запрос,
        возвращает код ответа, JSON с уникальным ключем пользователя'''

        headers = {
            'email': email,
            'password': passwd,
        }
        # получаем ключ пользователя
        res = requests.get(self.base_url+'api/key', headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    # get api/pets
    def get_list_of_pets(self, auth_key: json, filter: str = "") -> json:
        '''Метод возвращает код ответа и JSON со списком найденых питомцев:
        1. если в переменную filter передать значение my_pets, то метод возвращает список питомцев
        авторизованного пользователя;
        2. если в переменную filter передать пустую строку, то будет возвращен список всех питомцев сайта.'''

        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        # получаем список питомцев
        res = requests.get(self.base_url + 'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    # post api/pets
    def add_new_pet(self, auth_key: json, name: str, animal_type: str,
                    age: str, pet_photo: str) -> json:
        '''Метод позволяет добавить нового питомца, возвращает
        код ответа и JSON с данными нового питомца'''

        # Получаем полный путь к изображению питомца и сохраняем в переменную pet_photo
        pet_photo = os.path.join(os.path.dirname(__file__), os.path.abspath(pet_photo))
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        # добавляем нового питомца
        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    # delete api/pets/{petid}
    def delete_pet(self, auth_key: json, pet_id: str):
        '''Метод удаляет питомца с указанным ID, возвращает код 200'''

        headers = {'auth_key': auth_key['key']}

        # удаляем питомца
        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        status = res.status_code
        return status

    # put /api/pets/{petid}
    def update_pet_info(self, auth_key: json, pet_id: str, name: str,
                        animal_type: str, age: int) -> json:
        '''Метод обновляет данные о питомце с переданным ID, возвращает
        код ответа и JSON с обновлённыи данными питомца'''

        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }

        # обновляем данные
        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    # post /api/create_pet_simple
    def add_new_pet_without_photo(self, auth_key: json, name: str, animal_type: str, age: str) -> json:
        '''Метод позволяет добавить нового питомца без фото.
        Возвращает код ответа, JSON с данными питомца'''

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        # добавляем питомца без фото
        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    # post /api/pets/set_photo/{pet_id}
    def add_new_pet_photo(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        '''Метод позволяет добавить/заменить фотографию питомцу. Возвращает код ответа,
        JSON с данными питомца'''

        # Получаем полный путь к изображению питомца и сохраняем в переменную pet_photo
        pet_photo = os.path.join(os.path.dirname(__file__), os.path.abspath(pet_photo))
        data = MultipartEncoder(
            fields={
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        # добавляем фото питомцу
        res = requests.post(self.base_url + 'api/pets/set_photo/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result
