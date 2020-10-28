import rospy
from std_msgs.msg import Int8Multiarray


def callback_move(data):
    rospy.loginfo(rospy.get_caller_id() + "Message from: ", data.data)


def listener_move():
    rospy.init_node('iReceiveWheelValues', anonymous=True)
    rospy.Subscriber("chatter", Int8Multiarray, callback_move)
    rospy.spin()


if __name__ == '__main__':
    listener_move()

