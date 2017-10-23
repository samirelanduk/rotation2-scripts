"""Opens a browser, goes to PCDDB, logs in, and desposits. It will not submit,
so you can check first."""

from os.path import expanduser

data = {
    "username":             "samirelanduk",

    "protein_name":         "AOL5S6",
    "alt_protein_name":     "NavMS",
    "source_organism":      "M. marinus",
    "protein_supplier":     "A. Sula, Wallace Laboratory, Birkbeck College",
    "expression_system":    "E. coli",
    "expressed_as":         "Wild-type",
    "mutation_details":     "",
    "expression_tags":      "",
    "ligands_present":      "",
    "macromolecules":       "",

    "final_file":           expanduser("~") + "/Dropbox/PhD/Rotations/Rotation2/data/10 - Final data/a835/20.gen",
    "final_units":          "Delta Epsilon",
    "final_format":         "CDTool",

    "cd?":                  "CD",
    "concentration":        "1.01",
    "concentration_method": "Nanodrop",
    "protein_purity":       "",
    "purity_method":        "none",
    "buffer_contents":      "20 mM TRIS 100 mM NaF pH 7.4",
    "baseline_contents":    "20 mM TRIS 100 mM NaF pH 7.4",
    "experimental_temp":    "20",
    "instrument":           "Aviv",
    "detector_angle":       "",
    "pathlength":           "0.01",
    "calibration":          "Manufacturers Spec.",
    "cell_type":            "Cylindrical",
    "cell_composition":     "Quartz",
    "chamber_atmosphere":   "Nitrogen",
    "repeat_scans":         "3",
    "continuous/stepped":   "Stepped",
    "max_wavelength":       "280",
    "min_wavelength":       "190",
    "low_cutoff_criteria":  "HT value",
    "wavelength_interval":  "1",
    "dwell":                "",
    "collection_date":      "09-02-2017",
    "local_identifier":     "",

    "weight":               "32667.39",
    "residue_count":        "277",
    "mean_weight":          "117.9",
    "processing_software":  "CDTool",
    "software_version":     "",
    "smoothing_points":     "0",
    "zeroing_range":        "263-270 nm",

    "pdb":                  "5HVX",
    "uniprot":              "A0L5S6",
    "enzyme":               "",
    "medline":              "",
    "cath":                 "",
    "sequence":             "GSHMSRKIRDLIESKRFQNVITAIIVLNGAVLGLLTDTTLSASSQNLLERVDQLCLTIFIVEISLKIYAYGVRGFFRSGWNLFDFVIVAIALMPAQGSLSVLRTFRIFRVMRLVSVIPTMRRVVQGMLLALPGVGSVAALLTVVFYIAAVMATNLYGATFPEWFGDLSKSLYTLFQVMTLESWSMGIVRPVMNVHPNAWVFFIPFIMLTTFTVLNLFIGICVDAMAITKEQEEEAKTGHHQEPISQTLLHLGDRLDRIEXQLAQXNELLQRQQPQKK",
    "protein_type":         "membrane",
    "keywords":             ["navms", "A835"],
    "pub_authors":          "Sam M. Ireland, Altin Sula, B. A. Wallace",
    "pub_year":             "2017",
    "pub_journal":          "Biopolymers",
    "pub_title":            "Thermal melt circular dichroism spectroscopic studies for identifying stabilising amphipathic molecules for the voltage-gated sodium channel NavMs",
    "pub_volume":           "",
    "pub_pages":            "",

    "depositor_name":       "Sam Ireland",
    "department/school":    "Structural and Molecular Biology",
    "university":           "University College London",
    "country":              "United Kingdom",
    "email":                "sam.ireland.09@ucl.ac.uk",
    "telephone":            "+447469782559",
    "pi_name":              "Prof. Bonnie Wallace",
    "pi_email":             "b.wallace@mail.cryst.bbk.ac.uk",
}

import traceback
import sys
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from time import sleep

def login_pcddb(browser):
    browser.get("http://pcddb.cryst.bbk.ac.uk/home.php")
    credentials = browser.find_element_by_id("credentials")
    form = credentials.find_element_by_tag_name("form")
    inputs = form.find_elements_by_tag_name("input")
    inputs[0].send_keys(data["username"])
    inputs[1].send_keys(data["password"])
    inputs[-1].click()


def drop_down(browser, name, value):
    drowndown = browser.find_element_by_name(name)
    drowndown = Select(drowndown)
    drowndown.select_by_visible_text(value)


def click_tab(browser, i):
    tab = browser.find_elements_by_class_name("tab")[i]
    browser.execute_script("arguments[0].scrollIntoView();", tab)
    tab.click()


def submit_entry(browser):
    browser.get("http://pcddb.cryst.bbk.ac.uk/deposit.php")
    form = browser.find_element_by_tag_name("form")

    browser.find_element_by_name("Protein Name").send_keys(data["protein_name"])
    browser.find_element_by_name("Alternative Protein Names").send_keys(data["alt_protein_name"])
    browser.find_element_by_name("Source Organism").send_keys(data["source_organism"])
    browser.find_element_by_name("Protein Supplier").send_keys(data["protein_supplier"])
    drop_down(browser, "Expression System or natural source", data["expression_system"])
    drop_down(browser, "Expressed As", data["expressed_as"])
    browser.find_element_by_name("Mutation Details").send_keys(data["mutation_details"])
    browser.find_element_by_name("Expression tags (if any)").send_keys(data["expression_tags"])
    browser.find_element_by_name("Ligands Present and Concentration or ratio").send_keys(data["ligands_present"])
    browser.find_element_by_name("Macromolecular Partner(s) and Concentration or ratio").send_keys(data["macromolecules"])
   
    click_tab(browser, 1)
    browser.execute_script("arguments[0].scrollIntoView();",  browser.find_element_by_name("Input File Format of Processed Data"))
    browser.find_element_by_name("Final Processed Spectrum").send_keys(data["final_file"])
    drop_down(browser, "Dichroism Units of Processed Data", data["final_units"])
    drop_down(browser, "Input File Format of Processed Data", data["final_format"])

    click_tab(browser, 2)
    drop_down(browser, "CD or SRCD", data["cd?"])
    browser.find_element_by_name("Protein Concentration (mg/ml)").send_keys(data["concentration"])
    drop_down(browser, "Concentration Quantification Method", data["concentration_method"])
    browser.find_element_by_name("Protein Purity (%)").send_keys(data["protein_purity"])
    drop_down(browser, "Purity Quantification Method", data["purity_method"])
    browser.find_element_by_name("Buffer Contents and Concentrations").send_keys(data["buffer_contents"])
    browser.find_element_by_name("Baseline Contents").send_keys(data["baseline_contents"])
    browser.find_element_by_name("Experimental Temperature (C)").send_keys(data["experimental_temp"])
    drop_down(browser, "Instrument or beamline", data["instrument"])
    browser.find_element_by_name("Detector Angle (Scattering Angle)").send_keys(data["detector_angle"])
    browser.find_element_by_name("Sample Cell Pathlength (cm)").send_keys(data["pathlength"])
    drop_down(browser, "Cell Pathlength Calibration Method", data["calibration"])
    drop_down(browser, "Sample Cell Type", data["cell_type"])
    drop_down(browser, "Sample Cell Composition", data["cell_composition"])
    drop_down(browser, "Sample Chamber Atmosphere", data["chamber_atmosphere"])
    browser.find_element_by_name("Number of repeat scans").send_keys(data["repeat_scans"])
    drop_down(browser, "Continuous or Stepped scan", data["continuous/stepped"])
    browser.find_element_by_name("Maximum (highest) wavelength, nm").send_keys(data["max_wavelength"])
    browser.find_element_by_name("Minimum (lowest) wavelength, nm").send_keys(data["min_wavelength"])
    drop_down(browser, "Criteria for low wavelength cutoff", data["low_cutoff_criteria"])
    browser.find_element_by_name("Wavelength interval, nm").send_keys(data["wavelength_interval"])
    browser.find_element_by_name("Dwell or Averaging time, seconds").send_keys(data["dwell"])
    drop_down(browser, "Experimental Collection date2", data["collection_date"].split("-")[0])
    drop_down(browser, "Experimental Collection date1", data["collection_date"].split("-")[1])
    browser.find_element_by_name("Experimental Collection date0").send_keys(data["collection_date"].split("-")[2])
    browser.find_element_by_name("Local Spectrum Identifier").send_keys(data["local_identifier"])


    click_tab(browser, 4)
    browser.find_element_by_name("Molecular Weight").send_keys(data["weight"])
    browser.find_element_by_name("Number of Residues").send_keys(data["residue_count"])
    browser.find_element_by_name("Mean Residue Weight").send_keys(data["mean_weight"])
    drop_down(browser, "Data Processing Software Name", data["processing_software"])
    browser.find_element_by_name("Data Processing Software Version").send_keys(data["software_version"])
    browser.find_element_by_name("Number of Smoothing Points").send_keys(data["smoothing_points"])
    browser.find_element_by_name("Wavelength Range for Zeroing").send_keys(data["zeroing_range"])
    

    click_tab(browser, 6)
    browser.find_element_by_name("PDB ID").send_keys(data["pdb"])
    browser.find_element_by_name("UniProt ID").send_keys(data["uniprot"])
    browser.find_element_by_name("Enzyme Classification (EC)").send_keys(data["enzyme"])
    browser.find_element_by_name("Medline Entry").send_keys(data["medline"])
    browser.find_element_by_name("Cath Classification").send_keys(data["cath"])
    browser.find_element_by_name("Sequence").send_keys(data["sequence"])
    drop_down(browser, "Type of protein", data["protein_type"])
    for index, keyword in enumerate(data["keywords"]):
        char = chr(65 + index)
        browser.find_element_by_name("Keyword/phrase " + char).send_keys(keyword)
    browser.find_element_by_name("Publication Authors").send_keys(data["pub_authors"])
    browser.find_element_by_name("Publication Year").send_keys(data["pub_year"])
    browser.find_element_by_name("Publication Journal").send_keys(data["pub_journal"])
    browser.find_element_by_name("Publication Title").send_keys(data["pub_title"])
    browser.find_element_by_name("Publication Volume").send_keys(data["pub_volume"])
    browser.find_element_by_name("Publication Pages").send_keys(data["pub_pages"])

    click_tab(browser, 7)
    browser.find_element_by_name("Depositor Name").send_keys(data["depositor_name"])
    browser.find_element_by_name("Department/School name").send_keys(data["department/school"])
    browser.find_element_by_name("University/Institution/Corporation").send_keys(data["university"])
    drop_down(browser, "Depositor Country", data["country"])
    browser.find_element_by_name("Depositor Email").send_keys(data["email"])
    browser.find_element_by_name("Depositor Telephone").send_keys(data["telephone"])
    browser.find_element_by_name("Name of Principal Investigator (if not depositor)").send_keys(data["pi_name"])
    browser.find_element_by_name("Email of Principal Investigator (if not depositor)").send_keys(data["pi_email"])






if __name__ == "__main__":
    data["password"] = input("Enter PCDDB password: ")
    browser = webdriver.Chrome()
    try:
        login_pcddb(browser)
        submit_entry(browser)
        while True:
            sleep(10)
    except Exception as e:
        traceback.print_exc()
    finally:
        browser.close()