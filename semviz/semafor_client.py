"""
Author: Sam Thomson (sthomson@cs.cmu.edu)
"""
import json
import socket
from settings import SEMAFOR_HOST, SEMAFOR_PORT

DEFAULT_BUFFER_SIZE = 8192


class SocketClient(object):
    """ A client for interacting with a running TCP socket server. """
    def __init__(self, host, port, buffer_size=DEFAULT_BUFFER_SIZE):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size

    def make_request(self, request):
        """
        Sends request to the server and gets the server's response.
        (end of response is indicated by an empty string)
        """
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.host, self.port))
        client.sendall(request)
        client.shutdown(socket.SHUT_WR)
        response = []
        while True:
            chunk = client.recv(self.buffer_size)
            if not chunk:
                break
            response.append(chunk)
        return ''.join(response)


class SemaforClient(SocketClient):
    """
    A client for retrieving frame-semantic parses from a running SEMAFOR
    server. Creates a new connection for each request.
    """
    def __init__(self,
                 dependency_parser,
                 host=SEMAFOR_HOST,
                 port=SEMAFOR_PORT,
                 buffer_size=DEFAULT_BUFFER_SIZE):
        """
        Creates a new client with the given dependency parser, and host and
        port of a running SEMAFOR server.
        """
        super(SemaforClient, self).__init__(host, port, buffer_size)
        self.dependency_parser = dependency_parser

    def get_parse(self, sentence):
        """ Gets a frame-semantic parse as json from a sentence string. """
        return self.get_parses([sentence])[0]

    def get_parses(self, sentences):
        """
        Gets frame-semantic parses as a list of dicts from a list of sentence
        strings.
        """
        dependency_parses = self.dependency_parser.get_parses(sentences)
        return self.get_parses_from_conll(dependency_parses)

    def get_parses_from_conll(self, dependency_parses):
        """
        Gets frame-semantic parses as a list of dicts from dependency-parsed
        English sentences in conll format.
        """
        response = self.make_request(dependency_parses)
        return [json.loads(x) for x in response.splitlines()]
