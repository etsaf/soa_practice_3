import logging

import grpc
import mafia_pb2
import mafia_pb2_grpc

import random
import sys

import threading
import pika

import time


def run(lock):
    #name can be set in command line arguments or manually later
    mode = 'manual'
    user_input = ''
    if len(sys.argv) > 1:
        mode = 'auto'
        user_input = str(sys.argv[1])
    if mode == 'manual':
        with lock:
            print("Enter your name:")
        user_input = input()
    session = -1
    role = ''
    players = []
    guessed = False
    #when testing without Docker, use 'localhost:50051' instead of 'server:50051'
    time.sleep(15) #the server doesn't start listening right away
    with grpc.insecure_channel('server:50051') as channel:
        stub = mafia_pb2_grpc.MafiaStub(channel)
        #join the server and get the session number
        response = stub.SayHello(mafia_pb2.HelloRequest(name=user_input))
        if mode == 'manual':
            while response.message[:4] == "Name":
                with lock:
                    print(response.message)
                user_input = input()
                response = stub.SayHello(mafia_pb2.HelloRequest(name=user_input))
        session = response.session
        with lock:
            print(response.message)
        #subscribe to update messages
        for update in stub.SendUpdates(mafia_pb2.UpdateRequest(session=session,name=user_input)):
            with lock:
                print(update.message)
            message_array = update.message.split()
            if role == 'ghost':
                continue
            if len(message_array) > 1:
                #message that sets the role
                if message_array[1] == 'you':
                    role = message_array[-1]
                    if role == 'ghost':
                        continue
                    # start the chat, select the topics based on the role
                    # civilians don't get messages during the night
                    elif role == 'mafia' or role == 'commissioner':
                        topics = ['day'+ str(session), 'night'+ str(session)]
                        t2 = threading.Thread(target=receive_chat, args=(topics, lock))
                        t2.start()
                    else:
                        topics = ['day'+ str(session)]
                        t2 = threading.Thread(target=receive_chat, args=(topics, lock))
                        t2.start()
                #message that notifies about new users
                elif message_array[1] == 'joined':
                    players.append(message_array[0])
                
                #message that notifies about new day
                elif message_array[0] == 'Day':
                    # send a message to the chat through the server
                    text = "[x] Chat " + user_input + " says: let's decide"
                    topic = 'day' + str(session)
                    with lock:
                        print("sent message to chat:", text)
                    stub.SendToChat(mafia_pb2.ChatRequest(session=session,sender=user_input, \
                                                          topic=topic, text=text))
                    if role == 'commissioner' and guessed == True:
                        if random.randint(0, 1) == 1:
                            with lock:
                                print("Chose to disclose mafia")
                            stub.RevealPlayer(mafia_pb2.UpdateRequest(session=session,name=user_input))
                        else:
                            with lock:
                                print("Chose not to disclose mafia")
                    if random.randint(0, 1) == 1:
                        if message_array[1] != '0':
                            with lock:
                                print("Chose to end day")
                        stub.EndDay(mafia_pb2.UpdateRequest(session=session,name=user_input))
                    chosen = random.randint(0, 3)
                    if message_array[1] != '0':
                        with lock:
                            print("Chose to execute", players[chosen])
                    stub.ExecutePlayer(mafia_pb2.KillRequest(session=session,sender=user_input, \
                                                             victim=chosen))
                    guessed = False
                
                #message that notifies about new night
                elif message_array[0] == 'Night':
                    if role == 'commissioner':
                        text = "[x] Chat " + user_input + " says: i will find you"
                        topic = 'night' + str(session)
                        stub.SendToChat(mafia_pb2.ChatRequest(session=session,sender=user_input, \
                                                            topic=topic, text=text))
                        with lock:
                            print("sent message to chat:", text)
                        chosen = random.randint(0, 3)
                        with lock:
                            print("Chose to check", players[chosen])
                        response = stub.CheckPlayer(mafia_pb2.KillRequest(session=session, \
                                                                                sender=user_input, \
                                                                                victim=chosen))
                        if response.message == 'Correct':
                            with lock:
                                print("Was right", players[chosen], "is mafia")
                            guessed = True
                        else:
                            with lock:
                                print("Was wrong", players[chosen], "is not mafia")
                    elif role == 'mafia':
                        text = "[x] Chat " + user_input + " says: someone's going to die"
                        topic = 'night' + str(session)
                        stub.SendToChat(mafia_pb2.ChatRequest(session=session,sender=user_input, \
                                                                topic=topic, text=text))
                        with lock:
                            print("sent message to chat:", text)
                        chosen = random.randint(0, 3)
                        with lock:
                            print("Chose to kill", players[chosen])
                        stub.KillPlayer(mafia_pb2.KillRequest(session=session, sender=user_input, \
                                                                                victim=chosen))

# connect to the rabbitmq server and start consuming messages on selected topics
def receive_chat(topics, lock):
    credentials = pika.PlainCredentials(
        username="guest",
        password="guest")

    parameters = pika.ConnectionParameters(
        host='rabbitmq',
        port=5672,
        credentials=credentials,
        connection_attempts=30,
        retry_delay=5
    )

    connection = pika.BlockingConnection(
        parameters=parameters
    )
    chat_channel = connection.channel()
    chat_channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

    result = chat_channel.queue_declare(queue='', exclusive=False)
    queue_name = result.method.queue
    for topic in topics:
        chat_channel.queue_bind(
            exchange='direct_logs', queue=queue_name, routing_key=topic)
    def callback(ch, method, properties, body):
        with lock:
            print(body.decode())
    chat_channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)
    chat_channel.start_consuming()


if __name__ == '__main__':
    logging.basicConfig()
    lock = threading.Lock()
    t1 = threading.Thread(target=run, args=(lock,))
    t1.start()