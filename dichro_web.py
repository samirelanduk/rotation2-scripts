from selenium import webdriver
from time import sleep
import os
import sys
print("")

# Get arguments
if len(sys.argv) < 2:
    print("What is your username?\n")
    sys.exit()
username = sys.argv[1]
if len(sys.argv) < 3:
    print("What is your password?\n")
    sys.exit()
password = sys.argv[2]
if len(sys.argv) < 4:
    print("Where is the melt data?\n")
    sys.exit()
location = sys.argv[3]
if len(sys.argv) < 5:
    print("What is the concentration in mg/ml?\n")
    sys.exit()
concentration = float(sys.argv[4])

# Get the files
files = os.listdir(location)
data_files = sorted([f for f in files if f[-4:] in (".gen", ".dat")])
data_files = [os.path.abspath(location + "/" + f) for f in data_files]

browser = webdriver.Chrome()
try:
    # Go to the input page
    browser.get("http://dichroweb.cryst.bbk.ac.uk/html/process.shtml")
    inputs = browser.find_elements_by_tag_name("input")

    # Supply login details
    username_input = [
     i for i in inputs if i.get_attribute("name") == "CD-USERNAME"
    ][0]
    password_input = [
     i for i in inputs if i.get_attribute("name") == "CD-PWD"
    ][0]
    username_input.send_keys(username)
    password_input.send_keys(password)

    # Supply data
    name_input = [
     i for i in inputs if i.get_attribute("name") == "NAME"
    ][0]
    data_file_input = [
     i for i in inputs if i.get_attribute("name") == "FILE"
    ][0]
    name_input.send_keys(data_files[0].split("/")[-1])
    data_file_input.send_keys(data_files[0])
    sleep(5)

finally:
    browser.quit()
