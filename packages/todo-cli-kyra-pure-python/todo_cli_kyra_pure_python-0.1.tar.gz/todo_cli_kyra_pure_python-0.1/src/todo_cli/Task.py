# @Author : Kyra
# @Time : 2025/04/29,上午 09:34
# @Theme : 定义数据模型
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Task:
    id: int
    content: str
    done: bool = False
    priority: str = "low"
    tags: list = field(default_factory=lambda: ["study", "work"])
    created_at: datetime = field(default_factory=datetime.now)
    deadline: datetime = None

    '''
        field()和default_factory的使用：
            类的属性如果要赋一个默认初值，这个默认初值如果是不可变数据类型，例如bool，str等，直接赋值即可，
            所有对象共享同一个初值，共享同一片存储空间。如果初值是可变数据类型，例如列表/元组/字典等，或者是
            类的每个对象对该属性需要有不同的初值，需要有不同的存储空间，则需要field()和default_factory搭配使用。
            default_factory的值为一个无参的函数或方法。
        dataclasses模块用于自动为用户自定义的类添加生成的 特殊方法 例如 __init__() 和 __repr__()
    '''

'''
    為什麼要使用dataclasses？
        因為想對一些字段設置默認值，Python中一般有三種方式
        1、使用構造方法__init__中的參數列表為屬性指定默認值
        2、使用dataclasses模塊
        3、使用TypedDict
'''
