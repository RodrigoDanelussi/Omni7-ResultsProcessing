import csv_parser
import os
import helper
import output
from scipy import spatial
from scipy.spatial import KDTree
import csv
from shapely.geometry import Point, Polygon
from geo_points import GeoPoint, PointType, PolyArea


#parse
print('Parsing...')
filepath = os.path.join(os.path.dirname(__file__), r"Resources\municipios\Municipios.geo")
classifications = csv_parser.parse_classification(os.path.join(os.path.dirname(__file__),r"Resources\Classificacao\PLANILHA_CADASTRAMENTO.CSV"))
points_mun = csv_parser.parse_GEO(filepath, 0, 2)

#get classification bounds
print('calculating bound...')
lon, lat = (classifications[0]['lon_i'], classifications[0]['lat_i'])
bl = [lon, lat]
tr = [lon, lat]
for c in classifications:
    if c['lon_i'] < tr[0]:
        tr[0] = c['lon_i']
    if c['lon_i'] > bl[0]:
        bl[0] = c['lon_i']
    if c['lat_i'] < tr[1]:
        tr[1] = c['lat_i']
    if c['lat_i'] > bl[1]:
        bl[1] = c['lat_i']
    if c['lat_f'] is None:
        continue
    if c['lon_f'] < tr[0]:
        tr[0] = c['lon_f']
    if c['lon_f'] > bl[0]:
        bl[0] = c['lon_f']
    if c['lat_f'] < tr[1]:
        tr[1] = c['lat_f']
    if c['lat_f'] > bl[1]:
        bl[1] = c['lat_f']
print(bl,tr)
classification_bound_points = []
classification_bound_points.append((bl[0], bl[1]))
classification_bound_points.append((bl[0], tr[1]))
classification_bound_points.append((tr[0], tr[1]))
classification_bound_points.append((tr[0], bl[1]))
classification_bound_points.append((bl[0], bl[1]))

classification_bound = PolyArea()
classification_bound.polygon = Polygon(classification_bound_points)
classification_bound.points = classification_bound_points


#add ids
print('creating IDs...')
with open(filepath) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    all_borders = []
    line = 0
    for row in csv_reader:
        border = {}
        border['id0'] = int(row[0])
        border['id1'] = int(row[1])
        border['geo'] = points_mun[line]
        line = line + 1
        all_borders.append(border)

#create mun unique list
print('creating city list...')
mun_list = []
for b in all_borders:
    if not b['id0'] in mun_list:
        mun_list.append(b['id0'])
    if not b['id1'] in mun_list:
        mun_list.append(b['id1'])
mun_list.sort()

#create areas
areas = []
print('creating Areas...')
for mun in mun_list:
    if mun == 0:
        continue
    mun_borders = list(filter(lambda x: x['id0'] == mun or x['id1'] == mun, all_borders))
    if mun == 567:
        for m in mun_borders:
            print(m['id0'], m['id1'])
    geos = mun_borders[0]['geo']
    lastGeo = mun_borders[0]['geo'][-1]
    mun_borders.remove(mun_borders[0])
    while len(mun_borders) > 0:
        inverse = False
        next_border = next(filter(lambda x: x['geo'][0].lat == lastGeo.lat and x['geo'][0].lon == lastGeo.lon, mun_borders), None)
        if next_border is None:
            inverse = True
            next_border = next(filter(lambda x: x['geo'][-1].lat == lastGeo.lat and x['geo'][-1].lon == lastGeo.lon, mun_borders), None)
        if next_border is None:
            print(str(mun)+" border not found:" + str(lastGeo.lon)+','+str(lastGeo.lat))   
            break;  
        lastGeo = next_border['geo'][-1] if inverse is False else next_border['geo'][0]
        geos = geos + (next_border['geo'] if inverse is False else next_border['geo'][::-1])
        mun_borders.remove(next_border)
    area = {}
    area['id'] = mun
    area['geo'] = geos
    area['poly'] = helper.geo_to_poly(geos)
    area['poly'].name = str(mun)
    areas.append(area)
    #print(mun, len(geos))

#mun intersection
print("Getting bound intersections")
bound_areas = []
for a in areas:
    if a['poly'].polygon.intersects(classification_bound.polygon):
        bound_areas.append(a)

#find classificationPoints
print("Finding areas")
for c in classifications:
    point = Point(c['lon_i'], c['lat_i'])
    for a in bound_areas:
        if a['poly'].polygon.contains(point):
            c['mun_i'] = a['id']
            break
    if c['lat_f'] is not None:
        point = Point(c['lon_f'], c['lat_f'])
        for a in bound_areas:
            if a['poly'].polygon.contains(point):
                c['mun_f'] = a['id']
                break
    else:
        c['mun_f']=""
#csv output
with open('municipios.csv', mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(['id', 'municipio_i', 'municipio_f'])
    pts = classifications
    for p in pts:
        csv_writer.writerow([
            p['id'], 
            p['mun_i'],           
            p['mun_f']    
            ])

#KML
output = output.OutputKML()
#Border
#outArea = next(filter(lambda x: x['id'] == 567, areas), None)
folder_bound = output.createFolder("area")
#output.createLine(folder_area, outArea['geo'], 'FF'+color)
output.createPoly(folder_bound, classification_bound, 'FA7814')

folder_area = output.createFolder("Municipios")
for a in bound_areas:
    color = helper.randomColor()
    #output.createLine(folder_area, a['geo'], 'FF'+color)
    output.createPoly(folder_area, a['poly'], color)
folder_class = output.createFolder("itens")
for p in classifications:
    output.createDefaultPoint(folder_class, p['lon_i'], p['lat_i'], "ID:"+str(p['id'])+", Mun:"+str(p['mun_i']), output.style_map_road)
#save debug
output.save("municipios")