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

sw0 = []
sw1 = []
sw2 = []
sl = []
pw = []
pl = []

for i in range(len(iris)):
    if labels[i] == 0:
        print("Ирис {} принадлежит к кластеру 1".format(i))
        count1 += 1
        sw0.append(iris[i][0])
        # sl.append(iris[i][1])
        # pw.append(iris[i][2])
        # pl.append(iris[i][3])

    elif labels[i] == 1:
        print("Ирис {} принадлежит к кластеру 2".format(i))
        count2 += 1
        sw1.append(iris[i][0])
    else:
        print("Ирис {} принадлежит к кластеру 3".format(i))
        count3 += 1
        sw2.append(iris[i][0])

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

# print(target0)
# print(target1)
# print(target2)

# print(load_iris().target)

# print(labels)

f, p = f_oneway(sw0, sw1, sw2)

print(f)
print(p)

if p < 0.05:
    print('Отклонить нулевую гипотезу: хотя бы одно групповое среднее отличается')
else:
    print('Невозможно отвергнуть нулевую гипотезу: все средние значения группы одинаковы.')