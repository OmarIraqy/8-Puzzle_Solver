import tkinter as tk
from collections import deque
from heapq import heapify, heappush, heappop
import math

class PuzzleState:
    def __init__(self, state, parent=None, action=None, costType=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.costType = costType
        if costType == 1:
            self.cost = self.get_manhattan_distance(self.state) + parent.cost if parent else self.get_manhattan_distance(self.state)
        elif costType == 2:
            self.cost = self.get_euclidean_distance(self.state) + parent.cost if parent else self.get_euclidean_distance(self.state)

    def __eq__(self, other):
        return self.state == other.state

    def __hash__(self):
        return hash(str(self.state))

    def __str__(self):
        return str(self.state)

    def __repr__(self):
        return self.state

    def __lt__(self, other):
        return self.cost < other.cost

    def get_euclidean_distance(self, matrix1):
        cost = 0
        for i in range(3):
            for j in range(3):
                tile = matrix1[i][j]
                goal_row, goal_col = divmod(tile, 3)
                cost += math.sqrt((i - goal_row) ** 2 + (j - goal_col) ** 2)
        return cost

    def get_manhattan_distance(self, matrix1):
        cost = 0
        for i in range(3):
            for j in range(3):
                tile = matrix1[i][j]
                goal_row, goal_col = divmod(tile , 3)
                cost += abs(i - goal_row) + abs(j - goal_col)
        return cost

    def decreaseKey(self,node):
        if self.costType == 1:
            self.cost = self.get_manhattan_distance(self.state) + node.cost
        elif self.costType == 2:
            self.cost = self.get_euclidean_distance(self.state) + node.cost

        self.parent = node


class Game:
    def __init__(self, initial_state):
        self.root = tk.Tk()
        self.root.title("8-Puzzle Solver")
        self.random_initial_state = initial_state
        self.goal_state = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        self.solution_path = None

        self.cell_var = [[tk.StringVar() for _ in range(3)] for _ in range(3)]

        for i in range(3):
            for j in range(3):
                label = tk.Label(self.root, textvariable=self.cell_var[i][j], width=10, height=5, relief="solid",
                                 borderwidth=1, font=("Helvetica", 16), bg="lightblue", fg="darkblue")
                label.grid(row=i, column=j, padx=5, pady=5)

        self.arrow_label = tk.Label(self.root, text="", font=("Arial", 20), bg="lightgreen", fg="darkgreen")
        self.arrow_label.grid(row=3, column=1, padx=5, pady=5, sticky='nsew')

        bfs_button = tk.Button(self.root, text="BFS", command=lambda: self.run_algorithm(1), bg="orange", fg="white",
                               font=("Helvetica", 14), relief="raised")
        bfs_button.grid(row=4, column=0, padx=10, pady=10, sticky='nsew')

        dfs_button = tk.Button(self.root, text="DFS", command=lambda: self.run_algorithm(2), bg="purple", fg="white",
                               font=("Helvetica", 14), relief="raised")
        dfs_button.grid(row=4, column=1, padx=10, pady=10, sticky='nsew')

        a_star_manhattan_button = tk.Button(self.root, text="A* Manhattan", command=lambda: self.run_algorithm(3),
                                            bg="green", fg="white", font=("Helvetica", 14), relief="raised")
        a_star_manhattan_button.grid(row=4, column=2, padx=10, pady=10, sticky='nsew')

        a_star_euclidean_button = tk.Button(self.root, text="A* Euclidean", command=lambda: self.run_algorithm(4),
                                            bg="blue", fg="white", font=("Helvetica", 14), relief="raised")
        a_star_euclidean_button.grid(row=4, column=3, padx=10, pady=10, sticky='nsew')

        # Center the grid and buttons
        for i in range(5):
            self.root.grid_rowconfigure(i, weight=1)
            self.root.grid_columnconfigure(i, weight=1)

        # Update GUI with initial state
        self.update_gui_with_state(initial_state)

        self.root.mainloop()

    def update_gui_with_state(self, state):
        for i in range(3):
            for j in range(3):
                self.cell_var[i][j].set(state[i][j])
    def run_algorithm(self, algorithm):
        if algorithm == 1:
            self.solution_path = self.bfs(self.random_initial_state, self.goal_state)
            self.root.title("8-Puzzle Solver BFS")
        elif algorithm == 2:
            self.solution_path = self.dfs(self.random_initial_state, self.goal_state)
            self.root.title("8-Puzzle Solver DFS")
        elif algorithm == 3:
            self.solution_path = self.A_star(self.random_initial_state, self.goal_state, cost=1)
            self.root.title("8-Puzzle Solver A* Manhattan")
        elif algorithm == 4:
            self.solution_path = self.A_star(self.random_initial_state, self.goal_state, cost=2)
            self.root.title("8-Puzzle Solver A* Euclidean")

        self.update_gui_with_solution_path()

    def bfs(self, initial_state, goal_state):
        start_node = PuzzleState(initial_state)
        goal_node = PuzzleState(goal_state)

        queue = deque([start_node])
        visited = set()

        while queue:
            current_node = queue.popleft()

            if current_node == goal_node:
                print("Amount of nodes visited = " + str(len(visited)))
                path = self.get_path(current_node)
                print("Amount of nodes in Path = " + str(len(path)))
                return path

            if current_node not in visited:
                visited.add(current_node)

                neighbors = self.get_neighbors(current_node.state)
                for last_move, new_position, neighbor_state, move in neighbors:
                    neighbor_node = PuzzleState(neighbor_state, current_node, move)
                    if neighbor_node not in visited:
                        queue.append(neighbor_node)

        return None

    def dfs(self, initial_state, goal_state):
        #hna code aldfs
        return None

    def A_star(self, initial_state, goal_state, cost):
        start_node = PuzzleState(initial_state, costType=cost)
        goal_node = PuzzleState(goal_state, costType=cost)

        heap = [start_node]
        heapify(heap)
        visited = set()

        while heap:
            current_node = heappop(heap)

            if current_node == goal_node:
                print("Amount of nodes visited = " + str(len(visited)))
                path = self.get_path(current_node)
                print("Amount of nodes in Path = " + str(len(path)))
                return path

            if current_node not in visited:
                visited.add(current_node)

                neighbors = self.get_neighbors(current_node.state)
                for last_move, new_position, neighbor_state, move in neighbors:
                    neighbor_node = PuzzleState(neighbor_state, current_node, move, costType=cost)
                    if neighbor_node not in visited and neighbor_node not in heap:
                        heappush(heap, neighbor_node)
                    elif neighbor_node in heap:
                        neighbor_node.decreaseKey(current_node)

        return None

    def get_blank_position(self, state):
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    return i, j

    def get_neighbors(self, state):
        i, j = self.get_blank_position(state)
        neighbors = []

        moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        for move in moves:
            new_i, new_j = i + move[0], j + move[1]

            if 0 <= new_i < 3 and 0 <= new_j < 3:
                new_state = [row.copy() for row in state]
                new_state[i][j], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[i][j]
                neighbors.append(((i, j), (new_i, new_j), new_state, move))

        return neighbors

    def get_path(self, current_node):
        path = []
        while current_node.parent:
            path.insert(0, (current_node.state, current_node.action))
            current_node = current_node.parent
        path.insert(0, (current_node.state, None))
        return path

    def update_gui_with_arrow(self, state, move):
        for i in range(3):
            for j in range(3):
                self.cell_var[i][j].set(state[i][j])

        if move == (0, 1):
            self.arrow_label.config(text="→")
        elif move == (1, 0):
            self.arrow_label.config(text="↓")
        elif move == (0, -1):
            self.arrow_label.config(text="←")
        elif move == (-1, 0):
            self.arrow_label.config(text="↑")
        else:
            self.arrow_label.config(text="Start")

    def update_gui_with_solution_path(self):
        if self.solution_path:
            current_state, current_move = self.solution_path.pop(0)
            self.update_gui_with_arrow(current_state, current_move)
            self.root.after(1000, self.update_gui_with_solution_path)

# Example usage with a random initial state
random_initial_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
game = Game(random_initial_state)
