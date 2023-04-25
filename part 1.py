import overpy
import requests
import json
import shutil


def save_image(coords, name):
    res_image = requests.get('https://maps.googleapis.com/maps/api/streetview?size=2400x2400&location='+coords+'&radius=1234&key=AIzaSyAjSPCl4G3JOz8cXWL5GGiczLQHeVV37D8', stream=True)
    with open('results/'+name, 'wb') as f:
        shutil.copyfileobj(res_image.raw, f)


# получаем координаты жд стрелок
api = overpy.Overpass()
Data = api.query("""
area[name="Челябинск"];
(
  node["railway"~"switch"](area);
  way["railway"~"switch"](area);
  relation["railway"~"switch"](area);
);
out body;
>;
out skel qt;
""")


#записываем результаты
output = []
for way in Data.nodes:
    output.append (str(way.lat) + ', ' + str(way.lon))
f = open('output.json', 'w')
for i in output:
    f.write(i)
    f.write('\n')


# проверка, есть ли панорама/изображение в google steert view и если есть, то сохранить изображение
count = 0
for coords in output:
    res = requests.get('https://maps.googleapis.com/maps/api/streetview/metadata?size=600x300&location='+coords+'&heading=-45&pitch=42&fov=110&key=AIzaSyAjSPCl4G3JOz8cXWL5GGiczLQHeVV37D8')
    res_json = json.loads(res.text)
    if res_json.get('status') == 'OK':
        count += 1
        name = 'image_'+str(count)+'.jpg'
        save_image(coords, name)