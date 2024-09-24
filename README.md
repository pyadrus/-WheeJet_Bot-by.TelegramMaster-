Токен бота хранится в файле `.env` в директории `setting`.

Лог файлы хранятся в файле `log.log` в директории `logs`.

Команда админа: `/admin_start`

Команда пользователя: `/start`

Директория messages содержит все сообщения бота.

Установка зависимостей:

Установите библиотеки python-docx и pdfkit:
bash
Копировать код
pip install python-docx pdfkit
Убедитесь, что у вас установлен wkhtmltopdf, так как pdfkit использует его для конвертации HTML в PDF. На системах Linux и Windows его можно установить следующим образом:
Linux:

bash
Копировать код
sudo apt-get install wkhtmltopdf
Windows: Загрузите и установите wkhtmltopdf с официального сайта: https://wkhtmltopdf.org/downloads.html.