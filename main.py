import random
import math
import json
import sys

min_coord = -5000
max_coord = 5000
exist_coord = []
color_coord = []

# Saves clusters to a JSON file for future visualization or analysis
def save_clusters_to_file(clusters, filename="clusters.json"):
    with open(filename, 'w') as file:
        json.dump(clusters, file)

# Calculates the Euclidean distance between two points in 2D space
def euclidean_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

# Calculates the centroid (average point) of a set of points
def calculate_centroid(points):
    sum_x = sum(point[0] for point in points)
    sum_y = sum(point[1] for point in points)
    centroid_x = sum_x / len(points)
    centroid_y = sum_y / len(points)
    return (int(centroid_x), int(centroid_y))

# Finds the medoid, the point with the minimum sum of distances to all other points in the cluster
def calculate_medoid(points):
    medoids = []
    for current_medoid in points:
        cur_sum_path = sum(euclidean_distance(current_medoid, point2) for point2 in points)
        medoids.append((cur_sum_path, current_medoid))
    return min(medoids)[1]

# Generates 20 unique random coordinates
def generate_20_coordinates():
    i = 0
    while i < 20:
        x = random.randint(min_coord, max_coord)
        y = random.randint(min_coord, max_coord)
        if (x, y) not in exist_coord:
            exist_coord.append((x, y))
            i += 1

# Runs the k-means algorithm for clustering points using centroids or medoids
def k_means(points, centers, k, which_kmeans):
    while True:
        clusters = [[[], centers[i]] for i in range(k)]
        for point in points:
            distances = [euclidean_distance(point, center) for center in centers]
            closer_center = distances.index(min(distances))
            clusters[closer_center][0].append(point)
        last_centers = centers[:]
        for i in range(k):
            if which_kmeans == 1:
                clusters[i][1] = calculate_centroid(clusters[i][0])
            else:
                clusters[i][1] = calculate_medoid(clusters[i][0])
            centers[i] = clusters[i][1]
        print(last_centers)
        print(centers)
        if last_centers == centers:
            break
    return clusters

# Finds the cluster with the largest spread (sum of squared distances from the centroid)
def find_largest_spread(clusters):
    spreads = []
    for cluster in clusters:
        points = cluster[0]
        centroid = cluster[1]
        distances = sum(euclidean_distance(point, centroid) ** 2 for point in points)
        spreads.append(distances)
    return spreads.index(max(spreads))

# Runs the divisive clustering
def divisive_clustering(clusters, k, k_clusters):
    if k_clusters == 1:
        cluster = clusters
    else:
        max_clusters_index = find_largest_spread(clusters)
        cluster = clusters.pop(max_clusters_index)[0]
    res = (0, [(0, 0), (0, 0)])
    for point in cluster:
        for point2 in cluster:
            dist = euclidean_distance(point, point2)
            if dist > res[0]:
                res = (dist, [point, point2])
    centroids = res[1]
    if k_clusters == 1:
        clusters = k_means(cluster, centroids, 2, 1)
    else:
        new_clusters = k_means(cluster, centroids, 2, 1)
        clusters.append(new_clusters[0])
        clusters.append(new_clusters[1])
    k_clusters += 1
    print("Current number of clusters: " + str(k_clusters))
    if k_clusters == k:
        return clusters
    else:
        return divisive_clustering(clusters, k, k_clusters)

# Main function to initialize the clustering process based on user choice
def main():
    choice = sys.argv[1].lower()
    generate_20_coordinates()
    i = 0
    while i < 40000:
        parent = random.choice(exist_coord)
        max_x_offset = 100
        max_y_offset = 100
        min_x_offset = -100
        min_y_offset = -100
        if parent[0] + max_x_offset > max_coord:
            max_x_offset = max_coord - parent[0]
        if parent[1] + max_y_offset > max_coord:
            max_y_offset = max_coord - parent[1]
        if parent[0] + min_x_offset < min_coord:
            min_x_offset = min_coord - parent[0]
        if parent[1] + min_y_offset < min_coord:
            min_y_offset = min_coord - parent[1]
        x_offset = random.randint(min_x_offset, max_x_offset)
        y_offset = random.randint(min_y_offset, max_y_offset)
        new_x = parent[0] + x_offset
        new_y = parent[1] + y_offset
        if (new_x, new_y) not in exist_coord:
            exist_coord.append((new_x, new_y))
            i += 1
        if i % 1000 == 0:
            print('Processed {} points'.format(i))
    if choice == 'c':
        k = 20
        clusters = k_means(exist_coord, exist_coord[:k], k, 1)
    elif choice == 'm':
        k = 20
        clusters = k_means(exist_coord, exist_coord[:k], k, 0)
    else:
        k = 20
        clusters = divisive_clustering(exist_coord, k, 1)
    save_clusters_to_file(clusters)

if __name__ == "__main__":
    main()
