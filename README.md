# AB Global bot
![OpenSource](https://img.shields.io/badge/Open%20Source-%E2%99%A5-red)
![GPL-3.0 license ](https://img.shields.io/github/license/dan-sazonov/ab-global-bot)
![Tested on linux, Win10](https://img.shields.io/badge/tested%20on-Linux%20|%20Win10-blue)

**Телеграм-бот для проведения масштабных A/B тестирований названий или других текстовых данных** 

> Данная версия - предрелизная. Код нуждается в серьезной доработке, более подробно - в разделе [Разработка](#Разработка)

**Стэк:**
- Python 3
- SQLite 3
- Aiogram 3

## Установка и запуск
В качестве пакетного менеджера и виртуального окружения используется [Poetry](https://github.com/python-poetry/poetry). Требуемая версия python - 3.11.

Склонируйте этот репозиторий, перейдите в новую директорию и установите нужные пакеты:
```
$ git clone https://github.com/dan-sazonov/ab-global-bot.git
$ cd ab-global-bot
$ poetry install
```
Настройте переменные окружения: в файл `.env.example` вставьте токен бота и телеграм-айди администратора, после чего сохраните данный файл под названием `.env`.<br>

Добавьте список тестируемых названий. Создайте файл `words.txt`, в который вставьте названия, разделив их переносом строки (каждое название на новой строке).<br>

Запустите файл с точкой входа:
```
poetry run python main.py 
```

Программа протестирована на Windows 10 x64 и Ubuntu 20.04 x64.

## Использование
Бот работает следующим образом: пользователю, запустившего его, показываются два названия, которые рандомно вытаскиваются из файла `words.txt`. Задача пользователя - выбрать название, которое больше соответствует заданной цели. Показ пар будет бесконечным.<br>

Лица, проводящие A/B исследование, будут видеть статистику в таблице `words` в базе данных - в ней отображается список слов, а также показатели, сколько раз каждое слово было предложено для голосования, и сколько раз за него пользователи отдали голос.<br>

В таблице `users` отображается список пользователей, количество отданных голосов, а также время регистрации и последней активности. По этим данным можно оценивать паттерн поведения пользователя, и вероятность слепой "накрутки" голосов.<br>

## Исходники

## Разработка
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

## Автор