
import numpy as np


class FeatureExtracter:

    def __init__(self, data):
        self.data = data

    def extract(self):
            coords = {}
            x = np.nan_to_num([i['x'] for i in self.data])
            y = np.nan_to_num([i['y'] for i in self.data])
            p = np.nan_to_num([i['p'] for i in self.data])
            v = np.nan_to_num(self.find_velocity(self.data))
            acc = np.nan_to_num(self.find_acceleration(self.data, v))
            angle = np.nan_to_num(self.tan_angle(x,y))
            curvative_val = np.nan_to_num(self.curvative(np.array(x), np.array(y)))
            coords = {'x':x, 'y':y, 'p':p, 'v':v, 'acceleration': acc, 'angle':angle, 'radius':curvative_val}
            return coords

    def find_velocity(self, data):
        velocity = [0]
        for i in range(1, len(data)):
            if data[i]['t'] == 0:
                velocity.append(np.sqrt(np.abs(np.square(np.array(data[i]['x']) - np.array(data[i - 1]['x'])) + np.square(
                    np.array(data[i]['y']) - np.array(data[i - 1]['y'])))))
            else:
                velocity.append(np.sqrt(np.abs(np.square(np.array(data[i]['x']) - np.array(data[i-1]['x'])) + 
                np.square(np.array(data[i]['y']) - np.array(data[i-1]['y']))))/np.array(data[i]['t']))
        return velocity

    def find_acceleration(self, data, vel):
        acceleration = [0]
        for i in range(1, len(data)):
            if data[i]['t'] == 0:
                acceleration.append(np.array(vel[i]) - np.array(vel[i - 1]))
            else:
                acceleration.append((np.array(vel[i]) - np.array(vel[i-1]))/np.array(data[i]['t']))
        return acceleration

    def normalize_zscore(self, features):
        f2 = []
        for x in features:
            f2.append((x - np.mean(x))/np.std(x))
        return f2

    def interpolate(self, points):
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

    def curvative(self, x, y):
        x_t = np.gradient(x)
        y_t = np.gradient(y)
        xx_t = np.gradient(x_t)
        yy_t = np.gradient(y_t)
        curvature_val = np.abs(xx_t * y_t - x_t * yy_t) / (x_t * x_t + y_t * y_t) ** 1.5
        curvature_val[0] = 0
        return curvature_val

    def tan_angle(self, x, y):
        x_t = np.gradient(x)
        y_t = np.gradient(y)
        return np.degrees(np.arctan(y_t/x_t))

