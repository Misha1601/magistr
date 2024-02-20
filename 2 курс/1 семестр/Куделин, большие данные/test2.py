from sklearn.datasets import load_iris
from sklearn.cluster import KMeans
from scipy.stats import f_oneway

iris = load_iris().data
print(iris)
target = load_iris().target


kmeans = KMeans(n_clusters=3)

kmeans.fit(iris)
labels = kmeans.labels_

count1 = 0
count2 = 0
count3 = 0

target0 = 0
target1 = 0
target2 = 0

sw0 = []
sw1 = []
sw2 = []
sl0 = []
sl1 = []
sl2 = []
pw0 = []
pw1 = []
pw2 = []
pl0 = []
pl1 = []
pl2 = []

target_map1 = {
    1: 0,
    2: 0,
    3: 0
}
target_map2 = {
    1: 0,
    2: 0,
    3: 0
}
target_map3 = {
    1: 0,
    2: 0,
    3: 0
}

for i in range(len(iris)):
    if labels[i] == 0:
        print("Ирис {} принадлежит к кластеру 1".format(i))
        count1 += 1
        if i < 50:
            target0 += 1
            target_map1[1] += 1
        elif 50<=i<100:
            target_map1[2] += 1
        else:
            target_map1[3] += 1

        sw0.append(iris[i][0])
        sl0.append(iris[i][1])
        pw0.append(iris[i][2])
        pl0.append(iris[i][3])

    elif labels[i] == 1:
        print("Ирис {} принадлежит к кластеру 2".format(i))
        count2 += 1
        # if 50<=i<100:
            # target1 += 1

        if i < 50:
            target_map2[1] += 1
        elif 50<=i<100:
            target1 += 1
            target_map2[2] += 1
        else:
            target_map2[3] += 1
        sw1.append(iris[i][0])
        sl1.append(iris[i][1])
        pw1.append(iris[i][2])
        pl1.append(iris[i][3])
    else:
        print("Ирис {} принадлежит к кластеру 3".format(i))
        count3 += 1

        if i < 50:
            target_map3[1] += 1
        elif 50<=i<100:
            target_map3[2] += 1
        else:
            target2 += 1
            target_map3[3] += 1

        sw2.append(iris[i][0])
        sl2.append(iris[i][1])
        pw2.append(iris[i][2])
        pl2.append(iris[i][3])

print('count')
print(count1)
print(count2)
print(count3)


# target0 = 0
# target1 = 0
# target2 = 0
# for i in target:
#     if i == 0:
#         target0 += 1
#     if i == 1:
#         target1 += 1
#     if i == 2:
#         target2 += 1
print('target')
print(target0)
print(target1)
print(target2)
print('map')
print("map1", target_map1)
print("map2", target_map2)
print("map3", target_map3)
# print(load_iris().target)

# print(labels)

print('sw')
f, p = f_oneway(sw0, sw1, sw2)

print(f)
print(p)

if p < 0.05:
    print('Отклонить нулевую гипотезу: хотя бы одно групповое среднее отличается')
else:
    print('Невозможно отвергнуть нулевую гипотезу: все средние значения группы одинаковы.')

print('sl')
f, p = f_oneway(sl0, sl1, sl2)

print(f)
print(p)

if p < 0.05:
    print('Отклонить нулевую гипотезу: хотя бы одно групповое среднее отличается')
else:
    print('Невозможно отвергнуть нулевую гипотезу: все средние значения группы одинаковы.')

print('pw')
f, p = f_oneway(pw0, pw1, pw2)

print(f)
print(p)

if p < 0.05:
    print('Отклонить нулевую гипотезу: хотя бы одно групповое среднее отличается')
else:
    print('Невозможно отвергнуть нулевую гипотезу: все средние значения группы одинаковы.')

print('pl')
f, p = f_oneway(pl0, pl1, pl2)

print(f)
print(p)

if p < 0.05:
    print('Отклонить нулевую гипотезу: хотя бы одно групповое среднее отличается')
else:
    print('Невозможно отвергнуть нулевую гипотезу: все средние значения группы одинаковы.')

# print("  1|2|3")
row = "   "
for i in range(1, 4):
    row += f"{i: >4} |"
print(row)
print('-'*len(row))
row = "1 |"
for val in target_map1.values():
    row += f"{val: >4} |"
print(row)
row = "2 |"
for val in target_map2.values():
    row += f"{val: >4} |"
print(row)
row = "3 |"
for val in target_map3.values():
    row += f"{val: >4} |"
print(row)


# print("1 "+"|".join(list(map(str, target_map1.values()))))
# print("2 "+"|".join(list(map(str, target_map2.values()))))
# print("3 "+"|".join(list(map(str, target_map3.values()))))