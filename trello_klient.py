import requests
import sys
# Параметры авторизации на trello.vom укажите свои при необходимости
auth_params = {
    'key': "b1093c52216984760496f2993eaf4a99",
    'token': "700980b75ad09996008e7dd291142a25852218060948b63516d8df51604223dc"}
base_url = "https://api.trello.com/1/{}"
# Необходим полный ID вашей доски на trello.com
board_id = "6128a5f32ca42e20a4e6e65e"

def read():
    column_data = requests.get(base_url.format('boards')+'/'+board_id+'/lists',params=auth_params).json()
    for column in column_data:
        task_data = requests.get(base_url.format('lists')+'/'+column['id']+'/cards',params=auth_params).json()
        print(column['name']+' (задач: '+str(len(task_data))+')')
       
        if not task_data:
            print('\t'+'Нет задач!')
            continue
        for task in task_data:
            print('\t'+task['name'])

def create(name, column_name):
    column_data = requests.get(base_url.format('boards')+'/'+board_id+'/lists',params=auth_params).json()
    for column in column_data:
        if column['name']==column_name:
            requests.post(base_url.format('cards'),data={'name':name,'idList':column['id'],**auth_params})
            break

def createColumn(column_name):
    column_data = requests.post(base_url.format('lists'),data={'name':column_name,'idBoard':board_id,**auth_params})

def move(name, column_name):
    column_data=requests.get(base_url.format('boards')+'/'+board_id+'/lists', params=auth_params).json()
    task_id = None
    tasks_to_move = []
    task_to_move = {}
    for column in column_data:
        column_tasks=requests.get(base_url.format('lists')+'/'+column['id']+'/cards',params=auth_params).json()
        for task in column_tasks:
            if task['name']==name:
                task_to_move = {
                'id': task['id'],
                'name': task['name'],
                'column': column['name'],
                'desc': task['desc']
                }
                tasks_to_move.append(task_to_move)
    if tasks_to_move:
        if len(tasks_to_move) == 1:
            task_id = tasks_to_move[0]['id']
            for column in column_data:
                if column['name'] == column_name:
                    requests.put(base_url.format('cards')+'/'+task_id+'/idList',data={'value':column['id'],**auth_params})
                    break
        else: print('Найдено несколько задач с таким именем.')
        for i in range(len(tasks_to_move)):
            print(i+1, tasks_to_move[i]['name'], tasks_to_move[i]['column'], 'описание: '+tasks_to_move[i]['desc'], sep='  ')
        num_task = int(input('Введите номер задачи для переноса: '))
        if 0 < num_task <= len(tasks_to_move):
            task_id = tasks_to_move[num_task - 1]['id']
            for column in column_data:
               if column['name'] == column_name:
                    requests.put(base_url.format('cards')+'/'+task_id+'/idList',data={'value':column['id'],**auth_params})
                    break
    else: print('Задача с таким именем не существует')


if __name__ =="__main__":
    if len(sys.argv) <= 2:
        read()
    elif sys.argv[1] == 'create':
        create(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'move':
        move(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'createcolumn':
        createColumn(sys.argv[2])


