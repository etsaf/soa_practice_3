import asyncio
import logging

import grpc
import mafia_pb2
import mafia_pb2_grpc

import random

import pika

possible_roles = ["mafia", "commissioner", "civilian1", "civilian2"]

class Session:
    number = 0
    players = []
    started = False
    roles = {}
    ghosts = set()
    end_day_requests = 0
    day_number = 0
    night_number = 0
    is_day = True
    mafia_ans = False
    commissioner_ans = False
    num_mafia = 1
    num_civs = 2
    voting = [0 for i in range(4)]
    num_votes = 0
    num_ends = 0
    game_over = False

channel = ''

class MafiaServicer(mafia_pb2_grpc.MafiaServicer):
    def __init__(self):
        self.updates = []
        self.users = []
        self.sessions = []

    #add a new user and start a session if there are enough players
    async def SayHello(self, request, context):
        if request.name in self.users:
            return mafia_pb2.HelloReply(message='Name already exists, please try again:')
        if len(request.name.split()) > 1:
            return mafia_pb2.HelloReply(message='Name contains forbidden symbol, please try again:')
        self.users.append(request.name)
        selected_session = -1
        if (len(self.sessions) > 0) and (self.sessions[-1].started == False):
            selected_session = len(self.sessions) - 1
            self.sessions[-1].players.append(request.name)
            self.updates[selected_session].append(mafia_pb2.UpdateReply(message='%s joined' % request.name))
            if len(self.sessions[-1].players) == 4:
                self.sessions[-1].started = True
                self.updates[selected_session].append(mafia_pb2.UpdateReply(message='Session started: %i' % selected_session))
                print("Started session", selected_session)
                role_choice = random.sample(range(4), 4)
                for i in range(4):
                    self.sessions[-1].roles[self.sessions[-1].players[i]] = possible_roles[role_choice[i]]
                    self.updates[selected_session].append(mafia_pb2.UpdateReply(message='Assign %s %s' % (self.sessions[-1].players[i], possible_roles[role_choice[i]])))
                print("Chose roles", self.sessions[-1].roles)
                
                #self.sessions[-1].day_number = 0
                #self.sessions[-1].night_number = 0
                #self.sessions[-1].is_day = False
                #self.sessions[-1].ghosts = set()
                #self.updates[selected_session].append(mafia_pb2.UpdateReply(message='Night %i' % self.sessions[-1].night_number))

                self.sessions[-1].day_number = 0
                self.sessions[-1].night_number = 0
                self.sessions[-1].is_day = True
                self.sessions[-1].ghosts = set()
                self.sessions[-1].voting = [0 for i in range(4)]
                self.sessions[-1].num_votes = 0
                self.sessions[-1].num_ends = 0
                self.sessions[-1].mafia_ans = False
                self.sessions[-1].commissioner_ans = False
                self.updates[selected_session].append(mafia_pb2.UpdateReply(message='Day %i' % self.sessions[-1].day_number))



        else:
            self.sessions.append(Session())
            self.updates.append([])
            selected_session = len(self.sessions) - 1
            self.sessions[-1].number = selected_session
            self.sessions[-1].players = []
            self.sessions[-1].players.append(request.name)
            self.sessions[-1].started = False
            self.sessions[-1].roles = {}
            self.updates[selected_session].append(mafia_pb2.UpdateReply(message='%s joined' % request.name))
        return mafia_pb2.HelloReply(message='Hello, %s!' % request.name, session=selected_session)
    
    #send updates to the user
    async def SendUpdates(self, request, context):
        last_read = 0
        # For every client a infinite loop starts (in gRPC's own managed thread)
        while True:
            # Check if there are any new messages
            if len(self.updates[request.session]) > last_read:
                message = self.updates[request.session][last_read]
                last_read += 1
                if message.message[:6] == "Assign":
                    name, assigned = message.message.split()[1:]
                    if request.name == name:
                        yield mafia_pb2.UpdateReply(message='%s, you are %s' % (request.name, assigned))
                else:
                    yield message
            else:
                await asyncio.sleep(1)
    
    #mafia choosing to kill a player
    async def KillPlayer(self, request, context):
        s = request.session
        if (not self.sessions[s].is_day) and self.sessions[s].roles[request.sender] == "mafia":
            victim_name = self.sessions[s].players[request.victim]
            victim_role = self.sessions[s].roles[victim_name]
            self.updates[s].append(mafia_pb2.UpdateReply(message='Assign %s %s' % (victim_name, 'ghost')))
            self.updates[s].append(mafia_pb2.UpdateReply(message='%s killed' % victim_name))
            self.sessions[s].ghosts.add(victim_role)
            if victim_role[0] == 'm':
                self.sessions[s].num_mafia -= 1
            elif victim_role[:3] == 'civ':
                self.sessions[s].num_civs -= 1
            self.sessions[s].mafia_ans = True
            if self.sessions[s].num_mafia == 0:
                self.updates[s].append(mafia_pb2.UpdateReply(message='Game over, civilians win'))
                self.sessions[s].game_over = True
                print("Session %i game over" % s)
            elif self.sessions[s].num_mafia == self.sessions[s].num_civs:
                self.updates[s].append(mafia_pb2.UpdateReply(message='Game over, mafia wins'))
                self.sessions[s].game_over = True
                print("Session %i game over" % s)
            else:
                if self.sessions[s].commissioner_ans == True or ('commissioner' in self.sessions[s].ghosts):
                    self.sessions[s].day_number += 1
                    day_number = self.sessions[s].day_number
                    self.sessions[s].is_day = True
                    self.updates[s].append(mafia_pb2.UpdateReply(message='Day %i' % day_number))
                    self.sessions[s].mafia_ans = False
                    self.sessions[s].commissioner_ans = False
        return mafia_pb2.Empty()
    
    #commissioner choosing to check if a player is mafia
    async def CheckPlayer(self, request, context):
        s = request.session
        if (not self.sessions[s].is_day) and self.sessions[s].roles[request.sender] == "commissioner":
            victim_name = self.sessions[s].players[request.victim]
            victim_role = self.sessions[s].roles[victim_name]
            self.sessions[s].commissioner_ans = True
            guessed = False
            if victim_role == 'mafia':
                guessed = True
            if self.sessions[s].mafia_ans == True or ('mafia' in self.sessions[s].ghosts):
                if not self.sessions[s].game_over:
                    self.sessions[s].day_number += 1
                    day_number = self.sessions[s].day_number
                    self.sessions[s].is_day = True
                    self.updates[s].append(mafia_pb2.UpdateReply(message='Day %i' % day_number))
                    self.sessions[s].mafia_ans = False
                    self.sessions[s].commissioner_ans = False
            if guessed:
                return mafia_pb2.HelloReply(message='Correct')
            else:
                return mafia_pb2.HelloReply(message='Wrong')
        return mafia_pb2.HelloReply(message='You are not a commissioner')
    
    #commissioner choosing to reveal mafia's identity if guessed correctly the previous night
    async def RevealPlayer(self, request, context):
        s = request.session
        if self.sessions[s].roles[request.name] == "commissioner":
            mafia_player = ''
            for key, value in self.sessions[s].roles.items():
                if value == 'mafia':
                    mafia_player = key
            self.updates[s].append(mafia_pb2.UpdateReply(message='%s is mafia' % mafia_player))
        return mafia_pb2.Empty()
    
    #player voting to end the day
    async def EndDay(self, request, context):
        s = request.session
        self.sessions[s].num_ends += 1
        if (self.sessions[s].num_ends == (4 - len(self.sessions[s].ghosts))):
            self.sessions[s].night_number += 1
            night_number = self.sessions[s].night_number
            self.sessions[s].is_day = False
            self.updates[s].append(mafia_pb2.UpdateReply(message='Night %i' % night_number))
            self.sessions[s].voting = [0 for i in range(4)]
            self.sessions[s].num_votes = 0
            self.sessions[s].num_ends = 0
        return mafia_pb2.Empty()
    
    #player voting who is mafia during the day
    async def ExecutePlayer(self, request, context):
        s = request.session
        if self.sessions[s].is_day:
            self.sessions[s].num_votes += 1
            self.sessions[s].voting[request.victim] += 1
            if self.sessions[s].num_votes == (4 - len(self.sessions[s].ghosts)):
                if self.sessions[s].day_number == 0:
                    self.sessions[s].night_number += 1
                    night_number = self.sessions[s].night_number
                    self.sessions[s].is_day = False
                    self.updates[s].append(mafia_pb2.UpdateReply(message='Vote inconclusive'))
                    self.updates[s].append(mafia_pb2.UpdateReply(message='Night %i' % night_number))
                    self.sessions[s].voting = [0 for i in range(4)]
                    self.sessions[s].num_votes = 0
                    self.sessions[s].num_ends = 0
                    return mafia_pb2.Empty()
                candidates = []
                for i in range(len(self.sessions[s].voting)):
                    if self.sessions[s].voting[i] >= (4 - len(self.sessions[s].ghosts) + 1) // 2:
                        candidates.append(i)
                if len(candidates) == 1:
                    victim_name = self.sessions[s].players[candidates[0]]
                    victim_role = self.sessions[s].roles[victim_name]
                    self.updates[s].append(mafia_pb2.UpdateReply(message='Assign %s %s' % (victim_name, 'ghost')))
                    self.updates[s].append(mafia_pb2.UpdateReply(message='%s executed' % victim_name))
                    self.sessions[s].ghosts.add(victim_role)
                    if victim_role[0] == 'm':
                        self.sessions[s].num_mafia -= 1
                    elif victim_role[:3] == 'civ':
                        self.sessions[s].num_civs -= 1
                    if self.sessions[s].num_mafia == 0:
                        self.updates[s].append(mafia_pb2.UpdateReply(message='Game over, civilians win'))
                        self.sessions[s].game_over = True
                        print("Session %i game over" % s)
                    elif self.sessions[s].num_mafia == self.sessions[s].num_civs:
                        self.updates[s].append(mafia_pb2.UpdateReply(message='Game over, mafia wins'))
                        self.sessions[s].game_over = True
                        print("Session %i game over" % s)
                    else:
                        self.sessions[s].night_number += 1
                        night_number = self.sessions[s].night_number
                        self.sessions[s].is_day = False
                        self.updates[s].append(mafia_pb2.UpdateReply(message='Night %i' % night_number))
                        self.sessions[s].voting = [0 for i in range(4)]
                        self.sessions[s].num_votes = 0
                        self.sessions[s].num_ends = 0
                else:
                    self.sessions[s].night_number += 1
                    night_number = self.sessions[s].night_number
                    self.sessions[s].is_day = False
                    self.updates[s].append(mafia_pb2.UpdateReply(message='Vote inconclusive'))
                    self.updates[s].append(mafia_pb2.UpdateReply(message='Night %i' % night_number))
                    self.sessions[s].voting = [0 for i in range(4)]
                    self.sessions[s].num_votes = 0
                    self.sessions[s].num_ends = 0
        return mafia_pb2.Empty()
    
    # player sending a message to the chat
    async def SendToChat(self, request, context):
        s = request.session
        # check is the topic is right
        if self.sessions[s].is_day and request.topic[:3] == 'day':
            channel.basic_publish(
                exchange='direct_logs', routing_key=request.topic, body=request.text)
            print(" [x] Chat sent", request.text, "by", request.sender)
        elif (not self.sessions[s].is_day) and request.topic[:5] == 'night':
            channel.basic_publish(
                exchange='direct_logs', routing_key=request.topic, body=request.text)
            print(" [x] Chat sent", request.text, "by", request.sender)
        return mafia_pb2.Empty()


        

async def serve():
    port = '50051'
    server = grpc.aio.server()
    mafia_pb2_grpc.add_MafiaServicer_to_server(MafiaServicer(), server)
    server.add_insecure_port('[::]:' + port)
    await server.start()
    print("Server started, listening on " + port)
    await server.wait_for_termination()

#connect to the rabbitmq server as a publisher
def set_channel():
    global channel
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
    channel = connection.channel()
    channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    set_channel()
    asyncio.run(serve())