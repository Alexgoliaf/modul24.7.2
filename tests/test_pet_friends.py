from api import PetFriends
from settings import valid_email, valid_password

pf=PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result=pf.get_api_key(email,password)
    assert status==200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key=pf.get_api_key(valid_email,valid_password)
    status, result=pf.get_list_of_pets(auth_key,filter)
    assert status==200
    assert len(result['pets'])>0



def test_post_add_pet_with_valid_key():
    _, auth_key=pf.get_api_key(valid_email,valid_password)
    _, my_pets=pf.get_list_of_pets(auth_key,filter='my_pets')
    status, result=pf.post_add_new_pet(auth_key,name='Boris',animal_type='cat',age='7',pet_photo='images/foto.jpg')
    assert status==200
    assert 'name'in result
    print(my_pets)

def test_delete_pet_with_valid_key():
    _, auth_key=pf.get_api_key(valid_email,valid_password)
    _, my_pets=pf.get_list_of_pets(auth_key,filter='my_pets')
    if len(my_pets['pets']) == 0:
        pf.post_add_new_pet(auth_key, "Boriska", "кот", "4", "images/foto.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id=my_pets['pets'][0]['id']
    status,_=pf.delete_pet(auth_key,pet_id)
    _,my_pets=pf.get_list_of_pets(auth_key,'my_pets')
    assert status==200
    assert pet_id not in my_pets.values()
    print(my_pets)

def test_successful_update_self_pet_info(name='Борис', animal_type='Бритва', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")
def test_post_add_new_pets_simple():
    _, auth_key=pf.get_api_key(valid_email,valid_password)
    _, my_pets=pf.get_list_of_pets(auth_key,filter='my_pets')
    status, result=pf.post_add_new_pet_simple(auth_key, name='Красавчик', animal_type='dog',age='1')
    assert status==200
    assert  'name' in result
    print(my_pets)

def test_post_photo():
    _, auth_key=pf.get_api_key(valid_email,valid_password)
    _, my_pets=pf.get_list_of_pets(auth_key,filter='my_pets')
    # Еслди список не пустой, то пробуем добавить фотографию
    if len(my_pets['pets']) > 0:
        status, result = pf.post_add_photo(auth_key, my_pets['pets'][0]['id'],pet_photo='images/sobaka.jpg' )
        assert status==200
        assert 'name' in result
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")
def test_keys1():
    status, result=pf.get_api_key(email=valid_email)
    assert status==200
    assert 'key'in result
"""Попытка получить ключ без ввода пароля, тест падает"""

def test_keys2():
    _, auth_key=pf.get_api_key(valid_email,valid_password)
    _,my_pets=pf.get_list_of_pets(auth_key,filter='my_pets')
    if len(my_pets['pets']) >=3:
        pf.post_add_new_pet_simple(auth_key, "Boriska", "кот", "4")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][-1]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    assert status == 200
    assert pet_id not in my_pets.values()
    print(my_pets)
    """Если питомцев от 3 и более , удаляем последнего и заменяем его на питомца без фотографии, тест прошел"""

def test_keys3():
    _,auth_key=pf.get_api_key(valid_email,valid_password)
    _,my_pets=pf.get_list_of_pets(auth_key)
    status, result=pf.get_list_of_pets(auth_key,filter=my_pets)
    assert status==200
    assert ''in result
"""Статус 500. нет значения фильтра"""

def test_keys4():
    status, result=pf.get_list_of_pets(auth_key="5d8071c2cca0423c9ee594d9338778ae2f816da552bc3328ddda2d4e",filter='my_pets')
    assert status==200
    assert len(result['pets'])>=0
    """Не удается получить список животных используя валидный ключ и фильтр"""

