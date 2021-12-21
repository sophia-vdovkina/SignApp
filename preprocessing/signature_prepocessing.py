import numpy as np
import pandas as pd
import os
import re
import struct

from scipy import stats


class Point(object):
    def __init__(self, x, y, p, t):
        if (x, p, y, t is None):
            pass
        self.x = x
        self.y = y
        self.p = p
        self.t = t


def read_bim(file):
    """
    Read signature bim from special file 
    """
    bims = []
    b = file.read(4)
    b = file.read(36)
    header = struct.unpack('I2H10BHI2H8B', b)
    b = file.read(4)
    count = struct.unpack('I', b)[0]
    for i in range(count):
        ptc = []
        # bim = Bim()
        b = file.read(20)
        info = struct.unpack('2I2H8B', b)
        b = file.read(12)
        bim_header = struct.unpack('6H', b)
        n = bim_header[0]
        maxX = bim_header[1]
        maxY = bim_header[2]
        maxP = bim_header[3]
        dpix = bim_header[4]
        dpiy = bim_header[5]
        b = file.read(64)
        for point in range(n):
            x = struct.unpack('h', file.read(2))[0]
            y = struct.unpack('h', file.read(2))[0]
            p = struct.unpack('h', file.read(2))[0]
            t = struct.unpack('h', file.read(2))[0]
            ptc.append(Point(x, y, p, t))
        #bim.ptc = self.scaleDots(bim.ptc)
        bims.append(ptc)
    return bims

def read_features(ofile):
    points = []
    N = int(ofile.readline())
    for num in range(N):
        line = [int(round(float(x))) for x in ofile.readline().split()]
        x = line[0]
        if num == 0:
            t = 0
            t1 = line[2]
        y = line[1]
        p = line[len(line)-1]
        if num != 0:
            t = line[2] - t1
            t1 = line[2]
        points.append({'x':x, 'y':y, 'p':p, 't':t})
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


def tan_angle(x, y):
    x_t = np.gradient(x)
    y_t = np.gradient(y)
    return np.degrees(np.arctan(y_t/x_t))


def extractXY(data, i):
    coords = pd.Series()
    x = np.nan_to_num([i.x for i in data])
    y = np.nan_to_num([i.y for i in data])
    p = np.nan_to_num([i.p for i in data])
    v = np.nan_to_num(find_velocity(data))
    acc = np.nan_to_num(find_acceleration(data, v))
    angle = np.nan_to_num(tan_angle(x,y))
    curvative_val = np.nan_to_num(curvative(np.array(x), np.array(y)))
    coords = pd.Series({'x':x, 'y':y, 'p':p, 'v':v, 'acceleration': acc, 'angle':angle, 'radius':curvative_val, 'index': i}).fillna(0)
    # coords.append(coord)
    return coords

    
def preprocess_words(sig_true, dir):
    i = 1
    # dir = 'E:\\for-sophia\\BimBase\\Свои'
    for file in os.listdir(dir):
        with open(os.path.join(dir, file), 'rb') as ofile:
            sig = read_bim(ofile)
        for signature in sig:
            sig_true = sig_true.append(extractXY(signature, i), ignore_index=True)
        i += 1
    sig_true.to_pickle('words.pkl')


def read_gen_n_forg(sig_true, sig_forg, dir):
    i = 1
    for file in os.listdir(dir):
        sig = []
        if name != file[:5]:
            i += 1
            name = file[:5]
        
        if re.search(r'_g_', file):
            with open(os.path.join(dir, file), 'r') as ofile:
                sig = read_features(ofile)
            sig_true = sig_true.append(extractXY(sig, i), ignore_index=True)

        elif re.search(r'_s_', file):
            with open(os.path.join(dir, file), 'r') as ofile:
                sig = read_features(ofile)
            sig_forg = sig_forg.append(extractXY(sig, i), ignore_index=True)

    return sig_true, sig_forg


def preprocess_signatures(sig_true, sig_forg):
    sig_true, sig_forg = read_gen_n_forg(sig_true, sig_forg, os.path.join(os.getcwd(), 'preprocessing\DeepSignDB\Development\\finger'))
    sig_true, sig_forg = read_gen_n_forg(sig_true, sig_forg, os.path.join(os.getcwd(), 'preprocessing\DeepSignDB\Development\\stylus'))

    sig_forg.to_pickle('sigantures_forg.pkl')
    sig_true.to_pickle('signatures_gen.pkl')

   
if __name__ == "__main__":
    sig_true = pd.DataFrame(columns=['x', 'y', 'p', 'v', 'acceleration', 'angle', 'radius', 'index'])
    sig_forg = pd.DataFrame(columns=['x', 'y', 'p', 'v', 'acceleration', 'angle', 'radius', 'index'])