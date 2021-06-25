from datetime import date
from datetime import datetime
from datetime import timedelta
from numpy import *

class Timeline:

    date_end = None
    WeekList = None
    array = []

    def __init__(self, *args):
        date.fromisoformat('2019-12-04')
        self.length = 12
        self.height = 1
        self.array = []
        self.addLine()
        self.taskList = []
        self.WeekList = []
        if(len(args)>1):
            self.col_start = args[1]
        else:
            self.col_start = 4
        my_time = datetime.min.time()
        weekday = datetime.combine(args[0], my_time).weekday()
        firstWeekDay = args[0] - timedelta(days=weekday)
        self.WeekList = []
        for i in range(0, 12):
            self.WeekList.append([firstWeekDay, firstWeekDay+timedelta(days=6)])
            firstWeekDay += timedelta(days=7)

    def addLine(self):
        tmp = []
        for i in range(0, 12):
            tmp.append(0)
        self.array.append(tmp);

    def addTask(self, task):

        dic = {"phase": task}
        column = [-1, -1]
        for i in range(0, 12):
            if self.WeekList[i][0] <= task.Date_debut <= self.WeekList[i][1]:
                column[0] = i
            if self.WeekList[i][0] <= task.Deadline <= self.WeekList[i][1]:
                column[1] = i
        ok = None
        if column[0] > 0 and column[1] > 0:
            ok = True
        elif column[1] >= 0:
            column[0] = 0
            ok = True
        elif column[0] >= 0 and column[1] == -1:
            column[1] = 11
            ok = True
        else:
            ok = False

        if ok:
            j = -1
            in_place = False
            while not in_place:
                j += 1
                if j >= self.height:
                    self.height += 1
                    self.addLine()
                dic["line"] = "Line" + str(j+1);
                in_place = True
                for i in range(column[0]-1,column[1]):
                    if self.array[j][i] != 0:
                        in_place = False


            for i in range(column[0]-1, column[1]):
                self.array[j][i] = 1;

            dic["column"] = str(column[0] + (self.col_start)) + "/" + str(column[1] + (self.col_start+1))
            if task.State == "0":
                dic["state"] = "NotStart"
            elif task.State == "1":
                dic["state"] = "Progress"
            elif task.State == "2":
                dic["state"] = "Finish"
            self.taskList.append(dic)