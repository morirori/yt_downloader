from utils import *
from config import config
import time

PROJECT_FILE_PATH = config["destination_file_path"]
EXCEL_FILE_NAME = config["excel_file_name"]
URL = config["web_page"]


xls_file = PROJECT_FILE_PATH + EXCEL_FILE_NAME
copy_xls_file(xls_file)
driver = create_web_driver(PROJECT_FILE_PATH)
data = import_data(xls_file)

for folder, songs in data.items():
    skipped = 0
    download_file_path = PROJECT_FILE_PATH + folder
    create_filepath(download_file_path)
    for idx, song in enumerate(songs):
        download_song(driver, URL, song)
        if len(driver.window_handles) > 1: close_unused_tabs(driver)
        title = get_song_title(driver)
        if title is None:
            skipped += 1
            print("{}: {} Song not exist".format(folder, title))
            continue
        if check_if_filed_is_already_downloaded(download_file_path, title):
            print("{}: {} has been already downloaded".format(folder, title))
            driver.get(URL)
            continue
        wait_until_file_start_download(PROJECT_FILE_PATH, idx)
        print("{}: {} has started to download".format(folder, title))
    wait_until_files_exists(PROJECT_FILE_PATH, songs, skipped)
    time.sleep(30)
    move_data_from_dir_to_dir(PROJECT_FILE_PATH, download_file_path)
