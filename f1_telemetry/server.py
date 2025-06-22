import socket
from f1_telemetry.f1_2024_struct import *

UDP_IP = "0.0.0.0"
UDP_PORT = 20777


def get_telemetry():
    """
    Generator function which yields UDPPackets from
    the specified ip address and port

    :yield: A a packet send by F1 2024
    """
    sock = socket.socket(socket.AF_INET,
                         socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    while True:
        data, _ = sock.recvfrom(1460)
        m_header = Header.from_buffer_copy(data[0:29])
        player = 0
        if int(m_header.m_packetId) == 0:
            packet = PacketMotionData.from_buffer_copy(data[0:1349])
            theader = int(m_header.m_packetId)

        elif int(m_header.m_packetId) == 1:
            packet = PacketSessionData.from_buffer_copy(data[0:753])
            theader = int(m_header.m_packetId)

        elif int(m_header.m_packetId) == 2:
            packet = PacketLapData.from_buffer_copy(data[0:1285])
            theader = int(m_header.m_packetId)
            player = int(m_header.m_playerCarIndex)

        elif int(m_header.m_packetId) == 3:
            packet = PacketEventData.from_buffer_copy(data[0:45])
            theader = int(m_header.m_packetId)

        elif int(m_header.m_packetId) == 4:
            packet = PacketParticipantsData.from_buffer_copy(data[0:1350])
            theader = int(m_header.m_packetId)

        elif int(m_header.m_packetId) == 5:
            packet = PacketCarSetupData.from_buffer_copy(data[0:1133])
            theader = int(m_header.m_packetId)

        elif int(m_header.m_packetId) == 6:
            packet = PacketCarTelemetryData.from_buffer_copy(data[0:1352])
            theader = int(m_header.m_packetId)

        elif int(m_header.m_packetId) == 7:
            packet = PacketCarStatusData.from_buffer_copy(data[0:1239])
            theader = int(m_header.m_packetId)

        yield packet, theader, m_header, player
