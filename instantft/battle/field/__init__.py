# coding: utf-8
from instantft.algorighm import pathfind
import heapq
import numpy
import unittest
import itertools

BEST_TRASFERTA_POS = 3

NEIGHBORS_POS = range(8)
P1, P3, P5, P6, P7, P9, P11, P12 = NEIGHBORS_POS
OUTLET_P1_T = [P1, P12, P3, P11, P5, P9, P6, P5]
OUTLET_P3_T = [P3, P1, P5, P12, P6, P11, P7, P9]
OUTLET_P5_T = [P5, P3, P6, P1, P7, P9, P12, P11]
OUTLET_P6_T = [P6, P5, P7, P3, P9, P1, P11, P12]
OUTLET_P7_T = [P7, P6, P9, P5, P11, P3, P12, P1]
OUTLET_P9_T = [P9, P7, P11, P6, P12, P5, P1, P3]
OUTLET_P11_T = [P11, P9, P12, P7, P1, P6, P3, P5]
OUTLET_P12_T = [P12, P11, P1, P9, P3, P7, P5, P6]

ATK_SPOTS = [P1, P5, P6, P7, P11, P12]
OUTLET_P1_F = OUTLET_P3_T
OUTLET_P3_F = OUTLET_P3_T
OUTLET_P5_F = OUTLET_P3_T
OUTLET_P6_F = OUTLET_P6_T
OUTLET_P7_F = OUTLET_P9_T
OUTLET_P9_F = OUTLET_P9_T
OUTLET_P11_F = OUTLET_P9_T
OUTLET_P12_F = OUTLET_P12_T

ATK_POSITIONS = [P9, P3, P11, P7, P1, P5, P12, P6]

POS_EXTENDS = {
    P1: (1, -1),
    P3: (1, 0),
    P5: (1, 1),
    P6: (0, 1),
    P7: (-1, 1),
    P9: (-1, 0),
    P11: (-1, -1),
    P12: (0, -1),
}

NEAR_POSITIONS = [
    (P12, P3),
    (P1, P5),
    (P3, P6),
    (P5, P7),
    (P6, P9),
    (P7, P11),
    (P9, P12),
    (P11, P1),
]

DIRECTION_MAPPING = {
    (0, 1, True): OUTLET_P12_T,
    (0, 1, False): OUTLET_P12_F,
    (1, 0, True): OUTLET_P3_T,
    (1, 0, False): OUTLET_P3_F,
    (1, 1, True): OUTLET_P1_T,
    (1, 1, False): OUTLET_P1_F,
    (0, -1, True): OUTLET_P6_T,
    (0, -1, False): OUTLET_P6_F,
    (-1, 0, True): OUTLET_P9_T,
    (-1, 0, False): OUTLET_P9_F,
    (-1, -1, True): OUTLET_P7_T,
    (-1, -1, False): OUTLET_P7_F,
    (1, -1, True): OUTLET_P5_T,
    (1, -1, False): OUTLET_P5_F,
    (-1, 1, True): OUTLET_P11_T,
    (-1, 1, False): OUTLET_P11_F,
    (0, 0, True): OUTLET_P3_T,
    (0, 0, False): OUTLET_P3_F,
}

class BattleField(object):
    """
    """

    def __init__(self, mapinfo):
        """
        """

        self.xlen, self.ylen = mapinfo['size']
        self.maxpos = mapinfo['max_pos']
        self.pixel = mapinfo['pixel']
        self.focus = mapinfo['focus']
        self.sky = mapinfo['useless']
        self.places = [mapinfo['attack'], mapinfo['defend']]

    def heuristic(self, pos, goal):
        """
        """

        quo1, mod1 = divmod(goal, self.xlen)
        quo2, mod2 = divmod(pos, self.xlen)

        return numpy.abs((quo2 - quo1)) + numpy.abs((mod2 - mod1))

    def cost(self, from_pos, to_pos):
        """
        """

        return 2

    def in_range(self, pos, goal, width, high):
        """
        """

        h1, w1 = divmod(pos, self.xlen)
        h2, w2 = divmod(goal, self.xlen)

        return numpy.abs(h1 - h2) <= high and \
            numpy.abs(w1 - w2) <= width

    def straight_distance(self, pos, goal):
        """
        """

        quo1, mod1 = divmod(goal, self.xlen)
        quo2, mod2 = divmod(pos, self.xlen)
        xlen = numpy.abs(mod1 - mod2)
        ylen = numpy.abs(quo1 - quo2)

        if not xlen:
            return ylen
        
        if not ylen:
            return xlen

        return numpy.hypot(xlen, ylen)

    def touch_distance(self, pos, pos_volume, goal):
        ""
        ""

        xlen, ylen = pos_volume

        quo1, mod1 = divmod(goal, self.xlen)
        quo2, mod2 = divmod(pos, self.xlen)
        alen = numpy.ceil(numpy.abs(mod1 - mod2))
        blen = numpy.ceil(numpy.abs(quo1 - quo2))

        if not alen:
            return max(numpy.abs(blen - ylen), 0)

        if not blen:
            return max(numpy.abs(alen - xlen), 0)

        if alen > blen:
            return max(numpy.abs(alen - xlen), 0)
        
        return max(numpy.abs(blen - ylen), 0)

    def direction(self, pos, goal_pos):
        """
        """
        
        y1, x1 = divmod(pos, self.xlen)
        y2, x2 = divmod(goal_pos, self.xlen)
        xlen = x2 - x1
        ylen = y1 - y2
        xlen_abs = numpy.abs(xlen)
        ylen_abs = numpy.abs(ylen)

        key = (cmp(xlen, 0), cmp(ylen, 0), xlen_abs <= ylen_abs)

        return DIRECTION_MAPPING[key]

    def edges(self, pos, goal_pos, width, high):
        """ 查找指定点pos以中心到goal_pos的8个边缘点
        """

        ylen, xlen = divmod(pos, self.xlen)
        top_len = min(high, ylen) * self.xlen
        down_len = min(high, self.ylen - ylen) * self.xlen
        left_len = min(width, xlen)
        right_len = min(width, self.xlen - xlen)

        positions = [0, 0, 0, 0, 0, 0, 0, 0]
        positions[P3] = pos + right_len
        positions[P5] = positions[P3] + down_len
        positions[P6] = positions[P5] - right_len
        positions[P7] = positions[P6] - left_len
        positions[P9] = positions[P7] - down_len
        positions[P11] = positions[P9] - top_len
        positions[P12] = positions[P11] + left_len
        positions[P1] = positions[P12] + right_len

        for pos_id in NEIGHBORS_POS:
            current_pos = positions[pos_id]
            left, right = map(positions.__getitem__, NEAR_POSITIONS[pos_id])
            
            yield current_pos

    def focus_to(self, pos, goal_pos):
        """
        """

        return pos % self.xlen <= goal_pos % self.xlen

    def face_to(self, pos, goal_pos, current):
        """ 计算一个点是不是面对一个目标点

        Args:
           post: 起始点
           goal_pos: 目标点
           current: 当前面对的方向

        Returns:
           是否正向面对一个点
        """

        x1 = pos % self.xlen
        x2 = goal_pos % self.xlen

        if not current: # face to left
            return x1 <= x2

        return x1 >= x2

    def lateral_pos(self, pos, target_pos):
        """ 找到一个点与目标点的横向交叉点

        Args:
           pos: 指定点
           target_pos: 目标点

        Returns:
           交叉点id
        """

        y1, x1 = divmod(pos, self.xlen)
        y2, x2 = divmod(target_pos, self.xlen)

        return (y2 * 2 - y1) * self.xlen + x2

    def arounds(self, pos):
        """ 计算一个点周围的所有点

        Args:
           pos: 指定点

        Returns:
           四周点的列表, 对应点的有效性
        """

        posrow = pos / self.xlen
        toprow = posrow + 1
        downrow = posrow - 1
        realness = [False, False, False, False,
                    False, False, False, False]
        positions = [0, 0, 0, 0, 0, 0, 0, 0]
        positions[P3] = pos + 1
        positions[P5] = positions[P3] + self.xlen
        positions[P6] = positions[P5] - 1
        positions[P7] = positions[P6] - 1
        positions[P9] = positions[P7] - self.xlen
        positions[P11] = positions[P9] - self.xlen
        positions[P12] = positions[P11] + 1
        positions[P1] = positions[P12] + 1

        if positions[P3] / self.xlen == posrow:
            realness[P3] = True
            realness[P5] = positions[P5] <= self.maxpos
            realness[P1] = positions[P1] >= 0

        if positions[P9] / self.xlen == posrow:
            realness[P9] = True
            realness[P11] = positions[P11] >= 0
            realness[P7] = positions[P7] <= self.maxpos

        realness[P6] = positions[P6] <= self.maxpos
        realness[P12] = positions[P12] >= 0

        return positions, realness

    def xslice(self, pos):
        """ 根据X轴将点切片

        Args:
           pos: 要拆分的点

        Returns:
           (left_len, right_len) 切片后左右的长度
        """

        x = pos % self.xlen

        return self.xlen - x, x

    def yslice(self, pos):
        """ 根据X轴将点切片

        Args:
           pos: 要拆分的点

        Returns:
           (top_len, down_len) 切片后上下的长度
        """

        y = pos / self.xlen

        return self.ylen - y, y

    def near_empty(self, pos, blocks):
        """ 获取离中心点最近的空位

        Args:
           pos: 中心点
           blocks: 当前场上的障碍物

        Returns:
           有效的空位点
        """

        queue = [pos]
        waits = []

        while queue:
            value = heapq.heappop(queue)

            if not value in blocks:
                return value

            arounds = itertools.compress(*self.arounds(pos))

            heapq.heappush(waits, arounds)

            if not queue:
                queue = list(heapq.merge(*waits))
                waits = []

    def trasferta(self, pos, target_pos, max_len, blocks):
        """ 获取一个远离目标点的行动目标点

        当不能攻击时需要远离目标点行走，需要尽量保持与控制目标点的有效距离

        Args:
           pos: 当前位置
           target_pos: 要远离的目标位置
           max_len: 最大长度
           blocks: 障碍点
        """

        distance = self.heuristic(pos, target_pos)
        diff = distance - max_len

        if diff > 0:
            return pos

        diff -= diff
        direction = self.direction(target_pos, pos)
        positions, realness = self.arounds(pos)
        best_direction = direction[0:BEST_TRASFERTA_POS]

        for outlet in itertools.compress(best_direction, realness):
            near_pos = positions[outlet]
            out_pos = self.pos_extneds(near_pos, outlet, diff)

            if out_pos and not out_pos in blocks:
                return out_pos

        return pos

    def pos_extneds(self, pos, outlet, length):
        """ 从指定点按指定方向延长指定的长度

        Args:
            pos: 指定点id
            outlet: 出口id
            length: 延伸长度

        Returns:
            延伸长度的id, 没有返回None
        """

        x, y = POS_EXTENDS[outlet]

        outlet_pos =  pos + (x * length * self.xlen) + (y * length)

        if outlet_pos < 0 or outlet_pos > self.maxpos:
            return None

        return outlet_pos

    def neighbors(self, pos, blocks, goal_pos):
        """ 计算一个点周围的所有点

           在寻路过程中需要根据一个点查找到周围所有可以移动的点，在计算好周围点后，
        再和障碍物计算出有效的点，按照定义的顺序返回
        
           地图为x * y的一个矩阵，地图坐标是一个自然数，以x轴的长度换行
           0 1 2 3 4
           5 6 7 8 9
           5 * 2的一个地图

           计算周为点采用表盘格式，p3对应的是中心点的3点位置

        Args:
            pos: 要查找的中心点
            blocks: 在地图中所有障碍物的坐标id
            orders: 返回点的顺序
            direction: 默认的方向

        Returns:
            所有中心点可以移动到的点
        """

        positions, realness = self.arounds(pos)
        direction = self.direction(pos, goal_pos)

        for p in direction:
            if realness[p] and positions[p] not in blocks:
                return [positions[p]]

        return []

if __name__ == "__main__":
    from instantft.algorighm import pathfind

    mapinfo = {
        'defend': [9, 57, 23, 47], 
        'focus': {
            'attack': {'y': 0, 'x': 0}, 
            'defend': {'y': 0, 'x': 10}
        }, 
        'attack': [2, 50, 12, 36], 
        'useless': 2, 
        'max_pos': 71, 
        'pixel': 80, 
        'size': (12, 8)
    }

    # 10 278 33 33
    bf = BattleField(mapinfo)
    (12, 23, set([3, 36, 9, 12, 47, 51, 57])
     , 1.0)

    print(pathfind.astar(12, 23, set([3, 36, 9, 12, 47, 51, 57]), bf, 1))
