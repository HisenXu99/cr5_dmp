from dmp_discrete import dmp_discrete
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
# import sys 
# sys.path.append('..')

def openreadtxt(file_name):
    joints = []
    joints_all = []                         #每个joint的位置，速度，加速度。
    joints_all_position = []                #每个joint的位置。
    velocities = []
    accelerations = []
    for i in range(1,7):
        exec('joint{}_positions=[]'.format(i))
        exec('joint{}_velocities=[]'.format(i))
        exec('joint{}_accelerations=[]'.format(i))
        exec('joint{}=[]'.format(i))

    file = open(file_name,'r')  #打开文件
    file_data = file.readlines() #读取所有行
    for i,row in enumerate(file_data,1):
        row.strip('[\n,\t]')
        # print(row)
        if(i%3==1):
            positions = row.split() #按‘ ’切分每行的数据
            for i,position in enumerate(positions,1):
                exec('joint{}_positions.append(np.float64(position))'.format(i))
        elif(i%3==2):
            velocities = row.split() #按‘ ’切分每行的数据
            for i,velocity in enumerate(velocities,1):
                exec('joint{}_velocities.append(np.float64(velocity))'.format(i))
        else:
            accelerations = row.split() #按‘ ’切分每行的数据
            for i,acceleration in enumerate(accelerations,1):
                exec('joint{}_accelerations.append(np.float64(acceleration))'.format(i))
    for i in range(1,7): 
        exec('joint{}.append(joint{}_positions)'.format(i,i))
        exec('joint{}.append(joint{}_velocities)'.format(i,i))
        exec('joint{}.append(joint{}_accelerations)'.format(i,i))
    for i in range(1,7):
        exec('joints.append(joint{})'.format(i))
    for i in range(1,7): 
        exec('joints_all.append(joint{}_positions)'.format(i))
        exec('joints_all.append(joint{}_velocities)'.format(i))
        exec('joints_all.append(joint{}_accelerations)'.format(i))
        exec('joints_all_position.append(joint{}_velocities)'.format(i))
    return joints_all_position

def generate_figure(dmp,reference_trajectory):
    reproduced_trajectory, _, _ = dmp.reproduce()
    fig = plt.figure()
    ax=Axes3D(fig)
    plt.plot(reference_trajectory[0,:], reference_trajectory[1,:], reference_trajectory[2,:], 'g', label='reference')
    plt.plot(reproduced_trajectory[:,0], reproduced_trajectory[:,1], reproduced_trajectory[:,2], 'r--', label='reproduce')
    plt.legend()
    # fig = plt.figure()
    plt.subplot(311)
    plt.plot(reference_trajectory[0,:], 'g', label='reference')
    plt.plot(reproduced_trajectory[:,0], 'r--', label='reproduce')
    plt.legend()

    plt.subplot(312)
    plt.plot(reference_trajectory[1,:], 'g', label='reference')
    plt.plot(reproduced_trajectory[:,1], 'r--', label='reproduce')
    plt.legend()

    plt.subplot(313)
    plt.plot(reference_trajectory[2,:], 'g', label='reference')
    plt.plot(reproduced_trajectory[:,2], 'r--', label='reproduce')
    plt.legend()
    plt.draw()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()

    pass

def call():
    trajectory = openreadtxt('record.txt')
    reference_trajectory = np.array(trajectory)
    data_dim = reference_trajectory.shape[0]
    data_len = reference_trajectory.shape[1]
    y0 = reference_trajectory[:,0].copy()
    dmp = dmp_discrete(n_dmps=data_dim, n_bfs=1000, dt=1.0/data_len)
    dmp.learning(reference_trajectory)
    reproduced_trajectory, _, _ = dmp.reproduce()
    return reproduced_trajectory
    pass

if __name__=="__main__":
    trajectory = openreadtxt('cr5_ag95_gazebo/script/dmp/record.txt')
    print(trajectory)
    reference_trajectory = np.array(trajectory)
    data_dim = reference_trajectory.shape[0]
    data_len = reference_trajectory.shape[1]
    print(data_dim)
    print(data_len) 
    y0 = reference_trajectory[:,0].copy()
    dmp = dmp_discrete(n_dmps=data_dim, n_bfs=1000, dt=1.0/data_len)
    dmp.learning(reference_trajectory)

    generate_figure(dmp,reference_trajectory)
