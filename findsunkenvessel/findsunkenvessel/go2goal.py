#!/usr/bin/env python3
from numpy import rate
import rclpy
from rclpy.node import Node
import time
import geometry_msgs.msg as geometry
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import Image # Image is the message type
from cv_bridge import CvBridge # Package to convert between ROS and OpenCV Images
import cv2 # OpenCV library
from nav_msgs.msg import Odometry # This represents an estimate of a position and velocity in free space.  
import os


class rovGo2Goal(Node):
    def __init__(self):
        super().__init__("rexrov_go_to_goal")
        
        self.global_pose = Odometry()
        
        self.tolerance = 0.1


        self.cmdpose_pub = self.create_publisher(PoseStamped, '/rexrov/cmd_pose', 10)
        self.pose_subs = self.create_subscription(Odometry, '/rexrov/pose_gt', self.odometry_callback, 10)
        

     
    def odometry_callback(self, msg):
        self.global_pose.pose.pose.position = msg.pose.pose.position
        self.global_pose.pose.pose.orientation = msg.pose.pose.orientation
        
    
    def move2goal(self):
        msg = PoseStamped()
        msg.header.frame_id = "world"
        msg.pose.position.x = 120.0
        msg.pose.position.y = 135.0
        msg.pose.position.z = -18.0
        msg.pose.orientation.x = 127.0
        msg.pose.orientation.y = 0.0
        msg.pose.orientation.z = 0.5
        msg.pose.orientation.w = 1.0
        
        self.cmdpose_pub.publish(msg)
        
        # self.get_logger().info('Publishing: Position(x:"%f", y:"%f", z:"%f"), Orientation(x:"%f", y:"%f", z:"%f", w:"%f")' % (msg.pose.position.x, msg.pose.position.y, msg.pose.position.z, msg.pose.orientation.x, msg.pose.orientation.y, msg.pose.orientation.z, msg.pose.orientation.w))
        self.get_logger().info('Going to goal...')
        
    def back2spawn(self):
        msg = PoseStamped()
        msg.header.frame_id = "world"
        msg.pose.position.x = 0.0 
        msg.pose.position.y = 0.0
        msg.pose.position.z = -1.0
        msg.pose.orientation.x = 0.0
        msg.pose.orientation.y = 0.0
        msg.pose.orientation.z = 0.0
        msg.pose.orientation.w = 1.0
        
        self.cmdpose_pub.publish(msg)
        
        # self.get_logger().info('Publishing: Position(x:"%f", y:"%f", z:"%f"), Orientation(x:"%f", y:"%f", z:"%f", w:"%f")' % (msg.pose.position.x, msg.pose.position.y, msg.pose.position.z, msg.pose.orientation.x, msg.pose.orientation.y, msg.pose.orientation.z, msg.pose.orientation.w))
        self.get_logger().info('Backing to home...')
          
    def check_goal(self):
        if((self.global_pose.pose.pose.position.x - ( 120.0 ) < self.tolerance)   and
           (self.global_pose.pose.pose.position.y - ( 135.0) < self.tolerance)    and
           (self.global_pose.pose.pose.position.z - ( -18.0) < self.tolerance)    and
           (self.global_pose.pose.pose.orientation.x - ( 127.0) < self.tolerance) and
           (self.global_pose.pose.pose.orientation.y - ( 0.0) < self.tolerance)   and
           (self.global_pose.pose.pose.orientation.z - ( 0.5) < self.tolerance)   and
           (self.global_pose.pose.pose.orientation.w - ( 1.0) < self.tolerance) ):
            return True
        return False
    def check_init(self):
        if((self.global_pose.pose.pose.position.x - (0.0) < self.tolerance)   and
          (self.global_pose.pose.pose.position.y - (0.0) < self.tolerance)    and
          (self.global_pose.pose.pose.position.z - (-1.0) < self.tolerance)    and
          (self.global_pose.pose.pose.orientation.x - (0.0) < self.tolerance) and
          (self.global_pose.pose.pose.orientation.y - (0.0) < self.tolerance)   and
          (self.global_pose.pose.pose.orientation.z - (0.0) < self.tolerance)   and
          (self.global_pose.pose.pose.orientation.w - (1.0) < self.tolerance)):
           return True
        return False
            
        
        
class ImagePrint(Node):

    def __init__(self):
        super().__init__('take_picture')

        self.pose_subs = self.create_subscription(Image, '/rexrov/camera/image_raw', self.listener_callback, 10)

        # Used to convert between ROS and OpenCV images
        self.br = CvBridge()
        self.current_frame = None

    def listener_callback(self, data):
        # Convert ROS Image message to OpenCV image
        self.current_frame = self.br.imgmsg_to_cv2(data)

    def save_picture(self):
        img_rgb = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2RGB)
        cv2.imwrite(os.path.join(os.getcwd(), "imagem.jpg"), img_rgb)

        self.get_logger().info('Taking picture...')
        
        

def main(args = None):
    rclpy.init(args=args)
    node = rovGo2Goal()
    image_subscriber = ImagePrint()
    loop = False
    #rate = node.create_rate(2)
    while(loop == False):       
        node.move2goal()
        rclpy.spin_once(image_subscriber)
        
        time.sleep(0.5)
        rclpy.spin_once(node)
        if(node.check_goal()):
            image_subscriber.save_picture()
            loop = True   
            break

    while(loop == True):        
        node.back2spawn()
        time.sleep(0.5)
        if(node.check_init()):
            node.destroy_node()
            print('Arrived home!')
        rclpy.spin_once(node)
    
    rclpy.shutdown()

if __name__ == "__main__":
    main()

            