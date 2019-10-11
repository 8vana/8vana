import math

class ActorState:
    def __init__(self, x=0, y=0, x2=0, y2=0, actor_id=0, target_obj_map={}):
        self.x        = x
        self.y        = y
        self.x1       = x
        self.y1       = y
        self.x2       = x2
        self.y2       = y2
        self.pi       = math.pi
        self.distance = self.get_distance(x, y, x2, y2)
        self.degree   = self.get_degree(x, y, x2, y2)
        self.id       = actor_id
        self.obj_map  = target_obj_map
        self.wait     = 15
        self.wait_default = 15

    def set_position(self, x, y):
        self.x = x
        self.y = y
        return [self.x, self.y]

    def update_position(self, distance):
        xy = self.get_position(distance)
        if self.x < self.x2 - distance or self.x > self.x2 + distance:
            self.x = xy[0]
        elif(self.x == self.x2):
            # 目標地点に到達した
            if self.wait == 0:
                self.x    = self.x1
        else:
            self.x = self.x2

    
    
        if self.y < self.y2 - distance or self.y > self.y2 + distance:
            self.y = xy[1]
        elif(self.y == self.y2):
            # 目標地点に到達した
            if self.wait == 0:
                self.y    = self.y1
                self.wait = self.wait_default
            else:
                self.wait -= 1
        else:
            self.y = self.y2
        
        return [self.x, self.y]

    def get_distance(self, x, y, x2, y2):
        #print("get_distance input x: %f, y: %f, x2: %f, y2: %f" % (x, y, x2, y2))
        distance = math.sqrt((x2 - x) * (x2 - x) + (y2 - y) * (y2 - y))
        return distance

    def get_degree(self, x, y, x2, y2):
        #degree = math.degrees(math.atan2(y2 - y, x2 - x))
        degree = math.degrees(math.atan2(y - y2, x - x2))
        return degree

    def get_position(self, distance):
        x = self.x - math.cos(math.radians(self.degree)) * (distance)
        y = self.y - math.sin(math.radians(self.degree)) * (distance)
        return [x, y]

    def get_obj_map(self):
        return self.obj_map





    def _get_radian(self, x, y, x2, y2):
        #print("get_distance input x: %f, y: %f, x2: %f, y2: %f" % (x, y, x2, y2))
        radian = math.atan2(y2 - y, x2 - x)
        return radian