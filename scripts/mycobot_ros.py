#!/usr/bin/env python2
import time
import rospy
from myCobotROS.srv import *

from pymycobot.mycobot import MyCobot

mc = None


def create_handle():
    global mc
    rospy.init_node('mycobot_services')
    rospy.loginfo('start ...')
    port = rospy.get_param('~port')
    baud = rospy.get_param('~baud')
    rospy.loginfo("%s,%s" % (port, baud))
    mc = MyCobot(port, baud)


def create_services():
    rospy.Service('set_joint_angles', SetAngles, set_angles)
    rospy.Service('get_joint_angles', GetAngles, get_angles)
    rospy.Service('set_joint_coords', SetCoords, set_coords)
    rospy.Service('get_joint_coords', GetCoords, get_coords)
    rospy.Service('switch_gripper_status', GripperStatus, switch_status)
    rospy.loginfo('ready')
    rospy.spin()


def set_angles(req):
    angles = [
        req.joint_1,
        req.joint_2,
        req.joint_3,
        req.joint_4,
        req.joint_5,
        req.joint_6,
    ]
    sp = req.speed

    if mc:
        mc.send_angles(angles, sp)


def get_angles(req):
    if mc:
        angles = mc.get_angles()
        print(angles)
        return GetAnglesResponse(*angles)


def set_coords(req):
    coords = [
        req.x,
        req.y,
        req.z,
        req.rx,
        req.ry,
        req.rz,
    ]
    sp = req.speed
    mod = req.model

    if mc:
        mc.send_coords(coords, sp, mod)


def get_coords(req):
    if mc:
        coords = mc.get_coords()
        return GetCoordsResponse(*coords)


def switch_status(req):
    if mc:
        if req.Status:
            print(1)
            mc.set_gripper_state(0, 80)
        else:
            print(2)
            mc.set_gripper_state(1, 80)


robot_msg = '''
MyCobot Status
--------------------------------
Joint Limit:
    joint 1: -170 ~ +170
    joint 2: -170 ~ +170
    joint 3: -170 ~ +170
    joint 4: -170 ~ +170
    joint 5: -170 ~ +170
    joint 6: -180 ~ +180

Connect Status: %s

Servo Infomation: %s

Servo Temperature: %s

Atom Version: %s
'''


def output_robot_message():
    connect_status = False
    servo_infomation = 'unknown'
    servo_temperature = 'unknown'
    atom_version = 'unknown'

    if mc:
        cn = mc.is_controller_connected()
        if cn == 1:
            connect_status = True
        time.sleep(.1)
        si = mc.is_all_servo_enable()
        if si == 1:
            servo_infomation = 'all connected'

    print(robot_msg % (connect_status, servo_infomation,
          servo_temperature, atom_version))


if __name__ == '__main__':
    # print(MyCobot.__dict__)
    create_handle()
    output_robot_message()
    create_services()
