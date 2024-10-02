from peewee import *

# Создайте модель для таблицы в базе данных
db = SqliteDatabase('database.db')


class UserStart(Model):
    telegram_id = CharField()  # Идентификатор пользователя Telegram
    telegram_username = CharField()  # Идентификатор пользователя Telegram (username)
    user_first_name = CharField()  # Артикул товара
    user_last_name = CharField()  # Номер заказа
    user_date = CharField()  # Артикул товара

    class Meta:
        database = db


class Customer(Model):
    telegram_id = CharField()  # Идентификатор пользователя Telegram (id)
    telegram_username = CharField()  # Идентификатор пользователя Telegram (username)
    product_code = CharField()  # Артикул товара
    order_number = CharField()  # Номер заказа
    product_photo = CharField()  # Фото товара
    full_name = CharField()  # Ф.И.О. (full_name)
    contact = CharField()  # Контакт для связи
    communication_method = CharField()  # Коммуникация
    date_of_purchase = CharField()  # Дата покупки
    tipe_shop = CharField()  # Тип магазина
    warranty_number = CharField()  # Номер гарантийного талона

    class Meta:
        database = db


def entry_into_the_database_to_fill_out_a_warranty_card(user_id, user_name, product_code, order_number, product_photo,
                                                        full_name, contact, communication_method, date_of_purchase,
                                                        tipe_shop, warranty_number) -> None:
    """
    Вносит данные о пользователе и товаре в базу данных для оформления гарантийного талона.

    :param user_id: - ID пользователя в Telegram.
    :param user_name: - Имя пользователя в Telegram.
    :param product_code: - Код продукта.
    :param order_number: - Номер заказа.
    :param product_photo: - Путь к фотографии продукта.
    :param full_name: - Полное имя покупателя.
    :param contact: - Контактная информация покупателя.
    :param communication_method: - Предпочтительный способ связи.
    :param date_of_purchase: - Дата покупки.
    :param tipe_shop: - Тип магазина (например, онлайн или офлайн).
    :param warranty_number: - Номер гарантийного талона.

    :return: None
    """
    db.create_tables([Customer], safe=True)  # Создание таблицы, если она еще не создана
    customer = Customer.create(  # Создание записи в таблице
        telegram_id=user_id,
        telegram_username=user_name,
        product_code=product_code,
        order_number=order_number,
        product_photo=product_photo,
        full_name=full_name,
        contact=contact,
        communication_method=communication_method,
        date_of_purchase=date_of_purchase,
        tipe_shop=tipe_shop,
        warranty_number=warranty_number  # Номер гарантийного талона
    )
    customer.save()


def recording_user_data_of_the_launched_bot(user_id, user_name, user_first_name, user_last_name, user_date):
    # Создание таблицы, если она еще не создана
    db.create_tables([UserStart], safe=True)

    # Создание записи в таблице
    user_start = UserStart.create(
        telegram_id=user_id,
        telegram_username=user_name,
        user_first_name=user_first_name,
        user_last_name=user_last_name,
        user_date=user_date,
    )
    user_start.save()


def get_customer_by_warranty_number(warranty_number_value):
    """
    Находит запись в базе данных по номеру гарантийного талона и возвращает всю информацию о покупателе.

    :param warranty_number_value: Номер гарантийного талона.
    :return: Запись о покупателе, если она найдена, иначе None.
    """
    # try:
        # Поиск строки в базе данных по номеру гарантийного талона
    customer = Customer.get(Customer.warranty_number == warranty_number_value)
    return customer
    # except Customer.DoesNotExist:
    #     Возвращает None, если запись не найдена
    #     return None
