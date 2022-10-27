import jinja2
from xhtml2pdf import pisa
from read_xml import get_xml_data
from glob import glob
import os
import shutil
import time


# =============================================

# Utility function
def convert_html_to_pdf(source_html, output_filename):
    # open output file for writing (truncated binary)
    result_file = open(output_filename, "w+b")

    # convert HTML to PDF
    pisa_status = pisa.CreatePDF(
        src=source_html,  # the HTML to convert
        dest=result_file,  # file handle to recieve result
    )

    # close output file
    result_file.close()  # close output file

    # return False on success and True on errors
    return pisa_status.err


# ===================================


# Main program
if __name__ == "__main__":
    try:
        os.mkdir("PDF_Files")
    except Exception as e:
        pass

    try:
        os.mkdir("html_files")
    except Exception as e:
        pass
    # ====================== pdf ========================
    pisa.showLogging()
    templateLoader = jinja2.FileSystemLoader(searchpath=".")
    templateEnv = jinja2.Environment(loader=templateLoader)
    TEMPLATE_FILE = "pdf_report.html"
    template = templateEnv.get_template(TEMPLATE_FILE)

    # todo: specify the folder of xml files
    xmls = glob("all_xml_files/*.XML")
    for xml_file_path in xmls:
        output_filename = xml_file_path.split("\\")[1].split(".")[0]

        vehicle_infos, CodeScanSystems, body_controls, tire_pressures, readinesses, code_scan_type, top_information = get_xml_data(
            xml_file_path)

        output_text = template.render(
            vehicle_infos=vehicle_infos,
            CodeScanSystems=CodeScanSystems,
            body_controls=body_controls,
            tire_pressures=tire_pressures,
            readinesses=readinesses,
            code_scan_type=code_scan_type,
            top_information=top_information,
        )

        with open("html_files/" + output_filename + ".html", 'w') as html_file:
            html_file.write(output_text)
            html_file.close()

        for vehicle in vehicle_infos:
            if vehicle["@name"] == 'VIN':
                pdf_name = vehicle["@value"][-8:] + '_' + code_scan_type

        source_html = open("html_files/" + output_filename + ".html", "r+b")
        output_filename = "PDF_Files/" + pdf_name + ".pdf"

        convert_html_to_pdf(source_html, output_filename)

    # ====================== pdf ========================

'''
I need a script to change xml to pdf it’ll be the same format
and the file name should be last 8 of the vin + “pre” or “post”

issue: 
1. you’re missing all the top left information on the front page==done
2. you’re also missing the document headers==not possible currently
3. Also missing the last 9 of the VIN’s Characters on the end of each file
, the script to name each file last 8 characters of the VIN (Veichle Identification Number) + Post or Pre

4. See how this tag is “Pre” or “Post” this needs to get amended to the end of each PDF==done

'''
