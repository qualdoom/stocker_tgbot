from datetime import timedelta

request_url = ('https://iss.moex.com/iss/engines/stock/'
               'markets/shares/boards/TQBR/securities.json')

token = "YOUR TOKEN"

help_message_txt = "Привет! Я бот, который позволяет узнать цену акций на московской бирже и отслеживать их изменение за определенный промежуток времени.\n\n" \
                   "Каждый день в 9:30, 16:00 и в 22:00 по МСК(UTC+3) присылается уведомление об изменении акции за последнее время(с момента последнего уведомления). \n\n" \
                   "<b>Команды:</b>\n\n" \
                   "/help - Информация о боте\n" \
                   "/start - Начать работу с ботом\n" \
                   "/add - Добавить компанию в список отслеживаемых компаний\n" \
                   "/delete - Удалить компанию из списка отслеживаемых компаний\n" \
                   "/clear - Очистить список отслеживаемых компаний\n" \
                   "/list - Вывести список отслеживаемых компаний\n" \
                   "/statistics - Показать график акции за какое-то время\n" \
                   "/cost - Узнать стоимость акций отслеживаемых компаний\n" \
                   "/difference - Позволяет узнать разницу акций отслеживаемых компаний за определенное время\n"

company_in_list_txt = "Компания уже есть в списке!"
empty_list_txt = "Список пуст"
list_following_companies_txt = "Список отслеживаемых компаний:"
choose_company_txt = "Введите аббревиатуру компании"

company_successfully_added_txt = "Компания успешно добавлена"
company_not_exist_txt = "Неверная аббревиатура компании или её не существует"

company_successfully_deleted_txt = "Компания успешно удалена"
company_not_in_list_txt = "Компании нет в списке отслеживаемых"

show_company_plot_txt = "Показать компании график за"

price_following_companies_txt = "Цены на акции отслеживаемых компаний"

ruble = "₽"

full_deleted_txt = "Список отслеживаемых компаний успешно очищен"

dates = ['сегодня', 'последнюю неделю', 'последний месяц', 'последний год', 'все время']
intervals = [1, 10, 24, 7, 31]
delta = [timedelta(days=1), timedelta(days=7), timedelta(days=31), timedelta(days=365), timedelta(days=365 * 20)]
days = [7, 31, 365, 365 * 4, 365 * 20]

path_to_db = "stock_data_base.db"
