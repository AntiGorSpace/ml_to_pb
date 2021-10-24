import json
import os



def stethem_write(name,data):
    with open(name+'.json', 'w') as outfile:
        json.dump(data, outfile)
def stethem_reader(name):
    with open(name+'.json', "r") as infile:
        return json.load(infile)


def check_and_cre_folder(dirname):
        if not os.path.isdir(dirname):
            os.mkdir(dirname)