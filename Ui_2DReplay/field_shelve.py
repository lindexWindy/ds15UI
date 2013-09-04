'''ʹ��shelveģ��ĵ�ͼ�ļ��洢��д��ģ�顣
   �ۺϿ��ǣ�������shelve������ԡ���'''

import shelve
import basic

default = "default_map.db"
key = ("map", "base") # ����shelve��ļ�ֵΪ"map"��"base"


def change_path(path):
    '''����б�Ҫ�Ļ�������һ���ı�·���ĺ���Ҳ�Ǽ��õ�'''
    pass

def read_from(filename = default, change_path = 0):
    '''���ļ��ж�ȡ��ͼ��Ϣ�͵�λ��Ϣ�ĺ���,
    ���������ļ���(��չ��һ��Ϊ.db)��·���ı�
    ������Ϊ�βΣ����ض�ԪԪ��(map, base)����
    ͼ�͵�λ�б�'''
    if change_path:
        pass # TODO!!!
    try:
        shelv_in = shelve.open(filename)
        return (shelv_in[key[0]], shelv_in[key[1]])
    except IOError as err:
        print 'File error: ' + str(err)
    except KeyError as kerr:
        print 'Key error: ' + str(kerr)
    finally:
        shelv_in.close();

def write_to(info_tuple, filename = default, change_path = 0):
    '''����ͼ��Ϣ�͵�λ��Ϣд���ļ�, ���ܶ�ԪԪ��(map, base)
    Ϊ������filename��change_path����ͬ�ϡ�д��ɹ�����1��
    ���򷵻�0.'''
    if change_path:
        pass # TODO!!!
    try:
        shelv_out = shelve.open(filename)
        shelv_out[key[0]] = info_tuple[0]
        shelv_out[key[1]] = info_tuple[1]
        return 1 
    except IOError as err:
        print 'File error: ', str(err)
        return 0
    except KeyError as kerr:
        print 'Key error: ', str(kerr)
        return 0
    finally:
        shelv_out.close()

def main():
    '''������'''
    (field, base) = read_from()  
    for each in field:
        for eeach in each:
            print eeach.type
        print

    for each in base[0]:
        print each.position
    for each in base[1]:
        print each.position
    raw_input("press anything to continue")
if __name__ == '__main__':
    main()

