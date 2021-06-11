#videorender

videorender - it's django rest-service for creating videocollage by uploading video by REST-api.

This project was generated with [`wemake-django-template`](https://github.com/wemake-services/wemake-django-template). Current template version is: [e54aca50521f678f2578d354cb75a8d27d31aac0](https://github.com/wemake-services/wemake-django-template/tree/e54aca50521f678f2578d354cb75a8d27d31aac0). See what is [updated](https://github.com/wemake-services/wemake-django-template/compare/e54aca50521f678f2578d354cb75a8d27d31aac0...master) since then.


[![wemake.services](https://img.shields.io/badge/%20-wemake.services-green.svg?label=%20&logo=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAALGPC%2FxhBQAAAAFzUkdCAK7OHOkAAAAbUExURQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP%2F%2F%2F5TvxDIAAAAIdFJOUwAjRA8xXANAL%2Bv0SAAAADNJREFUGNNjYCAIOJjRBdBFWMkVQeGzcHAwksJnAPPZGOGAASzPzAEHEGVsLExQwE7YswCb7AFZSF3bbAAAAABJRU5ErkJggg%3D%3D)](https://wemake.services) 
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)


## Prerequisites

You will need:

- `python3.8` (see `pyproject.toml` for full version)
- `postgresql` with version `9.6`
- `docker` with [version at least](https://docs.docker.com/compose/compose-file/#compose-and-docker-compatibility-matrix) `18.02`


## Development

When developing locally, we use:

- [`editorconfig`](http://editorconfig.org/) plugin (**required**)
- [`poetry`](https://github.com/python-poetry/poetry) (**required**)
- `pycharm 2017+` or `vscode`


## Инсталляция.

Весь процесс интасляции уже описан в Makefile. Находясь в директории videorender, где лежит Makefile, можно воспольноваться встроенным командами. Полный писок команд:

> make help

### 1. Окружение:

Сперва создадим виртуальное окружение.

> make venv

Будет создана директория env38 (по версии python 3.8). 

### 2. Активация окружения

> source env38/bin/activate

### 3. Сборка контейнера.

Весь проект упакован в несколько docker-контейнеров. Для начала процесса сборки, просто введите make build

> make build

Процесс может занять какое-то время, так как шаблон cookiecutter обладает большим количество зависимостей, а также пакет ImageMagick-6 компилируется из исходного файла. 

### 4. Запуск

По завершении сборки контейра, его достаточно "поднять".

> make up



## Документация 

Список доступных API:

### video:
* http://127.0.0.1:8000/api/video/ - список всех загруженных на сервис видеороликов. [GET, POST, HEAD, OPTIONS]
* http://127.0.0.1:8000/api/video/<pk>/ - Данные по конкретному видео, доступные для просмотра и редактирования. [GET, PUT, PATCH, HEAD, OPTIONS]

### render:
* http://127.0.0.1:8000/api/render/ - список созданных и сохранённых рендеров по видеороликам. [GET, POST, HEAD, OPTIONS]
* http://127.0.0.1:8000/api/render/<pk>/ - данные по рендеру с конкретным PK.  [GET, HEAD, OPTIONS]
В зависимости от запроса может вернуть либо данные по рендеру (HEAD) либо сам рендер будет загружен с сервиса. Если рендера с указанным <pk> не существует, то можно будет наблюдать следующую картину:

> curl -X GET http://localhost:8000/api/render/42/
> 
> "Not found render with 'source' = 42"%
* http://127.0.0.1:8000/api/render/draw/<pk>/ - api для создания рендера по видео с указанным pk. Если видео с указанным pk в базе данных нет, будет возвращено сообщение:

> curl -X GET http://localhost:8000/api/render/draw/47/ 
> "No video with id==47" 

В случае, если видео с указанным pk в базе данных уже есть, но рендера по нему нет, то ответ на похожий запрос вызовет паузу: сервис начнёт создавать рендер, взяв видео по указанному pk, изменяя его размер, накладывая его на фон и печатая текст поверх. Это может занять какое-то время и нагрузка на процессор сильно возрастёт!
По завершении отрисовки, будет возвращено сообщение:

> curl -X GET http://localhost:8000/api/render/draw/47/ 
> "Render by key 47, was created!"

Это означает, что рендер создан и хранится в базе данных. Теперь можно загрузить его с сервиса через запрос

> curl -X GET http://localhost:8000/api/render/47/ --output render_47.mp4

или через браузер. Он сразу скачает файл рендера в загрузки, если тот имеется в наличии.

 
