from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import datetime


def get_all_users(collection_users) -> list:
    try:
        users_list = list(collection_users.find())
    except Exception as ex:
        print(f'The error from the "get_all_users" function: {ex}')
    else:
        return users_list


def get_config(collection_config) -> dict:
    try:
        deviation = list(collection_config.find())[0]
    except Exception as ex:
        print(f'The error from the "get_deviation" function: {ex}')
    else:
        return deviation


def get_id_list_from_the_db(collection_users) -> list:
    try:
        id_list = list(collection_users.find().sort({'_id': -1}))
    except Exception as ex:
        print(f'The error from the "get_id_from_the_db" function: {ex}')
    else:
        return id_list


def add_id_in_the_db(collection_users, user_id) -> bool:
    try:
        user_id = int(user_id)
        is_find = collection_users.find_one({'user': user_id})
        if is_find is None:
            collection_users.insert_one({'user': user_id})
            return True

    except Exception as ex:
        print(f'The error from the "add_id_in_the_db" function: {ex}')


def delete_id_from_the_db(collection_users, nums: str, id_list: list) -> bool:
    if ',' in nums:
        nums = nums.split(', ')
    elif nums.lower() == 'все':
        nums = 'all'
    else:
        nums = list(nums)

    try:
        if nums != 'all':
            for num in nums:
                collection_users.delete_one({'user': id_list[int(num) - 1]['user']})
        else:
            collection_users.delete_many({})

    except Exception as ex:
        print(f'The error in the delete_id_from_the_db function: {ex}')
    else:
        return True


def get_links(url: str) -> list:
    driver = webdriver.Firefox()
    list_of_links = []

    try:
        driver.get(url)
        time.sleep(5)
    except Exception as ex:
        print(f'The error in the get_links function: {ex}')
    else:
        max_y = int(driver.execute_script("return document.body.scrollHeight"))
        is_continue = True
        for i in range(0, max_y, 500):
            if is_continue:
                driver.execute_script(f"window.scrollTo(0, {i});")
                time.sleep(2)
                matches = driver.find_elements(By.CLASS_NAME, "match-container")
                for match in matches:
                    current_time = datetime.datetime.now().strftime("%H:%M")
                    match_time = match.find_element(By.CLASS_NAME, 'time').text

                    if current_time >= match_time:
                        list_of_links.append(match.get_attribute('href'))
                    else:
                        is_continue = False
                        break
            else:
                break

        return list(set(list_of_links))
    finally:
        driver.quit()
