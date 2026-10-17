import json
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Permission
from results.models import BranchGroup, Student, Subject, Score

RAW_DATA = [
  {
    "branch": "स्वामी सूबोधानंद शाखा",
    "roll_number": "1",
    "name": "कैवल्य काळोख",
    "standard": "5",
    "english": "9",
    "mathematics": "4.0",
    "science": "13.0",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "स्वामी सूबोधानंद शाखा",
    "roll_number": "2",
    "name": "श्लोक कुसाळकर",
    "standard": "5",
    "english": "14",
    "mathematics": "8.0",
    "science": "14.0",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "स्वामी सूबोधानंद शाखा",
    "roll_number": "3",
    "name": "तेजस म्हस्के",
    "standard": "5",
    "english": "0",
    "mathematics": "8.0",
    "science": "10.0",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "स्वामी सूबोधानंद शाखा",
    "roll_number": "4",
    "name": "सोहम खरिवले",
    "standard": "6",
    "english": "27",
    "mathematics": "29.0",
    "science": "11.0",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "स्वामी सूबोधानंद शाखा",
    "roll_number": "5",
    "name": "रुद्र दरवटकर",
    "standard": "6",
    "english": "16",
    "mathematics": "8.0",
    "science": "4.0",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "स्वामी सूबोधानंद शाखा",
    "roll_number": "6",
    "name": "राजन पड्याळ",
    "standard": "7",
    "english": "16",
    "mathematics": "11.0",
    "science": "4.0",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "स्वामी सूबोधानंद शाखा",
    "roll_number": "7",
    "name": "मल्हार कळसकर",
    "standard": "7",
    "english": "33",
    "mathematics": "16.0",
    "science": "5.0",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "स्वामी सूबोधानंद शाखा",
    "roll_number": "8",
    "name": "सोहम साळवे",
    "standard": "7",
    "english": "4",
    "mathematics": "1.0",
    "science": "",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "स्वामी सूबोधानंद शाखा",
    "roll_number": "9",
    "name": "आयुष लायगुडे",
    "standard": "7",
    "english": "17",
    "mathematics": "13.0",
    "science": "8.0",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "स्वामी सूबोधानंद शाखा",
    "roll_number": "10",
    "name": "पवन सापते",
    "standard": "7",
    "english": "0",
    "mathematics": "4.0",
    "science": "0.0",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "स्वामी सूबोधानंद शाखा",
    "roll_number": "11",
    "name": "संभव ठाकूर",
    "standard": "7",
    "english": "14",
    "mathematics": "8.0",
    "science": "8.0",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "स्वामी सूबोधानंद शाखा",
    "roll_number": "12",
    "name": "श्लोक गोळे",
    "standard": "7",
    "english": "6",
    "mathematics": "6.0",
    "science": "4.0",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "स्वामी सूबोधानंद शाखा",
    "roll_number": "13",
    "name": "तन्मय सातपुते",
    "standard": "8",
    "english": "7",
    "mathematics": "21.0",
    "science": "8.0",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "स्वामी सूबोधानंद शाखा",
    "roll_number": "14",
    "name": "तन्मय पडवेकर",
    "standard": "8",
    "english": "15",
    "mathematics": "15.0",
    "science": "2.0",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "स्वामी सूबोधानंद शाखा",
    "roll_number": "15",
    "name": "पार्थ साळवी",
    "standard": "9",
    "english": "25",
    "mathematics": "",
    "science": "",
    "mathematics_1": "0.0",
    "mathematics_2": "23.0",
    "science_1": "19.0",
    "science_2": "22.0"
  },
  {
    "branch": "स्वामी सूबोधानंद शाखा",
    "roll_number": "16",
    "name": "दर्श  साठे",
    "standard": "9",
    "english": "29",
    "mathematics": "",
    "science": "",
    "mathematics_1": "14.0",
    "mathematics_2": "20.0",
    "science_1": "25.0",
    "science_2": "20.0"
  },
  {
    "branch": "स्वामी सूबोधानंद शाखा",
    "roll_number": "17",
    "name": "अथर्व  लायगुडे",
    "standard": "9",
    "english": "17",
    "mathematics": "",
    "science": "",
    "mathematics_1": "2.0",
    "mathematics_2": "16.0",
    "science_1": "20.0",
    "science_2": "16.0"
  },
  {
    "branch": "राजर्षी शाहू महाराज शाखा",
    "roll_number": "501",
    "name": "Arnav zate",
    "standard": "5",
    "english": "35",
    "mathematics": "15",
    "science": "13",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "राजर्षी शाहू महाराज शाखा",
    "roll_number": "502",
    "name": "Gaurav salunke",
    "standard": "5",
    "english": "0",
    "mathematics": "1",
    "science": "1",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "राजर्षी शाहू महाराज शाखा",
    "roll_number": "503",
    "name": "parmeshwar ladkar",
    "standard": "5",
    "english": "14",
    "mathematics": "11",
    "science": "6",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "राजर्षी शाहू महाराज शाखा",
    "roll_number": "504",
    "name": "varad kadu",
    "standard": "5",
    "english": "0",
    "mathematics": "9",
    "science": "3",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "राजर्षी शाहू महाराज शाखा",
    "roll_number": "505",
    "name": "Sarthak birajdar",
    "standard": "5",
    "english": "35",
    "mathematics": "14",
    "science": "9",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "राजर्षी शाहू महाराज शाखा",
    "roll_number": "506",
    "name": "Atharva poul",
    "standard": "5",
    "english": "27",
    "mathematics": "4",
    "science": "0",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "राजर्षी शाहू महाराज शाखा",
    "roll_number": "507",
    "name": "rahul balla",
    "standard": "5",
    "english": "0",
    "mathematics": "11",
    "science": "0",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "राजर्षी शाहू महाराज शाखा",
    "roll_number": "508",
    "name": "Ayush Shinde",
    "standard": "5",
    "english": "0",
    "mathematics": "11",
    "science": "0",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "राजर्षी शाहू महाराज शाखा",
    "roll_number": "601",
    "name": "Arnav dalvi",
    "standard": "6",
    "english": "22",
    "mathematics": "12",
    "science": "3",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "राजर्षी शाहू महाराज शाखा",
    "roll_number": "602",
    "name": "Swaraj wanjale",
    "standard": "6",
    "english": "28",
    "mathematics": "22",
    "science": "8",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "राजर्षी शाहू महाराज शाखा",
    "roll_number": "603",
    "name": "Atul bharti",
    "standard": "6",
    "english": "4",
    "mathematics": "20",
    "science": "4",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "राजर्षी शाहू महाराज शाखा",
    "roll_number": "604",
    "name": "Rudar Chirake",
    "standard": "6",
    "english": "0",
    "mathematics": "25",
    "science": "0",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "राजर्षी शाहू महाराज शाखा",
    "roll_number": "605",
    "name": "Vedant survase",
    "standard": "6",
    "english": "9",
    "mathematics": "4",
    "science": "0",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "राजर्षी शाहू महाराज शाखा",
    "roll_number": "701",
    "name": "Vedant dalvi",
    "standard": "7",
    "english": "10",
    "mathematics": "17",
    "science": "10",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "राजर्षी शाहू महाराज शाखा",
    "roll_number": "702",
    "name": "Rameshwar Ladkar",
    "standard": "7",
    "english": "19",
    "mathematics": "14",
    "science": "10",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "राजर्षी शाहू महाराज शाखा",
    "roll_number": "703",
    "name": "Pratik Gaikwad",
    "standard": "7",
    "english": "0",
    "mathematics": "0",
    "science": "3",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "राजर्षी शाहू महाराज शाखा",
    "roll_number": "704",
    "name": "Ayush Hone",
    "standard": "7",
    "english": "32",
    "mathematics": "14",
    "science": "13",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "राजर्षी शाहू महाराज शाखा",
    "roll_number": "705",
    "name": "Vishnu Shinde",
    "standard": "7",
    "english": "0",
    "mathematics": "10",
    "science": "0",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "राजर्षी शाहू महाराज शाखा",
    "roll_number": "801",
    "name": "Manas Padekar",
    "standard": "8",
    "english": "35",
    "mathematics": "42",
    "science": "34",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "राजर्षी शाहू महाराज शाखा",
    "roll_number": "802",
    "name": "Shubham jadhav",
    "standard": "8",
    "english": "0",
    "mathematics": "0",
    "science": "23",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "राजर्षी शाहू महाराज शाखा",
    "roll_number": "803",
    "name": "Sujal Sutar",
    "standard": "8",
    "english": "18",
    "mathematics": "21",
    "science": "18",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "राजर्षी शाहू महाराज शाखा",
    "roll_number": "804",
    "name": "Sarthak  Chirake",
    "standard": "8",
    "english": "22",
    "mathematics": "31",
    "science": "0",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "राजर्षी शाहू महाराज शाखा",
    "roll_number": "805",
    "name": "Shreyash mundekar",
    "standard": "8",
    "english": "33",
    "mathematics": "34",
    "science": "29",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "राजर्षी शाहू महाराज शाखा",
    "roll_number": "806",
    "name": "Shreekrushna pawar",
    "standard": "8",
    "english": "0",
    "mathematics": "17",
    "science": "0",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "राजर्षी शाहू महाराज शाखा",
    "roll_number": "807",
    "name": "Mahesh Talwar",
    "standard": "8",
    "english": "0",
    "mathematics": "10",
    "science": "0",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "राजर्षी शाहू महाराज शाखा",
    "roll_number": "901",
    "name": "Mallikaarjun Shinde",
    "standard": "9",
    "english": "40",
    "mathematics": "",
    "science": "",
    "mathematics_1": "8",
    "mathematics_2": "18",
    "science_1": "9",
    "science_2": "9"
  },
  {
    "branch": "राजर्षी शाहू महाराज शाखा",
    "roll_number": "902",
    "name": "Soham Bagul",
    "standard": "9",
    "english": "39",
    "mathematics": "",
    "science": "",
    "mathematics_1": "0",
    "mathematics_2": "0",
    "science_1": "4",
    "science_2": "3"
  },
  {
    "branch": "राजर्षी शाहू महाराज शाखा",
    "roll_number": "903",
    "name": "Ashwamed Bhumbe",
    "standard": "9",
    "english": "52",
    "mathematics": "",
    "science": "",
    "mathematics_1": "8",
    "mathematics_2": "21",
    "science_1": "25",
    "science_2": "20"
  },
  {
    "branch": "राजर्षी शाहू महाराज शाखा",
    "roll_number": "904",
    "name": "Rudra Jadhav",
    "standard": "9",
    "english": "0",
    "mathematics": "",
    "science": "",
    "mathematics_1": "10",
    "mathematics_2": "12",
    "science_1": "0",
    "science_2": "0"
  },
  {
    "branch": "राजर्षी शाहू महाराज शाखा",
    "roll_number": "905",
    "name": "Ayush Shirgaionkar",
    "standard": "9",
    "english": "7",
    "mathematics": "",
    "science": "",
    "mathematics_1": "2",
    "mathematics_2": "6",
    "science_1": "5",
    "science_2": "12"
  },
  {
    "branch": "राजर्षी शाहू महाराज शाखा",
    "roll_number": "1001",
    "name": "Manoj koli",
    "standard": "10",
    "english": "12",
    "mathematics": "",
    "science": "",
    "mathematics_1": "2",
    "mathematics_2": "6",
    "science_1": "15",
    "science_2": ""
  },
  {
    "branch": "राजर्षी शाहू महाराज शाखा",
    "roll_number": "1002",
    "name": "naitik Mali",
    "standard": "10",
    "english": "43",
    "mathematics": "",
    "science": "",
    "mathematics_1": "7",
    "mathematics_2": "12",
    "science_1": "24",
    "science_2": ""
  },
  {
    "branch": "राजर्षी शाहू महाराज शाखा",
    "roll_number": "1003",
    "name": "Shantanu Hivarkar",
    "standard": "10",
    "english": "37",
    "mathematics": "",
    "science": "",
    "mathematics_1": "0",
    "mathematics_2": "22",
    "science_1": "21",
    "science_2": ""
  },
  {
    "branch": "राजर्षी शाहू महाराज शाखा",
    "roll_number": "",
    "name": "",
    "standard": "",
    "english": "",
    "mathematics": "",
    "science": "",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "राजर्षी शाहू महाराज शाखा",
    "roll_number": "",
    "name": "santosh PAWAR",
    "standard": "",
    "english": "",
    "mathematics": "",
    "science": "",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "स्वामी ब्रम्हानंद शाखा",
    "roll_number": "1",
    "name": "अमेय चव्हाण",
    "standard": "5",
    "english": "19",
    "mathematics": "11",
    "science": "6",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "स्वामी ब्रम्हानंद शाखा",
    "roll_number": "2",
    "name": "विराज डोईफोडे",
    "standard": "6",
    "english": "19",
    "mathematics": "32",
    "science": "7",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "स्वामी ब्रम्हानंद शाखा",
    "roll_number": "3",
    "name": "ओमकार पोतदार",
    "standard": "6",
    "english": "29",
    "mathematics": "26",
    "science": "4",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "स्वामी ब्रम्हानंद शाखा",
    "roll_number": "4",
    "name": "श्री खंदारे",
    "standard": "6",
    "english": "8",
    "mathematics": "23",
    "science": "0",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "स्वामी ब्रम्हानंद शाखा",
    "roll_number": "5",
    "name": "दक्ष चोरगे",
    "standard": "6",
    "english": "13",
    "mathematics": "17",
    "science": "4",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "स्वामी ब्रम्हानंद शाखा",
    "roll_number": "6",
    "name": "साईराज रूपनूर",
    "standard": "6",
    "english": "32",
    "mathematics": "30",
    "science": "4",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "स्वामी ब्रम्हानंद शाखा",
    "roll_number": "7",
    "name": "सार्थक आरकडे",
    "standard": "6",
    "english": "24",
    "mathematics": "18",
    "science": "4",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "स्वामी ब्रम्हानंद शाखा",
    "roll_number": "8",
    "name": "श्लोक साबळे",
    "standard": "7",
    "english": "19",
    "mathematics": "14",
    "science": "3",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "स्वामी ब्रम्हानंद शाखा",
    "roll_number": "9",
    "name": "ओमकार गायकवाड",
    "standard": "7",
    "english": "27",
    "mathematics": "19",
    "science": "8",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "स्वामी ब्रम्हानंद शाखा",
    "roll_number": "10",
    "name": "नील लोंढे",
    "standard": "7",
    "english": "15",
    "mathematics": "15",
    "science": "3",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "स्वामी ब्रम्हानंद शाखा",
    "roll_number": "11",
    "name": "स्वप्निल खंडागळे",
    "standard": "7",
    "english": "8",
    "mathematics": "18",
    "science": "4",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "स्वामी ब्रम्हानंद शाखा",
    "roll_number": "12",
    "name": "विराज उतांगळे",
    "standard": "7",
    "english": "22",
    "mathematics": "3",
    "science": "8",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "स्वामी ब्रम्हानंद शाखा",
    "roll_number": "13",
    "name": "यश सपकाळ",
    "standard": "7",
    "english": "34",
    "mathematics": "15",
    "science": "4",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "स्वामी ब्रम्हानंद शाखा",
    "roll_number": "14",
    "name": "श्रीतेज तनपुरे",
    "standard": "8",
    "english": "10",
    "mathematics": "5",
    "science": "5",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "स्वामी ब्रम्हानंद शाखा",
    "roll_number": "15",
    "name": "विनायक पोतदार",
    "standard": "8",
    "english": "11",
    "mathematics": "14",
    "science": "8",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "स्वामी ब्रम्हानंद शाखा",
    "roll_number": "16",
    "name": "वंश तोळनूर",
    "standard": "8",
    "english": "3",
    "mathematics": "1",
    "science": "1",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "स्वामी ब्रम्हानंद शाखा",
    "roll_number": "17",
    "name": "गणेश पवळे",
    "standard": "9",
    "english": "33",
    "mathematics": "",
    "science": "",
    "mathematics_1": "12",
    "mathematics_2": "23",
    "science_1": "16",
    "science_2": "18"
  },
  {
    "branch": "स्वामी ब्रम्हानंद शाखा",
    "roll_number": "18",
    "name": "आर्यन दिवेकर",
    "standard": "9",
    "english": "20",
    "mathematics": "",
    "science": "",
    "mathematics_1": "10",
    "mathematics_2": "9",
    "science_1": "3",
    "science_2": "4"
  },
  {
    "branch": "स्वामी ब्रम्हानंद शाखा",
    "roll_number": "19",
    "name": "यश औटी",
    "standard": "9",
    "english": "39",
    "mathematics": "",
    "science": "",
    "mathematics_1": "24",
    "mathematics_2": "19",
    "science_1": "4",
    "science_2": "18"
  },
  {
    "branch": "स्वामी ब्रम्हानंद शाखा",
    "roll_number": "20",
    "name": "साई खंदारे",
    "standard": "10",
    "english": "14",
    "mathematics": "",
    "science": "",
    "mathematics_1": "21",
    "mathematics_2": "6",
    "science_1": "18",
    "science_2": "0"
  },
  {
    "branch": "स्वामी ब्रम्हानंद शाखा",
    "roll_number": "21",
    "name": "स्वराज डोईफोडे",
    "standard": "10",
    "english": "28",
    "mathematics": "",
    "science": "",
    "mathematics_1": "32",
    "mathematics_2": "0",
    "science_1": "30",
    "science_2": "34"
  },
  {
    "branch": "स्वामी ब्रम्हानंद शाखा",
    "roll_number": "22",
    "name": "प्रज्वल देशपांडे",
    "standard": "10",
    "english": "13",
    "mathematics": "",
    "science": "",
    "mathematics_1": "32",
    "mathematics_2": "31",
    "science_1": "21",
    "science_2": "21"
  },
  {
    "branch": "स्वामी ब्रम्हानंद शाखा",
    "roll_number": "23",
    "name": "इंद्रजीत डुकरे",
    "standard": "10",
    "english": "12",
    "mathematics": "",
    "science": "",
    "mathematics_1": "18",
    "mathematics_2": "11",
    "science_1": "4",
    "science_2": "7"
  },
  {
    "branch": "स्वामी ब्रम्हानंद शाखा",
    "roll_number": "24",
    "name": "आदित्य शेंडगे",
    "standard": "10",
    "english": "0",
    "mathematics": "",
    "science": "",
    "mathematics_1": "20",
    "mathematics_2": "0",
    "science_1": "0",
    "science_2": "28"
  },
  {
    "branch": "नरवीर तानाजी मालुसरे शाखा",
    "roll_number": "401",
    "name": "रुद्र सोनार (४ थी)",
    "standard": "4",
    "english": "19",
    "mathematics": "22.0",
    "science": "21.0",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "नरवीर तानाजी मालुसरे शाखा",
    "roll_number": "402",
    "name": "ओमकार वाघमारे (४ थी)",
    "standard": "4",
    "english": "22",
    "mathematics": "22.5",
    "science": "25.0",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "नरवीर तानाजी मालुसरे शाखा",
    "roll_number": "403",
    "name": "श्री इरकर (४ थी)",
    "standard": "4",
    "english": "25",
    "mathematics": "23.0",
    "science": "28.0",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "नरवीर तानाजी मालुसरे शाखा",
    "roll_number": "404",
    "name": "युवराज राठोड (४ थी)",
    "standard": "4",
    "english": "20",
    "mathematics": "20.0",
    "science": "19.0",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "नरवीर तानाजी मालुसरे शाखा",
    "roll_number": "501",
    "name": "आरुष लोंढे (५ वी)",
    "standard": "5",
    "english": "19",
    "mathematics": "25.0",
    "science": "20.0",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "नरवीर तानाजी मालुसरे शाखा",
    "roll_number": "502",
    "name": "परशूराम मेलगिरी (५ वी)",
    "standard": "5",
    "english": "24",
    "mathematics": "23.0",
    "science": "21.0",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "नरवीर तानाजी मालुसरे शाखा",
    "roll_number": "601",
    "name": "मौसम कनोजिया (६ वी)",
    "standard": "6",
    "english": "22",
    "mathematics": "15.0",
    "science": "21.5",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "नरवीर तानाजी मालुसरे शाखा",
    "roll_number": "602",
    "name": "वेदांत भोसले (६ वी)",
    "standard": "6",
    "english": "27",
    "mathematics": "25.0",
    "science": "22.0",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "नरवीर तानाजी मालुसरे शाखा",
    "roll_number": "603",
    "name": "सम्राट राठोड (६ वी)",
    "standard": "6",
    "english": "20",
    "mathematics": "20.0",
    "science": "17.0",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "नरवीर तानाजी मालुसरे शाखा",
    "roll_number": "604",
    "name": "शौर्य जाधव (६ वी)",
    "standard": "6",
    "english": "21",
    "mathematics": "22.0",
    "science": "16.0",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "नरवीर तानाजी मालुसरे शाखा",
    "roll_number": "605",
    "name": "ओम देशमाने (६ वी)",
    "standard": "6",
    "english": "18",
    "mathematics": "21.0",
    "science": "20.0",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "नरवीर तानाजी मालुसरे शाखा",
    "roll_number": "606",
    "name": "श्रवण ढोरे (६ वी)",
    "standard": "6",
    "english": "26",
    "mathematics": "22.0",
    "science": "24.0",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "नरवीर तानाजी मालुसरे शाखा",
    "roll_number": "607",
    "name": "प्रथमेश नायकोडी (६ वी)",
    "standard": "6",
    "english": "23",
    "mathematics": "24.0",
    "science": "20.0",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "नरवीर तानाजी मालुसरे शाखा",
    "roll_number": "801",
    "name": "सुग्रीव सिंह (८ वी)",
    "standard": "8",
    "english": "20",
    "mathematics": "28.0",
    "science": "25.0",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "नरवीर तानाजी मालुसरे शाखा",
    "roll_number": "802",
    "name": "आदर्श बांगर (८ वी)",
    "standard": "8",
    "english": "25",
    "mathematics": "30.0",
    "science": "28.0",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "नरवीर तानाजी मालुसरे शाखा",
    "roll_number": "803",
    "name": "रितेश राठोड (८ वी)",
    "standard": "8",
    "english": "16",
    "mathematics": "24.0",
    "science": "20.0",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "नरवीर तानाजी मालुसरे शाखा",
    "roll_number": "804",
    "name": "अर्जुन झिंगे (८ वी)",
    "standard": "8",
    "english": "32",
    "mathematics": "32.0",
    "science": "25.0",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "नरवीर तानाजी मालुसरे शाखा",
    "roll_number": "805",
    "name": "साई देशमाने (८ वी)",
    "standard": "8",
    "english": "17",
    "mathematics": "23.0",
    "science": "21.5",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "नरवीर तानाजी मालुसरे शाखा",
    "roll_number": "806",
    "name": "चंदू मेलगिरी (८ वी)",
    "standard": "8",
    "english": "20",
    "mathematics": "20.0",
    "science": "15.0",
    "mathematics_1": "",
    "mathematics_2": "",
    "science_1": "",
    "science_2": ""
  },
  {
    "branch": "नरवीर तानाजी मालुसरे शाखा",
    "roll_number": "901",
    "name": "कार्तिक सूर्यवंशी (९ वी)",
    "standard": "9",
    "english": "20",
    "mathematics": "",
    "science": "",
    "mathematics_1": "25.0",
    "mathematics_2": "21.0",
    "science_1": "21.0",
    "science_2": "25.0"
  },
  {
    "branch": "नरवीर तानाजी मालुसरे शाखा",
    "roll_number": "902",
    "name": "वेदांत जाधव (९ वी)",
    "standard": "9",
    "english": "25",
    "mathematics": "",
    "science": "",
    "mathematics_1": "28.0",
    "mathematics_2": "25.0",
    "science_1": "19.0",
    "science_2": "22.0"
  },
  {
    "branch": "नरवीर तानाजी मालुसरे शाखा",
    "roll_number": "903",
    "name": "श्रेयस चिपटे (९ वी)",
    "standard": "9",
    "english": "27",
    "mathematics": "",
    "science": "",
    "mathematics_1": "30.0",
    "mathematics_2": "32.0",
    "science_1": "25.0",
    "science_2": "26.0"
  },
  {
    "branch": "नरवीर तानाजी मालुसरे शाखा",
    "roll_number": "1001",
    "name": "साईनाथ सूर्यवंशी (१० वी)",
    "standard": "10",
    "english": "24",
    "mathematics": "",
    "science": "",
    "mathematics_1": "22.0",
    "mathematics_2": "25.0",
    "science_1": "18.0",
    "science_2": "21.0"
  },
  {
    "branch": "नरवीर तानाजी मालुसरे शाखा",
    "roll_number": "1002",
    "name": "आदर्श साळुंखे (१० वी)",
    "standard": "10",
    "english": "22",
    "mathematics": "",
    "science": "",
    "mathematics_1": "20.0",
    "mathematics_2": "22.0",
    "science_1": "14.0",
    "science_2": "20.0"
  }
]

BRANCH_USERS = [
    ("SubodhanandaSHAKHA", "28-07-1993", "स्वामी सूबोधानंद शाखा"),
    ("ShahuSHAKHA", "08-12-2008", "राजर्षी शाहू महाराज शाखा"),
    ("BramhanandaSHAKHA", "01-08-2003", "स्वामी ब्रम्हानंद शाखा"),
    ("NarveerSHAKHA", "12-12-2012", "नरवीर तानाजी मालुसरे शाखा"),
]

class Command(BaseCommand):
    help = "Permanently seed all Superusers, Co-Admins, Branches, and 100 Students with Scores"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Starting permanent database seeding..."))

        # 1. Superusers
        inv, _ = User.objects.get_or_create(username="Invincible")
        inv.set_password("piyush@3050")
        inv.is_staff = True
        inv.is_superuser = True
        inv.save()

        hod, _ = User.objects.get_or_create(username="HOD ShakhaVibhag")
        hod.set_password("HOD@2026")
        hod.is_staff = True
        hod.is_superuser = True
        hod.save()
        self.stdout.write(self.style.SUCCESS("✓ Superusers configured."))

        # 2. Branches & Co-Admins
        perms = Permission.objects.filter(content_type__app_label='results')
        branch_map = {}
        for uname, pwd, bname in BRANCH_USERS:
            u, _ = User.objects.get_or_create(username=uname)
            u.set_password(pwd)
            u.is_staff = True
            u.is_superuser = False
            u.save()
            u.user_permissions.set(perms)

            b, _ = BranchGroup.objects.get_or_create(name=bname)
            b.co_admin = u
            b.save()
            branch_map[bname] = b
            # fallback for slight spelling variation in Marathi
            if "सुबोधानंद" in bname or "सूबोधानंद" in bname:
                branch_map["स्वामी सुबोधानंद शाखा"] = b
                branch_map["स्वामी सूबोधानंद शाखा"] = b

        self.stdout.write(self.style.SUCCESS("✓ Branches & Co-Admins configured."))

        # 3. Create or Get Subjects
        subj_definitions = [
            ('english', 'इंग्रजी (English)'),
            ('mathematics', 'गणित (Mathematics)'),
            ('science', 'विज्ञान (Science)'),
            ('mathematics_1', 'गणित भाग १ (Mathematics 1)'),
            ('mathematics_2', 'गणित भाग २ (Mathematics 2)'),
            ('science_1', 'विज्ञान भाग १ (Science 1)'),
            ('science_2', 'विज्ञान भाग २ (Science 2)'),
        ]
        subj_objs = {}
        for code, name in subj_definitions:
            s_obj, _ = Subject.objects.get_or_create(code=code, defaults={'name': name})
            subj_objs[code] = s_obj

        # 4. Insert all students and scores
        created_count = 0
        updated_count = 0

        for item in RAW_DATA:
            bname = item['branch']
            branch_obj = branch_map.get(bname)
            if not branch_obj:
                branch_obj, _ = BranchGroup.objects.get_or_create(name=bname)
                branch_map[bname] = branch_obj

            roll_no = item['roll_number']
            s_name = item['name']
            std = item['standard'] or '5'

            student, created = Student.objects.update_or_create(
                branch_group=branch_obj,
                roll_number=roll_no,
                defaults={'name': s_name, 'standard': std}
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

            # Populate scores
            marks_fields = [
                'english', 'mathematics', 'science',
                'mathematics_1', 'mathematics_2', 'science_1', 'science_2'
            ]
            for mf in marks_fields:
                val = item.get(mf, '')
                if val != '' and val is not None:
                    try:
                        m_val = float(val)
                        Score.objects.update_or_create(
                            student=student,
                            subject=subj_objs[mf],
                            defaults={'marks_obtained': m_val}
                        )
                    except ValueError:
                        pass

        self.stdout.write(self.style.SUCCESS(
            f"✓ Finished! Total Students seeded: {created_count + updated_count} ({created_count} new, {updated_count} updated)"
        ))
