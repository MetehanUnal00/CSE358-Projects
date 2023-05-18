import csv
from queue import PriorityQueue
import heapq
from collections import defaultdict


class CityNotFoundError(Exception):
    def __init__(self, city):
        print("%s does not exist" % city)


# Implement this function to read data into an appropriate data structure.
def build_graph(path):
    try:
        with open(path, 'r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header
            roads = [row for row in reader]
    except FileNotFoundError:
        print("The file was not found.")
        return

    graph = defaultdict(list)
    for city1, city2, distance in roads:
        graph[city1].append((city2, int(distance)))
        graph[city2].append((city1, int(distance)))

    return graph




# Implement this function to perform uniform cost search on the graph.
def uniform_cost_search(graph, start, end):
    if start not in graph or end not in graph:
        raise CityNotFoundError(start if start not in graph else end)

    queue = PriorityQueue()
    queue.put((0, start, []))
    visited = set()

    while not queue.empty():
        (cost, city, path) = queue.get()
        if city not in visited:
            visited.add(city)
            path = path + [city]

            if city == end:
                return cost, path

            for next_city, distance in graph[city]:
                if next_city not in visited:
                    queue.put((cost + distance, next_city, path))

    return float("inf"), []



# Implement main to call functions with appropriate try-except blocks
if __name__ == "__main__":
    path = input("Enter the path of the road map file: ")
    graph = build_graph(path)
    if graph:
        start = input("Enter the start city: ")
        end = input("Enter the target city: ")
        try:
            cost, path = uniform_cost_search(graph, start, end)
            if cost == float("inf"):
                print("There is no path from {} to {}.".format(start, end))
            else:
                print("The shortest path from {} to {} is: {}".format(start, end, " -> ".join(path)))
                print("The distance is: {} km".format(cost))
        except CityNotFoundError as e:
            print(e)

