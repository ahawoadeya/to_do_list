# Write your code here
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def today_tasks():
    today = datetime.today()
    list_tasks = session.query(Table).filter(Table.deadline == today.date()).all()
    if len(list_tasks) == 0:
        print('Today {} {}:'.format(today.day, today.strftime('%b')))
        print('Nothing to do!')
    else:
        for i in range(len(list_tasks)):
            print(list_tasks[i])
    print()

    menu()


def add_task():
    print("Enter task")
    new_task = input(' ')
    print('Enter deadline')
    n_year, n_month, n_day = input(' ').split("-")
    new_deadline = datetime(int(n_year), int(n_month), int(n_day))
    new_row = Table(task=new_task, deadline=new_deadline)
    session.add(new_row)
    session.commit()
    print('The task has been added!')

    menu()


def week_tasks():
    for day in range(7):
        date = datetime.today().date() + timedelta(days=day)
        list_tasks = session.query(Table).filter(Table.deadline == date).all()
        print(date.strftime('%A %d %b') + ':')
        if len(list_tasks) == 0:
            print('Nothing to do!')
        else:
            for every_task in range(len(list_tasks)):
                print(f'{every_task + 1}. {list_tasks[every_task].task}')
        print()

    menu()


def total_tasks():
    list_tasks = session.query(Table.task, Table.deadline).order_by(Table.deadline).all()
    print('All tasks:')
    for every_task in range(len(list_tasks)):
        print(f'{every_task + 1}. {list_tasks[every_task][0]}. {list_tasks[every_task][1].strftime("%d %b")}')
    print()
    menu()


def menu():
    print('1) Today\'s tasks')
    print('2) Week\'s tasks')
    print('3) All tasks')
    print('4) Add task')
    print('0) Exit')

    user_option = input(' ')
    if user_option == '1':
        today_tasks()
    elif user_option == '2':
        week_tasks()
    elif user_option == '3':
        total_tasks()
    elif user_option == '4':
        add_task()
    else:
        print('Bye!')
        exit()


menu()
