import datetime
import diff
import telebot
import control_db
# TODO: перечитать код
import stock
import stock_helper
from constants import *
from make_plot import make_plot
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from threading import Thread


# for scheduled notifications
def run_scheduled_task():
    rows = control_db.get_all()
    print("I am running")

    for v in rows:
        user_id = v[0]
        securities = stock.get_companies(user_id)
        last_date = datetime.strptime(v[2], "%y-%m-%d-%H-%M-%S")
        Text = "Изменение цен акций с последнего момента\n"
        for security in securities:
            x = diff.get_difference(security, last_time=last_date, current_time=datetime.today())
            additional = ""
            if x[2] >= 0:
                additional = f"(+{x[2]:0.2f} {ruble}, ↑{x[3]:0.2f}%)"
            else:
                additional = f"(-{abs(x[2]):0.2f} {ruble}, ↓{x[3]:0.2f}%)"
            Text += f"{security}  {x[0]} {ruble} ⟶ {x[1]} {ruble} <b>{additional}</b>\n"
        control_db.update_user_date(user_id, datetime.now().strftime("%y-%m-%d-%H-%M-%S"))
        bot.send_message(user_id, Text, parse_mode="HTML")


control_db.before_start()

bot = telebot.TeleBot(token)

scheduler = BlockingScheduler(
    timezone="Europe/Moscow")  # You need to add a timezone, otherwise it will give you a warning
scheduler.add_job(run_scheduled_task, "cron", hour=9, minute=30)
scheduler.add_job(run_scheduled_task, "cron", hour=16, minute=0)
scheduler.add_job(run_scheduled_task, "cron", hour=22, minute=0)


def schedule_checker():
    while True:
        scheduler.start()


Thread(target=schedule_checker).start()  # Notice that you refer to schedule_checker function which starts the job


# main part

@bot.message_handler(commands=['add'])
def add_company(message):
    bot.reply_to(message, choose_company_txt)
    bot.register_next_step_handler(message, add_on_click)


def add_on_click(message):
    company = message.text
    if stock.already_in(message.from_user.id, company):
        bot.send_message(message.chat.id, company_in_list_txt)
    else:
        result = stock.add_company(message.from_user.id, company)
        if result:
            bot.send_message(message.chat.id, company_successfully_added_txt)
        else:
            bot.send_message(message.chat.id, company_not_exist_txt)


@bot.message_handler(commands=['list'])
def show_companies(message):
    companies = stock.get_companies(message.from_user.id)
    Text = ""
    if len(companies) == 0:
        Text = empty_list_txt
    else:
        Text = list_following_companies_txt + "\n"
        for v in companies:
            Text += (str(v) + "\n")
    bot.send_message(message.chat.id, text=Text)


@bot.message_handler(commands=['delete'])
def delete_company(message):
    bot.reply_to(message, choose_company_txt)
    bot.register_next_step_handler(message, delete_on_click)


def delete_on_click(message):
    result = stock.delete_company(message.from_user.id, message.text)
    if result:
        bot.send_message(message.chat.id, company_successfully_deleted_txt)
    else:
        bot.send_message(message.chat.id, company_not_in_list_txt)


@bot.message_handler(commands=['statistics'])
def get_statistics(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
    for i in range(0, len(dates), 2):
        if i != len(dates) - 1:
            markup.add(telebot.types.KeyboardButton(dates[i]), telebot.types.KeyboardButton(dates[i + 1]))
        else:
            markup.add(telebot.types.KeyboardButton(dates[i]))
    msg = bot.reply_to(message, text=show_company_plot_txt, reply_markup=markup)
    bot.register_next_step_handler(msg, first_step_statistics)


interval = 0
start_time = 0
chosen_index = 0


def first_step_statistics(message):
    global interval, start_time, chosen_index
    for i in range(len(dates)):
        if message.text == dates[i]:
            interval = intervals[i]
            start_time = datetime.today() - delta[i]
            chosen_index = i

    reply_markup = telebot.types.ReplyKeyboardRemove()
    msg = bot.reply_to(message, choose_company_txt, reply_markup=reply_markup)
    bot.register_next_step_handler(msg, second_step_statistics)


def second_step_statistics(message):
    result = stock.get_info_about_company(message.text, interval=interval, start_time=start_time)
    if result['error']:
        bot.send_message(message.chat.id, company_not_exist_txt)
    else:
        make_plot(result['date'], result['price'])
        send_plot(message, f"График акций для компании {message.text} за {dates[chosen_index]}")


def send_plot(message, text):
    file = open('graphics.png', 'rb')
    bot.send_photo(message.chat.id, photo=file, caption=text)


@bot.message_handler(commands=['cost'])
def show_cost(message):
    if stock.get_size_companies(message.from_user.id) == 0:
        bot.send_message(message.chat.id, empty_list_txt)
    else:
        Text = f"{price_following_companies_txt}:\n"
        companies = stock.get_companies(message.from_user.id)
        for company in companies:
            cost = stock_helper.get_info_about_company(company)['close']
            Text += f'<b>{company}</b> - <b>{cost}</b> {ruble}\n'
        bot.send_message(message.chat.id, Text, parse_mode='HTML')


@bot.message_handler(commands=['help', 'start'])
def help_message(message):
    bot.send_message(message.chat.id, text=help_message_txt, parse_mode="HTML")


@bot.message_handler(commands=['difference'])
def show_cost(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
    for i in range(0, len(dates), 2):
        if i != len(dates) - 1:
            markup.add(telebot.types.KeyboardButton(dates[i]), telebot.types.KeyboardButton(dates[i + 1]))
        else:
            markup.add(telebot.types.KeyboardButton(dates[i]))

    msg = bot.reply_to(message, text="Показать изменение акций за", reply_markup=markup)
    bot.register_next_step_handler(msg, first_step_show_cost)


def first_step_show_cost(message):
    global interval, start_time, chosen_index
    for i in range(len(dates)):
        if message.text == dates[i]:
            interval = intervals[i]
            start_time = datetime.today() - delta[i]
            chosen_index = i

    companies = stock.get_companies(message.from_user.id)

    if len(companies) == 0:
        bot.send_message(message.chat.id, empty_list_txt)
        return

    Text = f"Изменение цен акций за {dates[chosen_index]}:\n\n"
    for company in companies:
        x = diff.get_difference(company, last_time=start_time, current_time=datetime.today())
        additional = ""
        if x[2] > 0:
            additional = f"(+{x[2]:0.2f} {ruble}, ↑{x[3]:0.2f}%)"
        else:
            additional = f"(-{abs(x[2]):0.2f} {ruble}, ↓{x[3]:0.2f}%)"
        Text += f"{company}  {x[0]} {ruble} ⟶ {x[1]} {ruble} <b>{additional}</b>\n"

    reply_markup = telebot.types.ReplyKeyboardRemove()

    bot.reply_to(message, text=Text, parse_mode="HTML", reply_markup=reply_markup)


@bot.message_handler(commands=['clear'])
def show_cost(message):
    stock.clear(message.from_user.id)
    bot.send_message(message.chat.id, full_deleted_txt)


bot.polling(none_stop=True)