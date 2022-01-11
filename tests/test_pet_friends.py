from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password, \
    petname, petage, pettype, petphoto, \
    newpetname, newpetage, newpettype, newpetphoto, \
    invalid_photo, longpetname


pf = PetFriends()

# получить ключ пользователя с корректными регистрационными данными
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    '''Тест проверяет, что в ответе на запрос приходит код 200,
     и содержится слово key'''

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

# получить ключ пользователя с НЕ корректными регистрационными данными
def test_get_api_key_for_invalid_user(email=invalid_email, password=invalid_password):
    '''Негативный тест, который проверяет, что в случае с не корректными значениями email и password
    в ответе на запрос приходит код 403'''

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert '403 Forbidden' in result

# получить список всех питомцев с корректным ключем
def test_get_all_pets_with_valid_key(filter=''):
    '''Тест проверяет, что запрос всех питомцев сайта возвращает не пустой список'''

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

# получить список своих питомцев с корректным ключем
def test_get_my_pets_with_valid_key(filter='my_pets'):
    '''Тест позволяет получить список своих питомцев'''

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert 'pets' in result

# добавить нового питомца с корректными данными
def test_add_new_pet_with_valid_data(name=petname, animal_type=pettype,
                                     age=petage, pet_photo=petphoto):
    '''Тест проверяет возможность добавления питомца с корректными данными.
    Проверяет код ответа и имя добавленного питомца'''

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

# удалить питомца
def test_successful_delete_self_pet():
    '''Тест удаляет первого питомца из списка своих питомцев. Если список пустой,
    то добавляет питомца и удаляет его.
    Проверяет код ответа и отсутствие ID удаленного питомца в списке питомцев'''

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, petname, pettype, petage, petphoto)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

# обновить данные о питомце
def test_successful_update_self_pet_info(name=newpetname, animal_type=newpettype, age=newpetage):
    '''Тест проверяет возможность обновления данных о питомце'''

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список питомцев пустой, то добавляем нового питомца и получаем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, petname, pettype, petage, petphoto)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Обновляем данные о питомце
    status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
    assert status == 200
    assert result['name'] == name

# добавить нового питомца без фото
def test_add_new_pet_without_photo(name=petname, animal_type=pettype, age=petage):
    '''Тест проверяет возможность добавления питомца с корректными данными, без фото.
    Проверяет код ответа, сравнивает имя пиомца'''

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

# добавить/обновить фотографию питомцу
def test_successful_update_pet_photo(photo=newpetphoto):
    '''Тест проверяет возможность обновления/добавления фотографии питомца.
    Проверяет код ответа, сравнивает ID питомца, фото которого обновляли
    и ID питомца, который вернул запрос, проверяет наличие фотографии'''

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список питомцев пустой, то добавляем нового питомца и получаем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet_without_photo(auth_key, petname, pettype, petage)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Обновляем данные о питомце
    status, result = pf.add_new_pet_photo(auth_key, my_pets['pets'][0]['id'], photo)
    assert status == 200
    assert result['id'] == my_pets['pets'][0]['id']
    assert result['pet_photo'] != ''

# попытка добавить/обновить фотографию питомцу, указав некорректный файл
def test_not_successful_update_pet_photo(photo=invalid_photo):
    '''Негативный тест на возможность добавления вместо фотографии некорректного файла
    Ожидает от сервера код ответа 500'''

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список питомцев пустой, то добавляем нового питомца и получаем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet_without_photo(auth_key, petname, pettype, petage)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Обновляем данные о питомце
    status, result = pf.add_new_pet_photo(auth_key, my_pets['pets'][0]['id'], photo)
    assert status == 500
    assert '500 Internal Server Error' in result

# добавить нового питомца с возрастом < 0
def test_add_new_pet_with_invalid_data(name=petname, animal_type=pettype,
                                     age='-1', pet_photo=petphoto):
    '''Тест проверяет возможность добавления питомца с не корректными данными (возраст < 0).
    Ожидает код ответа 400'''

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400

# добавить питомца без имени
def test_add_new_pet_without_name(name='', animal_type=pettype,
                                     age=petage, pet_photo=petphoto):
    '''Тест проверяет возможность добавления питомца без имени.
    Ожидает код ответа 400'''

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400

# удалить имя питомца
def test_not_successful_update_self_pet_info(name='', animal_type=newpettype, age=newpetage):
    '''Тест проверяет возможность удаления имени питомца.
    Ожидает код ответа 400.'''

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список питомцев пустой, то добавляем нового питомца и получаем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, petname, pettype, petage, petphoto)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Обновляем данные о питомце
    status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
    assert status == 400

# добавить нового питомца с динной имени более 50 символов
def test_add_new_pet_with_too_long_name(name=longpetname, animal_type=pettype,
                                     age=petage, pet_photo=petphoto):
    '''Тест проверяет возможность добавления питомца с не корректными данными (длинна имени более 50 символов).
    Ожидает код ответа 400'''

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400


# получить список своих питомцев с НЕ корректным ключем
def test_get_all_pets_with_invalid_key(filter='my_pets'):
    '''Тест проверяет возможность получить список своих питомцев,
    если ключ авторизации был изменен'''

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    auth_key['key'] += '1'
    status, _ = pf.get_list_of_pets(auth_key, filter)
    assert status == 403
    