import os
import datetime
import platform
import re
import requests
import tarfile


def save_screenshot(config_dir, driver, tag: str) -> None:
    '''if the development env var is set, then store the screenshot'''
    if os.environ.get("SCREENSHOT_LOG") == "TRUE":
        driver.save_screenshot(f"{config_dir}screenshots/{datetime.date.today()}-{tag}.png")

def check_config_dir(config_dir: str, log_file: str) -> None:
    '''checks or creates the config dir'''
    if not os.path.isdir(config_dir):
        os.mkdir(config_dir)

    if os.environ.get("SCREENSHOT_LOG") == "TRUE":
        if not os.path.isdir(f"{config_dir}screenshots/"):
            os.mkdir(f"{config_dir}screenshots/")
    
    if not os.path.isfile(log_file):
        with open(log_file, "w") as f:
            f.write(f"{datetime.date.today} Initialized app.log")


def trim_log(log_file: str) -> None:
    '''trim log file to 250 on startup'''
    if log_size(log_file) > 250:
        try:
            with open(log_file, 'r', encoding="utf-8") as scr, open(log_file+"-"+str(datetime.date.today())+".log", 'w', encoding="utf-8") as dst:
                for line in scr:
                    dst.write(line)
            with open(log_file, "w", encoding="utf-8") as logf:
                d = datetime.date.today()
                logf.write(f"logs split on {d}")
        except Exception as e:
            log(log_file, "LOG TRIM ERROR" + str(e))


def log(log_file: str, message: str, timestamp=True) -> None:
    '''global logging function'''
    if timestamp:
        d = datetime.date.today()
        inp = f'{d} - {message}'
    else:
        inp = f'{message}'

    print(inp)
    with open(log_file, "a", encoding="utf-8") as logf:
        logf.write(inp+"\n")


def log_size(log_file: str) -> int:
    '''get log line count'''
    with open(log_file, "r", encoding="utf-8") as logf:
        count = 0
        for count, _ in enumerate(logf):
            pass
        return count


def download_geckodriver(log_file: str, driver_dir: str, driver_tar: str, driver_link: str, driver_version: str) -> None:
    '''download the geckodriver in the correct directory'''
    log(log_file, "Downloading driver...")
    try:
        response = requests.get(driver_link, timeout=60)
    except requests.exceptions.Timeout:
        log(log_file, "Could not download driver, timed out, exiting...")
        exit(1)

    response.raise_for_status()

    with open(driver_tar, 'wb') as file:
        file.write(response.content)

    log(log_file, "Extracting driver...")

    with tarfile.open(driver_tar) as file:
        file.extractall(driver_dir, filter='data')

    with open(driver_dir+"version", "w", encoding="utf-8") as file:
        file.write(driver_version)

    log(log_file, "Driver seems successfully downloaded")


def check_geckodriver(log_file: str, driver_dir: str, driver_tar: str, driver_link: str, driver_version: str) -> None:
    '''check geckodriver status and download / update if applicable'''
    if platform.machine() == "aarch64":
        if not os.path.isdir(driver_dir):
            log(log_file, "Gecko driver directory not found, making it...")
            os.mkdir(driver_dir)
            download_geckodriver(log_file, driver_dir, driver_tar, driver_link, driver_version)
        else:
            if os.path.exists(driver_dir+"geckodriver"):
                with open(driver_dir+"version", "r", encoding="utf-8") as file:
                    if not file.read() == driver_version:
                        log(log_file, "Updating driver...")
                        download_geckodriver(log_file, driver_dir, driver_tar, driver_link, driver_version)

            else:
                log(log_file, "ERROR: could not find geckodriver in the correct place")
                exit(1)


def check_env(log_file):
    '''check the environment variables to be suitable for this code'''

    #check MODE
    if os.environ.get('MODE') is None:
        log(log_file, "ERROR: MODE ENVIRONMENT VARIABLE NOT SET")
        exit(1)

    if os.environ.get('MODE') != 'selenium' and os.environ.get('MODE') != 'socket':
        log(log_file, f"ERROR: unknown mode {os.environ.get('MODE')}")
        exit(1)

    #check auth
    if not os.environ.get('PASSWORD') is None:
        if os.environ.get('USERNAME') is None:
            log(log_file, "ERROR: USERNAME ENVIRONMENT VARIABLE EMPTY")
            exit(1)
    if not os.environ.get('USERNAME') is None:
        if os.environ.get('PASSWORD') is None:
            log(log_file, "ERROR: PASSWORD ENVIRONMENT VARIABLE EMPTY")
            exit(1)

    if os.environ.get('USERNAME') is None and os.environ.get('PASSWORD') is None:
        log(log_file, "No credentials found, assuming no credentials needed")
    else:
        log(log_file, "Credentials found, rolling with credentials")

    #check logging
    if os.environ.get("SCREENSHOT_LOG") == "TRUE":
        log(log_file, "Logging screenshots")

    #check RUN_MONTHS
    if os.environ.get('RUN_MONTHS') is None:
        log(log_file, "No months to run found, setting to all months")
        os.environ.setdefault('RUN_MONTHS', '1,2,3,4,5,6,7,8,9,10,11,12')

    run_months = os.environ.get('RUN_MONTHS')
    run_months = run_months.replace(' ', '').split(',')
    if len(run_months) == 0:
        log(log_file, "ERROR: NO VALUE FOUND IN RUN_MONTHS ENVIRONMENT VARIABLE")
        exit(1)
    try:
        run_months = [int(i) for i in run_months]
    except ValueError:
        log(log_file, "ERROR: FAULTY VALUE IN RUN_MONTHS")
        exit(1)

    #check days
    if os.environ.get('RUN_DAYS') is None or os.environ.get('RUN_DAYS') == "":
        log(log_file, "No days to run found, setting to all days")
        os.environ.setdefault('RUN_DAYS', '1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31')

    run_days = os.environ.get('RUN_DAYS')
    run_days = run_days.replace(' ', '').split(',')
    if len(run_days) == 0:
        log(log_file, "ERROR: RUN_DAYS env found no days")
        exit(1)
    try:
        run_days = [int(i) for i in run_days]
    except ValueError:
        log(log_file, "ERROR: faulty value in RUN_DAYS")
        exit(1)

    #check time
    if os.environ.get("RUN_TIME") is None:
        log(log_file, "ERROR: NO RUN_TIME ENVIRONMENT VARIABLE DETECTED")
        exit(1)
    if not len(os.environ.get("RUN_TIME")) == 5:
        log(log_file, "ERROR: RUN_TIME ENVIRONMENT VARIABLE IN WRONG FORMAT")
        exit(1)
