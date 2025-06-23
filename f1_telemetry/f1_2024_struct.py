import ctypes


class Header(ctypes.LittleEndianStructure):
    """
    Ctypes data structure for the header of a F1 2024 UDP packet
    https://forums.ea.com/discussions/f1-24-general-discussion-en/f1-24-udp-specification/8369125
    Size: 29 bytes
    """
    _pack_ = 1
    _fields_ = [
        ('m_packetFormat', ctypes.c_uint16),              # 2024
        ('m_gameYear', ctypes.c_uint8),                   # Game year - last two digits e.g. 24
        ('m_gameMajorVersion', ctypes.c_uint8),           # Game major version - "X.00"
        ('m_gameMinorVersion', ctypes.c_uint8),           # Game minor version - "1.XX"
        ('m_packetVersion', ctypes.c_uint8),              # Version of this packet type, all start from 1
        ('m_packetId', ctypes.c_uint8),                   # Identifier for the packet type, see below
        ('m_sessionUID', ctypes.c_uint64),                # Unique identifier for the session
        ('m_sessionTime', ctypes.c_float),                # Session timestamp
        ('m_frameIdentifier', ctypes.c_uint32),           # Identifier for the frame the data was retrieved on
        ('m_overallFrameIdentifier', ctypes.c_uint32),    # Overall identifier for the frame the data was retrieved on, doesn't go back after flashbacks
        ('m_playerCarIndex', ctypes.c_uint8),             # Index of player's car in the array
        ('m_secondaryPlayerCarIndex', ctypes.c_uint8),    # Index of secondary player's car in the array (splitscreen) 255 if no second player
    ]


class CarMotionData(ctypes.LittleEndianStructure):
    """
    Ctypes data structure for a single car motion data

    The motion packet gives physics data for all the cars being driven. There is additional data for the car being
    driven with the goal of being able to drive a motion platform setup.

    Frequency: Rate as specified in menus
    Size: 60 bytes
    """
    _pack_ = 1
    _fields_ = [
        ('m_worldPositionX', ctypes.c_float),      # World space X position - metres
        ('m_worldPositionY', ctypes.c_float),      # World space Y position
        ('m_worldPositionZ', ctypes.c_float),      # World space Z position
        ('m_worldVelocityX', ctypes.c_float),      # Velocity in world space X – metres/s
        ('m_worldVelocityY', ctypes.c_float),      # Velocity in world space Y
        ('m_worldVelocityZ', ctypes.c_float),      # Velocity in world space Z
        ('m_worldForwardDirX', ctypes.c_int16),    # World space forward X direction (normalised)
        ('m_worldForwardDirY', ctypes.c_int16),    # World space forward Y direction (normalised)
        ('m_worldForwardDirZ', ctypes.c_int16),    # World space forward Z direction (normalised)
        ('m_worldRightDirX', ctypes.c_int16),      # World space right X direction (normalised)
        ('m_worldRightDirY', ctypes.c_int16),      # World space right Y direction (normalised)
        ('m_worldRightDirZ', ctypes.c_int16),      # World space right Z direction (normalised)
        ('m_gForceLateral', ctypes.c_float),       # Lateral G-Force component
        ('m_gForceLongitudinal', ctypes.c_float),  # Longitudinal G-Force component
        ('m_gForceVertical', ctypes.c_float),      # Vertical G-Force component
        ('m_yaw', ctypes.c_float),                 # Yaw angle in radians
        ('m_pitch', ctypes.c_float),               # Pitch angle in radians
        ('m_roll', ctypes.c_float)                 # Roll angle in radians
    ]


class PacketMotionData(ctypes.LittleEndianStructure):
    """
    Ctypes data structure for all cars motion data

    Frequency: Rate as specified in menus
    Size: 1349 bytes
    """
    _pack_ = 1
    _fields_ = [
        ('m_header', Header),                              # Header
        ('m_carMotionData', CarMotionData * 22)            # Data for all cars on track
    ]


class MarshalZone(ctypes.LittleEndianStructure):
    """
    Ctypes data structure for the car data portion of a F1 2024 UDP packet
    """
    _pack_ = 1
    _fields_ = [
        ('m_zoneStart', ctypes.c_float),  # Fraction (0..1) of way through the lap the marshal zone starts
        ('m_zoneFlag', ctypes.c_int8)     # -1 = invalid/unknown, 0 = none, 1 = green, 2 = blue, 3 = yellow, 4 = red
    ]


class WeatherForecastSample(ctypes.LittleEndianStructure):
    """
    Ctypes data structure for the weather forecast
    """
    _pack_ = 1
    _fields_ = [
        ('m_sessionType', ctypes.c_uint8),             # Session type, see above
        ('m_timeOffset', ctypes.c_uint8),              # Time in minutes into the session that this forecast is for
        ('m_weather', ctypes.c_uint8),                 # Weather - 0 = clear, 1 = light cloud, 2 = overcast, 3 = light rain,
                                                       # 4 = heavy rain, 5 = storm
        ('m_trackTemperature', ctypes.c_int8),         # Track temp. in degrees celsius
        ('m_trackTemperatureChange', ctypes.c_int8),   # Track temp. change in degrees celsius
        ('m_airTemperature', ctypes.c_int8),           # Air temp. in degrees celsius
        ('m_airTemperatureChange', ctypes.c_int8),     # Air temp. change in degrees celsius
        ('m_rainPercentage', ctypes.c_uint8)           # Rain percentage (0-100)
    ]


class PacketSessionData(ctypes.LittleEndianStructure):
    """
    Ctypes data structure for Session Data

    The session packet includes details about the current session in progress.

    Frequency: 2 per second
    Size: 753 bytes
    """
    _pack_ = 1
    _fields_ = [
        ('m_header', Header),                                      # Header
        ('m_weather', ctypes.c_uint8),                             # Weather - 0 = clear, 1 = light cloud, 2 = overcast
                                                                   # 3 = light rain, 4 = heavy rain, 5 = storm
        ('m_trackTemperature', ctypes.c_int8),                     # Track temp. in degrees celsius
        ('m_airTemperature', ctypes.c_int8),                       # Air temp. in degrees celsius
        ('m_totalLaps', ctypes.c_uint8),                           # Total number of laps in this race
        ('m_trackLength', ctypes.c_uint16),                        # Track length in metres
        ('m_sessionType', ctypes.c_uint8),                         # 0 = unknown, see appendix
        ('m_trackId', ctypes.c_int8),                              # -1 for unknown, 0-21 for tracks, see appendix
        ('m_formula', ctypes.c_uint8),                             # Formula, 0 = F1 Modern, 1 = F1 Classic, 2 = F2, 3 = F1 Generic
                                                                   # 4 = Beta, 6 = Esports, 8 = F1 World, 9 = F1 Elimination
        ('m_sessionTimeLeft', ctypes.c_uint16),                    # Time left in session in seconds
        ('m_sessionDuration', ctypes.c_uint16),                    # Session duration in seconds
        ('m_pitSpeedLimit', ctypes.c_uint8),                       # Pit speed limit in kilometres per hour
        ('m_gamePaused', ctypes.c_uint8),                          # Whether the game is paused
        ('m_isSpectating', ctypes.c_uint8),                        # Whether the player is spectating
        ('m_spectatorCarIndex', ctypes.c_uint8),                   # Index of the car being spectated
        ('m_sliProNativeSupport', ctypes.c_uint8),                 # SLI Pro support, 0 = inactive, 1 = active
        ('m_numMarshalZones', ctypes.c_uint8),                     # Number of marshal zones to follow
        ('m_marshalZones', MarshalZone * 21),                      # List of marshal zones - max 21List of marshal zones - max 21
        ('m_safetyCarStatus', ctypes.c_uint8),                     # 0 = no safety car, 1 = full safety car, 2 = virtual safety car
                                                                   # 3 = formation lap
        ('m_networkGame', ctypes.c_uint8),                         # 0 = offline, 1 = online
        ('m_numWeatherForecastSamples', ctypes.c_uint8),           # Number of weather forecast samples to follow
        ('m_weatherForecastSamples', WeatherForecastSample * 64),  # Array of weather forecast samples
        ('m_forecastAccuracy', ctypes.c_uint8),                    # 0 = perfect, 1 = approximate
        ('m_aiDifficulty', ctypes.c_uint8),                        # AI difficulty, 0-110
        ('m_seasonLinkIdentifier', ctypes.c_uint32),               # Identifier for the season, persists across saves
        ('m_weekendLinkIdentifier', ctypes.c_uint32),              # Identifier for the weekend
        ('m_sessionLinkIdentifier', ctypes.c_uint32),              # Identifier for the session, persists across saves
        ('m_pitStopWindowIdealLap', ctypes.c_uint8),               # Ideal lap for pit stop window
        ('m_pitStopWindowLatestLap', ctypes.c_uint8),              # Latest lap for pit stop window
        ('m_pitStopRejoinPosition', ctypes.c_uint8),               # Position the car will rejoin at if pitting at the end of the pit stop window
        ('m_steeringAssist', ctypes.c_uint8),                      # 0 = off, 1 = on
        ('m_brakingAssist', ctypes.c_uint8),                       # 0 = off, 1 = low, 2 = medium, 3 = high
        ('m_gearboxAssist', ctypes.c_uint8),                       # 0 = off, 1 = on
        ('m_pitAssist', ctypes.c_uint8),                           # 0 = off, 1 = on
        ('m_pitReleaseAssist', ctypes.c_uint8),                    # 0 = off, 1 = on
        ('m_ERSSAssist', ctypes.c_uint8),                          # 0 = off, 1 = on
        ('m_DRSAssist', ctypes.c_uint8),                           # 0 = off, 1 = on
        ('m_dynamicRacingLine', ctypes.c_uint8),                   # 0 = off, 1 = corners only, 2 = full line
        ('m_dynamicRacingLineType', ctypes.c_uint8),               # 0 = 2D, 1 = 3D
        ('m_gameMode', ctypes.c_uint8),                            # Game mode id - see appendix
        ('m_ruleSet', ctypes.c_uint8),                             # Rule set id - see appendix
        ('m_timeOfDay', ctypes.c_uint32),                          # Time of day in seconds
        ('m_sessionLength', ctypes.c_uint8),                       # 0 = None, 2 = Very Short, 3 = Short, 4 = Medium
                                                                   # 5 = Medium Long, 6 = Long, 7 = Full
        ('m_speedUnitsLeadPlayer', ctypes.c_uint8),                # 0 = MPH, 1 = KPH
        ('m_temperatureUnitsLeadPlayer', ctypes.c_uint8),          # 0 = Celsius, 1 = Fahrenheit
        ('m_speedUnitsSecondaryPlayer', ctypes.c_uint8),           # 0 = MPH, 1 = KPH
        ('m_temperatureUnitsSecondaryPlayer', ctypes.c_uint8),     # 0 = Celsius, 1 = Fahrenheit
        ('m_numSafetyCarPeriods', ctypes.c_uint8),                 # Number of safety car periods in the session
        ('m_numVirtualSafetyCarPeriods', ctypes.c_uint8),          # Number of virtual safety car periods in the session
        ('m_numRedFlagPeriods', ctypes.c_uint8),                   # Number of red flags called during session
        ('m_equalCarPerformance', ctypes.c_uint8),                 # 0 = Off, 1 = On                         
        ('m_recoveryMode', ctypes.c_uint8),                        # 0 = None, 1 = Flashbacks, 2 = Auto-recovery    
        ('m_flashbackLimit', ctypes.c_uint8),                      # 0 = Low, 1 = Medium, 2 = High, 3 = Unlimited       
        ('m_surfaceType', ctypes.c_uint8),                         # 0 = Simplified, 1 = Realistic   
        ('m_lowFuelMode', ctypes.c_uint8),                         # 0 = Easy, 1 = Hard   
        ('m_raceStarts', ctypes.c_uint8),                          # 0 = Manual, 1 = Assisted           
        ('m_tyreTemperature', ctypes.c_uint8),                     # 0 = Surface only, 1 = Surface & Carcass       
        ('m_pitLaneTyreSim', ctypes.c_uint8),                      # 0 = On, 1 = Off      
        ('m_carDamage', ctypes.c_uint8),                           # 0 = Off, 1 = Reduced, 2 = Standard, 3 = Simulati 
        ('m_carDamageRate', ctypes.c_uint8),                       # 0 = Reduced, 1 = Standard, 2 = Simulation     
        ('m_collisions', ctypes.c_uint8),                          # 0 = Off, 1 = Player-to-Player Off, 2 = On  
        ('m_collisionsOffForFirstLapOnly', ctypes.c_uint8),        # 0 = Disabled, 1 = Enabled                    
        ('m_mpUnsafePitRelease', ctypes.c_uint8),                  # 0 = On, 1 = Off (Multiplayer)          
        ('m_mpOffForGriefing', ctypes.c_uint8),                    # 0 = Disabled, 1 = Enabled (Multiplayer)        
        ('m_cornerCuttingStringency', ctypes.c_uint8),             # 0 = Regular, 1 = Strict               
        ('m_parcFermeRules', ctypes.c_uint8),                      # 0 = Off, 1 = On      
        ('m_pitStopExperience', ctypes.c_uint8),                   # 0 = Automatic, 1 = Broadcast, 2 = Immersive        
        ('m_safetyCar', ctypes.c_uint8),                           # 0 = Off, 1 = Reduced, 2 = Standard, 3 = Increase 
        ('m_safetyCarExperience', ctypes.c_uint8),                 # 0 = Broadcast, 1 = Immersive           
        ('m_formationLap', ctypes.c_uint8),                        # 0 = Off, 1 = On    
        ('m_formationLapExperience', ctypes.c_uint8),              # 0 = Broadcast, 1 = Immersive              
        ('m_redFlags', ctypes.c_uint8),                            # 0 = Off, 1 = Reduced, 2 = Standard, 3 = Increase
        ('m_affectsLicenceLevelSolo', ctypes.c_uint8),             # 0 = Off, 1 = On               
        ('m_affectsLicenceLevelMP', ctypes.c_uint8),               # 0 = Off, 1 = On             
        ('m_numSessionsInWeekend', ctypes.c_uint8),                # Number of session in following array            
        ('m_weekendStructure' 	 , ctypes.c_uint8 * 12),           # List of session types to show weekend structure    
        ('m_sector2LapDistanceStart', ctypes.c_float),             # Distance in m around track where sector 2 starts   
        ('m_sector3LapDistanceStart', ctypes.c_float)              # Distance in m around track where sector 3 starts   
    ]


class LapData(ctypes.LittleEndianStructure):
    """
    The lap data packet gives details of all the cars in the session.

    Frequency: Rate as specified in menus
    """
    _pack_ = 1
    _fields_ = [
        ('m_lastLapTimeInMS', 	       	   ctypes.c_uint32),              # Last lap time in milliseconds
        ('m_currentLapTimeInMS',  	       ctypes.c_uint32),              # Current time around the lap in milliseconds
        ('m_sector1TimeMSPart',            ctypes.c_uint16),              # Sector 1 time milliseconds part
        ('m_sector1TimeMinutesPart',       ctypes.c_uint8),               # Sector 1 whole minute part
        ('m_sector2TimeMSPart',            ctypes.c_uint16),              # Sector 2 time milliseconds part
        ('m_sector2TimeMinutesPart',       ctypes.c_uint8),               # Sector 2 whole minute part
        ('m_deltaToCarInFrontMSPart',      ctypes.c_uint16),              # Time delta to car in front milliseconds part
        ('m_deltaToCarInFrontMinutesPart', ctypes.c_uint8),               # Time delta to car in front whole minute part
        ('m_deltaToRaceLeaderMSPart',      ctypes.c_uint16),              # Time delta to race leader milliseconds part
        ('m_deltaToRaceLeaderMinutesPart', ctypes.c_uint8),               # Time delta to race leader whole minute part
        ('m_lapDistance', 		           ctypes.c_float),               # Distance vehicle is around current lap in metres – could
                                                                          # be negative if line hasn’t been crossed yet
        ('m_totalDistance', 		       ctypes.c_float),               # Total distance travelled in session in metres – could 
                                                                          # be negative if line hasn’t been crossed yet
        ('m_safetyCarDelta',               ctypes.c_float),               # Delta in seconds for safety car
        ('m_carPosition',    	           ctypes.c_uint8),               # Car race position
        ('m_currentLapNum', 		       ctypes.c_uint8),               # Current lap number
        ('m_pitStatus',             	   ctypes.c_uint8),               # 0 = none, 1 = pitting, 2 = in pit area
        ('m_numPitStops',             	   ctypes.c_uint8),               # Number of pit stops taken in this race
        ('m_sector',                	   ctypes.c_uint8),               # 0 = sector1, 1 = sector2, 2 = sector3
        ('m_currentLapInvalid',     	   ctypes.c_uint8),               # Current lap invalid - 0 = valid, 1 = invalid
        ('m_penalties',             	   ctypes.c_uint8),               # Accumulated time penalties in seconds to be added
        ('m_totalWarnings',                ctypes.c_uint8),               # Accumulated number of warnings issued
        ('m_cornerCuttingWarnings',        ctypes.c_uint8),               # Accumulated number of corner cutting warnings issued
        ('m_numUnservedDriveThroughPens',  ctypes.c_uint8),               # Num drive through pens left to serve
        ('m_numUnservedStopGoPens',        ctypes.c_uint8),               # Num stop go pens left to serve
        ('m_gridPosition',          	   ctypes.c_uint8),               # Grid position the vehicle started the race in
        ('m_driverStatus',          	   ctypes.c_uint8),               # Status of driver - 0 = in garage, 1 = flying lap
                                                                          # 2 = in lap, 3 = out lap, 4 = on track
        ('m_resultStatus',                 ctypes.c_uint8),               # Result status - 0 = invalid, 1 = inactive, 2 = active
                                                                          # 3 = finished, 4 = didnotfinish, 5 = disqualified
                                                                          # 6 = not classified, 7 = retired
        ('m_pitLaneTimerActive',      	   ctypes.c_uint8),               # Pit lane timing, 0 = inactive, 1 = active
        ('m_pitLaneTimeInLaneInMS',    	   ctypes.c_uint16),              # If active, the current time spent in the pit lane in ms
        ('m_pitStopTimerInMS',         	   ctypes.c_uint16),              # Time of the actual pit stop in ms
        ('m_pitStopShouldServePen',    	   ctypes.c_uint8),               # Whether the car should serve a penalty at this stop
        ('m_speedTrapFastestSpeed',        ctypes.c_float),               # Fastest speed through speed trap for this car in kmph
        ('m_speedTrapFastestLap',          ctypes.c_uint8)                # Lap no the fastest speed was achieved, 255 = not set
    ]


class PacketLapData(ctypes.LittleEndianStructure):
    """
    Ctypes data structure for Lap data for all cars on track
    Size: 1285 bytes
    """
    _pack_ = 1
    _fields_ = [
        ('m_header', Header),                                             # Header
        ('m_lapsData', LapData * 22),                                     # Lap data for all cars on track
        ('m_timeTrialPBCarIdx', ctypes.c_uint8),                          # Index of Personal Best car in time trial (255 if invalid)
        ('m_timeTrialRivalCarIdx', ctypes.c_uint8)                        # Index of Rival car in time trial (255 if invalid)
    ]


class EventDataDetails(ctypes.LittleEndianStructure):
    """
    This packet gives details of events that happen during the course of a session.

    Frequency: When the event occurs
    """
    _pack_ = 1
    _fields_ = [

    ]


class PacketEventData(ctypes.LittleEndianStructure):
    """
    This packet gives details of events that happen during the course of the race.

    Frequency: When the event occurs
    """
    _pack_ = 1
    _fields_ = [
        ('m_header', Header),                         # Header
        ('m_eventStringCode', ctypes.c_uint8 * 4),    # Event string code, see below
        ('m_eventDetails', EventDataDetails),         # Event details - should be interpreted differently for each type
    ]


class ParticipantData(ctypes.LittleEndianStructure):
    """
    This is a list of participants in the race. If the vehicle is controlled by AI, then the name will be the driver
    name. If this is a multiplayer game, the names will be the Steam Id on PC, or the LAN name if appropriate.
    On Xbox One, the names will always be the driver name, on PS4 the name will be the LAN name if playing a LAN game,
    otherwise it will be the driver name.

    Frequency: Every 5 seconds
    """
    _pack_ = 1
    _fields_ = [
        ('m_aiControlled', ctypes.c_uint8),            # Whether the vehicle is AI (1) or Human (0) controlled
        ('m_driverId', ctypes.c_uint8),                # Driver id - see appendix
        ('m_networkId', ctypes.c_uint8),               # Network id – unique identifier for network players
        ('m_teamId', ctypes.c_uint8),                  # Team id - see appendix
        ('m_myTeam', ctypes.c_uint8),                  # My team flag – 1 = My Team, 0 = otherwise
        ('m_raceNumber', ctypes.c_uint8),              # Race number of the car
        ('m_nationality', ctypes.c_uint8),             # Nationality of the driver
        ('m_name', ctypes.c_char * 48),                # Name of participant in UTF-8 format - null terminated
                                                       # Will be truncated with (U+2026) if too long
        ('m_yourTelemetry', ctypes.c_uint8),           # The player's UDP setting, 0 = restricted, 1 = public
        ('m_showOnlineNames', ctypes.c_uint8),         # The player's show online names setting, 0 = off, 1 = on
        ('m_techLevel', ctypes.c_uint16),              # F1 World tech level
        ('m_platform', ctypes.c_uint8)                 # 1 = Steam, 3 = PlayStation, 4 = Xbox, 6 = Origin, 255 = unknown
    ]


class PacketParticipantsData(ctypes.LittleEndianStructure):
    """
    Ctypes data structure for participants data
    Size: 1350 bytes
    """
    _pack_ = 1
    _fields_ = [
        ('m_header', Header),                           # Header
        ('m_numActiveCars', ctypes.c_uint8),            # Number of cars in the data
        ('m_participants', ParticipantData * 22)
    ]


class CarSetupData(ctypes.LittleEndianStructure):
    """
    This packet details the car setups for each vehicle in the session. Note that in multiplayer games, other player
    cars will appear as blank, you will only be able to see your car setup and AI cars.

    Frequency: Every 2 seconds
    """
    _pack_ = 1
    _fields_ = [
        ('m_frontWing', ctypes.c_uint8),              # Front wing aero
        ('m_rearWing', ctypes.c_uint8),               # Rear wing aero
        ('m_onThrottle', ctypes.c_uint8),             # Differential adjustment on throttle (percentage)
        ('m_offThrottle', ctypes.c_uint8),            # Differential adjustment off throttle (percentage)
        ('m_frontCamber', ctypes.c_float),            # Front camber angle (suspension geometry)
        ('m_rearCamber', ctypes.c_float),             # Rear camber angle (suspension geometry)
        ('m_frontToe', ctypes.c_float),               # Front toe angle (suspension geometry)
        ('m_rearToe', ctypes.c_float),                # Rear toe angle (suspension geometry)
        ('m_frontSuspension', ctypes.c_uint8),        # Front suspension
        ('m_rearSuspension', ctypes.c_uint8),         # Rear suspension
        ('m_frontAntiRollBar', ctypes.c_uint8),       # Front anti-roll bar
        ('m_rearAntiRollBar', ctypes.c_uint8),        # Front anti-roll bar
        ('m_frontSuspensionHeight', ctypes.c_uint8),  # Front ride height
        ('m_rearSuspensionHeight', ctypes.c_uint8),   # Rear ride height
        ('m_brakePressure', ctypes.c_uint8),          # Brake pressure (percentage)
        ('m_brakeBias', ctypes.c_uint8),              # Brake bias (percentage)
        ('m_engineBraking', ctypes.c_uint8),          # Engine braking (percentage)
        ('m_rearLeftTyrePressure', ctypes.c_float),   # Rear left tyre pressure (PSI)
        ('m_rearRightTyrePressure', ctypes.c_float),  # Rear right tyre pressure (PSI)
        ('m_frontLeftTyrePressure', ctypes.c_float),  # Front left tyre pressure (PSI)
        ('m_frontRightTyrePressure', ctypes.c_float), # Front right tyre pressure (PSI)
        ('m_ballast', ctypes.c_uint8),                # Ballast
        ('m_fuelLoad', ctypes.c_float)                # Fuel load
    ]


class PacketCarSetupData(ctypes.LittleEndianStructure):
    """
    Ctypes data structure for Cars setup
    Frequency: 2 per second
    Size: 1133 bytes

    """
    _pack_ = 1
    _fields_ = [
        ('m_header', Header),  # Header
        ('m_carSetups', CarSetupData * 22),
        ('m_nextFrontWingValue', ctypes.c_float)   # Value of front wing after next pit stop - player only
    ]


class CarTelemetryData(ctypes.LittleEndianStructure):
    """
    This packet details telemetry for all the cars in the race. It details various values that would be recorded on the
    car such as speed, throttle application, DRS etc.

    Frequency: Rate as specified in menus
    """
    _pack_ = 1
    _fields_ = [
        ('m_speed', ctypes.c_uint16),                        # Speed of car in kilometres per hour
        ('m_throttle', ctypes.c_float),                      # Amount of throttle applied (0 to 100)
        ('m_steer', ctypes.c_float),                         # Steering (-100 (full lock left) to 100 (full lock right))
        ('m_brake', ctypes.c_float),                         # Amount of brake applied (0 to 100)
        ('m_clutch', ctypes.c_uint8),                        # Amount of clutch applied (0 to 100)
        ('m_gear', ctypes.c_int8),                           # Gear selected (1-8, N=0, R=-1)
        ('m_engineRPM', ctypes.c_uint16),                    # Engine RPM
        ('m_drs', ctypes.c_uint8),                           # 0 = off, 1 = on
        ('m_revLightsPercent', ctypes.c_uint8),              # Rev lights indicator (percentage)
        ('m_revLightsBitValue', ctypes.c_uint16),            # Rev lights (bit 0 = leftmost LED, bit 14 = rightmost LED)
        ('m_brakesTemperature', ctypes.c_uint16 * 4),        # Brakes temperature (celsius)
        ('m_tyresSurfaceTemperature', ctypes.c_uint8 * 4),   # Tyres surface temperature (celsius)
        ('m_tyresInnerTemperature', ctypes.c_uint8 * 4),     # Tyres inner temperature (celsius)
        ('m_engineTemperature', ctypes.c_uint16),            # Engine temperature (celsius)
        ('m_tyresPressure', ctypes.c_float * 4),             # Tyres pressure (PSI)
        ('m_surfaceType', ctypes.c_uint8 * 4)                # Driving surface, see appendices
    ]


class PacketCarTelemetryData(ctypes.LittleEndianStructure):
    """
    Ctypes data structure for Cars telemetry Data
    Frequency: Rate as specified in menus
    Size: 1352 bytes
    """
    _pack_ = 1
    _fields_ = [
        ('m_header', Header),                                # Header
        ('m_carTelemetryData', CarTelemetryData * 22),
        ('m_mfdPanelIndex', ctypes.c_uint8),                 # Index of MFD panel open - 255 = MFD closed
        ('m_mfdPanelIndexSecondaryPlayer', ctypes.c_uint8),  # Index of MFD panel open for secondary player - 255 = MFD closed
        ('m_suggestedGear', ctypes.c_int8)                   # Suggested gear for the player (1-8)
    ]


class CarStatusData(ctypes.LittleEndianStructure):
    """
    This packet details car statuses for all the cars in the race.
    Frequency: Rate as specified in menus
    Size: 1239 bytes
    """
    _pack_ = 1
    _fields_ = [
        ('m_tractionControl', ctypes.c_uint8),          # 0 (off) - 2 (high)
        ('m_antiLockBrakes', ctypes.c_uint8),           # 0 (off) - 1 (on)
        ('m_fuelMix', ctypes.c_uint8),                  # Fuel mix - 0 = lean, 1 = standard, 2 = rich, 3 = max
        ('m_frontBrakeBias', ctypes.c_uint8),           # Front brake bias (percentage)
        ('m_pitLimiterStatus', ctypes.c_uint8),         # Pit limiter status - 0 = off, 1 = on
        ('m_fuelInTank', ctypes.c_float),               # Current fuel mass
        ('m_fuelCapacity', ctypes.c_float),             # Fuel capacity
        ('m_fuelRemainingLaps', ctypes.c_float),        # Fuel remaining in terms of laps (value on MFD)
        ('m_maxRPM', ctypes.c_uint16),                    # Cars max RPM, point of rev limiter
        ('m_idleRPM', ctypes.c_uint16),                   # Cars idle RPM
        ('m_maxGears', ctypes.c_uint8),                 # Maximum number of gears
        ('m_drsAllowed', ctypes.c_uint8),               # 0 = not allowed, 1 = allowed, -1 = unknown
        ('m_drsActivationDistance', ctypes.c_uint16),   # 0 = DRS not available, non-zero - DRS will be available
        ('m_actualTyreCompound', ctypes.c_uint8),       # F1 Modern - 16 = C5, 17 = C4, 18 = C3, 19 = C2, 20 = C1
   					                                    # 21 = C0, 7 = inter, 8 = wet
   					                                    # F1 Classic - 9 = dry, 10 = wet
   					                                    # F2 - 11 = super soft, 12 = soft, 13 = medium, 14 = hard
   					                                    # 15 = wet
        ('m_visualTyreCompound', ctypes.c_uint8),       # F1 visual (can be different from actual compound)
                                                        # 16 = soft, 17 = medium, 18 = hard, 7 = inter, 8 = wet
                                                        # F1 Classic – same as above
                                                        # F2 ‘19, 15 = wet, 19 – super soft, 20 = soft
                                                        # 21 = medium , 22 = hard
        ('m_tyresAgeLaps', ctypes.c_uint8),             # Age in laps of the current set of tyres
        ('m_vehicleFiaFlags', ctypes.c_int8),           # -1 = invalid/unknown, 0 = none, 1 = green
                                                        # 2 = blue, 3 = yellow
        ('m_enginePowerICE', ctypes.c_float),           # Engine power output of ICE (W)
        ('m_enginePowerMGUK', ctypes.c_float),          # Engine power output of MGU-K (W)
        ('m_ersStoreEnergy', ctypes.c_float),           # ERS energy store in Joules
        ('m_ersDeployMode', ctypes.c_uint8),            # ERS deployment mode, 0 = none, 1 = medium
                                                        # 2 = hotlap, 3 = overtake
        ('m_ersHarvestedThisLapMGUK', ctypes.c_float),  # ERS energy harvested this lap by MGU-K
        ('m_ersHarvestedThisLapMGUH', ctypes.c_float),  # ERS energy harvested this lap by MGU-H
        ('m_ersDeployedThisLap', ctypes.c_float),       # ERS energy deployed this lap
        ('m_networkPaused', ctypes.c_uint8),            # Whether the car is paused in a network game
    ]


class PacketCarStatusData(ctypes.LittleEndianStructure):
    """
    Ctypes data structure for cars status data
    Frequency: Rate as specified in menus
    Size: 1239 bytes
    """
    _pack_ = 1
    _fields_ = [
        ('m_header', Header),                              # Header
        ('m_carStatusData', CarStatusData * 22)
    ]
