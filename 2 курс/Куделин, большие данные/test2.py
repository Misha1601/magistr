from sklearn.datasets import load_iris
from sklearn.cluster import KMeans

iris = load_iris().data

kmeans = KMeans(n_clusters=3)

kmeans.fit(iris)
labels = kmeans.labels_

print(123)