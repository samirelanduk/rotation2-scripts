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

def run_dichroweb(data_file, program, file_results, nrmsd=False, scale=1):
    scale_extra = 0
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
        file_format.select_by_visible_text("FREE (with preview, use col 4)")
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
        scale_value = scale + scale_extra
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
        try:
            mean_mass_input = [
             i for i in inputs if i.get_attribute("name") == "MRW"
            ][0]
        except:
            sleep(10000)
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
        if nrmsd:
            show_links[1].click()
            nrmsd_index = browser.find_element_by_tag_name("body").text.find("NRMSD:") + 6
            nrmsd = float(browser.find_element_by_tag_name("body").text[nrmsd_index:].split(" ")[0])
            return nrmsd
        else:
            try:
                show_links[0].click()
                table = browser.find_elements_by_tag_name("table")[1]
                rows = table.find_elements_by_tag_name("tr")
                values = [td.text for td in rows[-1].find_elements_by_tag_name("td")]
                helix_content = float(values[0]) + float(values[1]) if program == "CDSSTR" else float(values[1]) + float(values[2])
                program_results[program] = helix_content
            except:
                scale_extra += 0.001
                print("Fail: %s°C, %s" % (data_file["temperature"], program))
    finally:
        browser.quit()


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
    print("Please provide a label in the form Agent,Sample\n")
    sys.exit()
agent, sample = sys.argv[7].split(",") if "," in sys.argv[7] else (sys.argv[7], None)
if len(sys.argv) < 9:
    print("Please provide a chart filename\n")
    sys.exit()
chart_file_name = sys.argv[8]

# Get the files
files = os.listdir(location)
data_files = sorted(
 [f for f in os.listdir(location) if f[-4:] == ".gen"]
)
data_files = [os.path.abspath(location + "/" + f) for f in data_files if "_" not in f]
data_files = [{"location": f, "temperature": int(f.split(".")[0].split("/")[-1])} for f in data_files]

scales = [0.9 + (0.01 * n) for n in range(20)]
for scale in scales:

    print(scale, run_dichroweb(data_files[0], "SELCON3", [], scale=scale,  nrmsd=True))

file_results = []
for data_file in data_files:
    program_results = {"temperature": data_file["temperature"]}
    for program in ("SELCON3", "CONTIN", "CDSSTR"):
        while program not in program_results:
            run_dichroweb(data_file, program, "file_results")
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
    y = [temp["mean"] * 100 for temp in file_results]
    selcon = [temp["SELCON3"] * 100 for temp in file_results]
    contin = [temp["CONTIN"] * 100 for temp in file_results]
    cdsstr = [temp["CDSSTR"] * 100 for temp in file_results]
    error = [temp["error"] * 100 for temp in file_results]
    plt.errorbar(x, y, yerr=error, fmt="o", color="#000000", label="Average")

    plt.scatter(x, selcon, color="#FF0000", marker="x", label="SELCON3")
    plt.scatter(x, contin, color="#00FF00", marker="x", label="CONTIN")
    plt.scatter(x, cdsstr, color="#0000FF", marker="x", label="CDSSTR")

    plt.grid(True, lw=0.5, ls=":")
    plt.xlabel("Temperature (°C)")
    plt.ylabel("Helix Content (%)")
    plt.xlim(x[0] - 5, x[-1] + 5)
    plt.ylim(0, 100)
    if sample:
        plt.title("%s: Sample %s" % (agent, sample))
    else:
        plt.title(agent)
    plt.legend(prop={'size':8}, framealpha=1)
    plt.savefig("../charts/secondary_structure/%s.png" % chart_file_name)
    plt.clf()
