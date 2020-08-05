# Write your code here
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime

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
    list_tasks = session.query(Table).all()
    if len(list_tasks) == 0:
        print('Nothing to do!')
    else:
        for i in range(len(list_tasks)):
            print(list_tasks[i])
    print()
    menu()


def add_task():
    print("Enter task")
    new_task = input(' ')
    new_row = Table(task=new_task, deadline=datetime.strptime('08-05-2020', '%m-%d-%Y').date())
    session.add(new_row)
    session.commit()
    print('The task has been added!')

    menu()


def menu():
    print('1) Today\'s tasks')
    print('2) Add task')
    print('0) Exit')

    user_option = input(' ')
    if user_option == '1':
        today_tasks()
    elif user_option == '2':
        add_task()
    else:
        print('Bye!')
        exit()


menu()
