from datetime import datetime
from kusto.ingest import ingest_kusto
from f1_telemetry.server import get_telemetry


batch_freq_high = 9 # 22 cars per packet * batch_freq_high(x) packets
batch_freq_low = 2

ingest_sessiondataCnt = 0
ingest_sessiondataBuffer = ""
ingest_lapdataCnt = 0
ingest_lapdataBuffer = ""
ingest_cartelemetrydataCnt = 0
ingest_cartelemetryBuffer = ""
ingest_carstatusdataCnt = 0
ingest_carstatusdataBuffer = ""
ingest_cardamagedataCnt = 0
ingest_cardamagedataBuffer = ""


def ingest_sessiondata(sessiondatapacket, m_header):
    global ingest_sessiondataBuffer
    global ingest_sessiondataCnt
    data = [
        datetime.utcnow(),
        m_header.m_sessionUID,
        m_header.m_sessionTime,
        m_header.m_frameIdentifier,
        m_header.m_playerCarIndex,
        sessiondatapacket.m_weather,
        sessiondatapacket.m_trackTemperature,
        sessiondatapacket.m_airTemperature,
        sessiondatapacket.m_totalLaps,
        sessiondatapacket.m_trackLength,
        sessiondatapacket.m_sessionType,
        sessiondatapacket.m_trackId,
        sessiondatapacket.m_sessionTimeLeft,
        sessiondatapacket.m_sessionDuration
    ]
    ingest_sessiondataBuffer = ','.join(map(str, data))
    ingest_sessiondataBuffer +="\n"

    if ingest_sessiondataCnt == batch_freq_low:
        ingest_kusto("Session24", ingest_sessiondataBuffer)
        ingest_sessiondataBuffer=""
        ingest_sessiondataCnt=0
    else:
        ingest_sessiondataCnt+=1


def ingest_lapdata(packet, m_header):
    global ingest_lapdataBuffer
    global ingest_lapdataCnt
     
    for idx,lapdata in enumerate(packet.m_lapsData):
        data = [
            datetime.utcnow(),
            m_header.m_sessionUID,
            m_header.m_sessionTime,
            m_header.m_frameIdentifier,
            m_header.m_playerCarIndex,
            idx,
            lapdata.m_lastLapTimeInMS,
            lapdata.m_currentLapTimeInMS,
            lapdata.m_deltaToCarInFrontMSPart,
            lapdata.m_deltaToCarInFrontMinutesPart,
            lapdata.m_deltaToRaceLeaderMSPart,
            lapdata.m_deltaToRaceLeaderMinutesPart,
            lapdata.m_lapDistance,
            lapdata.m_totalDistance,
            lapdata.m_safetyCarDelta,
            lapdata.m_carPosition,
            lapdata.m_currentLapNum,
            lapdata.m_pitStatus,
            lapdata.m_numPitStops,
            lapdata.m_penalties,
            lapdata.m_totalWarnings,
            lapdata.m_gridPosition,
            lapdata.m_driverStatus,
            lapdata.m_resultStatus,
            lapdata.m_pitLaneTimerActive,
            lapdata.m_pitLaneTimeInLaneInMS,
            lapdata.m_pitStopTimerInMS
        ]
        ingest_lapdataBuffer += ','.join(map(str, data))
        ingest_lapdataBuffer +="\n"

    if ingest_lapdataCnt == batch_freq_high:
        ingest_kusto("Lap24", ingest_lapdataBuffer)
        ingest_lapdataBuffer=""
        ingest_lapdataCnt=0
    else: 
        ingest_lapdataCnt+=1


def ingest_participantdata(packet, m_header):
    participantdataBuffer=""
    for idx,participantdata in enumerate(packet.m_participants):
        data = [
            datetime.utcnow(),
            m_header.m_sessionUID,
            m_header.m_sessionTime,
            m_header.m_frameIdentifier,
            m_header.m_playerCarIndex,
            idx,
            participantdata.m_aiControlled,
            participantdata.m_driverId,
            participantdata.m_teamId,
            participantdata.m_raceNumber,
            participantdata.m_nationality,
            participantdata.m_name.decode(),
            packet.m_numActiveCars
        ]
        participantdataBuffer += ','.join(map(str, data))
        participantdataBuffer+="\n"
    ingest_kusto("Participant24", participantdataBuffer)


def ingest_cartelemetrydata(packet, m_header):
    global ingest_cartelemetryBuffer
    global ingest_cartelemetrydataCnt
    for idx,cartelemetrydata in enumerate(packet.m_carTelemetryData):
        data = [
            datetime.utcnow(),
            m_header.m_sessionUID,
            m_header.m_sessionTime,
            m_header.m_frameIdentifier,            
            m_header.m_playerCarIndex,
            idx,
            cartelemetrydata.m_speed,
            cartelemetrydata.m_throttle,
            cartelemetrydata.m_steer,
            cartelemetrydata.m_brake,
            cartelemetrydata.m_clutch,
            cartelemetrydata.m_gear,
            cartelemetrydata.m_engineRPM,
            cartelemetrydata.m_drs,
            cartelemetrydata.m_revLightsPercent,
            cartelemetrydata.m_revLightsBitValue,
            cartelemetrydata.m_brakesTemperature[0],
            cartelemetrydata.m_brakesTemperature[1],
            cartelemetrydata.m_brakesTemperature[2],
            cartelemetrydata.m_brakesTemperature[3],
            cartelemetrydata.m_tyresSurfaceTemperature[0],
            cartelemetrydata.m_tyresSurfaceTemperature[1],
            cartelemetrydata.m_tyresSurfaceTemperature[2],
            cartelemetrydata.m_tyresSurfaceTemperature[3],
            cartelemetrydata.m_tyresInnerTemperature[0],
            cartelemetrydata.m_tyresInnerTemperature[1],
            cartelemetrydata.m_tyresInnerTemperature[2],
            cartelemetrydata.m_tyresInnerTemperature[3],
            cartelemetrydata.m_engineTemperature,
            cartelemetrydata.m_tyresPressure[0],
            cartelemetrydata.m_tyresPressure[1],
            cartelemetrydata.m_tyresPressure[2],
            cartelemetrydata.m_tyresPressure[3]
        ]
        ingest_cartelemetryBuffer += ','.join(map(str, data))
        ingest_cartelemetryBuffer +="\n"

    if ingest_cartelemetrydataCnt == batch_freq_high:
        ingest_kusto("CarTelemetry24", ingest_cartelemetryBuffer)
        ingest_cartelemetryBuffer=""
        ingest_cartelemetrydataCnt=0
    else:
        ingest_cartelemetrydataCnt+=1



def ingest_carstatusdata(packet, m_header):
    global ingest_carstatusdataBuffer
    global ingest_carstatusdataCnt
    
    for idx,carstatusdata in enumerate(packet.m_carStatusData):
        data = [            
            datetime.utcnow(),
            m_header.m_sessionUID,
            m_header.m_sessionTime,
            m_header.m_frameIdentifier,
            m_header.m_playerCarIndex,
            idx,
            carstatusdata.m_tractionControl,
            carstatusdata.m_antiLockBrakes,
            carstatusdata.m_fuelMix,
            carstatusdata.m_fuelInTank,
            carstatusdata.m_fuelCapacity,
            carstatusdata.m_fuelRemainingLaps,
            carstatusdata.m_maxRPM,
            carstatusdata.m_idleRPM,
            carstatusdata.m_maxGears,
            carstatusdata.m_drsAllowed,
            carstatusdata.m_actualTyreCompound,
            carstatusdata.m_visualTyreCompound,
            carstatusdata.m_vehicleFiaFlags
        ]
        ingest_carstatusdataBuffer += ','.join(map(str, data))
        ingest_carstatusdataBuffer +="\n"

    if ingest_carstatusdataCnt == batch_freq_high:
        ingest_kusto("CarStatus24", ingest_carstatusdataBuffer)
        ingest_carstatusdataBuffer=""
        ingest_carstatusdataCnt=0
    else:
        ingest_carstatusdataCnt+=1


def ingest_cardamagedata(packet, m_header):
    global ingest_cardamagedataBuffer
    global ingest_cardamagedataCnt
    
    for idx,cardamagedata in enumerate(packet.m_carDamageData):
        data = [            
            datetime.utcnow(),
            m_header.m_sessionUID,
            m_header.m_sessionTime,
            m_header.m_frameIdentifier,
            m_header.m_playerCarIndex,
            idx,
            cardamagedata.m_tyresWear[0],
            cardamagedata.m_tyresWear[1],
            cardamagedata.m_tyresWear[2],
            cardamagedata.m_tyresWear[3],
            cardamagedata.m_tyresDamage[0],
            cardamagedata.m_tyresDamage[1],
            cardamagedata.m_tyresDamage[2],
            cardamagedata.m_tyresDamage[3],
            cardamagedata.m_brakesDamage[0],
            cardamagedata.m_brakesDamage[1],
            cardamagedata.m_brakesDamage[2],
            cardamagedata.m_brakesDamage[3],
            cardamagedata.m_frontLeftWingDamage,
            cardamagedata.m_frontRightWingDamage,
            cardamagedata.m_rearWingDamage,
            cardamagedata.m_floorDamage,
            cardamagedata.m_diffuserDamage,
            cardamagedata.m_sidepodDamage,
            cardamagedata.m_drsFault,
            cardamagedata.m_ersFault,
            cardamagedata.m_gearBoxDamage,
            cardamagedata.m_engineDamage
        ]
        ingest_cardamagedataBuffer += ','.join(map(str, data))
        ingest_cardamagedataBuffer +="\n"

    if ingest_cardamagedataCnt == batch_freq_low:
        ingest_kusto("CarDamage24", ingest_cardamagedataBuffer)
        ingest_cardamagedataBuffer=""
        ingest_cardamagedataCnt=0
    else:
        ingest_cardamagedataCnt+=1

        
if __name__ == '__main__':
    print("Server started on 20777")
    for packet, theader, m_header, player in get_telemetry():
        if theader == 1:
            # PacketSessionData
            ingest_sessiondata(packet, m_header)

        elif theader == 2:
            # PacketLapData
            ingest_lapdata(packet, m_header)

        elif theader == 4:
            # PacketParticipantsData
            ingest_participantdata(packet, m_header)
        
        elif theader == 6:
            # PacketCarTelemetryData
            ingest_cartelemetrydata(packet, m_header)
                
        elif theader == 7:
            # PacketCarStatusData
            ingest_carstatusdata(packet, m_header)
        
        elif theader == 10:
            # PacketCarDamageData
            ingest_cardamagedata(packet, m_header)

        # Packet Name	            Value	    Description
        # Motion	                0	        Contains all motion data for player’s car – only sent while player is in control
        # Session	                1	        Data about the session – track, time left
        # Lap Data	                2	        Data about all the lap times of cars in the session
        # Event	                    3	        Various notable events that happen during a session
        # Participants	            4	        List of participants in the session, mostly relevant for multiplayer
        # Car Setups	            5	        Packet detailing car setups for cars in the race
        # Car Telemetry	            6	        Telemetry data for all cars
        # Car Status	            7	        Status data for all cars
        # Final Classification	    8	        Final classification confirmation at the end of a race
        # Lobby Info	            9	        Information about players in a multiplayer lobby
        # Car Damage	            10	        Damage status for all cars
        # Session History	        11	        Lap and tyre data for session
        # Tyre Sets	                12	        Extended tyre set data
        # Motion Ex	                13	        Extended motion data for player car
        # Time Trial	            14	        Time Trial specific data
