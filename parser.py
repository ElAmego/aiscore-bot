from utils.utils import *


def activate_parser(bot, collection_users, url):
    links = get_links(url)

    if links and len(links) != 0:
        users = get_all_users(collection_users)
        driver = webdriver.Firefox()
        msg = None
        print(links)
        for link in links:
            try:
                driver.get(link)
                time.sleep(3)
            except Exception as ex:
                print(f'The error in the activate_parser function: {ex}')
            else:
                nums = driver.find_element(By.CLASS_NAME, 'stats2').text.split('\n')
                first_num = int(nums[6])
                second_num = int(nums[8])

                print(f'{first_num} - {second_num}')

                if first_num != 0 and second_num != 0 and (first_num/second_num >= 3 or second_num/first_num >= 3):
                    msg = f'🔎Signal Dangerous Attack\n➡️{url}'
                elif (first_num == 0 or second_num == 0) and (first_num - second_num >= 3 or second_num - first_num >= 3):
                    msg = f'🔎Signal Dangerous Attack\n➡️{url}'

                if msg:
                    for user in users:
                        try:
                            bot.send_message(user['user'], msg)
                        except Exception:
                            pass

        driver.quit()
