import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

# Path to GeckoDriver (update this path if needed)
geckodriver_path = "/usr/local/bin/geckodriver"

# File containing extracted codes
codes_file = "filtered_codes.txt"

# Binance Red Packet Redemption URL
binance_url = "https://www.binance.com/en/my/wallet/account/payment/cryptobox"

# Initialize WebDriver for Firefox
driver = webdriver.Firefox()
wait = WebDriverWait(driver, 15)

# CSS selector for the fallback button
fallback_css_selector = ["#__APP > div > main > div > div > div.bn-trans.data-show.bn-mask.bn-modal.\[\&_\.bn-modal-wrap\]\:\!w-fit > div > div > div.navbar.relative.z-header.w-full.flex.flex-row.justify-center.items-center.bg-popupBg > div.absolute.z-10.right-0.flex.flex-row.flex-nowrap.hover\:cursor-pointer.pl-m > svg > path",".bn-modal-header-next > svg:nth-child(1) > path:nth-child(1)"]  # Replace with the CSS selector for the fallback button

# Function to collect reward
def collect_reward():
    try:
        # Attempt to find and click the "Open" button
        try:
            open_button = WebDriverWait(driver, 3).until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "#__APP > div > main > div > div > div.bn-trans.data-show.bn-mask.bn-modal.\[\&_\.bn-modal-wrap\]\:\!w-fit > div > div > button")
            ))
            open_button.click()
            print("Clicked 'Open' button.")

            # Attempt to auto-click another button after "Open"
            auto_click_button = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "#__APP > div > main > div > div > div.bn-trans.data-show.bn-mask.bn-modal.\[\&_\.bn-modal-wrap\]\:\!w-fit > div > div > div.navbar.relative.z-header.w-full.flex.flex-row.justify-center.items-center.bg-popupBg > div.absolute.z-10.right-0.flex.flex-row.flex-nowrap.hover\:cursor-pointer.pl-m > svg > path")  # Replace with actual selector
            ))
            auto_click_button.click()
            print("Clicked auto-click button after 'Open'.")

        except Exception:
            print("'Open' button not found within 3 seconds.")

            # If "Open" button not found, click the fallback button
            fallback_button = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, fallback_css_selector)
            ))
            fallback_button.click()
            print("Fallback button clicked.")

    except Exception as e:
        print(f"Error during reward collection: {e}")

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
        time.sleep(5)

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
