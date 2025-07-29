# @Author : Kyra
# @Time : 2025/04/29,下午 03:35
# @Theme :
import csv
from collections import Counter
from datetime import datetime

import jieba
from fuzzywuzzy import fuzz

from todo_cli.Storage import Storage
from todo_cli.Task import Task


class TaskService:
    # 使用構造函數，避免硬編碼，支持外部傳入storage實例
    def __init__(self, storage=None):
        self.storage = storage or Storage("tasks.json")

    def add_task(self, **collections):
        tasks = self.storage.load_tasks()
        # 获得新任务的id
        try:
            self.storage.next_id = max([task.id for task in tasks]) + 1
        except:
            self.storage.next_id = 1
        # 处理任务内容重复
        for task in tasks:
            if task.content.strip() == collections['content']:
                raise ValueError(f"任務已存在:{collections['content']}")
        if not collections['content']:
            raise ValueError("任務內容不能為空")
        if type(collections['done']) != bool:
            raise ValueError("完成狀態類型不合法")
        if collections['priority'] not in ['low', 'medium', 'high']:
            raise ValueError("priority值不合法，需要在'low', 'medium', 'high'中")
        if type(collections['tags']) != list:
            raise ValueError("tags數據類型不合法，需要為list類型")
        if type(collections['created_at']) != datetime:
            raise ValueError("created_at需要為datetime類型")
        if collections['deadline'] and type(collections['deadline']) != datetime:
            raise ValueError("deadline需要為datetime類型")
        if collections['deadline'] and collections['deadline'] <= datetime.now():
            raise ValueError("截截止時間不能早于當前時間")
        if len(collections['content']) > 50:
            raise ValueError("內容過長，不能超過50個字符")
        new_task = Task(
            self.storage.next_id,
            collections['content'],
            collections['done'],
            collections['priority'],
            collections['tags'],
            collections['created_at'],
            collections['deadline']
        )
        tasks.append(new_task)
        self.storage.save_tasks(tasks)
        return new_task

    def list_tasks(self):
        tasks = self.storage.load_tasks()
        return tasks

    def delete_task(self, id):
        tasks = self.storage.load_tasks()
        task = self.search_by_id(id)
        if task:
            tasks.remove(task)
            self.storage.save_tasks(tasks)
            return True
        else:
            raise ValueError(f"不存在任務 id={id}")

    def search_by_id(self, id):
        tasks = self.storage.load_tasks()
        for task in tasks:
            if task.id == id:
                return task
        else:
            raise ValueError("待查找的id不存在")

    def update_task(self, id, **updates):
        tasks = self.storage.load_tasks()
        for task in tasks:
            if task.id==id:
                # 遍历 updates 中的每个字段
                for k, v in updates.items():
                    # 内置函数hasattr(obj,"attribute_name") 用于检查对象是否拥有指定属性
                    if hasattr(task, k):
                        # 特殊处理时间字段，内置函数isinstance(object, classinfo)用于检查一个对象是否是一个类的实例
                        if k == "deadline" and isinstance(v, str):
                            # 内置函数setattr(object, attribute_name, value)用于动态设置对象属性
                            setattr(task, k, datetime.fromisoformat(v))
                        else:
                            setattr(task, k, v)
                    else:
                        raise ValueError(f"无效字段：{k}")
                self.storage.save_tasks(tasks)
                return True
        raise ValueError(f"要更新的任務不存在")

    def flag_done(self, id):
        tasks = self.storage.load_tasks()
        task = self.search_by_id(id)
        if task:
            for item in tasks:
                if id == item.id:
                    item.done = True
        else:
            raise ValueError(f"id為{id}的任務不存在")
        self.storage.save_tasks(tasks)

    def priority_sort(self):
        tasks = self.storage.load_tasks()
        coefficient = {"high": 0.8, "medium": 0.5, "low": 0.2}
        expired_tasks = []
        dynamic_priority = {}
        for task in tasks:
            # 計算每個任務的權重，並按照權重排序 dynamic_prio = priority * 0.6 + 剩餘時間係數 * 0.4
            # 這裡計算出每個task的剩餘時間係數
            try:
                delta = (task.deadline - datetime.now()).days
            except:
                delta = 9999  # 如果deadline為空，將delta設置為一個較大值，默認此任務不緊急
            if delta >= 7:
                remain_time = 0
            elif delta <= 0:
                remain_time = 1
            else:
                remain_time = delta / 7
            dynamic_priority[task.id] = coefficient[task.priority] * 0.6 + remain_time * 0.4
        sorted_task_id = sorted(dynamic_priority, key=dynamic_priority.get, reverse=True)
        sorted_tasks = [self.search_by_id(id) for id in sorted_task_id]
        return sorted_tasks

    def deadline_notify(self, due_within):
        tasks = self.storage.load_tasks()
        expiring_tasks = []
        if type(due_within) != int or due_within < 0:
            raise ValueError(f"輸入的due_within不合法")
        for task in tasks:
            if task.deadline:
                if 0 < (task.deadline - datetime.now()).seconds / 3600 + (
                        task.deadline - datetime.now()).days * 24 < due_within:
                    expiring_tasks.append(task)
        return expiring_tasks

    def export_to_csv(self, path):
        tasks_data = self.storage.load_tasks_data()

        # 获取所有可能的列名
        fieldnames = set()
        for item in tasks_data:
            fieldnames.update(item.keys())
        fieldnames = sorted(fieldnames)
        # 写入CSV文件
        with open(path, 'w', encoding='utf-8', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for item in tasks_data:
                writer.writerow(item)

    def fuzzy_search(self, match_string, threshold):
        tasks = self.storage.load_tasks()
        if not match_string:
            raise ValueError("匹配串不能為空")
        if not 0 <= threshold <= 100 or type(threshold) != int:
            raise ValueError("閾值类型为整型且範圍在0-100")
        match_tasks = []
        for task in tasks:
            if fuzz.partial_ratio(task.content, match_string) >= threshold:
                match_tasks.append(task)
        return match_tasks

    def filter(self, **conditions):
        tasks = self.storage.load_tasks()
        filter_tasks = []
        condition_count = len(conditions)
        for ele in conditions.keys():
            if not hasattr(Task, ele):
                condition_count -= 1
                raise ValueError(f"無效字段{ele}")
        for task in tasks:
            count = 0
            if "done" in conditions.keys() and task.done == conditions['done']:
                count += 1
            if "priority" in conditions.keys() and task.priority == conditions['priority']:
                count += 1
            if "tags" in conditions.keys() and task.tags == conditions['tags']:
                count += 1
            if "create_start" in conditions.keys() and task.created_at > conditions['create_start']:
                count += 1
            if "create_end" in conditions.keys() and task.created_at < conditions['create_end']:
                count += 1
            if "deadline_start" in conditions.keys() and task.deadline > conditions['deadline_start']:
                count += 1
            if "deadline_end" in conditions.keys() and task.deadline < conditions['deadline_end']:
                count += 1
            if condition_count == count:
                filter_tasks.append(task)
        return filter_tasks

    def statistics(self, dimension):
        # 優先級分佈/任務完成情況/類別分佈 : 餅狀圖  matplotlib庫
        # 文本分析 : 詞雲圖  word-cloud庫
        if dimension == 'priority':
            return self.priority_statistics()
        if dimension == 'completion_status':
            return self.completion_status_statistics()
        if dimension == 'category':
            return self.category_statistics()
        if dimension == 'text_analysis':
            return self.text_analysis()

    def priority_statistics(self):
        counts = [0, 0, 0]
        tasks = self.storage.load_tasks()
        for task in tasks:
            if task.priority == 'high':
                counts[0] += 1
            if task.priority == 'medium':
                counts[1] += 1
            if task.priority == 'low':
                counts[2] += 1
        sizes = [count / len(tasks) for count in counts]
        labels = [f'high {sizes[0]}', f'medium {sizes[1]}', f'low {sizes[2]}']
        return labels, sizes

    def completion_status_statistics(self):
        counts = [0, 0]
        tasks = self.storage.load_tasks()
        for task in tasks:
            if task.done == False:
                counts[0] += 1
            if task.done == True:
                counts[1] += 1
        sizes = [count / len(tasks) for count in counts]
        labels = [f'未完成 {sizes[0]}', f'已完成 {sizes[1]}']
        return labels, sizes

    def category_statistics(self):
        category_dict = {}
        tasks = self.storage.load_tasks()
        for task in tasks:
            task.tags = str(task.tags)
            if task.tags not in category_dict:
                category_dict[task.tags] = 1
            else:
                category_dict[task.tags] += 1
        labels = [tags for tags in category_dict.keys()]
        sizes = [size / len(tasks) for size in category_dict.values()]
        return labels, sizes

    def text_analysis(self):
        tasks = self.storage.load_tasks()
        # 合并所有任务内容,str.join(iterable)方法是將可迭代對象的每一個元素由str串聯起來
        text = " ".join([task.content for task in tasks])
        # 中文分词：將文本分割為詞語列表，因此中文文本詞語之間沒有顯式的間隔
        words = (jieba.lcut(text))
        # 統計詞頻，生成一個字典  {詞語：出現次數，詞語：出現次數，...}
        word_counts = Counter(words)

        # 过滤停用词
        stopwords = set(["的", "了", "在", "是", "我"])
        # 生成一個排除掉停用詞的詞頻字典
        filtered = {k: v for k, v in word_counts.items() if k not in stopwords}
        return filtered