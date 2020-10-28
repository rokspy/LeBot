import rospy
from std_msgs.msg import Int8Multiarray


def talker_move():
    pub = rospy.Publisher('wheel_chatter', Int8Multiarray, queue_size=10)
    rospy.init_node('wheel_talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    msg = Int8Multiarray()
    msg.wheelSpeed = [4, 2, 3]
    while not rospy.is_shutdown():
        rospy.loginfo(msg)
        pub.publish(msg)
        rate.sleep()


if __name__ == '__main__':
    try:
        talker_move()
    except rospy.ROSInterruptException:
        pass
