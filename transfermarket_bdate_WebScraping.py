#TRYING NEW APPROACH BC DRIVER.BACK DIDNT WORK. GETTING ALL URLS OF TEAMS
#17:20 best cell atm

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re


def handle_cookie_consent(driver):
    # Find the consent button using XPath
    button_xpath = '/html/body/div/div[2]/div[3]/div[2]/button' #change to class_name better long term!
    
    # Switch to the consent frame bc cookie policy button is inside an iframe
    iframe = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="sp_message_iframe_757749"]')))
    driver.switch_to.frame(iframe)
    #find and clickconsent button
    consent_button = driver.find_element(By.XPATH, button_xpath)
    consent_button.click()
    #switch back to regular frame
    driver.switch_to.default_content()

def irregular_names(name):
    return name.endswith('€ ') or name.endswith('€  ') or name.endswith('U19 ') or name.endswith('U19  ') or name.endswith('U19') or name.endswith("U18") or name.endswith("U17") or name.endswith("U19-BL N/NO") or name.endswith("DFB-Pokal der Junioren") or name.endswith('Spiele') or name.endswith('S') or name.endswith('U') or name.endswith('N') or name.endswith('PPS') or name.endswith('19')

#WORKING!
#Getting german leagues and seasons! NO VALUE ERRORS 

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import numpy as np

# opening web browser 
options = FirefoxOptions()
# options.add_argument("--headless") # headless means invisible- browser don't open
# options.add_argument("--disable-gpu")  # Disable GPU acceleration (useful for headless mode)

driver = webdriver.Firefox(options=options)
driver.get("https://www.transfermarkt.de/wettbewerbe/europaJugend") 
wait = WebDriverWait(driver, 10) 

# accept cookies
handle_cookie_consent(driver)


#filtering out the german leagues
german_leagues = [element.text for element in league_table if "BL" in element.text or "Bundesliga" in element.text ]
print(german_leagues)
# looping through league name list


i = 0
seasons = ['2022', '2021', '2020', '2019', '2018']
#list catching all the teams that have uneven number of names and bdates
value_error_teams = []
#df collecting all the final data
all_data_df = pd.DataFrame()
while i < len(german_leagues):
    j = 1
    league_table = driver.find_elements(By.CLASS_NAME, "inline-table")
    print("here before clicking on league")
    german_leagues = [element for element in league_table if "BL" in element.text or "Bundesliga" in element.text ]
    
    print("league name: ", german_leagues[i].text)
    german_leagues[i].click()
    print("after clicking on league")
    try:
        print("checking for cookie consent")
        handle_cookie_consent(driver)
        print("consent button try happened")
    except:
        pass
    #try this before cookie consent 
    current_url = driver.current_url
    print("current_url", current_url)
    base_url = current_url
    for year in seasons:
        season_url = base_url+"/plus/?saison_id="+year
        print("season_url", season_url)
        driver.get(season_url)
        print("driver got url")

        # finding and clicking into each team
        table = driver.find_element(By.CLASS_NAME, 'items')
        print("found table")
        # Find all the image elements within the table using a suitable locating strategy
        image_elements = table.find_elements(By.TAG_NAME, 'img')
        print("found image elements")

        # Collect the URLs of the team pages
        team_urls = []
        
        for image in image_elements:
            parent_a_tag = image.find_element(By.XPATH, ".//ancestor::a")  # Get the <a> tag parent of the <img> tag
            team_url = parent_a_tag.get_attribute("href")

            # Filter out irrelevant URLs (adjust this condition as needed)
            if "verein" in team_url and "/startseite" in team_url:
                team_urls.append(team_url)
        #print("printing team_urls",team_urls)

        j = 1  # Resetting j before starting the loop for image_elements
        print("j = ", j)
        while j < len(image_elements):
            # Iterate through the URLs and visit each team page
            for url in team_urls:
                driver.get(url)
                print(url)
                try:
                    handle_cookie_consent(driver)
                    print("cookie policy accepted within try")
                except: 
                    pass

                print("continuing after try except block")
                names = driver.find_elements(By.CLASS_NAME, "hauptlink")
                print("names found")
                bdates = driver.find_elements(By.CLASS_NAME, "zentriert")
                print("bdates found")
                print("bdates elements len: ", len(bdates))
                
                #processing and cleaning names
                names = [element.text for element in names]
                names = [name for name in names if name.strip() != '']
                # Filter out team names
                names = [name for name in names if not irregular_names(name)]
                print("full names list: ",names)

                #processing and cleaning birthdates
                bdates = [element.text if element.text != '- (-)' and not re.search(r'k\. A\. \(\d{2}\)', element.text) else '00.00.0000 (00)' for element in bdates]
                print("replaced bdates list: ", bdates)
                pattern = r'\d{2}\.\d{2}\.\d{4} \(\d+\)' #format of the date so exclude anything else
                bdates = [value for value in bdates if re.match(pattern, value)]
                
                print(len(bdates))
                print(len(names))
                
                # Check if there are more names than birthdates
                if len(names) > len(bdates):
                    print("more names than bdates. According processing follows ")
                    diff = len(names) - len(bdates)
                    removed_names = names[-diff:]  # Get the last 'diff' names
                    names = names[:-diff]  # Remove the last 'diff' names from the list

                    print("All the following names are wrong and have been removed:", ", ".join(removed_names))
                    print("len names", len(names))
                    print("len bdates", len(bdates))
                    print("processed names: ",names, "processed bdates: ", bdates )
                #saving data (names & b-dates) into df
                data = {"Player_name":names,
                "Birthdate":bdates}
                try:
                    temp_df = pd.DataFrame(data)
                    all_data_df = all_data_df.append(temp_df, ignore_index=True)
                    print("done with saving data in df")
                except ValueError:
                    print("Value Error")
                    #list of all team urls that did not have matching len bdate and name 
                    value_error_teams.append(url) 
                print("continuing after third try except")
                j += 1
                print("printing j number: ", j)

            print("done with clicking into all teams")

    # back to league page
    driver.get("https://www.transfermarkt.de/wettbewerbe/europaJugend")
    print("original league page was reloaded")
    try:
        handle_cookie_consent(driver)
    except:
        pass
    i += 1
    print("i increase:", i)

print("done with accessing all the leagues and all teams")
driver.quit() 

excel_file_path = './bdates_output.xlsx'

# Export the DataFrame to Excel
all_data_df.to_excel(excel_file_path, index=False)

print(f"Excel file saved at: {excel_file_path}")
print("DONE!!!!!!!!!!")