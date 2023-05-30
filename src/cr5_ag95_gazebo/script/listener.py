import rospy
from control_msgs.msg import FollowJointTrajectoryActionGoal, FollowJointTrajectoryGoal
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

def callback_function(data):
    # 处理获取到的数据
    joints=data.goal.trajectory.joint_names
    points=data.goal.trajectory.points
    print("1")
    with open("/home/hisen/Project/ROS/cr5_dmp/src/cr5_ag95_gazebo/script/record.txt","a") as file:
        for point in points:
            file.write(str(point.velocities) + " "+"\n")
            file.write(str(point.positions) + " "+"\n")
            file.write(str(point.accelerations) + " "+"\n")
    # print(data)

def main():
    # 初始化ROS节点
    rospy.init_node('listener')

    # 订阅要获取的topic
    rospy.Subscriber('/cr5_robot/joint_controller/follow_joint_trajectory/goal', FollowJointTrajectoryActionGoal, callback_function)

    # 保持节点运行
    rospy.spin()

if __name__ == '__main__':
    main()
