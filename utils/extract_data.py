import xml.etree.ElementTree as ET
import os
import csv


def full_path_to_data(directory, file_name):
    """

    :param directory: directory where data is located
    :param file_name: name of tuple that contains data
    :return: String - joins the params
    """
    full_path = os.path.join(os.path.join((os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), directory),
                             file_name)
    return full_path


def root_in_memory(full_path):
    """
    Function to read the root of xml into memory
    :param full_path: full path to data

    :return: Iterable object
    """

    tree = ET.parse(full_path)
    root = tree.getroot()
    return root


def clean_sales_data(data, directory, out_file_name):
    """
    Reads data xml iterator (root), extracts relevant data and output to specific file in specific directory
    :param data: data in the form of root in xml
    :param directory: output directory
    :param out_file_name: output file name
    :return: None
    """

    path = os.path.join(os.path.join((os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), directory), out_file_name)

    fhand = csv.writer(open(path, 'w', encoding='utf-8', newline=''), delimiter='|')
    for count, child in enumerate(data):
        header_list = []
        content_list = []
        for el in child:
            if count == 0:
                header_list.append(el.tag)
            else:
                if el.text is None:
                    content_list.append('')
                else:
                    content_list.append(el.text)
        if len(header_list) != 0:
            #print(header_list)
            fhand.writerow(header_list)
        if len(content_list) != 0:
            #content_list = ["" if i == 'None' or i =='NONE' else i for i in content_list]
            #print(content_list)
            fhand.writerow(s.replace('\n', "None") for s in content_list)
# Need to think about about the commas in the strings - they cause errors Might be worth just using a unique delimiter
# Change from inserting list to actual rows


def clean_booking_data(path_to_raw_data, out_dir_name, out_file_name):
    """
    Converts comma separated file to at pipe separated file
    :param path_to_raw_data: full path to raw data
    :param out_dir_name: output directory
    :param out_file_name: output file name
    :return: None
    """

    full_output_path = full_path_to_data(out_dir_name, out_file_name)

    with open(path_to_raw_data, "r", encoding='utf-8') as in_text:
        in_reader = csv.reader(in_text, delimiter=',')
        with open(full_output_path, "w", encoding='utf-8', newline='') as out_csv:
            out_writer = csv.writer(out_csv, delimiter='|')
            for row in in_reader:
                out_writer.writerow(row)