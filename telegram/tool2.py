import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import random

# Configurations
geckodriver_path = "/usr/local/bin/geckodriver"  # Update this path if needed
codes_file = "filtered_codes.txt"
binance_url = "https://www.binance.com/en/my/wallet/account/payment/cryptobox"

# Initialize WebDriver for Firefox
driver = webdriver.Firefox()
wait = WebDriverWait(driver, 15)

# Function to collect reward based on conditions
def collect_reward():
    try:
        # Attempt to find and click the "Open" button
        open_button = WebDriverWait(driver, 3).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#__APP > div > main > div > div > div.bn-trans.data-show.bn-mask.bn-modal.\[\&_\.bn-modal-wrap\]\:\!w-fit > div > div > button")
        ))
        open_button.click()
        print("Clicked 'Open' button.")

        # Wait and check if any of the trigger elements appear on the screen
        try:
            refresh_trigger_1 = "#__APP > div > main > div > div > div.bn-modal > div > div > div:nth-child(4)"
            refresh_trigger_2 = "#.bn-modal-content .t-caption1"  # Replace with the second CSS selector

            # Check if either of the selectors is present
            WebDriverWait(driver, 3).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, refresh_trigger_1)
            ))
            print(f"Trigger element detected: {refresh_trigger_1}. Refreshing page...")
            driver.refresh()
            return  # Exit the function after refreshing the page

        except Exception:
            try:
                # Check for the second CSS selector
                WebDriverWait(driver, 3).until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, refresh_trigger_2)
                ))
                print(f"Trigger element detected: {refresh_trigger_2}. Refreshing page...")
                driver.refresh()
                return  # Exit the function after refreshing the page
            except Exception:
                print("No trigger element found. Clicking X button instead.")

        # If none of the trigger elements are found, click the X button
        x_button = WebDriverWait(driver, 3).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, ".bn-modal .navbar .absolute svg path")
        ))
        x_button.click()
        print("Clicked 'X' button after 'Open'.")

    except Exception as e:
        print(f"Error during reward collection: {e}")       
	# Refresh the page when an error occurs
        print("Refreshing page due to error...")
        driver.refresh()  # Refresh the page

# Function to process codes
def process_codes():
    processed_codes = set()

    # Check if the output file already exists
    if os.path.exists(codes_file):
        with open(codes_file, "r") as f:
            processed_codes = set(line.strip() for line in f if line.strip())

    while True:
        try:
            # Load codes from the file
            with open(codes_file, "r") as f:
                codes = [code.strip() for code in f if code.strip() and code.strip() not in processed_codes]

            # Process each new code
            for code in codes:
                print(f"Submitting code: {code}")

                try:
                    # Find the input field for the code
                    input_field = wait.until(EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "#__APP > div > main > div > div > div.pt-3xl.tablet\\:pt-\\[56px\\].block > div > div.flex.flex-col.tablet\\:flex-row.gap-m.tablet\\:gap-5xl > div:nth-child(2) > div > div.bn-formItem > div > input")
                    ))
                    input_field.clear()
                    input_field.send_keys(code)

                    # Find and click the submit button
                    submit_button = wait.until(EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, "#__APP > div > main > div > div > div.pt-3xl.tablet\\:pt-\\[56px\\].block > div > div.flex.flex-col.tablet\\:flex-row.gap-m.tablet\\:gap-5xl > div:nth-child(2) > button")
                    ))
                    submit_button.click()

                    # Wait for the reward collection process
                    collect_reward()

                    # Mark the code as processed
                    processed_codes.add(code)

                except Exception as e:
                    print(f"Error submitting code {code}: {e}")

        except Exception as e:
            print(f"Error while processing codes: {e}")

        # Wait for new codes to be added to the file
        time.sleep(random.uniform(2, 5))  # Random delay between 2 and 5 seconds

try:
    # Open Binance Redemption Page
    driver.get(binance_url)

    # Log in manually
    print("Log in to Binance manually.")
    input("Press Enter after logging in and navigating to the red packet redemption page...")

    # Start processing codes
    process_codes()

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser
    driver.quit()
