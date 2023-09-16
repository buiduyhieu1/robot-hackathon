from mindstorms import MSHub, Motor, MotorPair, ColorSensor, DistanceSensor
from mindstorms.control import wait_for_seconds, Timer, wait_until

hub = MSHub()
motor_pair = MotorPair('C', 'A')
left_motor = Motor('C')
right_motor = Motor('A')
claw_motor = Motor('B')
# arms_and_head_motor = Motor('D')
# color_sensor = ColorSensor('E')
distance_sensor = DistanceSensor('F')
cellSize = 15

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
motor_pair.set_default_speed(70)

hub.motion_sensor.reset_yaw_angle()
print("Starting patrolling...")
wait_for_seconds(2)

right = 1
left = -1

maxDistance = 200
posEye = 0

steps = 0
#hub.speaker.play_sound('Scanning')
def get_distance():
    d = distance_sensor.get_distance_cm()
    if d == None:
        d = distance_sensor.get_distance_cm()
        if d == None:
            d = maxDistance
    return d

def get_moved():
    return -(left_motor.get_degrees_counted()*10//192)

def eye_right():
    global posEye
    claw_motor.run_for_rotations(0.24*(posEye+1), 50)
    posEye = -1;

def eye_left():
    global posEye
    claw_motor.run_for_rotations(0.24*(posEye-1), 50)
    posEye = 1;

def eye_straight():
    global posEye
    claw_motor.run_for_rotations(0.24*(posEye), 50)
    posEye = 0;

def robot_turn(turn):
    degrees = 178
    left_motor.set_degrees_counted(0)
    motor_pair.start(steering = turn*100,speed = 60)
    if turn == right:
        degrees = 178

    def turn_angle():
        if get_distance() < 6:
            motor_pair.stop()
            return True
        angle = -turn * left_motor.get_degrees_counted()
        if angle > 100:
            motor_pair.start(steering = turn*100,speed = 30)            
        return  angle > degrees
    
    wait_until(turn_angle)
    motor_pair.stop()

distanceToStop = 15
distanceToWall = 9

pathTurns = [-1,-1,1,-1,1,-1,1,1,1,1]
while True:
    count = 0
    while count == 0:
        distanceToGo = get_distance() - distanceToStop
        if distanceToGo < 8 and distanceToGo > -8:
            distanceToGo = 0
        print("distance to go straght: ",distanceToGo)
        turn = left
        left_motor.set_degrees_counted(0)
        position = 0;
        distanceBefore = 0;
        distanceAfter = 0;
        turnAngle = 0;
        runSpeed = 50
        eye_right()
        distanceBefore = get_distance()
        steer = get_distance() - distanceToWall
        if steer < -5 or steer > 5 :
            steer = 0
        if distanceToGo < 30:
            runSpeed = 30
        motor_pair.start(steering = steer, speed = runSpeed)       
        while get_moved() <= (distanceToGo):
            steer = get_distance() - distanceToWall
            if steer < -5 or steer > 5 :
                steer = 0
            if get_moved() == (position+1)*cellSize and turn == left:
                position += 1
                turnAngle = get_distance() - distanceBefore
                if turnAngle > 10 or turnAngle < -10:
                    turnAngle = 0
                motor_pair.start(steering = turnAngle*10 + steer, speed = runSpeed)
            if position != 0 and get_moved() == position*cellSize + 5:
                motor_pair.start(steering = steer,speed = runSpeed)
                distanceBefore = get_distance()

            if (position > 0) and (get_distance() > 40) and (turn == left):
                distanceToGo = get_moved() + 10
                turn = right
            if get_moved() == distanceToGo - 10:
                runSpeed = 30
                motor_pair.start(steering = 0, speed = runSpeed)
            if get_distance() < 5:
                count = 1
                break
            # print("moved: ",get_moved(),"distance: ",get_distance(), "turn angle: ",turnAngle)

        eye_straight()
        if get_distance() < 30 and count == 0:
            motor_pair.move(amount = get_distance() - (distanceToStop - 5), speed = 20)
        motor_pair.stop()
        if count == 0:
            robot_turn(turn)
        if get_distance() < 6:
            count = 1

    print ("Stoped!")
    wait_for_seconds(2)
    # claw_motor.run_for_rotations(0.25, 50)
    eye_straight();
    # arms_and_head_motor.run_for_degrees(150)
    hub.right_button.wait_until_pressed()

motor_pair.stop()
#hub.speaker.play_sound('Mission Accomplished')

