#!/usr/bin/python3
import os
import tempfile
from datetime import datetime
import gzip
import xml.etree.ElementTree as ET

def get_current_holidays_xml():
    year = datetime.now().year
    with tempfile.TemporaryDirectory() as tempdir_path:
        rc = os.system("wget http://xmlcalendar.ru/data/ru/" + str(year) + "/calendar.xml.gz " + \
                       "-O " + tempdir_path + "/calendar-" + str(year) + ".xml.gz >/dev/null 2>&1")
        gz = gzip.open(tempdir_path + "/calendar-" + str(year) + ".xml.gz", 'r')
        tree = ET.parse(gz)
        root = tree.getroot()
        return root


def extract_holidays_from_xml(xml):
    holidays = []
    halfholidays = []
    result = (holidays, halfholidays)
    for day in xml.iter("day"):
        result[int(day.attrib["t"]) - 1].append(
            datetime.strptime(day.attrib["d"], "%m.%d").replace(year=datetime.now().year)
        )
    return result


def get_holidays_tuple():
    holidays_xml = get_current_holidays_xml()
    return extract_holidays_from_xml(holidays_xml)

def get_holidays_dict():
    holidays, halfholidays = get_holidays_tuple()
    return { "holidays": holidays, "halfholidays": halfholidays }


def print_holidays():
    print(get_holidays_dict())

if __name__ == '__main__':
    print_holidays()
