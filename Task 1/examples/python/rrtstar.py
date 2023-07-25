import numpy as np
import cv2 as cv
import networkx as nx

brown_colour = [11, 27, 47]  # in bgr


# finding a path using rrt* first
class RRTStar:
    def __init__(
        self,
        maze,
        start,
        goal,
        max_iter=10000,
        max_dist=10,
        goal_sample_rate=0.2,
        search_radius=30,
    ):
        self.maze = maze
        self.start = start
        self.goal = goal
        self.graph = nx.Graph()
        self.graph.add_node(start)
        self.goal_sample_rate = goal_sample_rate
        self.max_iter = max_iter
        self.max_dist = max_dist
        self.search_radius = search_radius

    def run(self):
        # for _ in range(self.max_iter):
        for _ in range(self.max_iter):
            if np.random.uniform() < self.goal_sample_rate:
                q_rand = self.goal
            else:
                q_rand = self.sample_random()

            q_near = self.find_nearest(self.graph.nodes, q_rand)
            q_new = self.steer(q_near, q_rand)

            # print("q_rand: ", q_rand)
            # print("q_near: ", q_near)
            # print("q_new: ", q_new)

            if self.is_valid_move(q_near, q_new):
                # find the least cost node to connect to q_new
                near_nodes = self.find_near_nodes(q_new)
                q_min = q_near
                c_min = self.cost(q_near) + self.dist(q_near, q_new)
                for node in near_nodes:
                    if self.is_valid_move(node, q_new):
                        c = self.cost(node) + self.dist(node, q_new)
                        if c < c_min:
                            c_min = c
                            q_min = node

                # print("added")
                self.graph.add_node(q_new)
                self.graph.add_edge(q_min, q_new)

                # check if we can reach the goal
                if self.is_valid_move(q_new, self.goal):
                    self.graph.add_node(self.goal)
                    self.graph.add_edge(q_new, self.goal)
                    return nx.shortest_path(
                        self.graph, source=self.start, target=self.goal
                    )

                # check if q_new helps other nodes reduce their cost
                for node in near_nodes:
                    if node != q_min and self.is_valid_move(q_new, node):
                        c = self.cost(q_new) + self.dist(q_new, node)
                        if c < self.cost(node):
                            # parent = self.find_nearest(self.graph.neighbors(node), node)
                            # self.graph.remove_edge(node, parent)
                            self.graph.add_edge(q_new, node)

                self.visualize_path(
                    nx.shortest_path(self.graph, source=self.start, target=q_new)
                )

        print(self.graph)
        return None

    def sample_random(self):
        y, x = np.random.uniform(0, self.maze.shape[:2])
        return (x, y)

    def steer(self, q_near, q_rand):
        if self.dist(q_near, q_rand) < self.max_dist:
            return int(q_rand[0]), int(q_rand[1])
        dx = q_near[0] - q_rand[0]
        dy = q_near[1] - q_rand[1]
        angle = np.arctan2(dy, dx) + np.pi
        q_new = int(q_near[0] + self.max_dist * np.cos(angle)), int(
            q_near[1] + self.max_dist * np.sin(angle)
        )
        return q_new

    def find_nearest(self, list, q_rand):
        nearest_dist = float("inf")
        nearest_node = None
        for node in list:
            dist = self.dist(node, q_rand)
            if dist < nearest_dist:
                nearest_dist = dist
                nearest_node = node
        return nearest_node

    def dist(self, q1, q2):
        return np.sqrt((q1[0] - q2[0]) ** 2 + (q1[1] - q2[1]) ** 2)

    def cost(self, node):
        return nx.shortest_path_length(self.graph, source=self.start, target=node)

    def is_valid_move(self, q_near, q_new):
        x_near, y_near = int(q_near[0]), int(q_near[1])
        x_new, y_new = int(q_new[0]), int(q_new[1])

        dx = x_new - x_near
        dy = y_new - y_near
        steps = max(abs(dx), abs(dy))

        if steps == 0:
            return True

        for i in range(1, steps + 1):
            x = x_near + int(i * dx / steps)
            y = y_near + int(i * dy / steps)

            flag = 0
            sub_array = maze_img[y - 1 : y + 2, x - 1 : x + 2]
            for row in sub_array:
                for ele in row:
                    if list(ele) == brown_colour:
                        flag = 1
                        break
                if flag:
                    break

            if flag:
                return False

        return True

    def find_near_nodes(self, q_new):
        near_nodes = []
        for node in self.graph.nodes:
            if self.dist(node, q_new) < self.search_radius:
                near_nodes.append(node)
        return near_nodes

    def visualize_path(self, path):
        maze_with_path = self.maze.copy()
        for node in path:
            x, y = int(node[0]), int(node[1])
            cv.circle(maze_with_path, (x, y), 1, (0, 0, 255), -1)

        cv.imshow("RRT* Path Visualization", maze_with_path)
        cv.waitKey(1)


def avoid_walls(maze_img, path_orig):
    path = np.array(path_orig.copy())

    n = len(path)
    for q in range(1, n - 1):
        node = path[q]
        x, y = node[0], node[1]
        i, j = 0, 0
        flag = 0
        sub_array = maze_img[y - 3 : y + 4, x - 3 : x + 4]
        for i in range(7):
            for j in range(7):
                if list(sub_array[i][j]) == [11, 27, 47]:
                    flag = 1
                    break
            if flag:
                break

        if flag:
            i -= 3
            j -= 3
            if i < 0:
                path[q][1] += 4 + i
            else:
                path[q][1] -= 4 - i
            if j < 0:
                path[q][0] += 4 + j
            else:
                path[q][0] -= 4 - j

    return path


maze_img = cv.imread("map.png")

start_y, start_x = np.where((maze_img == [255, 255, 255]).all(axis=-1))
goal_y, goal_x = np.where((maze_img == [255, 0, 0]).all(axis=-1))

start = (start_x[0], start_y[0])
goal = (goal_x[0], goal_y[0])

while True:
    rrt_star = RRTStar(maze_img, start, goal)
    path = rrt_star.run()

    if path is not None:
        print("Path found!")
        n = len(path)
        for i in range(n - 1):
            cv.line(maze_img, path[i], path[i + 1], (0, 0, 150))
        cv.imshow("path", maze_img)
        cv.imwrite("orig_path.png", maze_img)
        path = avoid_walls(maze_img, path)
        n = len(path)
        for i in range(n - 1):
            cv.line(maze_img, path[i], path[i + 1], (0, 0, 255))
        cv.imshow("path", maze_img)
        cv.imwrite("path.png", maze_img)
        np.savez("path.npz", path_arr=path)
        cv.waitKey(0)
        cv.destroyAllWindows()
        break

    else:
        print("not found")
        print("trying again...")
