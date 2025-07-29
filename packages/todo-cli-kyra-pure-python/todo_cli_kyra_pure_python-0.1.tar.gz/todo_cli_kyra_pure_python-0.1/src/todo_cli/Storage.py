# @Author : Kyra
# @Time : 2025/04/29,上午 10:15
# @Theme :
import json
import os.path
from dataclasses import asdict
from datetime import datetime
from json import JSONDecodeError
from pathlib import Path

from todo_cli.Task import Task


# 實現json文件的讀寫

class Storage:

    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.next_id = 1

    def load_tasks(self) -> list[Task]:
        # 讀數據 並把[dict1,dict2,...] ----> [task1,task2,...]
        object_tasks = []
        try:
            with open(self.file_path, 'r', encoding="UTF-8") as f:
                tasks = json.load(f)
                for ele in tasks:
                    task = Task(1, "default")
                    task.id = ele['id']
                    try:
                        task.content = ele['content']
                    except:
                        print("error")
                        continue
                    # item.get("key",default)和item['key']类似，都可以通过字典的key访问value.
                    # 区别在于get获取的key不存在时会返回默认值，而[]获取的key不存在时会直接报错
                    task.done = ele['done']
                    task.priority = ele["priority"]
                    task.tags = ele['tags']
                    if ele['deadline']:
                        # strptime()将字符串按照指定格式解析为datetime类型的对象
                        task.deadline = datetime.strptime(ele['deadline'], "%Y-%m-%d %H:%M")
                    if ele['created_at']:
                        task.created_at = datetime.strptime(ele['created_at'], "%Y-%m-%d %H:%M")
                    object_tasks.append(task)
                return object_tasks
        except FileNotFoundError:  # 文件不存在
            self.file_path.touch()
            return []
        except JSONDecodeError:  # 文件內容為空或者內容不是有效的json格式
            '''
                什麼叫有效的json格式：
                1、頂層結構通常是一個對象{}或者數組[]
                2、對象和數組可以任意嵌套
                3、細節
                    對象的key必須用雙引號包裹
                    字符串值必須用雙引號
                    最尾部不能有逗號，文件不能包含注釋
            '''
            return []

    def save_tasks(self, tasks):
        # 存數據  並把[task1,task2,...]  ----> [dict1,dict2,...]
        dict_tasks = []
        if not os.path.exists(self.file_path):
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            self.file_path.touch()
        with open(self.file_path, 'w', encoding="UTF-8") as f:
            for ele in tasks:
                if not hasattr(ele, "content") or not ele.content:
                    print(f"警告：content為空或content屬性不存在{ele.id}")
                    continue
                task = asdict(ele)
                task['created_at'] = ele.created_at.strftime('%Y-%m-%d %H:%M')
                if ele.deadline:
                    task['deadline'] = ele.deadline.strftime('%Y-%m-%d %H:%M')
                dict_tasks.append(task)
            json.dump(dict_tasks, f, indent=4)
            return tasks

    def load_tasks_data(self):
        try:
            with open(self.file_path, 'r', encoding="UTF-8") as f:
                tasks_data = json.load(f)
                return tasks_data
        except FileNotFoundError:  # 文件不存在
            self.file_path.touch()
            return None
        except JSONDecodeError:  # 文件內容為空
            return None
