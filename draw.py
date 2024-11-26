import json
import math
import matplotlib.pyplot as plt

min_coord = -5000
max_coord = 5000

# Load clusters from a file
def load_clusters_from_file(filename="clusters.json"):
    with open(filename, 'r') as f:
        clusters = json.load(f)
    return clusters


# Calculate the Euclidean distance between two points
def euclidean_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


# Evaluate the quality of clusters and return the average distance for each cluster
def evaluate_cluster_quality(clusters):
    average_distances = []

    for i, cluster in enumerate(clusters):
        points = cluster[0]
        centroid = cluster[1]

        distances = [euclidean_distance(point, centroid) for point in points]
        average_distance = sum(distances) / len(distances)
        average_distances.append(average_distance)

    return average_distances


# Visualize clusters and centroids with the average distance displayed
def draw_clusters_with_distances(clusters, average_distances, min_coord, max_coord):
    color_map = plt.get_cmap('tab20', len(clusters))
    plt.figure(figsize=(8, 8))

    for i, cluster in enumerate(clusters):
        points = cluster[0]
        centroid = cluster[1]

        x_coords = [point[0] for point in points]
        y_coords = [point[1] for point in points]

        # Display cluster points
        plt.scatter(x_coords, y_coords, c=[color_map(i)], s=10)

        # Display centroid
        plt.scatter(centroid[0], centroid[1], c=[color_map(i)], edgecolors='black', s=20)

        # Add text with the average distance near the centroid
        plt.text(centroid[0], centroid[1], f"{average_distances[i]:.2f}",
                 fontsize=8, ha='right', color='black')

    plt.title('Clusters Visualization with Average Distances')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.grid(True)
    plt.xlim(min_coord, max_coord)
    plt.ylim(min_coord, max_coord)
    plt.show()


def main():
    clusters = load_clusters_from_file()

    # Evaluate cluster quality and get the average distance for each cluster
    average_distances = evaluate_cluster_quality(clusters)

    # Visualize clusters with the average distance displayed
    draw_clusters_with_distances(clusters, average_distances, min_coord, max_coord)


if __name__ == "__main__":
    main()
