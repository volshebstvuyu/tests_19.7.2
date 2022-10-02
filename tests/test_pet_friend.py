from api import PetFriends
from settings import *
import json
import os

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_api_key_for_invalid_user(email=invalid_email, password=invalid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

def test_get_list_of_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_get_list_of_pets_with_invalid_key(filter=''):
    status, result = pf.get_list_of_pets(invalid_auth_key, filter)
    assert status == 403
    assert 'pets' not in result

def test_successfill_delete_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        _, _ = pf.add_new_pet(auth_key, 'name', 'anymal_type', 'age', 'pet_photo')
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, result = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()
    # assert result != ''



def test_add_new_pet_with_valid_data(name= 'Гоголь', animal_type= 'Шобак', age= '3', pet_photo= 'images/IMG_5554.JPG'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

def test_add_new_pet_with_invalid_data(name= 'Гоголь', anymal_type= 'Шобак', age= '3', pet_photo= 'images/dog-044.png'):
    status, result = pf.add_new_pet(invalid_auth_key, name, anymal_type, age, pet_photo)
    assert status == 403
    assert type(result) != json



def test_successful_update_pet(name= 'Хрюндель', animal_type= 'Шобакинг', age= '5'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, list_of_pets = pf.get_list_of_pets(auth_key, '')
    if len(list_of_pets['pets']) > 0:
        old_name = list_of_pets['pets'][0]['name']
        status, result = pf.update_pet(auth_key, list_of_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] != old_name
    else:
        assert True

def test_add_new_pet_simple_with_valid_data(name='Гоголь', anymal_type='Шобак', age='3'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth_key, name, anymal_type, age)
    assert status == 200
    assert result['name'] == name

def test_add_new_pet_simple_with_invalid_data(name=3365654654, anymal_type=True, age='3'):
    status, result = pf.add_new_pet_simple(invalid_auth_key, name, anymal_type, age)
    assert status == 403
    assert type(result) != json

def test_add_photo_of_a_pet_with_valid_data(pet_photo= 'images/IMG_5554.JPG'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, list_of_pets = pf.get_list_of_pets(auth_key, '')
    if len(list_of_pets['pets']) > 0:

        pet_id = list_of_pets['pets'][0]['id']
        status, result = pf.add_photo_of_a_pet(auth_key, pet_id, pet_photo)
        assert status == 200
        assert pet_id in result['id']
    else:
        assert True

def test_add_photo_of_a_pet_with_invalid_data(pet_photo= 'images/dog-044.png',):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_id = 'invalid_pet_id'
    status, result = pf.add_photo_of_a_pet(auth_key, pet_id, pet_photo)
    assert status != 200
    assert pet_id not in result




# def test_deleting_pet_with_valid_key(pet_id):
#     _, auth_key = pf.delete_pet(pet_id=



