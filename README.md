Переименовать `.env.example` в `.env`, при необходимости проставить свои переменные

## Для запуска в Docker
Из корневой директории:

`docker-compose up --build`

Таблицы базы данных будут созданы автоматически при запуске


## Для запуска тестов
Из корневой директории:

`docker-compose -f docker-compose.test.yml up --build`


## Описание методов API

### Метод сохранения статистики

`POST http://localhost:8000/api/v1/statistic/`

`Payload: {
"date": "2023-03-29",
"views": 20,
"clicks": 10,
"cost": 3.15
}`

`Status code: 200`

`Response: {
"date": "2023-03-29",
"views": 20,
"clicks": 10,
"cost": 3.15,
"cpc": 0.315,
"cpm": 157.5
}`


### Метод показа статистики
`GET http://localhost:8000/api/v1/statistic/?from=2023-03-29&to=2024-01-01&sort=date&order=ASC`

`Status code: 200`

`Response: [
{
"date": "2023-03-29",
"views": 20,
"clicks": 10,
"cost": 3.15,
"cpc": 0.315,
"cpm": 157.5
}
]`

### Метод сброса статистики

`DELETE http://localhost:8000/api/v1/statistic/`

`Status code: 204`