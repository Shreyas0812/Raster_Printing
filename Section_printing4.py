import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.axes import Axes
import sys
import time

ros_path = '/opt/ros/kinetic/lib/python2.7/dist-packages'
if ros_path in sys.path:
    sys.path.remove(ros_path)
import cv2
sys.path.append('/opt/ros/kinetic/lib/python2.7/dist-packages')

sys.setrecursionlimit(10**6) 

class visualizer():
    def __init__(self, lines):
        self.x_pts = []
        self.y_pts = []

        self.pts = []

        self.fig = plt.figure()
        #self.ax = plt.axes(xlim = (0,500), ylim = (0,500))
        self.lines = lines
    
    #def Printing(self, pt1, pt2, line):
        
    def plot(self, p1):
        idx = 0
        clrs = ['b-', 'g-', 'r-', 'c-', 'm-', 'y-', 'k-', 'w-']
        mark_pts = ['bo', 'go', 'ro', 'co', 'mo', 'yo', 'ko', 'wo']

        for line in self.lines:
            #print(len(line))
            x = list(line[i][0] for i in range(len(line)))
            y = list(line[i][1] for i in range(len(line)))

            p1.plot(y, x, clrs[idx])
            p1.plot(y, x, mark_pts[idx],  label = 'Robot'+ str(idx))
            
            idx = idx + 1

            if (idx == len(clrs)):
                idx = 0
        #plt.show()
    
    def points_on_line(self):
        time_print = []
        time_travel = []
        for line in self.lines:
            time_print_individual = 0
            time_travel_individual = 0
            lx = []
            ly = []
            for index in range(len(line) - 1):
                pt1 = line[index]
                pt2 = line[index+1]
                
                print(pt1, pt2)
                x1 = pt1[0]
                y1 = pt1[1]
                x2 = pt2[0]
                y2 = pt2[1]
                
                if index%2 ==0 :    #printing
                    num_btw = 3*int(math.sqrt((x2 - x1)**2 + (y2 - y1)**2))#Number of points btw 2 points
                    time_print_individual = time_print_individual + num_btw
                else:           #travelling
                    num_btw = 1*int(math.sqrt((x2 - x1)**2 + (y2 - y1)**2))#Number of points btw 2 points
                    time_travel_individual = time_travel_individual + num_btw
                
                for t in range(num_btw):
                    x = x1 + (x2-x1) * (1/num_btw) * t
                    y = y1 + (y2-y1) * (1/num_btw) * t

                    lx.append(x)
                    ly.append(y)
                    
            #print (lx, ly)
            self.x_pts.append(lx)
            self.y_pts.append(ly)
            #print(line)
            time_print.append(time_print_individual)
            time_travel.append(time_travel_individual)
        time_bot = []
        for i, j in zip(time_print, time_travel):
            time_bot.append(i + j)

        return time_bot

    def animation(self):
        mark_pts = ['bo', 'go', 'ro', 'co', 'mo', 'yo', 'ko', 'wo']
        idx = 0
        Anim = []
        #self.fig = plt.figure()
        
        p1 = self.fig.add_subplot(111)
        
        self.plot(p1)

        #p1.set_xlim([0, 60])
        #p1.set_ylim([0, 60])
 
        #for the rest
        def next(index):
            #i = 0
            color_id = index

            if (color_id+1 == len(mark_pts)):
                color_id = 5 #yellow, so black is shown

            pt, = p1.plot([], [], mark_pts[color_id+1])
            
            def bot():
                i = 0
                while(True):
                    yield i
                    i += 1
                    
            def run(c):
                #Takes one more than original index
                pt.set_data(self.y_pts[index][c], self.x_pts[index][c])
                    
            Anim.append(animation.FuncAnimation(self.fig,run,bot,interval=1))
            
            if index == len(self.x_pts) :
                Axes.set_aspect(p1, 'equal')
                plt.axis([0, 500, 500, 0])
                plt.legend()
                plt.show()
            else:
                #print (index)
                index = index + 1
                next(index) #Recursive Function as a loop

        next(index = -1)

    def main(self):
        #self.plot()
        clr = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
        clrdot = ['bo', 'go', 'ro', 'co', 'mo', 'yo', 'ko', 'wo']
        time_bot = self.points_on_line()
        self.animation()
        
        #frames to min
        for i in range(len(time_bot)):
            time_bot[i] = time_bot[i] * 0.1
            time_bot[i] = time_bot[i]/120

        xaxis_val = []
        val = np.arange(len(time_bot))
        for i in range(len(val)):
            xaxis_val.append('Robot ' + str(val[i]))
        
        for i,t in enumerate(time_bot):
            print('Robot',i,': ', t)
        
        p2=self.fig.add_subplot(111)
        barval = plt.bar( xaxis_val, time_bot, width = 0.5, align = 'center' )
        for i in range(len(time_bot)):
            barval[i].set_color(clr[i])  
        Axes.set_aspect(p2,'equal')
        plt.title('Elapsed Time')
        plt.ylabel('Time in Minutes')
        plt.show()

        p3 = self.fig.add_subplot(111)
        i = 0
        Axes.set_aspect(p2, 'equal')
        plt.axis([0, 500, 500, 0])
        print('25 percent')
        #plt.title('25% Graph')
        for ptx, pty in zip(self.x_pts, self.y_pts):
            ptx25 = ptx[0:int(len(ptx)/4)]
            pty25 = pty[0:int(len(ptx)/4)]

            plt.plot(pty25, ptx25, clr[i])
            plt.plot(pty25[-1], ptx25[-1], clrdot[i])
            i = i+1
            
        plt.show()
        
        i = 0
        plt.axis([0, 500, 500, 0])
        #plt.title('50% Graph')
        for ptx, pty in zip(self.x_pts, self.y_pts):
            ptx50 = ptx[0:int(len(ptx)/2)]
            pty50 = pty[0:int(len(ptx)/2)]

            plt.plot(pty50, ptx50, clr[i])
            plt.plot(pty50[-1], ptx50[-1], clrdot[i])
            i = i+1
        plt.show()
        
        i = 0
        plt.axis([0, 500, 500, 0])
        #plt.title('75% Graph')
        for ptx, pty in zip(self.x_pts, self.y_pts):
            ptx75 = ptx[0:int(len(ptx)*0.75)]
            pty75 = pty[0:int(len(ptx)*0.75)]

            plt.plot(pty75, ptx75, clr[i])
            plt.plot(pty75[-1], ptx75[-1], clrdot[i])
            i = i+1
        plt.show()

        i = 0
        plt.axis([0, 500, 500, 0])
        #plt.title('100% Graph')
        for ptx, pty in zip(self.x_pts, self.y_pts):
            plt.plot(pty, ptx, clr[i])
            plt.plot(pty[-1], ptx[-1], clrdot[i])
            i = i+1
        plt.show()
        
def get_image(img):

    black_points = []
    y_cor = []
    for num_row, line in enumerate(img):
        if (num_row%12 == 0):
            for num_col, column in enumerate(line):
                if column == 0:
                    y_cor.append(num_col)
                    black_points.append([num_row, num_col])

                    #isolated points:
                    try:
                        if (line[num_col+1] == line[num_col-1] == 255 ):
                            #putting extra same value, start and end at same point
                            y_cor.append(num_col)
                            black_points.append([num_row, num_col])
                    except:
                        pass

    Points_of_Interest = []
    
    #Getting corners
    y_index = []
    for i in range(len(y_cor) - 1):
        if (y_cor[i] == y_cor[i+1] - 1 or y_cor[i] == y_cor[i+1] - 2) and (y_cor[i] == y_cor[i-1] + 1 or y_cor[i] == y_cor[i-1] + 2): continue
        y_index.append(i)

    for pts_index in y_index:
        Points_of_Interest.append(black_points[pts_index])

    #list of lists to list of tuples
    #Points_of_Interest = [tuple(l) for l in Points_of_Interest]    

    black_lines = []
    i = 0
    j = 1
    b = False
    while True:
        one_line = []
        one_line.append(Points_of_Interest[i])
        while (Points_of_Interest[i][0] == Points_of_Interest[j][0]):
            one_line.append(Points_of_Interest[j])
            j = j + 1
            if j >= len(Points_of_Interest):
                break
        
        one_line = sorted(one_line, key=lambda x: (x[1]), reverse=b)
        i = i + len(one_line)
        j = i + 1
        
        if b is False:
            b = True
        else:
            b = False
        if len(one_line)%2 == 0:
            black_lines.append(one_line)
        elif len(one_line) == 1:
            one_line = [one_line[0], one_line[0]]
            black_lines.append(one_line)
    
        if j >= len(Points_of_Interest):
            break

    black_lines_final = []
    #Each element will always have even number of elements
    for line in black_lines:
        if len(line) == 2:
            black_lines_final.append(line)
        else:
            temp_arr = [[line[i], line[i+1]] for i in range(len(line)) if i%2 == 0]
            for temp_pts in temp_arr:
                black_lines_final.append(temp_pts)
    
    return black_lines_final

if __name__ == '__main__':
    Paths  = []
    
    #Initial position of each robot
    pose = np.array([(300,350), (25,250), (50, 75), (250,25), (100,450)])

    img = cv2.imread('ipsum-slice-0.bmp', cv2.IMREAD_GRAYSCALE)
    lineSet0 = get_image(img)

    #for i,val in enumerate(lineSet0):
        #print(val)
      
    line0 = []
    for line in lineSet0:
        for pts in line:
            line0.append(pts)
    #for i in newline0:
        #print(i)
    num = list(pose[0])
    #line0.insert(0, num)
    for i in line0:
        print(i)
    Paths.append(line0)

    img = cv2.imread('ipsum-slice-1.bmp', cv2.IMREAD_GRAYSCALE)
    lineSet1 = get_image(img)
    line1 = []
    for line in lineSet1:
        for pts in line:
            line1.append(pts)
    num = list(pose[1])
    #line1.insert(0, num)
    Paths.append(line1)
    #print(line1)
    
    img = cv2.imread('ipsum-slice-2.bmp', cv2.IMREAD_GRAYSCALE)
    lineSet2 = get_image(img)
    line2 = []
    for line in lineSet2:
        for pts in line:
            line2.append(pts)
    num = list(pose[2])
    #line2.insert(0, num)
    Paths.append(line2)
    #print(line2)
    
    img = cv2.imread('ipsum-slice-3.bmp', cv2.IMREAD_GRAYSCALE)
    lineSet3 = get_image(img)
    line3 = []
    for line in lineSet3:
        for pts in line:
            line3.append(pts)
    num = list(pose[3])
    #line3.insert(0, num)
    Paths.append(line3)
    #print(line3)
    
    img = cv2.imread('ipsum-slice-4.bmp', cv2.IMREAD_GRAYSCALE)
    lineSet4 = get_image(img)
    line4 = []
    for line in lineSet4:
        for pts in line:
            line4.append(pts)
    num = list(pose[4])
    #line4.insert(0, num)
    Paths.append(line4)
    #print(line4)
    
    clrdot = ['bo', 'go', 'ro', 'co', 'mo', 'yo', 'ko', 'wo']
    i = 0
    plt.axis([0, 500, 500, 0])
    #plt.title('Initial Positions')
    for pts in pose:
        plt.plot(pts[1], pts[0], clrdot[i])
        i = i+1
    plt.show()
    
    display = visualizer(lines = Paths)
    display.main()