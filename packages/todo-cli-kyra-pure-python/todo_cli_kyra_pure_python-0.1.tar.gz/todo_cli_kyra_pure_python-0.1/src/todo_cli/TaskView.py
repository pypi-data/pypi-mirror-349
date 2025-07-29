# @Author : Kyra
# @Time : 2025/04/29,下午 03:35
# @Theme :
from datetime import datetime

import click
import jieba
import matplotlib.pyplot as plt
from plyer import notification
from tabulate import tabulate
from wordcloud import WordCloud

from todo_cli.TaskService import TaskService

taskOperation = TaskService()


@click.command() # 將add函數註冊為cli命令組的子命令
@click.argument("content")  # 定義位置參數（必填）
@click.option("--done", type=bool, is_flag=True, default=False) # 定義可選參數（以--開頭）
@click.option("--priority", type=click.Choice(['low', 'medium', 'high']), default="low")
@click.option("--tags", default='study,work')
@click.option("--deadline", type=click.DateTime(formats=['%Y-%m-%d %H:%M']), default=None) # click库中的type属性具有转换数据类型的效果
def add(content, done, priority, tags, deadline):
    """添加任務"""
    if not content.strip():
        click.secho("content不能為空", fg='red')
        raise click.Abort()
    tags_list = [tag.strip() for tag in tags.split(",")]
    collections = {
        "content": content,
        "done": done,
        "priority": priority,
        "tags": tags_list,
        "deadline": deadline,
        "created_at": datetime.now()
    }
    try:
        taskOperation.add_task(**collections)
    except ValueError as e:
        click.secho(f"{e}", fg='red')
        raise click.Abort()
    click.secho(f"任務{content}添加成功", fg='green')


@click.command()
def list():
    """查看任務列表"""
    click.echo("待办事项如下：\n")
    tasks = taskOperation.list_tasks()
    try:
        formatted_list_tasks(tasks)
    except Exception as e:
        click.secho(e,fg='red')
        click.Abort()
    return tasks


def formatted_list_tasks(tasks):
    """将任务列表转换为美化后的表格字符串"""
    if not tasks:
        raise ValueError("当前没有任务")
    headers = ["id", "content", "done", "priority", "tags", "created_at", "deadline"]
    table_data = []
    for task in tasks:
        # 状态处理
        status = "√" if task.done else "×"
        status_color = "green" if task.done else "red"

        # 优先级颜色映射,这里{}中定义了一个匿名字典，用于获取任务优先级对应的颜色，如果没有值，则默认为白色
        priority_color = {
            "high": "red",
            "medium": "yellow",
            "low": "cyan"
        }.get(task.priority, "white")  # 添加默认值

        # datetime对象.strftime(format)用于格式化datetime对象，将其转换为一个日期时间字符串
        created_at = task.created_at.strftime("%Y-%m-%d %H:%M")
        deadline = task.deadline.strftime("%Y-%m-%d %H:%M") if task.deadline else "无"

        # 构建行数据
        row = [
            click.style(str(task.id), fg="bright_white"),
            task.content,
            click.style(task.priority, fg=priority_color),
            click.style(status, fg=status_color),
            task.tags,
            created_at,
            deadline
        ]
        table_data.append(row)
    click.secho(tabulate(table_data, headers=headers, tablefmt="fancy_grid",
                    colalign=("center", "center", "center", "center", "center", "center", "center")))


@click.command()
@click.argument("ids")
def delete(ids):
    """刪除任務"""
    try:
        id_list = [int(id.strip()) for id in ids.split(",")]
    except:
        click.secho("輸入的id不合法", fg='red')
        raise click.Abort()
    for id in id_list:
        try:
            taskOperation.delete_task(id)
            click.secho(f"id={id}的任務刪除成功", fg='green')
        except Exception as e:
            click.secho(e, fg='red')


@click.command()
@click.argument("id")
@click.option("--content", type=str)
@click.option("--done", type=bool, is_flag=True)
@click.option("--priority", type=click.Choice(['low', 'medium', 'high']))
@click.option("--tags")
@click.option("--deadline", type=click.DateTime(formats=['%Y-%m-%d %H:%M']))
def update(id, content, done, priority, tags, deadline):
    """編輯任務"""
    ctx = click.get_current_context()
    if tags:
        tags_list = [tag.strip() for tag in tags.split(",")]
    updates = {}
    if ctx.params['content']:
        updates['content'] = content
    if ctx.params['done']:
        updates['done'] = True
    if ctx.params['priority']:
        updates['priority'] = priority
    if ctx.params['tags']:
        updates['tags'] = tags_list
    if ctx.params["deadline"]:
        updates['deadline'] = deadline
    try:
        taskOperation.update_task(int(id), **updates)
    except Exception as e:
        click.secho(e, fg='red')
        raise click.Abort()
    click.secho(f"任務更新成功 id={id}", fg="green")


@click.command()
@click.argument("ids")
def flag_done(ids):
    """批量標記任務已完成"""
    try:
        id_list = [int(id.strip()) for id in ids.split(",")]
    except:
        click.secho("輸入的id不合法", fg='red')
        raise click.Abort()
    for id in id_list:
        try:
            taskOperation.flag_done(id)
            click.secho(f"id={id}的任務標記成功", fg='green')
        except Exception as e:
            click.secho(e, fg='red')


@click.command()
def priority_sort():
    """按照動態優先級排序"""
    sorted_tasks = taskOperation.priority_sort()
    click.echo("待办事项按優先級排序如下：\n")
    formatted_list_tasks(sorted_tasks)


@click.command()
@click.argument("due_within", type=int)
def deadline_notify(due_within):
    """任務截止時間提醒"""
    try:
        expiring_tasks = taskOperation.deadline_notify(due_within)
    except Exception as e:
        click.secho(e, fg='red')
        raise click.Abort()
    if expiring_tasks:
        for task in expiring_tasks:
            notification.notify(title="臨期任務提醒", message=f"{task.content}將在{due_within}小時內到期", timeout=5)
    else:
        click.secho(f"没有在{due_within}小时内到期的任务", fg='red')


@click.command()
@click.option("--path", default="tasks.csv")
def export_to_csv(path):
    """導出到CSV文件中"""
    taskOperation.export_to_csv(path)
    click.secho("CSV文件導出成功！", fg='green')


@click.command()
@click.argument("match_string")
@click.option("--threshold", default=80, type=click.IntRange(0,100))
def fuzzy_search(match_string, threshold):
    """內容模糊搜索"""
    try:
        match_tasks = taskOperation.fuzzy_search(match_string, threshold)
    except Exception as e:
        click.secho(e, fg='red')
    if match_tasks:
        print(formatted_list_tasks(match_tasks))
    else:
        click.secho("沒有匹配的任務", fg='red')


@click.command()
@click.option("--done", type=bool)
@click.option("--priority", type=click.Choice(['low', 'medium', 'high']))
@click.option("--tags")
@click.option("--create_start", type=click.DateTime(formats=['%Y-%m-%d %H:%M']))
@click.option("--create_end", type=click.DateTime(formats=['%Y-%m-%d %H:%M']))
@click.option("--deadline_start", type=click.DateTime(formats=['%Y-%m-%d %H:%M']))
@click.option("--deadline_end", type=click.DateTime(formats=['%Y-%m-%d %H:%M']))
def filter(done, priority, tags, create_start, create_end, deadline_start, deadline_end):
    """多條件過濾"""
    conditions = {}
    if done in [False, True]:
        conditions['done'] = done
    if priority:
        conditions['priority'] = priority
    if tags:
        conditions['tags'] = [tag.strip() for tag in tags.split(",")]
    if create_start:
        conditions['create_start'] = create_start
    if create_end:
        conditions['create_end'] = create_end
    if deadline_start:
        conditions['deadline_start'] = deadline_start
    if deadline_end:
        conditions['deadline_end'] = deadline_end
    filter_tasks = taskOperation.filter(**conditions)
    if filter_tasks:
        formatted_list_tasks(filter_tasks)
    else:
        click.secho("没有符合条件的任务",fg='red')

@click.command()
@click.argument("dimension")
def statistics(dimension):
    """數據統計 優先級分佈/任務完成情況/類別分佈/文本分析"""
    if dimension in ['priority','completion_status','category']:
        try:
            labels, sizes = taskOperation.statistics(dimension)
        except Exception as e:
            click.secho(e,fg='red')
        plt.rcParams['font.sans-serif'] = 'SimHei'
        plt.pie(sizes,labels=labels)
        plt.axis('equal')
        plt.show()
    elif dimension == 'text_analysis':
        # 生成詞雲圖
        text = taskOperation.statistics(dimension)
        # 生成词云（需指定中文字体路径，如 simhei.ttf）
        wordcloud = WordCloud(
            # 定義字體路徑
            font_path="C:\Windows\Fonts\Arvo-Regular.ttf",  # 替换为你的中文字体路径
            width=800,
            height=400,
            background_color="white",
            max_words=50,
        ).generate_from_frequencies(text)
        # 显示并保存
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.show()
        wordcloud.to_file("chinese_wordcloud.png")