from peewee import *

# Создайте модель для таблицы в базе данных
db = SqliteDatabase('my_database.db')


class UserStart(Model):
    telegram_id = CharField()  # Идентификатор пользователя Telegram
    telegram_username = CharField()  # Идентификатор пользователя Telegram (username)
    user_first_name = CharField()  # Артикул товара
    user_last_name = CharField()  # Номер заказа
    user_date = CharField()  # Артикул товара

    class Meta:
        database = db


def entry_into_the_database_to_fill_out_a_warranty_card(user_id, user_name, product_code, order_number, product_photo,
                                                        full_name, phone_number_text):
    db.create_tables([Customer])
    customer = Customer.create(
        telegram_id=user_id,  # Идентификатор пользователя Telegram
        telegram_username=user_name,  # Идентификатор пользователя Telegram (username)
        product_code=product_code,
        order_number=order_number,
        product_photo=product_photo,
        full_name=full_name,
        phone_number=phone_number_text
    )
    customer.save()


def recording_user_data_of_the_launched_bot(user_id, user_name, user_first_name, user_last_name, user_date):
    db.create_tables([UserStart])
    user_start = UserStart.create(
        telegram_id=user_id,
        telegram_username=user_name,
        user_first_name=user_first_name,
        user_last_name=user_last_name,
        user_date=user_date,
    )
    user_start.save()


class Customer(Model):
    telegram_id = CharField()  # Идентификатор пользователя Telegram
    telegram_username = CharField()  # Идентификатор пользователя Telegram (username)
    product_code = CharField()  # Артикул товара
    order_number = CharField()  # Номер заказа
    product_photo = CharField()  # Артикул товара
    full_name = CharField()  # Ф.И.О.
    phone_number = CharField()  # Телефон

    class Meta:
        database = db
