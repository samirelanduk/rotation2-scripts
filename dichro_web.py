from selenium import webdriver
from selenium.webdriver.support.ui import Select
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
    name_input.send_keys(data_files[0].split("/")[-1].split(".")[0])
    data_file_input.send_keys(data_files[0])

    # Describe data file
    selects = browser.find_elements_by_tag_name("select")
    file_format = [
     s for s in selects if s.get_attribute("name") == "FORMAT"
    ][0]
    file_format = Select(file_format)
    file_format.select_by_visible_text("FREE (with preview)")
    units = [
     s for s in selects if s.get_attribute("name") == "units"
    ][0]
    units = Select(units)
    units.select_by_visible_text("millidegrees / theta (machine units)")
    with open(data_files[0]) as f:
        data = f.read()
    lines = data.split("\n")
    lines = [line.strip() for line in lines if line.strip()]
    high_wavelength = 10000
    low_wavelength = 0
    for line in lines:
        try:
            wavelength = float(line.split()[0])
            if high_wavelength == 10000:
                high_wavelength = wavelength
            low_wavelength = wavelength
        except ValueError:
            pass
    initial_wavelength = [
     i for i in inputs if i.get_attribute("name") == "START"
    ][0]
    final_wavelength = [
     i for i in inputs if i.get_attribute("name") == "END"
    ][0]
    initial_wavelength.send_keys(str(high_wavelength))
    final_wavelength.send_keys(str(low_wavelength))
    wavestep = [
     i for i in inputs if i.get_attribute("name") == "WAVESTEP"
    ][-1]
    wavestep.click()
    lowest_nm = [
     i for i in inputs if i.get_attribute("name") == "QUALDATA"
    ][0]
    lowest_nm.send_keys(str(low_wavelength))

    # Choose analysis methods
    programs = [
     s for s in selects if s.get_attribute("name") == "prog"
    ][0]
    programs = Select(programs)
    programs.select_by_visible_text("SELCON3")
    reference_sets = [
     s for s in selects if s.get_attribute("name") == "basis"
    ][0]
    reference_sets = Select(reference_sets)
    reference_sets.select_by_visible_text(
     "SMP180 (Optimised for 190-240 nm # Less nm required)"
    )

    # Set output units and submit
    output_units = [
     s for s in selects if s.get_attribute("name") == "output_units"
    ][0]
    output_units = Select(output_units)
    output_units.select_by_visible_text("theta (machine units), mdeg")
    submit = [
     i for i in inputs if i.get_attribute("name") == "submit data"
    ][0]
    submit.click()
    sleep(5)


finally:
    browser.quit()
