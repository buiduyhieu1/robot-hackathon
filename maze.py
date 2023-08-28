from mindstorms import MSHub, Motor, MotorPair, ColorSensor, DistanceSensor
from mindstorms.control import wait_for_seconds, Timer, wait_until

hub = MSHub()
motor_pair = MotorPair('C', 'A')
left_motor = Motor('C')
right_motor = Motor('A')
claw_motor = Motor('B')
arms_and_head_motor = Motor('D')
color_sensor = ColorSensor('E')
distance_sensor = DistanceSensor('F')
cellSize = 40
maze = [[1,1,1,2,1,3,1,4,1,5,1,6,1,7,1,8,1,9,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
        [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
        [4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
        [5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
        [6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
        [7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
        [8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
        [9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,1,1,2,1,3,1,4,1,5,1,6,1,7,1,8,1,9,1]]

# maze = [["0","0","0","0"],["0","0","0","0"]]
# This is Blast’s animation.
animation = {
    'Scanning': [
        '00000:00000:56789:00000:00000',
        '00000:00000:45698:00000:00000',
        '00000:00000:34987:00000:00000',
        '00000:00000:29876:00000:00000',
        '00000:00000:98765:00000:00000',
        '00000:00000:89654:00000:00000',
        '00000:00000:78943:00000:00000',
        '00000:00000:67892:00000:00000'
    ]
}

hub.status_light.on('red')
hub.light_matrix.set_orientation('left')
hub.light_matrix.start_animation(animation['Scanning'], 5, True, 'overlay')

# This resets the relative position to mark the starting position.
right_motor.set_degrees_counted(0)
# claw_motor.run_for_seconds(1)
claw_motor.set_degrees_counted(0)
motor_pair.set_default_speed(20)

hub.motion_sensor.reset_yaw_angle()
print("Starting patrolling...")
wait_for_seconds(2)

right = 1
left = -1

maxDistance = 200
posX = 17
posY = 9
posDirX = -1
posDirY = 0
posEye = 0

steps = 0
#hub.speaker.play_sound('Scanning')
def get_distance():
    d = distance_sensor.get_distance_cm()
    if d == None:
        d = maxDistance
    return d

def get_moved():
    return -(left_motor.get_degrees_counted()*10//192)

def eye_right():
    global posEye
    claw_motor.run_for_rotations(0.25*(posEye+1), 50)
    posEye = -1;

def eye_left():
    global posEye
    claw_motor.run_for_rotations(0.25*(posEye-1), 50)
    posEye = 1;

def eye_straight():
    global posEye
    claw_motor.run_for_rotations(0.25*(posEye), 50)
    posEye = 0;

def maze_update():
    xSign = -posDirY*posEye
    ySign = posDirX*posEye
    if posEye == 0:
        xSign = posDirX
        ySign = posDirY

    cells = get_distance()//cellSize
    x = posX + xSign*(cells*2 + 1)
    y = posY + ySign*(cells*2 + 1)

    print(cells,xSign,x,ySign,y)
    if (x < 18) and (y < 18):
        maze[x][y] = 1

def robot_turn(turn):
    global posDirX
    global posDirY

    xSign =posDirY*turn
    ySign = -posDirX*turn

    posDirX = xSign
    posDirY = ySign

    left_motor.set_degrees_counted(0)
    motor_pair.start(steering = turn*100)
    if turn == 1:
        degrees = 174
    else:
        degrees = 173
    def turn_angle():
        return -turn * left_motor.get_degrees_counted() > 174
    wait_until(turn_angle)
    motor_pair.stop()


# arms_and_head_motor.run_for_degrees(-150)
maze_update()
maze[posX][posY] = 8

pathTurns = [-1,-1,1,-1,1,-1,1,1,1,1]
for count in range(2):
    distance = get_distance()
    left_motor.set_degrees_counted(0)
    motor_pair.start()
    position = 0;
    while get_moved() <= (distance - 10):
        if get_moved() > (position*cellSize + cellSize/2):
            position += 1
            posX += posDirX*2
            posY += posDirY*2
            eye_right()
            maze_update()
            eye_left()
            maze_update()
        if get_moved() == (position*cellSize + cellSize/2 - 2):
            eye_straight()

        if get_distance() < 6:
            break
        # print("moved: ",get_moved(),"distance: ",get_distance())
    eye_straight()
    motor_pair.stop()
    
    maze[posX][posY] = 8
    for y in maze:
        print(y)

    # robot_turn(pathTurns[count])


wait_for_seconds(2)
# claw_motor.run_for_rotations(0.25, 50)
eye_straight();
# arms_and_head_motor.run_for_degrees(150)


motor_pair.stop()
#hub.speaker.play_sound('Mission Accomplished')

