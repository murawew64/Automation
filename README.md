# Проекты с отложенным запуском в Task Shedule

## Начало работы

1. Склонировать данный репозиторий
2. Прописать в файл config.ini path=<Путь к клонированному репозиторию>

## Описание

Общая структура проекта:

./Automation/
- Scripts - тут хранятся все проекты с исполняемым кодом
- Data - сюда сохраняются все артефакты, созданные в результате работы проекта

**Требования к названию проекта**

1. У папок в /Scripts и /Data, относящихся к одному проекту,
одинаковое название.
2. В названии проекта нет пробелов.
3. Названия задач в Task Schedule (или аналогах) совпадают с названием проекта.

Данные условия будут соблюдены автоматически при работе с проектами через CLI.

## Создание теневой задачи

**Windows** - для постоянного выполнения задач используется Task Sheduler.
В нем в корне создается папка \Automation, в которой будут размещаться все
исполняемые задачи.

## Создание проекта

Создать проект можно вручную, а можно с помощью скрипта `manage_project.py`,
который лежит в папке `.../Automation`.

Данный способ является приоритетным, так как учитывает все требования
к проектам.

! Важно - скрипт использует только стандартные библиотеки python
! Важно - для корректной работы скрипта все пути и названия проектов должны быть на английском языке

Так как скрипт не может редактировать конфиги Task Sheduler непосредственно, то
вся работа выполняется посредством утилиты командной строки schtasks, что накладывает
свои ограничения на работу со скриптом.

### Из папки Automation

Запуск скрипта выполняется из папки `.../Automation`

Создание проекта
```
python manage_project.py create --help
```
Удаление проекта
```
python manage_project.py delete --help
```
Получение информации о созданных проектах
python manage_project.py list --help

### Из любого места через cmd

Для этого требуется сделать два действия:
- Добавить путь до папки `.../Automation` в PATH
- Зарегистрировать python как стандартную программу для
открытия файлов с расширением .py

Запуск скрипт из любого места:

Создание проекта
```
manage_project.py create "<project name>"
```