import csv
import pydot

person_dict = {}
output_file = open('output.dot', 'w')
output_file.write("digraph G{\n")
output_file.write("graph [pad=""0.5"", nodesep=""0.5"", ranksep=""2""];\n")
output_file.write("node [shape=plain]\n")

with open('family_data.csv', newline='\n') as csvfile:
  reader = csv.DictReader(csvfile)
  for row in reader:
    temp_dict = {}
    
    identif = row['pid']
    gen = row['generation']
    name = row['name']
    birthYear = row['byear']
    deathYear = row['dyear'][-4:]
    dage = row['dage']
    myear = row['myear']
    mage = row['mage']
    spouseId = row['spouseId']
    gender = row['gender']
    parentNodeId = row['parentNodeId']

    if gender == 'M':
      gender = "Male"
      genderColor = "Blue"
    else:
      gender = "Female"
      genderColor = "Pink"
      
    parentId1 = row['parentId1']
    parentId2 = row['parentId2']
    spouseID = row['spouseId']
    output_file.write("node" + identif + "[shape=none label=<\n")
    output_file.write('<TABLE border="0" cellspacing="0" cellpadding="10" style="rounded" bgcolor="Grey">\n')
    output_file.write('<TR><TD bgcolor="' + genderColor + '">Name:</TD>\n')
    output_file.write('<TD bgcolor="' + genderColor + '">' + name + "</TD></TR>\n")
    output_file.write('<TR><TD bgcolor="Grey">BirthYear:</TD>\n')
    output_file.write('<TD bgcolor="Grey">' + birthYear + '</TD></TR>\n')
    output_file.write('<TR><TD bgcolor="Grey">DeathYear:</TD>\n')
    output_file.write('<TD bgcolor="Grey">' + deathYear + "</TD></TR>\n")
    output_file.write('<TR><TD bgcolor="Grey">MarriageYear:</TD>\n')
    output_file.write('<TD bgcolor="Grey">' + myear + "</TD></TR>\n")
    output_file.write('<TR><TD bgcolor="Grey">Marriage Age:</TD>\n')
    output_file.write('<TD bgcolor="Grey">' + mage + "</TD></TR>\n")
    output_file.write("</TABLE>>];\n")
    if spouseId != "":
      output_file.write("node" + identif + " -> node" + spouseId + "[arrowhead=none headlabel=Married]\n")
    if spouseId != "":
      if parentId1 != "":
        output_file.write("node" + parentId1 + " -> node" + identif + "\n")
      if parentId2 != "":
        output_file.write("node" + parentId2 + " -> node" + identif + "\n")

    if parentNodeId != "":
        if parentNodeId != "-1":
          output_file.write("node" + identif + " -> node" + parentNodeId + "\n")
      
    temp_dict[name] = {"name": name, "birthYear": birthYear, "deathYear": deathYear, "gender": gender, "parentId1": parentId1, "parentId2": parentId2, "spouseID": spouseID}

    person_dict.update(temp_dict)
output_file.write("}\n")
print(person_dict)
output_file.close()
