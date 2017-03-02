# -*-coding:utf-8-*-


import dryscrape
import re
from bs4 import BeautifulSoup
import sys
import datetime
import logging
import os.path
import time


logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG, filename=u'mylog.log')

# set charset
reload(sys)
sys.setdefaultencoding('utf-8')


def get_url(url):
    try:
        if 'linux' in sys.platform:
            # start xvfb in case no X is running. Make sure xvfb
            # is installed, otherwise this won't work!
            dryscrape.start_xvfb()

        session = dryscrape.Session()
        session.visit(url)
        return session.body()
    except Exception as e:
        logging.exception("No get %s" % url)


def get_translations_list(date):
    url = 'https://matchtv.ru/tvguide?date=' + date
    need_channels = ['Матч ТВ', 'Матч! Футбол 1', 'Матч! Футбол 2', 'Матч! Футбол 3']

    response = get_url(url)

    soup = BeautifulSoup(response, "lxml")

    need_channels_divs = soup.find_all('div', {
        'class': '_MatchTV_Components_TVProgrammComponent_TVProgrammComponent'})  # get HTML elements
    list = ''  # out string

    for item in need_channels_divs:
        chanel_name = item.find('h3', {'class': 'channel-item-title'})
        if chanel_name:
            chanel_name = chanel_name.find('span',{}).text
            #chanel_name = str(chanel_name)
            if chanel_name:
                chanel_name = chanel_name.strip()
                if chanel_name in need_channels:
                    # print (chanel_name)
                    list += "*{}*\n".format(chanel_name)
                    chanel_translations = item.find_all('div', {'class': 'tv_transmission'})
                    for translations in chanel_translations:
                        # translation_time = translations.find("span").text # translation_label with time
                        translation_label = translations.text
                        translation_label = translation_label.strip()
                        translation_label = re.sub(r'\s', " ", translation_label)
                        translation_label = re.sub("                        ", " ", translation_label)

                        #if ('Футбол.' not in translation_label) and ('Чемпионат' not in translation_label):
                        if (chanel_name == 'Матч ТВ' and 'Футбол.' not in translation_label):
                            continue


                        list += "_{}\n----_\n\n".format(translation_label)

    return list


def get_last_results():
    url = 'http://www.readfootball.com/'

    response = get_url(url)
    soup = BeautifulSoup(response, "lxml")

    last_result_divs = soup.find_all('div', {'class': 'block_football_match'})
    list = ''

    for item in last_result_divs:
        country = item.find('div', {'class': 'country'}).text

        list += country + " / "

        date = item.find('span', {'class': 'date-block-matches'}).text

        list += date + "\n"

        team1 = item.find('td', {'class': 'team1'}).text
        team2 = item.find('td', {'class': 'team2'}).text

        result = item.find('div', {'class': 'button_game'}).find("span").text

        list += "{} {} {}\n\n".format(team1,result,team2)

    return list


def grab():
    now = datetime.datetime.now()
    for x in range(0, 3):  # grab translations of 3 day
        date_set = now + datetime.timedelta(days=x)
        file_path = './tdata/%s_translations' % date_set.strftime("%d-%m-%Y") # date format for grab
        if (os.path.isfile(file_path)):
            continue
        else:
            f = get_translations_list(date_set.strftime("%d-%m-%Y"))

            my_file = open(file_path, "wb")
            my_file.write(f)
            my_file.close()
            time.sleep(3)  # delays for 5 seconds

    time.sleep(1)

    file_path_last_result = './tdata/last_result'
    f = get_last_results()

    print (f.encode('utf8'))
    my_file = open(file_path_last_result, "wb")
    my_file.write(f)
    my_file.close()
    logging.debug(u'Grab success')

    yesterday_date = now - datetime.timedelta(days=1)

    file_path = './tdata/%s_translations' % yesterday_date.strftime("%d-%m-%Y")
    if (os.path.isfile(file_path)):
        os.remove(file_path)
        logging.debug(u'Deleting yesterday results')




if __name__ == '__main__':
    try:
        grab()
    except Exception as e:
        logging.exception("grab error")
