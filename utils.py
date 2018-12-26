import os
import pandas as pd
from selenium import webdriver
import shutil
from numpy import nan
from bs4 import BeautifulSoup


def move_data_from_dir_to_dir(src, dest):
    all_files = os.listdir(src)
    files_to_copy = list(filter(lambda file: True if file.find(".mp3") != -1 else False, all_files))
    if not os.path.exists(dest): os.mkdir(dest)
    for file in files_to_copy:
        shutil.move(src + "\\" + file, dest)


def create_filepath(dest):
    if not os.path.exists(dest): os.mkdir(dest)


def wait_until_file_start_download(src, idx):
    all_files = os.listdir(src)
    parsed_files = list(filter(lambda file: True if file.find(".mp3") != -1
                                                    and file.find("crdownload") != -1 else False, all_files))
    while idx + 1 != len(parsed_files):
        all_files = os.listdir(src)
        parsed_files = list(filter(lambda file: True if file.find(".mp3") != -1
                                                        and file.find("crdownload") == -1 else False, all_files))


def wait_until_files_exists(src, songs, skipped):
    all_files = os.listdir(src)
    parsed_files = list(filter(lambda file: True if file.find(".mp3") != -1
                                                    and file.find("crdownload") == -1 else False, all_files))
    while len(parsed_files) + skipped < len(songs):
        all_files = os.listdir(src)
        parsed_files = list(filter(lambda file: True if file.find(".mp3") != -1
                                                        and file.find("crdownload") == -1 else False, all_files))


def import_data(file_path):
    file = pd.read_excel(file_path)
    parsed_file = {}
    for col, row in file.items():
        parsed_file[col] = [record for record in row if record is not nan]
    return parsed_file


def create_web_driver(project_file_path):
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": project_file_path}
    options.add_experimental_option("prefs", prefs)
    return webdriver.Chrome("C:\\Users\\michal\\Downloads\\chromedriver.exe",
                            chrome_options=options)


def check_if_filed_is_already_downloaded(path, title):
    all_files = os.listdir(path)
    return True if title in all_files else False


def download_song(driver, url, song):
    driver.get(url)
    search = driver.find_element_by_id("downloader-input")
    convert = driver.find_element_by_id("submit-button")
    search.send_keys(song)
    convert.submit()


def close_unused_tabs(driver):
    driver.switch_to.window(driver.window_handles[-1])
    driver.close()
    driver.switch_to.window(driver.window_handles[0])


def get_song_title(driver):
    html = driver.page_source
    parser = BeautifulSoup(html, 'html.parser')
    for tag in parser.find_all('input'):
        if tag["name"] == "filename":
            return tag["value"]
    return None


def copy_xls_file(xls_file):
    if not os.path.exists(xls_file): shutil.copyfile("./links.xlsx", xls_file)
