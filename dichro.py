from selenium import webdriver
from selenium.webdriver.support.ui import Select
from time import time, sleep

def run_dichro(username, password, data_file, program, concentration, residue_mass, pathlength, scale, epsilon=False, attempts=10000):
    scale_plus = 0
    helix_content = None
    attempt = 0
    while not helix_content and attempt < attempts:
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
            name_input.send_keys(data_file.split("/")[-1].split(".")[0].replace("#", "").replace("_", "") + "T" + str(int(time())))
            data_file_input.send_keys(data_file)

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
            units.select_by_visible_text(
             "delta epsilon" if epsilon else "millidegrees / theta (machine units)"
            )
            with open(data_file) as f:
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
            scale_input.clear()
            scale_input.send_keys(str(scale + scale_plus))

            # Set output units and submit
            output_units = [
             s for s in selects if s.get_attribute("name") == "output_units"
            ][0]
            output_units = Select(output_units)
            output_units.select_by_visible_text("delta epsilon" if epsilon else "theta (machine units), mdeg")
            submit = [
             i for i in inputs if i.get_attribute("name") == "submit data"
            ][0]
            submit.click()

            if epsilon:
                inputs = browser.find_elements_by_tag_name("input")
                submit = [
                 i for i in inputs if i.get_attribute("value") == "submit"
                ][0]
                submit.click()
            else:
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

            # What is the NMSD?
            links = browser.find_elements_by_tag_name("a")
            show_links = [a for a in links if a.text == "SHOW"]
            show_links[1].click()
            nrmsd_index = browser.find_element_by_tag_name("body").text.find("NRMSD:") + 6
            nrmsd = float(browser.find_element_by_tag_name("body").text[nrmsd_index:].split(" ")[0].split("\n")[0])

            # What is the helical content?
            browser.back()
            links = browser.find_elements_by_tag_name("a")
            show_links = [a for a in links if a.text == "SHOW"]
            show_links[0].click()
            table = browser.find_elements_by_tag_name("table")[1]
            rows = table.find_elements_by_tag_name("tr")
            values = [td.text for td in rows[-1].find_elements_by_tag_name("td")]
            helix_content = float(values[0]) + float(values[1]) if program == "CDSSTR" else float(values[1]) + float(values[2])

            return {
             "temperature": data_file.split("/")[-1].split(".")[0] + "°C",
             "program": program,
             "nrmsd": nrmsd,
             "concentration": concentration,
             "helix_content": helix_content
            }
        except Exception as e:
            attempt += 1
            print(e)
            print("{} attempts".format(attempt))
            scale_plus += 0.00001
            sleep(2)
        finally:
            browser.quit()
    return {
     "temperature": data_file.split("/")[-1].split(".")[0] + "°C",
     "program": program,
     "nrmsd": None,
     "concentration": concentration,
     "helix_content": None
    }
