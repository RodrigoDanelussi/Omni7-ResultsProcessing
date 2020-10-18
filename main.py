import sys
import xlsxwriter
import xmltodict
from header import Column
from database import Get_Contiuos_Data, Get_Types, Get_Discrete_Data

# try:
dr = 10
road = 71
with open(f"//192.168.2.22/Compartilhada/FTPSERVER/Projeto_DER/Omni7/Bundles/DR{dr}/{road}/{road}.omni") as fd:
    doc = xmltodict.parse(fd.read())

xml = doc['Header']['frameInfos']['FrameInfo']

inverse = 'Normal' if xml[0]['type'] == 'ROAD' or xml[0]['type'] == 'DEVICE' else 'Inverso'
print(doc['Header']['road'])
data = Get_Contiuos_Data(doc['Header']['road'], inverse)
index = 0

col = []
for val in xml:
    if(val['type'] == 'ROAD' or val['type'] == 'DEVICE'):
        c = Column()
        c.frame = index
        index += +1
        c.latitude = val['latitude']
        c.longitude = val['longitude']
        c.altitude = val['altitude']
        c.cameraTime = val['cameraTime'].split('T')[0]
        c.imageName = val['imageName']
        col.append(c)
        
workbook = xlsxwriter.Workbook(f"DER_SP-{road}.xlsx")
worksheet = workbook.add_worksheet('Continuo')

bold = workbook.add_format({'bold': True})
date_formats = ('dd/mm/yy')

worksheet.write('A1', 'Frame', bold)
worksheet.write('B1', 'Latitude', bold)
worksheet.write('C1', 'Longitude', bold)
worksheet.write('D1', 'Altitude', bold)
worksheet.write('E1', 'Data', bold)
worksheet.write('F1', 'Sentido', bold)
worksheet.write('G1', 'Image', bold)
worksheet.write('H1', 'KM', bold)
worksheet.write('I1', 'Municipio', bold)

for i in range(0, len(col)):
    if(col[i].sentido == 'Normal'):
        worksheet.write('A' + str(i+2) , col[i].frame)
        worksheet.write('B' + str(i+2) , col[i].latitude)
        worksheet.write('C' + str(i+2) , col[i].longitude)
        worksheet.write('D' + str(i+2) , col[i].altitude)
        worksheet.write('E' + str(i+2) , col[i].cameraTime)
        worksheet.write('F' + str(i+2) , col[i].imageName)
    # print(list[i].frame)

types = Get_Types('Continuous')

for t in range(0, len(types)):
    letter = xlsxwriter.utility.xl_col_to_name(t+8)
    worksheet.write(letter + '1', types[t], bold)
    old_sub_type = ''
    for f in range(0, len(col)):
        subType = list(filter(lambda x: x.frame == f and x.type == types[t], data))
        if(subType != None):
            for i in subType:
                if(i.type != old_sub_type):
                    old_sub_type = i.subType
            worksheet.write(letter + str(f+2), old_sub_type)

worksheet = workbook.add_worksheet('Pontual')

worksheet.write('A1', 'Categoria', bold)
worksheet.write('B1', 'Subcategoria', bold)
worksheet.write('C1', 'Complemento 1', bold)
worksheet.write('D1', 'Complemento 2', bold)
worksheet.write('E1', 'Frame', bold)
worksheet.write('F1', 'Latitude', bold)
worksheet.write('G1', 'Longitude', bold)
worksheet.write('H1', 'Altitude', bold)
worksheet.write('I1', 'Image', bold)
worksheet.write('J1', 'KM', bold)
worksheet.write('K1', 'Municipio', bold)

data = Get_Discrete_Data(doc['Header']['road'], inverse)
print(data)
for i in range(0, len(data)):
    worksheet.write('A' + str(i+2), data[i].type)
    worksheet.write('B' + str(i+2), data[i].subType)
    if(hasattr(data[i], 'complement1')):
        worksheet.write('C' + str(i+2), data[i].complement1)
    if(hasattr(data[i], 'complement2')):
        worksheet.write('D' + str(i+2), data[i].complement2)
    worksheet.write('E' + str(i+2), data[i].frame)
    worksheet.write('F' + str(i+2), data[i].latitude)
    worksheet.write('G' + str(i+2), data[i].longitude)
    worksheet.write('H' + str(i+2), data[i].altitude)
    worksheet.write('I' + str(i+2), data[i].image)

workbook.close()