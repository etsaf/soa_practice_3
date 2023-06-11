## Практика 3. Клиент-серверный чат на основе системы RabbitMQ на Python

Сафонова Елизавета, БПМИ-206

-------

### Структура

Следующие команды запускают все контейнеры:

```
docker compose build
docker compose up -d
```

При этом запускается один rabbitmq сервер, один сервер мафии и 8 клиентов-ботов, и проводятся две игры по 4 игрока: мафия, комиссар и два мирных жителя. Ход игры, действия каждого игрока, результат игры и сообщения из чата можно посмотреть в выводе каждого контейнера, например, с помощью Docker Desktop.


### Работа очереди сообщений

В Docker Compose запускается образ rabbitmq:3-management с сервером RabbitMQ. Все клиенты мафии подключаются к нему как слушатели, сервер мафии подключается как отправитель. Каждый клиент слушает сообщения на определенные темы (topics), определяемые параметром routing_key. Например, мирные жители получают только сообщения с темой "day" + str(номер сессии), мафия и комиссары могут общаться в заданной сессии и ночью. Поскольку в системе с ботами одна мафия и один комиссар, они для наглядности получают сообщения друг друга. Если клиент хочет отправить сообщение, он отправляет gRPC запрос на сервер, который проверяет, имеет ли данный клиент право отправлять сообщения с данной темой в данной фазе игры, и если все хорошо, перенаправляет сообщение в очередь сообщений на сервере RabbitMQ, откуда ее получают клиенты, подписанные на заданную тему.


### Отправляемые ботами сообщения

Сообщения, полученные из чата, начинаются в выводе клиентов со знака [x].

```
i will find you         // ночью отправлеят комиссар
someone's going to die  // ночью отправляет мафия
let's decide            // днем отправляет каждый живой участник
```

### Комментарии

- Первые сообщения, отправленные в очередь сообщений, могут не дойти до некоторых участников, если они еще не подключились к очереди как слушатели на момент их отправки. Поэтому в первый день участники, подключившиеся позже, получают не все сообщения. Это можно было бы исправить, дожидаясь подтверждений от всех участников, что они подключились к чату, но я не успеваю это доделать. Если случайная игра сложилась таким образом, что в ней присутствует второй день, в нем уже все участники получают все сообщения. Также все сообщения доходят до адресатов и ночью.

- В каждом клиенте происходит вывод из двух разных threads: одна для чата, одна для уведомлений игры, и уведомления могут печататься в один stdout не в хронологическом порядке.

- В клиенте может возникать ошибка grpc.InactiveRPC, если RPC-сервер не успел подняться. Можно увеличить время ожидания в 32 строчке client.py.

