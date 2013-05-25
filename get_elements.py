# get the atomic masses of the elements from a webpage
from bs4 import BeautifulSoup
import urllib2

url = "http://www.csudh.edu/oliver/chemdata/atmass.htm"
page = urllib2.urlopen(url)
contents = page.read()
page.close()

data = BeautifulSoup(contents)
data_table = data.body.table

elements = []
d = {}

for element in data_table.find_all("tr")[1:]:
  element_data = [item.contents[0] for item in element.find_all("td") if len(item.contents) > 0]
  atomic_mass = element_data[3]
  if "(" in atomic_mass and ")" in atomic_mass:
    atomic_mass = atomic_mass[:len(atomic_mass) - 3] # remove the parentheses
    element_data[3] = atomic_mass
  element_string = ",".join(element_data[:4])
  #elements.append(element_string)
  d[int(element_data[2])] = element_string

keys = d.keys()
keys.sort()
for number in keys:
  elements.append(d[number])

final_data = "\n".join(elements)
filename = "new_element_list.txt"
f = open(filename, "w")
f.write(final_data)
f.close()
print filename + " written"