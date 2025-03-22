#!/usr/bin/env python3

import pandas as pd
import random
import time
from datetime import datetime
from obs_image import create_obs_image

SHEET_URL = "https://docs.google.com/spreadsheets/d/1m8z5sIElnUFGTBNhCEiscEqK3429PPnf7z-KQ8s5HXc/edit"

def get_current_show(sheet_url):
    csv_url = sheet_url.replace('/edit', '/export?format=csv&')

    try:
        df = pd.read_csv(csv_url)

        now = datetime.now().time()

        for _, row in df.iterrows():
            try:
                start_time = datetime.strptime(row['TIME START'], "%H:%M").time()
                end_time = datetime.strptime(row['TIME END'], "%H:%M").time()

                if start_time <= now <= end_time:
                    return row['SHOW NAME']
            except Exception as e:
                print(f"Skipping row due to error: {e}")
    except Exception as e:
        print(f"Error reading sheet: {e}")

    return None


def main_loop():
    while True:
        try:
            show_name = get_current_show(SHEET_URL)

            if show_name:
                create_obs_image(show_name)
            else:
                create_obs_image("You're listening to DCUfm!")

            wait_time = random.randint(30, 45)
            time.sleep(wait_time)

        except Exception as e:
            print(f"Error occurred: {e}. Retrying in 5 seconds...")
            create_obs_image("You're listening to DCUfm!")
            time.sleep(5)


if __name__ == "__main__":
    while True:
        try:
            main_loop()
        except Exception as e:
            print(f"Critical error in main loop: {e}. Restarting...")
            time.sleep(5)
