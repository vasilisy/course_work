from tkinter import *
from tkinter import filedialog
import overpy
import requests
import json
import shutil
import os


count = 0
path = ''
operations = 1


def save_path():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askdirectory()
    return file_path


def save_image(coords, name_of_image, name_of_folder):
    res_image = requests.get('https://maps.googleapis.com/maps/api/streetview?size=640x300&location='+coords+'&pitch=0&fov=120&radius=10&key=AIzaSyAjSPCl4G3JOz8cXWL5GGiczLQHeVV37D8', stream=True)
    with open(name_of_folder+'/'+name_of_image, 'wb') as f:
        shutil.copyfileobj(res_image.raw, f)


def get_status(coords):
    res = requests.get('https://maps.googleapis.com/maps/api/streetview/metadata?size=600x300&location='+coords+'&radius=10&key=AIzaSyAjSPCl4G3JOz8cXWL5GGiczLQHeVV37D8')
    res_json = json.loads(res.text)
    return res_json.get('status')


def function(text):
    # Отправляем запрос на openstreetmap
    api = overpy.Overpass()
    request = f"""
    area[name="{text}"];
    (
    node["railway"~"switch"](area);
    way["railway"~"switch"](area);
    relation["railway"~"switch"](area);
    );
    out body;
    >;
    out skel qt;
    """
    Data = api.query(request)

    # Сохраняем все координаты
    output = []
    for way in Data.nodes:
        output.append(str(way.lat) + ', ' + str(way.lon))

    # Проверяем есть ли у данной координаты панорама в Google Street View
    # И если есть - сохраняем изображение
    global count
    count = 0
    global path
    for coords in output:
        # Запрашиваем информацию о координате и проверяем статус
        if get_status(coords) == 'OK':
            if count == 0:
                # Узнаем директорию, в которую все сохранять
                global path
                path = save_path()
                # Создаем файл, в котором будут храниться все координаты с панорамой
                f = open(path + '/' + f'{text}.json', 'w')
            # Сохраняем координаты
            f.write(coords)
            f.write('\n')
            count += 1
            # Создаем название файла
            name = 'image_'+str(count)+'.jpg'
            # Сохраняем изображение
            save_image(coords, name, path)


def open_folder():
    folder_path = path # получаем текущую рабочую директорию
    os.startfile(folder_path) # открываем папку в проводнике


def error():
    root = Tk()
    root.title('Ошибка')
    root.geometry('200x200')
    lbl = Label(root, text="Вы не ввели населенный пункт")
    lbl.pack(anchor=CENTER, expand=1)


def forma():
    global count
    def clicked():
        global operations
        try:
            function(txt.get())

            lbl_1 = Label(window, text = str(operations) + '. ' + txt.get())
            lbl_1.grid(column=0, row=operations+1, sticky="W")
            if count == 0:
                lbl_2 = Label(window, text = 'Панорамы жд стрелок в этом городе нет')
                lbl_2.grid(column=1, row=operations+1, sticky="W")
            else:
                btn_1 = Button(window, text="Открыть папку", command=open_folder)
                btn_1.grid(column=1, row=operations+1, sticky="W")
            operations += 1
        except:
            error()
    window = Tk()
    window.title("Railway Switch Coords")
    window.geometry('600x400')
    lbl = Label(window, text="Введите населенный пункт:")
    lbl.grid(column=0, row=0)
    txt = Entry(window, width=10)
    txt.grid(column=1, row=0)
    btn = Button(window, text="Получить изображения", command=clicked)
    btn.grid(column=2, row=0)
    window.mainloop()


if __name__ == '__main__':
    forma()
