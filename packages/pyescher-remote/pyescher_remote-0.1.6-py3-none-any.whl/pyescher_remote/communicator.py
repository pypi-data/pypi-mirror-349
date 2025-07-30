
from __future__ import annotations
import msgpack
import msgpack_numpy as m
import zmq
from typing import Callable, Any
import traceback
from loguru import logger
from sys import getsizeof

m.patch()

class DataPacket:
    def __init__(self, message: str = '', data: Any = None, is_test_message=False, ack: bool = False):
        self.message: str = message
        self.data: Any = data
        self.is_test_message: bool = is_test_message
        self.ack: bool = ack
    
    def pickle(self):
        logger.debug('Pickling data')
        classdata = dict(message=self.message, data=self.data, is_test_message=self.is_test_message, ack=self.ack)
        data = msgpack.packb(classdata)
        logger.debug(f'Data pickled with size {getsizeof(data)} bytes')
        return data
    
    @staticmethod
    def unpickle(data) -> DataPacket:
        logger.debug('Unpickling data')
        data = msgpack.unpackb(data)
        logger.debug('Data unpickled')
        
        return DataPacket(data['message'], data['data'], data['is_test_message'], data['ack'])

    @staticmethod
    def testpacket():
        return DataPacket(message='Test', is_test_message=True)

class Receiver:
    
    def __init__(self, forward_function: Callable = None, address: str = "tcp://*:5555"):
        logger.debug(f'Starting receiver class at address: {address}')
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind(address)
        
        if forward_function is None:
            self.forward_function = self.print_data
        else:
            self.forward_function = forward_function
        
        logger.debug('Receiver class started')
            
    def print_data(self, data) -> None:
        logger.debug('Data received:', data)

    def run(self):
        logger.debug('Waiting for plot calls...')
        while True:

            received_dp = DataPacket.unpickle(self.socket.recv())

            if received_dp.is_test_message:
                self.socket.send(DataPacket(ack=True).pickle())
                continue
            
            if received_dp.message:
                logger.debug(received_dp.message)

            return_dp = DataPacket(message='SUCCESS')
            try:
                return_dp.data = self.forward_function(received_dp.data)
                logger.debug(f'Data parsed: {received_dp.data[0][0]}')
            except Exception as e:
                return_dp.message = f'FAILURE: {traceback.format_exc()}'
                logger.error(f"Data parsing error: {traceback.format_exc()}")
            self.socket.send(return_dp.pickle())
            
class Sender:
    
    def __init__(self, address: str = "tcp://localhost:5555"):
        logger.debug(f'Starting sender class with address: {address}')
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect(address)
        self.test_line()
        
    def send_data(self, data: Any) -> Any:
        try:
            data = DataPacket(data=data)
        except Exception as e:
            logger.error(f"Data serialization error: {e}")
            return 'FAILURE'
        
        logger.debug(f'Sending data: {str(data)}')

        self.socket.send(data.pickle())

        dp = DataPacket.unpickle(self.socket.recv())

        logger.debug(dp.message)

        return dp.data

    def test_line(self) -> None:
        logger.debug('Testing connection...')
        
        transmit = DataPacket.testpacket()
        
        self.socket.send(transmit.pickle())
        
        receive = DataPacket.unpickle(self.socket.recv())
        
        if receive.ack:
            logger.debug('Connection successful')
        else:
            logger.error('Connection failed')
        