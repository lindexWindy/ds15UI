# -*- coding: UTF-8 -*-

from Ui_Units import *

m = Map_Basic
u = Base_Unit

maps = [[m(0), m(0), m(1), m(1)],
        [m(1), m(1), m(0), m(1)],
        [m(1), m(0), m(1), m(0)],
        [m(0), m(0), m(1), m(1)]]
units0 = [[u(1, (0, 0)), u(2, (0, 1)), u(3, (0, 2))],
          [u(3, (3, 3)), u(2, (3, 2)), u(1, (3, 1))]]
iniInfo = Begin_Info(maps, units0)


#初始位置:(0, 0) (0, 1) (0, 2)
#        (3, 3) (3, 2) (3, 1)

units1 = [[u(1, (1, 1)), u(2, (0, 1)), u(3, (0, 2))],
          [u(3, (3, 3)), u(2, (3, 2)), u(1, (3, 1))]]
begInfo0 = Round_Begin_Info((0, 0), [], units0, [])
cmd0 = Command(0, (1, 1))
endInfo0 = Round_End_Info(units1, [], (-1, -1), (0, 0), -1)

#第零回合：
#id 0 : (0, 0)->(1, 1) standby

units2 = [[u(1, (1, 1)), u(2, (2, 1)), u(3, (0, 2))],
          [u(3, (3, 3)), u(2, (3, 2)), u(1, (3, 1))]]
begInfo1 = Round_Begin_Info((0, 1), [], units1, [])
cmd1 = Command(0, (2, 1))
endInfo1 = Round_End_Info(units2, [], (-1, -1), (0, 0), 0)

#第一回合：
#id 1 : (0, 1)->(2, 1) standby
