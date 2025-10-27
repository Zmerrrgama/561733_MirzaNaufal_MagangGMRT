import math
import numpy as nm
import matplotlib.pyplot as plt

def UI():
    print("\n")
    print("1. Kinematic Formula (DoF 2)")
    print("2. Kinematic Formula (DoF N)")
    print("3. Show Arm in 2D")
    print("4. Show Arm in 3D")
    print("5. Inverse Kinematic (DoF 2)")
    print("0. Exit")
    print("\n")

def takematrix():
    n_str=input("How many DoF: ")
    n=int(n_str)
    allangle=[]
    alllength=[]
    for i in range(n):
        angle_str=input(f"Enter Angle No.{i+1} in Degree: ")
        angle=math.radians(int(angle_str))
        allangle.append(angle)
        
        length_str=input(f"Enter Length No.{i+1} in cm: ")
        length=int(length_str)
        alllength.append(length)
    
    return n, alllength, allangle

def kinematicdof2(): #hasil study , NIM 25/561733/PA/23684, Sehingga Femur=33 dan Tibia=84
    a=math.radians(30)   
    l1=33
    b=math.radians(40)
    l2=84    
    
    H01=nm.matrix(([math.cos(a), -math.sin(a), 0],
                    [math.sin(a), math.cos(a), 0],
                    [0, 0, 1]))

    H12=nm.matrix(([1, 0, l1],
                    [0, 1, 0],
                    [0, 0, 1]))

    H23=nm.matrix(([math.cos(b), -math.sin(b), 0],
                    [math.sin(b), math.cos(b), 0],
                    [0, 0, 1]))

    H34=nm.matrix(([1, 0, l2],
                    [0, 1, 0],
                    [0, 0, 1]))
    
    H04=H01*H12*H23*H34
    print("Tibia=33\n")
    print("FIbula=84\n")
    print("Theta 1=30\n")
    print("Theta 2=40\n")
    print("H04: ")
    print(H04)
    
def KinematicDoFN():
    n, alllength, allangle=takematrix()
    H0N=nm.matrix(([1, 0, 0],
                  [0, 1, 0],
                  [0, 0, 1]))
    
    for i in range(n):
        angle_n=allangle[i]
        length_n=alllength[i]
        
        rotation=nm.matrix(([math.cos(angle_n), -math.sin(angle_n), 0],
                            [math.sin(angle_n), math.cos(angle_n), 0],
                            [0, 0, 1]))
        
        trans=nm.matrix(([1, 0, length_n],
                        [0, 1, 0],
                        [0, 0, 1]))
        
        HRT=rotation*trans
        H0N=H0N*HRT
    print(f"H0{2*(i)}: ")
    print(H0N)        
    
def inversekin():
    x_str=input("X final: ")
    x_final=int(x_str)
    y_str=input("Y final: ")
    y_final=int(y_str)
    l1_str=input("Enter L1: ")
    l1=int(l1_str)
    l2_str=input("Enter L2: ")
    l2=int(l2_str)
    
    if ((l1<0) or (l2<0)):
        print("Input value l1 and l2 greater than 0")
        return

    r=math.sqrt((x_final**2+y_final**2))
    
    if ((r>(l1+l2)) or r<(abs(l1-l2))):
        print(f"The point in ({x_final}, {y_final}) is unreachable ")
        return
        
    theta2=math.acos((x_final**2+y_final**2-l1**2-l2**2)/(2*l1*l2))
    theta1=math.atan2(y_final, x_final)-math.atan2((l2*math.sin(theta2)), (l1+l2*math.cos(theta2)))
    
    print(f"First angle is {math.degrees(theta1)} with arm length of {l1}")
    print(f"Second angle is {math.degrees(theta2)} with arm length of {l2}")
    
    print("Do you want to show the arm? [Y/n]")
    choice=input()
    
    if (choice=="Y" or choice=="y"):
        x0, y0=0, 0    
        plt.figure()
        plt.plot(x0, y0, 'ko', markersize=8, label="Origin")
        x1=l1*math.cos(theta1)
        x2=l1*math.cos(theta1)+l2*math.cos(theta1+theta2)
        y1=l1*math.sin(theta1)
        y2=l1*math.sin(theta1)+l2*math.sin(theta1+theta2)
        
        plt.plot([x0, x1], [y0, y1], "b-", linewidth=2, label="L1")
        plt.plot(x1, y1, "ro", markersize=8, label="Joint 1")
        plt.plot([x1, x2], [y1, y2], "b-", linewidth=2, label="2")
        plt.plot(x_final, y_final, 'xc', markersize=8, label="End Effector")
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.title(f'Forward Kinematics DoF 2')
        plt.grid(True)
        plt.axis('equal')  
        plt.legend()
        plt.show()
    else:
        return
    
def showarmN():
    n, alllength, allangle=takematrix()

    x0, y0=0, 0    
    plt.figure()
    plt.plot(x0, y0, 'ko', markersize=8, label="Origin")
    
    H0N=([1, 0, 0],
         [0, 1, 0],
         [0, 0, 1])
    
    for i in range (n):
        angle_n=allangle[i]
        length_n=alllength[i]
        
        rotation=nm.matrix(([math.cos(angle_n), -math.sin(angle_n), 0],
                            [math.sin(angle_n), math.cos(angle_n), 0],
                            [0, 0, 1]))
        
        trans=nm.matrix(([1, 0, length_n],
                        [0, 1, 0],
                        [0, 0, 1]))
        
        HRT=rotation*trans
        H0N=H0N*HRT
        x1=H0N[0, 2]
        y1=H0N[1, 2]
        
        plt.plot([x0, x1], [y0, y1], "b-", linewidth=2, label=(f"L{i}"))
        if (i<n-1):
            plt.plot(x1, y1, "ro", markersize=8, label=(f"Joint {i+1}"))
            
        x0=x1
        y0=y1
    plt.plot(x1, y1, 'xc', markersize=8, label="End Effector")
        
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title(f'Forward Kinematics DoF {n}')
    plt.grid(True)
    plt.axis('equal')  
    plt.legend()
    plt.show()

def showarmN3D():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    x0, y0, z0=0, 0, 0
    plt.plot(x0, y0, z0, 'ko', markersize=10, label="Origin")
    n_str=input("How many DoF: ")
    n=int(n_str)
    allangle=[]
    alllength=[]
    for i in range(n):
        angle_str=input(f"Enter Angle No.{i+1} in Degree: ")
        angle=math.radians(int(angle_str))
        allangle.append(angle)
        
        length_str=input(f"Enter Length No.{i+1} in cm: ")
        length=int(length_str)
        alllength.append(length)
    H0N=nm.matrix(([1, 0, 0, 0],
                  [0, 1, 0, 0],
                  [0, 0, 1, 0],
                  [0, 0, 0, 1]))
    
    for i in range(n):
        angle_n=allangle[i]
        length_n=alllength[i]
        
        rotation=nm.matrix(([math.cos(angle_n), -math.sin(angle_n), 0, 0],
                            [math.sin(angle_n), math.cos(angle_n), 0, 0],
                            [0, 0, 1, 0],
                            [0, 0, 0, 1]))
        
        trans=nm.matrix(([1, 0, 0, length_n],
                        [0, 1, 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]))
        
        HRT=rotation*trans
        H0N=H0N*HRT
        x1=H0N[0, 3]
        y1=H0N[1, 3]
        z1=H0N[2, 3]
        
        ax.plot([x0, x1], [y0, y1], [z0, z1], linewidth=2, label=(f'l{i+1}'))
        if (i>0 and i<=n-1 ):
            ax.plot(x0, y0, z0, "ro", markersize=10, label=(f'Joint {i}')) 
               
        x0=H0N[0, 3]
        y0=H0N[1, 3]
        z0=H0N[2, 3]

    plt.plot(x1, y1, z1, 'xc', markersize=10, label="End Effector")
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')
    ax.set_title('Kinematic Arm in 3D')
    ax.axis('equal')
    ax.legend()
    plt.show()
    
#main function
running=True
while running:
    UI()
    x_str=input("Enter Option: ")
    x=int(x_str)
    match x:
        case 0:
            break
        case 1: 
            kinematicdof2()
        case 2:
            KinematicDoFN()
        case 3:
            showarmN()
        case 4:
            showarmN3D()
        case 5:
            inversekin()


        
