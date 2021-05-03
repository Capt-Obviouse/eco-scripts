###########################################################################
# Place update_trees.py into your servers root directory
# Run update_trees.py with python3
# treeGrowthValue is tree growth speed in days
# plantGrowthValue is plant growth speed in days
# treeList is the name of each tree in the game. This list determines which value
# in the directory mods/AutoGen/Plant the file will get. If its not a tree, it gets
# set to the plant value.
###########################################################################
import fileinput
import os
import sys
import pathlib

treeList = ['Birch', 'Cedar', 'Ceiba', 'Fir', 'Joshua', 'Oak', 'Palm', 'Redwood', 'Saguaro', 'Spruce']
treeFiles = []
plantFiles = []
treeGrowthValue = 3.0
plantGrowthValue = 0.5
GROWTH_SEARCH_STRING = "this.MaturityAgeDays = "
GROWTH_STRING = "{}this.MaturityAgeDays = {}f;\n"

currentDirectory = pathlib.Path().absolute()
workingDirectory = pathlib.Path(os.path.join(currentDirectory, "Mods", "AutoGen", "Plant"))

for currentFile in workingDirectory.iterdir():
    plantFiles.append(currentFile)
    for tree in treeList:
        try:
            if str(currentFile).index(tree):
                treeList.remove(tree)
                plantFiles.remove(currentFile)
                treeFiles.append(currentFile)
        except ValueError:
            continue

def find_replace_string(file_name, string_to_search, growth_value):
    update_file = False
    read_obj = open(file_name, 'r')
    spaces = 0

    # Get spacing 
    for line in read_obj:
        old_line = None
        if string_to_search in line:
            update_file = True
            old_line = line
            for char in line:
                if char.isspace():
                    spaces += 1
                else:
                    break
            break
    read_obj.close()


    if update_file:
        filedata = open(file_name, 'r').read()
        filedata = filedata.replace(old_line, GROWTH_STRING.format(spaces * " ", growth_value))

        with open(file_name, 'w') as write_file:
            write_file.write(filedata)
        return True

    return False


for file_name in treeFiles:
    find_replace_string(file_name, GROWTH_SEARCH_STRING, treeGrowthValue)

for file_name in plantFiles:
    find_replace_string(file_name, GROWTH_SEARCH_STRING, plantGrowthValue)
