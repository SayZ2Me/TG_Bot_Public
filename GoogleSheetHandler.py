import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import time

scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('Auth_Data.json', scope)
client = gspread.authorize(creds)

DataSheet = client.open("Telegram_Bot_Test")

ProjectData = DataSheet.get_worksheet(0)
UserData = DataSheet.get_worksheet(1)

def GetDate():
    date = datetime.datetime.now() + datetime.timedelta(hours=3)
    date = str(date.day)+'.'+str(date.month)+'.'+str(date.year)+' '+str(date.hour)+':'+str(date.minute)+':'+str(date.second)
    return date

def GetUserIds():
    return UserData.col_values(1)

def GetNameById(Id):
    ids = UserData.col_values(1)
    row = ids.index(str(Id)) + 1
    return UserData.cell(row,2).value
def AddUser(Id,name):
    ids = UserData.col_values(1)
    UserData.update_cell(len(ids)+1,1,Id)
    UserData.update_cell(len(ids)+1,2,name)
def GetProjects():
    return UserData.col_values(3)
def SetTask(user_id,project_name,task_name):
    date = GetDate()
    row_num = len(ProjectData.col_values(1)) + 1
    ProjectData.update_cell(row_num,1,date)
    user_name = GetNameById(user_id)
    ProjectData.update_cell(row_num,3,user_name)
    ProjectData.update_cell(row_num,4,project_name)
    ProjectData.update_cell(row_num,5,task_name)
    return row_num
def EndTask(row_num):
    date = GetDate()
    ProjectData.update_cell(row_num,2,date)
