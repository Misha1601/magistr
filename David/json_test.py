import json
import os

def main():
    # Получаем имя текущей директории
    current_dir = os.getcwd()
    directory = str(current_dir)
    files = os.listdir(directory)
    doc = list(filter(lambda x: x[-5:] == '.json', files))


    # js_file = os.path.join(current_dir, 'request_17_02_2023.json')
    js_file = [os.path.join(current_dir, i) for i in doc if os.path.join(current_dir, i) != os.path.join(current_dir, 'data.json')]
    # print(js_file)
    if len(js_file) == 0:
        return None

    # Open the JSON file
    with open(js_file[0]) as json_file:
        data = json.load(json_file)

    # Access data
    # print(data['model']['record'][0])
    # for i in data['model']['record']:
    #     print(f"{i['date']} - {i['param']['data']} generate")
        # print(i['date'], i['param']['data'])

    year = [i['date'] for i in data['model']['record']]
    generate = [float(i['param']['data'].replace(',', '.')) if isinstance(i['param']['data'], str) else float(i['param']['data']) for i in data['model']['record']]
    # generate = [i['param']['data'] for i in data['model']['record']]

    # print(year)
    # print(generate)

    # Create a dictionary
    data = dict(zip(year, generate))

    # print(data)
    # print(float(data[2008].replace(',', '.')))

    for i in doc:
        os.remove(os.path.join(current_dir, i))

    # Write the JSON file
    with open('data.json', 'w') as json_file:
        json.dump(data, json_file)

main()