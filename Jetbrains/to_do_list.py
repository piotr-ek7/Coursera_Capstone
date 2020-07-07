from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    today = datetime.today()
    deadline = Column(Date)
    Session = sessionmaker(bind=engine)
    session = Session()

    def __repr__(self):
        return "{}".format(self.task)

    def add_task(self, task, deadline):
        new_row = Table(task=task, deadline=datetime.strptime(deadline, '%Y-%m-%d')
                        if deadline.strip() else self.today)
        self.session.add(new_row)
        self.session.commit()
        print('The task has been added!\n')

    def show_today_task(self):
        rows = self.session.query(Table).filter(Table.deadline == self.today.date()).all()
        print("{} {} {}:".format('Today', self.today.day, self.today.strftime('%b')))
        if len(rows) != 0:
            id_task = 0
            for row in rows:
                id_task += 1
                print("{}. {}".format(id_task, row))
            print("")
        else:
            print("Nothing to do!\n")

    def show_week_task(self):
        for shift_day in range(7):
            given_day = self.today + timedelta(days=shift_day)
            rows = self.session.query(Table).filter(Table.deadline == given_day.date()).all()
            print("{} {} {}:".format(given_day.strftime('%A'), given_day.day, given_day.strftime('%b')))
            if len(rows) != 0:
                id_task = 0
                for row in rows:
                    id_task += 1
                    print("{}. {}".format(id_task, row))
                print("")
            else:
                print("Nothing to do!\n")

    def show_all_task(self, text_printed="All tasks:"):
        rows = self.session.query(Table).order_by(Table.deadline).all()
        print(text_printed)
        if len(rows) != 0:
            id_task = 0
            mapping_id = {}
            for row in rows:
                id_task += 1
                mapping_id[str(id_task)] = row.id
                print("{}. {}. {} {}".format(id_task, row, row.deadline.day, row.deadline.strftime('%b')))
            print("")
        else:
            print("Nothing to do!\n")
        return mapping_id


    def delete_task(self):
        show_all = self.show_all_task("Chose the number of the task you want to delete:")
        self.session.query(Table).filter(Table.id == show_all[input()]).delete()
        self.session.commit()
        print("The task has been deleted!\n")

    def missing_task(self):
        rows = self.session.query(Table).filter(Table.deadline < self.today.date()).order_by(Table.deadline).all()
        print("Missed tasks:")
        if len(rows) != 0:
            id_task = 0
            for row in rows:
                id_task += 1
                print("{}. {}. {} {}".format(id_task, row, row.deadline.day, row.deadline.strftime('%b')))
            print("")
        else:
            print("Nothing to do!\n")

Base.metadata.create_all(engine)
user_input = ''
assignment = Table()

while user_input != '0':
    user_input = input("1) Today's tasks\n2) Week's tasks\n3) All tasks\n"
                       "4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit\n")
    if user_input == '1':
        assignment.show_today_task()
    elif user_input == '2':
        assignment.show_week_task()
    elif user_input == '3':
        assignment.show_all_task()
    elif user_input == '4':
        assignment.missing_task()
    elif user_input == '5':
        assignment.add_task(input('Enter task\n'), input('Enter deadline\n'))
    elif user_input == '6':
        assignment.delete_task()
    elif user_input == '0':
        print('Bye!')
    else:
        print('Incorrect input')
