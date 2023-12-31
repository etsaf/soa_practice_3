# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import mafia_pb2 as mafia__pb2


class MafiaStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SayHello = channel.unary_unary(
                '/Mafia/SayHello',
                request_serializer=mafia__pb2.HelloRequest.SerializeToString,
                response_deserializer=mafia__pb2.HelloReply.FromString,
                )
        self.SendUpdates = channel.unary_stream(
                '/Mafia/SendUpdates',
                request_serializer=mafia__pb2.UpdateRequest.SerializeToString,
                response_deserializer=mafia__pb2.UpdateReply.FromString,
                )
        self.EndDay = channel.unary_unary(
                '/Mafia/EndDay',
                request_serializer=mafia__pb2.UpdateRequest.SerializeToString,
                response_deserializer=mafia__pb2.Empty.FromString,
                )
        self.KillPlayer = channel.unary_unary(
                '/Mafia/KillPlayer',
                request_serializer=mafia__pb2.KillRequest.SerializeToString,
                response_deserializer=mafia__pb2.Empty.FromString,
                )
        self.CheckPlayer = channel.unary_unary(
                '/Mafia/CheckPlayer',
                request_serializer=mafia__pb2.KillRequest.SerializeToString,
                response_deserializer=mafia__pb2.UpdateReply.FromString,
                )
        self.RevealPlayer = channel.unary_unary(
                '/Mafia/RevealPlayer',
                request_serializer=mafia__pb2.UpdateRequest.SerializeToString,
                response_deserializer=mafia__pb2.Empty.FromString,
                )
        self.ExecutePlayer = channel.unary_unary(
                '/Mafia/ExecutePlayer',
                request_serializer=mafia__pb2.KillRequest.SerializeToString,
                response_deserializer=mafia__pb2.Empty.FromString,
                )
        self.SendToChat = channel.unary_unary(
                '/Mafia/SendToChat',
                request_serializer=mafia__pb2.ChatRequest.SerializeToString,
                response_deserializer=mafia__pb2.Empty.FromString,
                )


class MafiaServicer(object):
    """Missing associated documentation comment in .proto file."""

    def SayHello(self, request, context):
        """Sends a greeting
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendUpdates(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def EndDay(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def KillPlayer(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CheckPlayer(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RevealPlayer(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ExecutePlayer(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendToChat(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MafiaServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SayHello': grpc.unary_unary_rpc_method_handler(
                    servicer.SayHello,
                    request_deserializer=mafia__pb2.HelloRequest.FromString,
                    response_serializer=mafia__pb2.HelloReply.SerializeToString,
            ),
            'SendUpdates': grpc.unary_stream_rpc_method_handler(
                    servicer.SendUpdates,
                    request_deserializer=mafia__pb2.UpdateRequest.FromString,
                    response_serializer=mafia__pb2.UpdateReply.SerializeToString,
            ),
            'EndDay': grpc.unary_unary_rpc_method_handler(
                    servicer.EndDay,
                    request_deserializer=mafia__pb2.UpdateRequest.FromString,
                    response_serializer=mafia__pb2.Empty.SerializeToString,
            ),
            'KillPlayer': grpc.unary_unary_rpc_method_handler(
                    servicer.KillPlayer,
                    request_deserializer=mafia__pb2.KillRequest.FromString,
                    response_serializer=mafia__pb2.Empty.SerializeToString,
            ),
            'CheckPlayer': grpc.unary_unary_rpc_method_handler(
                    servicer.CheckPlayer,
                    request_deserializer=mafia__pb2.KillRequest.FromString,
                    response_serializer=mafia__pb2.UpdateReply.SerializeToString,
            ),
            'RevealPlayer': grpc.unary_unary_rpc_method_handler(
                    servicer.RevealPlayer,
                    request_deserializer=mafia__pb2.UpdateRequest.FromString,
                    response_serializer=mafia__pb2.Empty.SerializeToString,
            ),
            'ExecutePlayer': grpc.unary_unary_rpc_method_handler(
                    servicer.ExecutePlayer,
                    request_deserializer=mafia__pb2.KillRequest.FromString,
                    response_serializer=mafia__pb2.Empty.SerializeToString,
            ),
            'SendToChat': grpc.unary_unary_rpc_method_handler(
                    servicer.SendToChat,
                    request_deserializer=mafia__pb2.ChatRequest.FromString,
                    response_serializer=mafia__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Mafia', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Mafia(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def SayHello(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Mafia/SayHello',
            mafia__pb2.HelloRequest.SerializeToString,
            mafia__pb2.HelloReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SendUpdates(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/Mafia/SendUpdates',
            mafia__pb2.UpdateRequest.SerializeToString,
            mafia__pb2.UpdateReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def EndDay(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Mafia/EndDay',
            mafia__pb2.UpdateRequest.SerializeToString,
            mafia__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def KillPlayer(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Mafia/KillPlayer',
            mafia__pb2.KillRequest.SerializeToString,
            mafia__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CheckPlayer(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Mafia/CheckPlayer',
            mafia__pb2.KillRequest.SerializeToString,
            mafia__pb2.UpdateReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RevealPlayer(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Mafia/RevealPlayer',
            mafia__pb2.UpdateRequest.SerializeToString,
            mafia__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ExecutePlayer(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Mafia/ExecutePlayer',
            mafia__pb2.KillRequest.SerializeToString,
            mafia__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SendToChat(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Mafia/SendToChat',
            mafia__pb2.ChatRequest.SerializeToString,
            mafia__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
