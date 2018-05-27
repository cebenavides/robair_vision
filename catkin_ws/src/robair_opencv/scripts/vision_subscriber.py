#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist

velocity_publisher = 0

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)

    if data.data == "bottle":
        vel_msg = Twist()

        #Since we are moving just in x-axis
        vel_msg.linear.x = 0
        vel_msg.linear.y = 0
        vel_msg.linear.z = 0
        vel_msg.angular.x = 1
        vel_msg.angular.y = 1
        vel_msg.angular.z = 0

        #Publish the velocity
        velocity_publisher.publish(vel_msg)

def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('vision_listener', anonymous=True)

    rospy.Subscriber('vision', String, callback)

    velocity_publisher = rospy.Publisher('/turtlesim_node/cmd_vel', Twist, queue_size=10)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
