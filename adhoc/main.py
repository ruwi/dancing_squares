#!/home/ruwi/venv/bin/python

def debug(*args):
    for i in args:
        print i,
    print

# def debug(self, *args):
#     pass

class DancingSquatres(object):
    def __init__(self, squares=[]):
        self.squares = squares
        self.update_pos = {}

    def step(self):
        self.update_pos = {s:True for s in self.squares}
        current_state = {(s.x, s.y):s for s in self.squares}
        next_state = {}
        relation_graph = {s:[] for s in self.squares}
        for s in self.squares:
            n = s.next_pos()
            l = next_state.get(n, [])
            l.append(s)
            next_state[n] = l
            if n != (s.x, s.y):
                if n not in current_state.keys():
                    continue
                l = relation_graph.get( current_state[n], [])
                l.append(s)
                relation_graph[current_state[n]] = l
        for i in next_state:
            if len(next_state[i]) > 1:
                for s in next_state[i]:
                    self.not_update(s, relation_graph)
        for s in self.squares:
            if self.update_pos[s]:
                s.update_pos(*s.next_pos())
            else:
                s.flip_period(s.steps_left_x==0, s.steps_left_y==0)
            s.update_steps_left(*s.next_steps_left())


    def not_update(self, s, relation_graph):
        self.update_pos[s] = False
        for ss in relation_graph[s]:
            if self.update_pos[ss]:
                self.not_update(ss, relation_graph)

    def __str__(self):
        return '\n'.join([str(s) for s in self.squares])
                


class Square(object):
    def __init__(self, x, y, period_x, period_y,
                 steps_left_x=0, steps_left_y=0):
        self.x = x
        self.y = y
        self.period_x = period_x
        self.period_y = period_y
        self.steps_left_x = steps_left_x
        self.steps_left_y = steps_left_y

    def next_pos(self):
        x = self.x
        y = self.y
        if self.steps_left_x == 0:
            x += (self.period_x != 0) * ((self.period_x > 0)*2 - 1)
        if self.steps_left_y == 0:
            y += (self.period_y != 0) * ((self.period_y > 0)*2 - 1)
        return x, y

    def flip_period(self, x, y):
        if x:
            self.period_x = - self.period_x
        if y:
            self.period_y = - self.period_y

    def next_steps_left(self):
        sx = self.steps_left_x
        if self.period_x !=  0:
            sx = (sx - 1) % abs(self.period_x)
        sy = self.steps_left_y
        if self.period_y !=  0:
            sy = (sy - 1) % abs(self.period_y)
        return sx, sy

    def update_steps_left(self, sx, sy):
        self.steps_left_x = sx
        self.steps_left_y = sy


    def update_pos(self, x, y):
        self.x = x
        self.y = y


    def __str__(self):
        args = (self.x, self.y, self.period_x, self.period_y, self.steps_left_x,
                self.steps_left_y)
        string = 'x: %+3i  y: %+3i  tx: %+3i  ty: %+3i slx: %+3i sly: %+3i'
        return string % args

    def __repr__(self):
        horiz = '-'
        if self.period_x > 0 and self.steps_left_x == 0:
            horiz = '>'
        if self.period_x < 0 and self.steps_left_x == 0:
            horiz = '<'
        vert = '|'
        if self.period_y > 0 and self.steps_left_y == 0:
            vert = '^'
        if self.period_y < 0 and self.steps_left_y == 0:
            vert = 'v'
        return '(%i, %i; %s%s)' % (self.x, self.y, horiz, vert)


class DancingSquatresPloter(object):
    direction2unicode = {
        (-1, 0) : u'\u2190',
        (0, 1) : u'\u2191',
        (1, 0) : u'\u2192',
        (0, -1) : u'\u2193',
        'left-right' : '\u2194',
        'up-down' : '\u2195',
        (-1, 1) : u'\u2196',
        (1, 1) : u'\u2197',
        (1, -1) : u'\u2198',
        (-1, -1) : u'\u2199',
        (0, 0) : u'\u2022',
    }
    def __init__(self, max_x, max_y, min_x=0, min_y=0):
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y

    def plot(self, ds):
        SPACE = u'\u2000'
        out = [[SPACE 
                for i in range(self.max_x - self.min_x)]
               for i in range(self.max_y - self.min_y)]
        for s in ds.squares:
            x, y = self.get_pos(s)
            mx, my = self.get_size()
            if x >= 0 and x < mx and y >= 0 and y < my:
                out[y][x] = self.direction2unicode[self.square_direction(s)]
        return '\n'.join([SPACE.join(row) for row in out][::-1])
            
    def get_pos(self, s):
        x = s.x - self.min_x
        y = s.y - self.min_y
        return x, y

    def get_size(self):
        mx = self.max_x - self.min_x
        my = self.max_y - self.min_y
        return mx, my


    def square_direction(self, s):
        x = 0
        y = 0
        if s.steps_left_x == 0 and s.period_x:
            x = (s.period_x > 0) * 2 - 1
        if s.steps_left_y == 0 and s.period_y:
            x = (s.period_y > 0) * 2 - 1
        return (x, y)

# class DancingSquatresPloterAnimationSerializerSVG(object):
#     START = '''
#     <svg width="%(width)s0" height="%(height)s0">
#         <defs>
#             <g id="arrow">
#                 <circle cx="0" cy="0" r="5"/>
#                 <path d="9"
#             </g>
#         </defs>
#     '''
#     ARROWS = {
#         (0, 1) : "use"
#     }
#     END = '''
#     </svg>
#     '''
#     def __init__(self, ds, dsp, steps):
#         self.ds = ds
#         self.dsp = dsp
#         self.steps = steps
# 
#     def dump(self):
#         ds = self.ds
#         dsp = self.dsp
#         for i in range(self.steps):
#             self.ds.step()
#             for s in ds.squares:
#                 x, y = ds.get_pos(s)
#                 mx, my = ds.get_size()
#                 if x >= 0 and x < mx and y >= 0 and y < my:
#                     text = self.ds
#                 s
# 
# 
#     def 
# 
        

        
if __name__ == '__main__':
    ds = DancingSquatres([Square(0, 0, 0, 0), Square(1, 0, 1, 0),
                         Square(2, 0, 1, 0), Square(5, 0, 0, 0)]) 
    print "Step: 0"
    dsp = DancingSquatresPloter(10, 1)
    print dsp.plot(ds)
    i = 1
    while True:
        try:
            w = raw_input()
        except:
            print
            break
        if w == 'q':
            break
        print "Step: %i" % i
        ds.step()
        print dsp.plot(ds)
        i += 1
        

    

        

