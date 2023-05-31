#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import actionlib

from control_msgs.msg import FollowJointTrajectoryAction, FollowJointTrajectoryGoal
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

import sys
sys.path.append('cr5_ag95_gazebo/script/dmp')
import process

class TrajectoryDemo():
    def __init__(self,trajectory):
        rospy.init_node('trajectory_demo')
        
        # # 是否需要回到初始化的位置
        reset = rospy.get_param('~reset', True)
        
        # 机械臂中joint的命名
        arm_joints = ['joint1',
                      'joint2',
                      'joint3', 
                      'joint4',
                      'joint5',
                      'joint6']
        
        if reset:
            # 如果需要回到初始化位置，需要将目标位置设置为初始化位置的六轴角度
            arm_goal  = [0, 0, 0, 0, 0, 0]

        else:
            # 如果不需要回初始化位置，则设置目标位置的六轴角度
            arm_goal  = [-0.3, -1.0, 0.5, 0.8, 1.0, -0.7]
    
        # 连接机械臂轨迹规划的trajectory action server
        rospy.loginfo('Waiting for arm trajectory controller...')       
        arm_client = actionlib.SimpleActionClient('cr5_robot/joint_controller/follow_joint_trajectory', FollowJointTrajectoryAction)
        arm_client.wait_for_server()        
        rospy.loginfo('...connected.')  
    
        # 使用设置的目标位置创建一条轨迹数据
        arm_trajectory = JointTrajectory()
        arm_trajectory.joint_names = arm_joints
        # arm_trajectory.points.append(JointTrajectoryPoint())
        # arm_trajectory.points[0].positions = arm_goal
        # arm_trajectory.points[0].velocities = [0.0 for i in arm_joints]
        # arm_trajectory.points[0].accelerations = [0.0 for i in arm_joints]
        # arm_trajectory.points[0].time_from_start = rospy.Duration(3.0)
        print()

        for i,val in enumerate(trajectory[0]):   #data
            arm_trajectory.points.append(JointTrajectoryPoint())
            positions=[]
            velocities=[]
            accelerations= []
            for j,_ in enumerate(trajectory[0][0]):   #type
                positions.append(trajectory[0][i][j])
                velocities.append(trajectory[1][i][j])
                accelerations.append(trajectory[2][i][j])
            # for j,point in enumerate(row):   #type
            # positions.append(point)
            # for j,point in enumerate(row):   #type
            #     if(j%3==0): 
            #         positions.append(point)
            #     if(j%3==0): 
            #         velocities.append(point)
            #     if(j%3==2): 
            #         accelerations.append(point)
            arm_trajectory.points[i].positions = positions
            arm_trajectory.points[i].velocities = velocities
            arm_trajectory.points[i].accelerations = accelerations
            arm_trajectory.points[i].time_from_start = rospy.Duration(0.02*i)
            print(arm_trajectory.points[i])

        print(arm_trajectory.points)
    
        rospy.loginfo('Moving the arm to goal position...')
        
        # 创建一个轨迹目标的空对象
        arm_goal = FollowJointTrajectoryGoal()
        
        # 将之前创建好的轨迹数据加入轨迹目标对象中
        arm_goal.trajectory = arm_trajectory
        
        # 设置执行时间的允许误差值
        arm_goal.goal_time_tolerance = rospy.Duration(0.0)
    
        # 将轨迹目标发送到action server进行处理，实现机械臂的运动控制
        arm_client.send_goal(arm_goal)

        # 等待机械臂运动结束
        arm_client.wait_for_result(rospy.Duration(5.0))
        
        rospy.loginfo('...done')
        
if __name__ == '__main__':
    try:
        trajectory = process.call(load='cr5_ag95_gazebo/script/parameter.txt')
        print(trajectory)
        TrajectoryDemo(trajectory)
    except rospy.ROSInterruptException:
        pass
    