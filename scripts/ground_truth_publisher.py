#!/usr/bin/env python3

import rospy
import tf
from apriltag_ros.msg import AprilTagDetectionArray
from nav_msgs.msg import Odometry

# TODO: what if no detections are made? or if it is not tag_0

class GroundTruthPublisher():

    def __init__(self):
        rospy.init_node('ground_truth_publisher', anonymous=False)

        self.base_frame_id = rospy.get_param("~base_frame_id", "base_footprint")
        self.odom_frame_id = rospy.get_param("~odom_frame_id", "ground")

        self.ground_truth_pub = rospy.Publisher('/base_pose_ground_truth', Odometry, queue_size=128)
        rospy.wait_for_message('/tag_detections', AprilTagDetectionArray)
        rospy.Subscriber('/tag_detections', AprilTagDetectionArray, self.pub_ground_truth)
        rospy.loginfo("Publishing ground truth on /base_pose_ground_truth")

        self.tf_pub = tf.TransformBroadcaster()

    def pub_ground_truth(self, msg):
        odom = Odometry()
        if msg.detections:
            odom.header = msg.header
            odom.header.frame_id = self.odom_frame_id
            odom.child_frame_id = self.base_frame_id
            odom.pose = msg.detections[0].pose.pose
            x = odom.pose.pose.position.x
            y = odom.pose.pose.position.y
            self.ground_truth_pub.publish(odom)
            quat = tf.transformations.quaternion_from_euler(0, 0, 0)
            # april already sends transform, so not needed. we can take tf from the move_tf, so this script and publishing of ground_truth might be unnecessary
            #self.tf_pub.sendTransform((x,y,0), quat, odom.header.stamp, odom.child_frame_id, odom.header.frame_id)


if __name__ == '__main__':
    try:
        GroundTruthPublisher()
        rospy.spin()
    except:
        pass
