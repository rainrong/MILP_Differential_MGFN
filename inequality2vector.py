import re

file = open("MGFN_Inequalities_vector.txt", "r")
fileout = open("MGFN_Inequalities.txt", "w")

for line in file.readlines():
    pattern = re.compile(r'-*\d{1,2}')
    result = pattern.findall(line)
    for ans in result[:-1]:
        fileout.write(" " + ans + " ")
    fileout.write(" ")
    fileout.write("\n")
