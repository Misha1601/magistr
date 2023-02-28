import os
import xml.etree.ElementTree as ET

# Получаем имя текущей директории
current_dir = os.getcwd()

# Получаем имя файла XML
xml_file = os.path.join(current_dir, 'request_17_02_2023.xml')

# Читаем XML-файл
tree = ET.parse(xml_file)
root = tree.getroot()
print(len(root[2].attrib))
for i in root:
    print(root.text)

# Создаем новый XML-файл
new_xml_file = os.path.join(current_dir, 'new_data.xml')
tree.write(new_xml_file)