path = 'E:/YandexDisk/Work/pydnameth/methylation_and_proteomic/limma/liver'

f = open(f'{path}/test3.txt')
t1_list = f.readlines()
t1_list = list(map(str.strip, t1_list))
f.close()
t1 = set(t1_list)
x = len(t1)

f = open(f'{path}/test2.txt')
t2_list = f.readlines()
t2_list = list(map(str.strip, t2_list))
f.close()
t2 = set(t2_list)
y = len(t2)

t_int = t1.intersection(t2)

a = len(t_int)

ololo = 1


