from selenium import webdriver
from selenium.webdriver.support.ui import Select
from time import sleep, time
from math import sqrt
import matplotlib.pyplot as plt
import json
import inferi
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
if len(sys.argv) < 6:
    print("What is the mean residue mass in Da?\n")
    sys.exit()
residue_mass = float(sys.argv[5])
if len(sys.argv) < 7:
    print("What is the pathlength in cm?\n")
    sys.exit()
pathlength = float(sys.argv[6])
if len(sys.argv) < 8:
    print("Please provide a label in the form Agent,Run,Sample\n")
    sys.exit()
agent, run, sample = sys.argv[7].split(",")

# Get the files
files = os.listdir(location)
data_files = sorted(
 [f for f in os.listdir(location) if f[-4:] == ".gen"],
 key=lambda k: int("".join([char for char in k.split()[-1] if char.isdigit()]))
)
data_files = [os.path.abspath(location + "/" + f) for f in data_files]
data_files = [{"location": f, "temperature": 20 + (5 * index)} for index, f in enumerate(data_files)]

file_results = []
for data_file in data_files:
    program_results = {"temperature": data_file["temperature"]}
    for program in ("SELCON3", "CONTIN", "CDSSTR"):
        scale_extra = 0
        while program not in program_results:
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
                name_input.send_keys(data_file["location"].split("/")[-1].split(".")[0].replace("#", "").replace("_", "") + "T" + str(int(time())))
                data_file_input.send_keys(data_file["location"])

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
                with open(data_files[0]["location"]) as f:
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
                programs.select_by_visible_text(program)
                reference_sets = [
                 s for s in selects if s.get_attribute("name") == "basis"
                ][0]
                reference_sets = Select(reference_sets)
                reference_sets.select_by_visible_text(
                 "SMP180 (Optimised for 190-240 nm # Less nm required)"
                )

                # Set scale
                scale_input = [
                 i for i in inputs if i.get_attribute("name") == "scale_data"
                ][0]
                scale_value = 1 + scale_extra
                scale_input.clear()
                scale_input.send_keys(str(scale_value))

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

                # Provide mass, concentration, and pathlength
                inputs = browser.find_elements_by_tag_name("input")
                mean_mass_input = [
                 i for i in inputs if i.get_attribute("name") == "MRW"
                ][0]
                concentration_input = [
                 i for i in inputs if i.get_attribute("name") == "CONC"
                ][0]
                pathlength_input = [
                 i for i in inputs if i.get_attribute("name") == "PATH"
                ][0]
                mean_mass_input.send_keys(str(residue_mass))
                concentration_input.send_keys(str(concentration))
                pathlength_input.send_keys(str(pathlength))
                submit = [
                 i for i in inputs if i.get_attribute("value") == "submit"
                ][0]
                submit.click()

                # Go to results page
                inputs = browser.find_elements_by_tag_name("input")
                submit = [
                 i for i in inputs if i.get_attribute("value") == "submit"
                ][0]
                submit.click()

                # What are the results?
                links = browser.find_elements_by_tag_name("a")
                show_links = [a for a in links if a.text == "SHOW"]
                try:
                    show_links[0].click()
                    table = browser.find_elements_by_tag_name("table")[1]
                    values = [
                     [td.text for td in row.find_elements_by_tag_name("td")[1:]]
                    for row in table.find_elements_by_tag_name("tr")[1:]]
                    helix_content = float(values[-1][0]) + float(values[-1][1])
                    program_results[program] = helix_content
                except:
                    scale_extra += 0.0001
                    print("Fail: %s°C, %s" % (data_file["temperature"], program))
            finally:
                browser.quit()
    values = [
     program_results["SELCON3"],
     program_results["CONTIN"],
     program_results["CDSSTR"]
    ]
    values = [v for v in values if v]
    values = inferi.Series(*values, sample=False)
    program_results["mean"] = values.mean()
    program_results["error"] = values.standard_deviation() / sqrt(len(values))
    file_results.append(program_results)

    with open("%s/ss.json" % location, "w") as f:
        json.dump(file_results, f)

    x = [temp["temperature"] for temp in file_results]
    y = [temp["mean"] for temp in file_results]
    error = [temp["error"] for temp in file_results]
    plt.errorbar(x, y, yerr=error, fmt="o")
    # plt.scatter(x, y)

    plt.grid(True)
    plt.xlabel("Temperature (°C)")
    plt.ylabel("Helix Content (%)")
    plt.xlim(x[0] - 5, x[-1] + 5)
    plt.title("%s: Run %s, Sample %s" % (agent, run, sample))
    plt.savefig("%s/ss.png" % location)
