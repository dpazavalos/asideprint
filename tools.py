"""Common used tools"""
from typing import List
from socket import socket


# # # Common send/recv functions


def send_data(*, to_socket: socket, data_stream: bytes,
              send_timeout=2) -> None:
    """
    Centralised function to handle sending data stream to receive data. Sends data in consistent
    buffer sizes
    Args:
        to_socket:
            Socket to send stream to
        data_stream:
            Data stream to send
        send_timeout:
            Set timeout for to_socket
    """
    to_socket.settimeout(send_timeout)
    try:
        data_fragments = []
        for i in range(0, len(data_stream), 4096):
            # Break data stream into byte sized bites
            data_fragments.append(data_stream[i:i + 4096])
        if data_fragments[-1] == 4096:
            # Make sure last fragment isn't BUFFER bytes long
            data_fragments.append(b'\n')
        for frag in data_fragments:
            to_socket.send(frag)
    except TimeoutError:
        pass


def receive_data(*, from_socket: socket,
                 from_timeout=2) -> bytes:
    """
    Centralised fuction to handle receiving one or more packet buffers from TCP socket
    Args:
        from_socket:
            Socket sending stream to this instance.
        from_timeout:
            Set timeout for from_socket
    Returns:
            Complete binary stream from socket
    """
    from_socket.settimeout(from_timeout)
    fragments: List[bytes] = []
    try:
        stream = from_socket.recv(4096)
        fragments.append(stream)
        while True:
            if len(stream) < 4096:
                break
            else:
                stream = from_socket.recv(4096)
                fragments.append(stream)
    except TimeoutError:
        pass
    return b''.join(fragments)
