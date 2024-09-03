from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import datetime

url = 'https://www.aiscore.com/ru'


def get_links(link: str) -> list:
    driver = webdriver.Firefox()
    list_of_links = []

    try:
        driver.get(link)
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


def data_parse(lnks: list):
    driver = webdriver.Firefox()
    for link in lnks:
        try:
            driver.get(link)
            time.sleep(3)

            nums = driver.find_element(By.CLASS_NAME, 'stats2').text.split('\n')
            first_num = int(nums[6])
            second_num = int(nums[8])
            print(f'Link: {link}, {first_num} - {second_num}')

            if first_num != 0 and second_num != 0 and (first_num / second_num >= 3 or second_num / first_num >= 3):
                print('Signal')
            elif (first_num == 0 or second_num == 0) and (first_num - second_num >= 3 or second_num - first_num >= 3):
                print('Signal')
        except Exception as ex:
            print(f'The error in the data_parse function: {ex}')

    driver.quit()


links = get_links(url)
data_parse(links)


# Если находит today's upcomind match, то не парсим дальше
# (int(nums[6])/int(nums[8]) >= 3) or (int(nums[8])/int(nums[6]) >= 3)