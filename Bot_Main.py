from telegram import InlineKeyboardButton, InlineKeyboardMarkup,Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler,CallbackContext,Updater,Filters,MessageHandler

import GoogleSheetHandler as SheetHandler
from datetime import timedelta  
import time

TG_Token = '777041716:AAF9R2Kum6YvZ0wra8O5qRAtF0z4Ifl8S1k'

unregistred_pool=[]

selected_project_data={}

def button(update, context):
    _id = str(update.callback_query.message.chat.id)
    
    if(str(update.callback_query.data)=='Done_btn'):
        
        SheetHandler.EndTask(selected_project_data.get(str(_id))[1])
        
        keyboard = []
        projects = SheetHandler.GetProjects()
        for i in range(1,len(projects)):
            keyboard.append([InlineKeyboardButton(projects[i], callback_data=projects[i])])

        reply_markup = InlineKeyboardMarkup(keyboard)

        update.callback_query.edit_message_text(text="Я смотрю вы освободились, значит пора приступать к следующей задаче!\nВот тебе список проектов, выбирай.")
        update.callback_query.edit_message_reply_markup(reply_markup=reply_markup)
        return None
    if(str(update.callback_query.data)=='Pause_btn'):
        SheetHandler.EndTask(selected_project_data.get(_id)[1])
        
        keyboard = []
        projects = SheetHandler.GetProjects()
        
        keyboard.append([InlineKeyboardButton('Продолжить.', callback_data='Resume_btn')])

        reply_markup = InlineKeyboardMarkup(keyboard)

        update.callback_query.edit_message_text(text="Вы поставили на паузу время выполнения задания.")
        update.callback_query.edit_message_reply_markup(reply_markup=reply_markup)
        return None
    if(str(update.callback_query.data)=='Resume_btn'):

        text = selected_project_data.get(_id)[2]
        
        selected_project_data.update({_id : [str(selected_project_data.get(str(_id))[0]),SheetHandler.SetTask(str(_id),str(selected_project_data.get(str(_id))[0]),str(text)),str(text),selected_project_data.get(str(_id))[3]]})
        
        keyboard = []
        
        keyboard.append([InlineKeyboardButton('Завершить задачу.', callback_data='Done_btn')])

        keyboard.append([InlineKeyboardButton('Пауза.', callback_data='Pause_btn')])

        reply_markup = InlineKeyboardMarkup(keyboard)

        update.callback_query.edit_message_text(text="Как только завершишь задачу, жми на кнопку.")
        update.callback_query.edit_message_reply_markup(reply_markup=reply_markup)
        return None
    else:
        selected_project_data[_id] = [str(update.callback_query.data),0,'',0]
        print('Query data: '+str(update.callback_query.data))
        print('Selected projects data'+str(selected_project_data))
        update.callback_query.edit_message_text(text="И какую задачу в проекте \"{}\" вы решились сделать?".format(update.callback_query.data))

def message_handler (update, context):
    if(update.effective_user.id in unregistred_pool):
        SheetHandler.AddUser(update.effective_user.id,update.message.text)
        unregistred_pool.pop(unregistred_pool.index(update.effective_user.id))
        print('Unregistred ids: '+str(unregistred_pool))
        update.message.reply_text(text = 'Добро пожаловать на Небеса, ' + str(SheetHandler.GetNameById(update.effective_user.id)) + '. \nКоманда /help в помошь.')
        _projects(update, context)
    if(selected_project_data.get(str(update.effective_user.id))!=None):
        print('Project task started')
        selected_project_data.update({str(update.effective_user.id) : [str(selected_project_data.get(str(update.effective_user.id))[0]),SheetHandler.SetTask(str(update.effective_user.id),str(selected_project_data.get(str(update.effective_user.id))[0]),str(update.message.text)),str(update.message.text),time.time()]})
        print(selected_project_data)
        update.message.reply_text('Шикарно, ' + str(update.message.text) + ' в проекте \"' + str(selected_project_data.get(str(update.effective_user.id))[0]) + '\", поехали!')
        update.message.reply_text('Кстати, дедлайн был вчера. Продуктивной работы!')
        keyboard = []
        
        keyboard.append([InlineKeyboardButton('Завершить задачу.', callback_data='Done_btn')])

        keyboard.append([InlineKeyboardButton('Пауза.', callback_data='Pause_btn')])

        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text('Как только завершишь задачу, жми на кнопку.', reply_markup=reply_markup)
    
def _start(update, context):
    
    ids = SheetHandler.GetUserIds()
    
    if (str(update.effective_user.id) in ids):
        print('User name : ' + str(SheetHandler.GetNameById(update.effective_user.id))+' connected')
        update.message.reply_text(text = 'Добро пожаловать на Небеса!')
        _projects(update,context)
    else:
        update.message.reply_text(text = 'Введите имя и фамилию для добавления в базу данных.')
        if(not update.effective_user.id in unregistred_pool):
            unregistred_pool.append(update.effective_user.id)
            print('Unregistred ids: '+str(unregistred_pool))
def _help(update, context):
        update.message.reply_text(text = 'Команды:\n/help Список команд\n/projects Выбор проекта\n/...')
def _projects(update, context):
    keyboard = []
    projects = SheetHandler.GetProjects()
    for i in range(1,len(projects)):
        keyboard.append([InlineKeyboardButton(projects[i], callback_data=projects[i])])

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Над каким проектом сегодня трудимся?', reply_markup=reply_markup)
def main():
    updater = Updater(token = TG_Token, use_context = True)
    updater.dispatcher.add_handler(CommandHandler('start', _start))
    updater.dispatcher.add_handler(CommandHandler('help', _help))
    updater.dispatcher.add_handler(CommandHandler('projects', _projects))
    updater.dispatcher.add_handler(MessageHandler(filters=Filters.all,callback=message_handler))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.start_polling()

    print('Bot connected to telegram.')
    print('Token - {}'.format(TG_Token))
    print('Request handling started.')
    
    updater.idle()
    
if __name__ == '__main__':
    main()

