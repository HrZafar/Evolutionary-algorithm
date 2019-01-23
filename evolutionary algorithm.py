import random


def fitness(x, y):
    return round(100 * (x ** 2 - y) ** 2 + (1 - x) ** 2, 2)


def insertionSort(alist, check):
    for i in range(1, len(alist)):
        key = alist[i]
        j = i - 1
        while j >= 0 and key['fitness'] < alist[j]['fitness']:
            alist[j + 1] = alist[j]
            j -= 1
        alist[j + 1] = key
    if check == 0:
        return alist[-1]['fitness']
    else:
        return alist


def gen_individuals(n):
    list = []
    for i in range(n):
        dict = {}
        dict['x'] = round(random.uniform(-2, 2.01), 2)
        if dict['x'] > 2:
            dict['x'] = 2
        dict['y'] = round(random.uniform(-1, 3.01), 2)
        if dict['y'] > 3:
            dict['y'] = 3
        dict['fitness'] = fitness(dict['x'], dict['y'])
        list.append(dict)
    return list


def random_parents(n):
    p1 = random.randint(0, n - 1)
    p2 = random.randint(0, n - 1)
    while p1 == p2:
        p2 = random.randint(0, n - 1)
    return p1, p2


def truncation_survival(list):
    list = insertionSort(list, 1)
    list1 = []
    i = len(list) - 1
    for k in range(n):
        list1.append(list[i])
        i -= 1
    return list1


def check_cumulative(list):
    a = round(random.uniform(0, 1.00001), 5)
    if a > 1:
        a = 1
    for i in range(len(list)):
        if a <= list[i]['cumulative']:
            return list[i]['position']


def fitness_proportion(list):
    total_fitness = 0
    for i in range(len(list)):
        total_fitness = list[i]['fitness'] + total_fitness
    a = 0
    fitness = []
    for i in range(len(list)):
        dict = {}
        dict['proportion'] = round(list[i]['fitness'] / total_fitness, 5)
        dict['cumulative'] = round(dict['proportion'] + a, 5)
        dict['position'] = i
        a = a + dict['proportion']
        fitness.append(dict)
    p1 = check_cumulative(fitness)
    p2 = check_cumulative(fitness)
    while p1 == p2:
        p2 = check_cumulative(fitness)
    return p1, p2


def rank_based(list):
    total = 0
    for i in range(1, len(list) + 1):
        total = i + total
    fitness = []
    for i in range(len(list)):
        dict = {}
        dict['fitness'] = list[i]['fitness']
        dict['position'] = i
        fitness.append(dict)
    fitness = insertionSort(fitness, 1)
    a = 0
    for i in range(len(fitness)):
        fitness[i]['proportion'] = round((i + 1) / total, 5)
        fitness[i]['cumulative'] = round(fitness[i]['proportion'] + a, 5)
        a = a + fitness[i]['proportion']
    p1 = check_cumulative(fitness)
    p2 = check_cumulative(fitness)
    while p1 == p2:
        p2 = check_cumulative(fitness)
    return p1, p2


def binary_tournament(list):
    p1_1 = random.randint(0, len(list) - 1)
    p1_2 = random.randint(0, len(list) - 1)
    while p1_1 == p1_2:
        p1_2 = random.randint(0, len(list) - 1)
    if list[p1_1]['fitness'] > list[p1_2]['fitness']:
        p1 = p1_1
    else:
        p1 = p1_2
    p2_1 = random.randint(0, len(list) - 1)
    p2_2 = random.randint(0, len(list) - 1)
    while p2_1 == p2_2:
        p2_2 = random.randint(0, len(list) - 1)
    if list[p2_1]['fitness'] > list[p2_2]['fitness']:
        p2 = p2_1
    else:
        p2 = p2_2
    while p1 == p2:
        p1, p2 = binary_tournament(list)
    return p1, p2


def mutation(child):
    probability = random.randint(1, 100)
    if probability > 25:
        mutation_value = random.randint(1, 100)
        if mutation_value > 50:
            mutation_value = .25
        else:
            mutation_value = -.25
        which_gene = random.randint(1, 100)
        if which_gene > 50:
            child['x'] = round(child['x'] + mutation_value, 2)
            if child['x'] < -2:
                child['x'] = -2
            elif child['x'] > 2:
                child['x'] = 2
        else:
            child['y'] = round(child['y'] + mutation_value, 2)
            if child['y'] < -1:
                child['y'] = -1
            elif child['y'] > 3:
                child['y'] = 3
    return child


def crossover(list, p1, p2):
    ch1, ch2 = {}, {}
    ch1['x'], ch1['y'] = list[p1]['x'], list[p2]['y']
    ch2['x'], ch2['y'] = list[p2]['x'], list[p1]['y']
    ch1 = mutation(ch1)
    ch1['fitness'] = fitness(ch1['x'], ch1['y'])
    ch2 = mutation(ch2)
    ch2['fitness'] = fitness(ch2['x'], ch2['y'])
    return ch1, ch2


file = open('max_fitness per generation.txt', 'w')
n = 25
m = 20
gen = 50
childs = []
generation = gen_individuals(n)
print('Generation 0', generation)
file.write(str(round(insertionSort(generation, 0), 2)))
file.write('\n')

for i in range(gen - 1):
    for j in range(int(m / 2)):
        parent1, parent2 = binary_tournament(generation)  ######## PARENT SELECTION ##################
        childs.extend(crossover(generation, parent1, parent2))
    generation_1 = generation + childs
    # generation=truncation_survival(generation_1)             ######## SURVIVAL SELECTION ##################
    generation = []
    for k in range(int(n + 1 / 2)):
        p1, p2 = binary_tournament(generation_1)  ######## SURVIVAL SELECTION ##################
        generation.append(generation_1[p1])
        generation.append(generation_1[p2])
    print('Generation', i + 1, generation)
    file.write(str(round(insertionSort(generation, 0), 2)))
    file.write('\n')

file.close()
