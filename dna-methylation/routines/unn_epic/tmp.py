def cycle_recover(cycle):  # функция для приведения списка связанности к виду, который требует степик
    result_str = str(cycle[0][0])+'->'+str(cycle[0][1])+'->'
    for i in range(1, len(cycle) - 1):
        result_str += str(cycle[i][1])
        result_str += '->'
    result_str += str(cycle[len(cycle) - 1][1])
    return result_str


def euler_cycle(connectivity_components):  # поиск эйлерова цикла в графе
    start = connectivity_components[0]
    cycle = [start]  # стек в который записываются компоненты связанности цикла, который мы ищем
    bad_ways = set()  #
    while True:
        while True:  # ищем какой-то путь, пока не замкнем цикл
            for edge in connectivity_components:
                if start[1] == edge[0] and edge not in cycle and edge not in bad_ways:
                    cycle.append(edge)
                    start = edge
                    bad_ways.clear()
                    break
            if start[1] == cycle[0][0]:
                bad_ways.add(start)
                break
        if len(cycle) == len(connectivity_components):  # если найденый нами цикл обходит все ребра, то он эйлеров и
            #  работа функции завершена
            break

        for c in reversed(cycle):  # проходим по стеку с конца и ищем элемент, из которого мы можем пойти по другому
            # пути.
            for ed in connectivity_components:
                flag = False
                if c[1] == ed[0] and ed not in cycle and ed not in bad_ways:
                    start = c
                    flag = True
                    break
            if flag == False:  # если мы не нашли куда можно перейти из текущего ребра в cycle, то мы удаляем это
                # ребро из cycle и записываем его в bad_ways, чтобы потом снова по нему не пойти
                bad_ways.add(c)
                cycle.pop()
            else:
                break
    # эти два цикла чередуют друг друга. Сначала ищем какой-то цикл, и если он не эйлеров, то удаляем элементы из
    #     стека пока не дойдем до элемента, из которого можем продолжить цикл по другому пути
    #  в конечном итоге этот алгоритм должен привести нас к эйлерову пути
    return cycle


# Input ------------------------------------
def inp():
    with open('tmp.txt') as f:
        lines = f.read().split('\n')
        connectivity_components = []
        for line in lines:
            if line:
                line = line.split('->')
                str1 = line[1].split(',')
                for s in str1:
                    connectivity_components.append((int(line[0]), int(s)))
            else:
                break
        return connectivity_components
# ---------------------------------------------


if __name__ == '__main__':
    connectivity_components = inp()  # список связанности
    cycle = euler_cycle(connectivity_components)
    result = cycle_recover(cycle)
    print(result)