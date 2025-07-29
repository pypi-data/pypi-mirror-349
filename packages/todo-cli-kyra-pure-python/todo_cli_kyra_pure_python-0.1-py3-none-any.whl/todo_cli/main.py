# @Author : Kyra
# @Time : 2025/04/29,下午 03:44
# @Theme :
import click

from todo_cli import TaskView


@click.group()  # 裝飾器：定義一個命令組，命令组的名字叫cli
def cli():  # 命令入口
    """命令行待办事项工具"""
    pass

# 將現有命令註冊為子程序
cli.add_command(TaskView.add)
cli.add_command(TaskView.list)
cli.add_command(TaskView.delete)
cli.add_command(TaskView.update)
cli.add_command(TaskView.flag_done)
cli.add_command(TaskView.priority_sort)
cli.add_command(TaskView.deadline_notify)
cli.add_command(TaskView.export_to_csv)
cli.add_command(TaskView.fuzzy_search)
cli.add_command(TaskView.filter)
cli.add_command(TaskView.statistics)

if __name__ == "__main__":
    cli()  # 調用cli命令組，解析用戶輸入的命令行參數，並觸發對應的子命令函數
