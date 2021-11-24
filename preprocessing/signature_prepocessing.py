import numpy as np
import pandas as pd
import os
import re

from scipy import stats


class Point(object):
    def __init__(self, x, y, p, t):
        if (x, p, y, t is None):
            pass
        self.x = x
        self.y = y
        self.p = p
        self.t = t


def read_features(ofile):
    points = []
    N = int(ofile.readline())
    for num in range(N):
        line = [int(x) for x in ofile.readline().split()]
        x = line[0]
        if num == 0:
            t = 0
            t1 = line[2]
        y = line[1]
        p = line[len(line)-1]
        if num != 0:
            t = line[2] - t1
            t1 = line[2]
        points.append(Point(x, y, p, t))
    return points


def find_velocity(data):
    velocity = [0]
    for i in range(1, len(data)):
        if data[i].t == 0:
            velocity.append(np.sqrt(np.abs(np.square(np.array(data[i].x) - np.array(data[i - 1].x)) + np.square(
                np.array(data[i].y) - np.array(data[i - 1].y)))))
        else:
            velocity.append(np.sqrt(np.abs(np.square(np.array(data[i].x) - np.array(data[i-1].x)) + np.square(np.array(data[i].y) - np.array(data[i-1].y))))/np.array(data[i].t))
    return velocity


def find_acceleration(data, vel):
    acceleration = [0]
    for i in range(1, len(data)):
        if data[i].t == 0:
            acceleration.append(np.array(vel[i]) - np.array(vel[i - 1]))
        else:
            acceleration.append((np.array(vel[i]) - np.array(vel[i-1]))/np.array(data[i].t))
    return acceleration


def normalize_zscore(features):
    f2 = []
    for x in features:
        f2.append((x - np.mean(x))/np.std(x))
    return f2


def interpolate(points):
    points_inter = []
    for i in range(len(points)):
        sign = []
        for x in points[i]:
              sign.append(stats.zscore(np.interp(np.arange(0, len(x),  len(x)/256), np.arange(0, len(x)), x)))
        points_inter.append(sign)
    x = []
    for point in points_inter:
        x.append(np.array(point).flatten())
    return x


def curvative(x, y):
    x_t = np.gradient(x)
    y_t = np.gradient(y)
    xx_t = np.gradient(x_t)
    yy_t = np.gradient(y_t)
    curvature_val = np.abs(xx_t * y_t - x_t * yy_t) / (x_t * x_t + y_t * y_t) ** 1.5
    curvature_val[0] = 0
    return curvature_val


def extractXY(data):
    coords = pd.Series()
    x = []
    y = []
    p = []
    v = []
    acc = []
    tan_angle = []
    curvative_val = []
    for point in data:
        x.append([i.x for i in point])
        y.append([i.y for i in point])
        p.append([i.p for i in point])
        v = find_velocity(point)
        acc = find_acceleration(point, v)
        tan_angle = np.degrees(np.arctan(np.array(x)/np.array(y)))
        curvative_val = curvative(np.array(x), np.array(y))
        coords = pd.Series({'A': 10, 'B': 20, 'C': 30, 'D': 40}, name=3)
        coords.append((x, y, p, v, acc, tan_angle, curvative_val))
    return coords


if __name__ == "__main__":
    sig_true = pd.DataFrame(columns=['x', 'y', 'p', 'v', 'angle', 'radius', 'index'])
    sig_forg = pd.DataFrame(columns=['x', 'y', 'p', 'v', 'angle', 'radius', 'index'])
    i = 0
    name = 0
    for file in os.listdir('./DeepSignDB/Development/finger'):
        sig = []
        if name != file[:5]:
            i += 1
            name = file[:5]
        if re.search(r'_g_', file):
            with open(file, 'r') as ofile:
                sig.append(read_features(ofile))
            sig_true = sig_true.append(extractXY(sig))
        # elif re.search(r'_s_', file):
        #     sig.append(read_features(file))
        # sig_forg_finger.append(extractXY(sig))

    # for i in range(1, 41):
    #     sig = []
    #     for j in range(1, 21):
    #         with open(".\DeepSignDB\Development\finger\".format(i, j), 'r') as ofile:
    #             sig.append(read_features(ofile))
    #     sig_true.append(extractXY(sig))
    #     sig = []
    #     for j in range(21, 41):
    #         with open("/media/danil/SOPHIA/Task2/U{}S{}.TXT".format(i, j), 'r') as ofile:
    #             sig.append(read_features(ofile))
    #     sig_forg.append(extractXY(sig))
    # for i in range(0, 40):
    #     file_open = "/media/danil/SOPHIA/sig_forg/sig_{}".format(i+1)
    #     with open(file_open, 'w+') as file:
    #         file.write(str(len(sig_forg[i])) + '\n')
    #         for sign in sig_forg[i]:
    #             file.write(str(len(sign)) + '\n')
    #             file.write(str(len(sign[0])) + '\n')
    #             for x in sign:
    #                 for j in x:
    #                     file.write(str(j) + ' ')
    #                 file.write('\n')
    #     file_open = "/media/danil/SOPHIA/sig_true/sig_{}".format(i + 1)
    #     with open(file_open, 'w+') as file:
    #         file.write(str(len(sig_true[i])) + '\n')
    #         for sign in sig_true[i]:
    #             file.write(str(len(sign)) + '\n')
    #             file.write(str(len(sign[0])) + '\n')
    #             for x in sign:
    #                 for j in x:
    #                     file.write(str(j) + ' ')
    #                 file.write('\n')