# -*- coding: cp936 -*-
'''
	������Ϊshortest��pythonģ�飬�ṩ�����ڽ������ʽ15��
	�߼���������Ҫ�Ŀ��Ե����������ĺ�����ʹ�õ������ص�
	Dijkstra�㷨��
'''
import basic
from field_shelve import read_from, write_to # For testing

def available_spots(map_list, unit_list, source_num, prev = None):
    '''�ú������ڼ��㵱ǰ��ͼ��ĳ��λ�Ļ��Χ��
    �������map_list��Ϊ������ͼ��Ԫ�Ķ�ά���鴢���˵�ͼ��ȫ����Ϣ��
    unit_list�ǵ�λ��Ϣ�б�
    source_num��һ��Ԫ�飬Ϊ(side_num, object_num)��
    �β�prev���÷���README��
    ����һ���б��������пɵ���ĵ㣬˳�����ɽ���Զ��'''
    #���㵥λ�赲��λ��
    u_block = [unit_list[i][j].position \
               for i in range(2) for j in range(len(unit_list[i]))]        
    d_spots = [] # �����Ѿ�ȷ���ɵ����ɳ���ϵĵ�
    s_unit = unit_list[source_num[0]][source_num[1]] # Ŀ�굥λ
    s_position = s_unit.position # Դ������
    a_spots = [s_position] # ���б��ɳڹ���δȷ���ɵ��ĵ�
    a_weight = [0]         # ���е�Ȩֵ
    row = len(map_list)
    column = len(map_list[0])
    prev_a = [0]
    d_index = -1 # �����ɴ����d_spots�е���ţ����ڼ���prev
    while True:
        if a_weight == []:
            break
        min_weight = min(a_weight) # ��a_weight����Сֵ
        if min_weight > s_unit.move_range: # ���Ｋ��
            break
        d_index += 1
        s = a_weight.index(min_weight) # ȡ�������
        # �ɳڲ���
        p_modify = ((1, 0), (-1, 0), (0, 1), (0, -1))
        for i in range(4):
            # �����ɳڵ��ĸ������
            p = (p_modify[i][0] + a_spots[s][0], p_modify[i][1] + a_spots[s][1])
            if p[0] < 0 or p[1] < 0 or p[0] >= row or p[1] >= column:
                continue    
            if not (p in u_block or p in d_spots): # �ɳڵ������
                lf = map_list[p[0]][p[1]].type # �ɳڵ�ĵ��� 
                move_cost = basic.FIELD_EFFECT[lf][0] # �õ����������
                if p in a_spots: # ����
                    p_id = a_spots.index(p) # �ɳڵ���a_spots���index
                    if move_cost + a_weight[s] < a_weight[p_id]:
                        a_weight[p_id] = move_cost + a_weight[s]
                        if a_weight[p_id] <= s_unit.move_range:
                            prev_a[p_id] = d_index
                else: 			#�¼���
                    lf = map_list[p[0]][p[1]].type
                    a_spots.append(p)
                    a_weight.append(a_weight[s] + move_cost)
                    if a_weight[s] + move_cost <= s_unit.move_range:
                        prev_a.append(d_index)
        # �ɳڽ����󣬽� s ��a����ɾ���� �������뵽d������
        d_spots.append(a_spots[s]) 
        if not prev == None:      
            prev.append(prev_a[s])
        a_spots.pop(s)
        a_weight.pop(s)
        prev_a.pop(s)
    return d_spots

def GetRoute(maps, units, idnum, end):
    route = []
    last = []
    try:
        field = available_spots(maps, units, idnum, last)
        ind = field.index(end)
        start = units[idnum[0]][idnum[1]].position
        route.append(field[ind])
        while (start!=field[ind]):
            ind = last[ind]
            route.append(field[ind])
        route.reverse()
        return route
    except:
        pass #raise error
    #possibility: 1. invalid pos 2. invalid idnum

def main():
    (map_list, unit_list) = read_from()
    prev = []
    print available_spots(map_list, unit_list, (1, 0), prev)
    print prev
    raw_input("print anything to continue")

if __name__ == '__main__':
    main()


