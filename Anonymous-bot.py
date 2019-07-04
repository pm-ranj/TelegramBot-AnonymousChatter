import logging

from telegram.ext import Updater, Dispatcher, CommandHandler, MessageHandler, Filters
CURRENT_CHATS = {}
def logUserRegister(id, username, first, last):
    with open('accounts.txt', 'a') as fi:
        name = str(first)
        if last != None:
            name = name + " " + str(last)
        inFile = str(username) + " -- " + name + " -- " + str(id) + '\n'
        fi.write(inFile)
        fi.close()


def createUserFile(userId):
    if userId != None:
        file = str(userId) + ".txt"
        with open(file, 'a') as f:
            f.close()
            return True

    else:
        return False

def isRegistered(userId):
    with open("users.txt", "r") as f:
        users = f.readlines()
        for usr in users:
            u = usr.split('.')
            if str(userId) == u[0]:
                createUserFile(userId)
                f.close()
                return True
    return False

def addToUsers(userId):
    if userId == None:
        return False
    with open('users.txt', 'a') as f:
        f.write(str(userId)+'.\n')
        f.close()
        return True

def start(bot, update, args):

    username = update.message.from_user.username
    userId = update.message.from_user.id
    chatId = update.message.chat_id
    try:
        arglist = args[0].split('_')

        CURRENT_CHATS[userId] = arglist[0]
        START_MESSAGE = f"Hello there! \n " \
                        f"you are now in anonymous chat with {arglist[1]}. \n" \
                        f"from now every message you send will go to his/her inbox\n" \
                        f"you can use this features by /register"

        bot.send_message(chat_id=chatId, text=START_MESSAGE)
        return

    except IndexError:
        bot.send_message(chat_id=chatId,text="welcome to anonymous chatter \n"
                                             "you can register your self for getting anonymous messages by /register")



def register(bot, update):
    userId = update.message.from_user.id
    name = update.message.from_user.first_name
    username = update.message.from_user.username
    chatId = update.message.chat_id
    lastname = update.message.from_user.last_name

    if userId == None:
        bot.send_message(chat_id=chatId, text="ERROR: \nYou must have a username to register")

    else:
        if isRegistered(userId):
            bot.send_message(chat_id=chatId, text="you've already registered!\n your share link is:\n"
                                                  f"t.me/AnonymousChatterBot?start={userId}_{name}")
        else:
            addToUsers(userId)
            logUserRegister(userId, username, name, lastname)
            bot.send_message(chat_id=chatId, text="you successfully registered \n  " +
                                              "your share link is: \n" +
                                              "your share link is: \n" +
                                              f"t.me/AnonymousChatterBot?start={userId}_{name} \n" +
                                              "now the world can chat with you anonymously via your link")




def inbox(bot, update):

    username = update.message.from_user.username
    userId = update.message.from_user.id
    chatId = update.message.chat_id

    if isRegistered(userId):
        fileName = str(userId)+ ".txt"
        with open(fileName, "r") as f:
            st = f.read()
            if st == "":
                bot.send_message(chat_id=chatId, text="your inbox is empty")
            else:
                bot.send_message(chat_id=chatId, text=st)
            f.close()
    else:
        bot.send_message(chat_id=chatId, text="you have not registered yet! \nregister yourself by /register")

def endChat(bot, update):
    userId = update.message.from_user.id

    username = update.message.from_user.username
    chatId = update.message.chat_id
    if CURRENT_CHATS[userId] != None:
        bot.send_message(chat_id=chatId, text=f"your anonymous chat has been ended")
        CURRENT_CHATS[userId] = None
    else:
        bot.send_message(chat_id=chatId, text="you are not in an anonymous chat to end")


def messageHandler(bot, update):
    userId = update.message.from_user.id


    messageText = update.message.text
    username = update.message.from_user.username
    name = update.message.from_user.first_name
    chatId = update.message.chat_id
    receiverId = None

    try:
        receiverId = CURRENT_CHATS[userId]
    except:
        pass


    if receiverId != None:
        if receiverId == str(userId):
            bot.send_message(chat_id=chatId, text="opssie!! \nyou can not be anonymous to yourself \n/end it now!")
            return

        filename = str(receiverId) + ".txt"

        bot.send_message(chat_id=chatId, text=f"your highly anonymous message sent  ;) ")
        with open(filename, "a") as f:
            toFileText = "\n \n************************************** \n" + \
                         "   id: " + str(username) + \
                         " | name: " + str(update.message.from_user.first_name) + \
                         " | lastname: " + \
                         str(update.message.from_user.last_name) + "\n\n  " + str(messageText)

            f.write(toFileText)
            f.close()
    else:
        bot.send_message(chat_id=chatId, text="why are you sending messages? nobody gonna receive that!\n"
                                              "make sure you enter this bot by a 'share link' ")




def main():
    yourTokenFile = 'token.txt'

    with open(yourTokenFile) as f:
        token = f.readline()
        
    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    startHandler = CommandHandler('start', start, pass_args=True)
    registerHandler = CommandHandler('register', register)
    inboxHandler = CommandHandler('inbox', inbox)
    endChatHandler = CommandHandler('end', endChat)
    msgHandler = MessageHandler(Filters.text, callback=messageHandler)
    dispatcher.add_handler(startHandler)
    dispatcher.add_handler(registerHandler)
    dispatcher.add_handler(inboxHandler)
    dispatcher.add_handler(endChatHandler)
    dispatcher.add_handler(msgHandler)
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    updater.start_polling()
    updater.idle()



if __name__ == '__main__':
    main()