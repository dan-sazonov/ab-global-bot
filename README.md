# AB Global bot
![OpenSource](https://img.shields.io/badge/Open%20Source-%E2%99%A5-red)
![GPL-3.0 license ](https://img.shields.io/github/license/dan-sazonov/ab-global-bot)
![Tested on linux, Win10](https://img.shields.io/badge/tested%20on-Linux%20|%20Win10-blue)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-%23FE5196?logo=conventionalcommits&logoColor=white)](https://conventionalcommits.org)

**Телеграм-бот для проведения масштабных A/B тестирований названий или других текстовых данных** 

> Данная версия - предрелизная. Код нуждается в серьезной доработке, более подробно - в разделе [Разработка](#Разработка)

**Стэк:**
- Python 3
- SQLite 3 + Peewee
- Aiogram 3

## 📦 Установка и запуск
В качестве пакетного менеджера и виртуального окружения используется [Poetry](https://github.com/python-poetry/poetry). Требуемая версия python - 3.11.

Склонируйте этот репозиторий, перейдите в новую директорию и установите нужные пакеты:
```
$ git clone https://github.com/dan-sazonov/ab-global-bot.git
$ cd ab-global-bot
$ poetry install
```
Настройте переменные окружения: в файл `.env.example` вставьте токен бота и телеграм-айди администратора, после чего сохраните данный файл под названием `.env`.<br>

Добавьте список тестируемых названий. Создайте файл `words.txt`, в который вставьте названия, разделив их переносом строки (каждое название на новой строке).<br>

Отредактируйте файл `messages.py`, заменив примеры на сообщения, которые должен отправлять бот в соответствии с вашей задачей.<br>

Запустите файл с точкой входа:
```
poetry run python main.py 
```

Программа протестирована на Windows 10 x64 и Ubuntu 20.04 x64.

## ⚙ Использование
Бот работает следующим образом: пользователю, запустившего его, показываются два названия, которые рандомно вытаскиваются из файла `words.txt`. Задача пользователя - выбрать название, которое больше соответствует заданной цели. Показ пар будет бесконечным.<br>

Лица, проводящие A/B исследование, будут видеть статистику в таблице `words` в базе данных - в ней отображается список слов, а также показатели, сколько раз каждое слово было предложено для голосования, и сколько раз за него пользователи отдали голос.<br>

В таблице `users` отображается список пользователей, количество отданных голосов, а также время регистрации и последней активности. По этим данным можно оценивать паттерн поведения пользователя, и вероятность слепой "накрутки" голосов.<br>

## 🎯 Разработка
Код разрабатывался в соответствии с методологией "х-х и в продакшн", поэтому нуждается в рефакторинге. Ближайшие задачи:

- [ ] Разделить работу с БД, бизнес-логику, отображение, конфигурацию aiogram на отдельные модули
- [ ] Внедрить лучшие практики Aiogram 3
- [ ] Прописать type hint для функций и классов
- [ ] Улучшить логирование
- [ ] Добавить обработку возможных исключений, EAFP
- [ ] Написать тесты
- [ ] Внедрить линтер и проверку типизации, настроить CI на гитхаб 
- [ ] Пересесть на Postgres

**Баги и фичи:**
- [ ] Добавить работу с изображениями
- [ ] Обрабатывать и игнорировать механическое бездумное "накручивание" количества голосов от пользователя
- [ ] Улучшить скорость отправки нового сообщения после получения голоса
- [ ] Сохранять в БД ссылку на аккаунт пользователей
- [ ] Рассылать раз в nный промежуток времени пользователям сообщение с приглашением продолжить опрос
- [ ] Сообщать пользователю, сколько раз он уже проголосовал

Если вы хотите внести свой вклад, откройте ишью, в котором опишите, над чем вы работаете и ваше видение реализации, сделайте форк репозитория, и после завершения работы предложите пулл-реквест в ветку `dev` с названием как у ишью. Для именования коммитов используйте английский язык и [Conventional Commits](https://github.com/conventional-commits/conventionalcommits.org).

## 🛠 Исходники
Весь исполняемый код бота расположен в директории `/bot`. Точка входа - файл `main.py`. В корневой директории лежат файлы, отвечающие за конфигурацию и прочее. Также в корне располагается файл `words.txt`, в котором должен находится контент для тестирования, а также файл базы данных `data.db`. Основная идея на данный момент по организации кодовой базы:
- `main.py` - точка входа, обработчики действий пользователя. Также, логика отвечающая за отображение 
- `config.py` - обработка переменных окружения, объекты, используемые для хранения параметров
- `models.py` - модели ORM
- `db.py` - функционал по работе с БД, а также функции, отвечающие за обработку данных из моделей
- `messages.py` - тексты сообщений, отправляемые ботом
- `keyboards.py` - клавиатуры бота
- `services.py` - вспомогательные функции

## 👨‍💻 Автор
Автор этого репозитория, идеи и кода - [@dan-sazonov](https://github.com/dan-sazonov). <br>
**Связаться со мной:**<br>
[✈️ Telegram](https://t.me/dan_sazonov) <br>
[📧 Email](mailto:p-294803@yandex.com) <br>
