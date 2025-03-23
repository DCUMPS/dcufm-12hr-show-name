#!/usr/bin/env python3

import pandas as pd
import random
import time
from datetime import datetime
from obs_image import create_obs_image

SHEET_URL = "https://docs.google.com/spreadsheets/d/1ZeVVX9UOG8q1Fl_nT5uzFNnEM88Gqb2Wdsq7WYqaJc0/edit"

def get_current_show(sheet_url):
    csv_url = sheet_url.replace('/edit', '/export?format=csv&')

    try:
        df = pd.read_csv(csv_url)

        df['Time'] = pd.to_datetime(df['Time'], format="%H:%M", errors='coerce').dt.time
        df = df.dropna(subset=['Time'])

        now = datetime.now().time()

        current_show = None
        latest_time = None

        for _, row in df.iterrows():
            show_time = row['Time']
            if show_time <= now and (latest_time is None or show_time > latest_time):
                latest_time = show_time
                current_show = row['Show']

        return current_show

    except Exception as e:
        print(f"Error reading or parsing sheet: {e}")
        return None

def main_loop():
    while True:
        try:
            show_name = get_current_show(SHEET_URL)

            if show_name:
                create_obs_image(show_name)
            else:
                create_obs_image("You're watching the 12hr broadcast!")

            wait_time = random.randint(30, 45)
            time.sleep(wait_time)

        except Exception as e:
            print(f"Error occurred: {e}. Retrying in 5 seconds...")
            create_obs_image("You're watching the 12hr broadcast!")
            time.sleep(5)

if __name__ == "__main__":
    while True:
        try:
            main_loop()
        except Exception as e:
            print(f"Critical error in main loop: {e}. Restarting...")
            time.sleep(5)
