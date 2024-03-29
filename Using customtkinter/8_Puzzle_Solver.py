import time
import tkinter
import customtkinter
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
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title("8-Puzzle Solver")
        self.random_initial_state = None
        self.goal_state = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        self.solution_path = None

        self.cell_var = [[tkinter.StringVar() for _ in range(3)] for _ in range(3)]

        for i in range(3):
            for j in range(3):
                label = customtkinter.CTkLabel(master= self.root, textvariable=self.cell_var[i][j], width=150, height=100, font=("Helvetica", 16), fg_color="#90d0f5", corner_radius=10)
                label.grid(row=i, column=j, padx=5, pady=5)

        self.initial_state_entry =customtkinter.CTkEntry(master=self.root, font=("Helvetica", 12))
        self.initial_state_entry.grid(row=3, columnspan=3, pady=10)

        submit_button = customtkinter.CTkButton(master=self.root, text="Submit Initial State", command=self.submit_initial_state,
                                   fg_color="gray", font=("Helvetica", 12))
        submit_button.grid(row=4, columnspan=3, pady=10)

        self.arrow_label = customtkinter.CTkLabel(master=self.root, text="", font=("Arial", 20), fg_color="white", text_color="black")
        self.arrow_label.grid(row=5, columnspan=3, pady=7, sticky='nsew')

        bfs_button = customtkinter.CTkButton(master=self.root, text="BFS", command=lambda: self.run_algorithm(1), fg_color="dark blue",
                               font=("Helvetica", 14), border_width=3)
        bfs_button.grid(row=6, column=0, padx=10, pady=10, sticky='nsew')

        dfs_button = customtkinter.CTkButton(master= self.root, text="DFS", command=lambda: self.run_algorithm(2), fg_color="dark blue",
                               font=("Helvetica", 14),border_width=3)
        dfs_button.grid(row=6, column=1, padx=10, pady=10, sticky='nsew')

        a_star_manhattan_button = customtkinter.CTkButton(master=self.root, text="A* Manhattan", command=lambda: self.run_algorithm(3),
                                            fg_color="dark blue", font=("Helvetica", 14),border_width=3)
        a_star_manhattan_button.grid(row=6, column=2, padx=10, pady=10, sticky='nsew')

        a_star_euclidean_button = customtkinter.CTkButton(master=self.root, text="A* Euclidean", command=lambda: self.run_algorithm(4),
                                            fg_color="dark blue", font=("Helvetica", 14),border_width=3)
        a_star_euclidean_button.grid(row=6, column=3, padx=10, pady=10, sticky='nsew')

        for i in range(7):
            self.root.grid_rowconfigure(i, weight=1)
            self.root.grid_columnconfigure(i, weight=1)

        self.root.mainloop()

    def submit_initial_state(self):
        input_text = self.initial_state_entry.get()
        try:
            self.random_initial_state = [[int(char) for char in row] for row in input_text.split(',')]
            self.update_gui_with_state(self.random_initial_state)
        except ValueError:
            print("Invalid input. Please enter a valid comma-separated 3x3 matrix.")

    def update_gui_with_state(self, state):
        for i in range(3):
            for j in range(3):
                self.cell_var[i][j].set(state[i][j])

    def run_algorithm(self, algorithm):
        start = 0
        end = 0
        if algorithm == 1:
            start = time.time()
            self.solution_path = self.bfs(self.random_initial_state, self.goal_state)
            end = time.time()
            self.root.title("8-Puzzle Solver BFS")
        elif algorithm == 2:
            start = time.time()
            self.solution_path = self.dfs(self.random_initial_state, self.goal_state)
            end = time.time()
            self.root.title("8-Puzzle Solver DFS")
        elif algorithm == 3:
            start = time.time()
            self.solution_path = self.A_star(self.random_initial_state, self.goal_state, cost=1)
            end = time.time()
            self.root.title("8-Puzzle Solver A* Manhattan")
        elif algorithm == 4:
            start = time.time()
            self.solution_path = self.A_star(self.random_initial_state, self.goal_state, cost=2)
            end = time.time()
            self.root.title("8-Puzzle Solver A* Euclidean")

        print("Time Taken by Algorithm = " + str(end - start))

        if self.solution_path is not None:
            self.update_gui_with_solution_path()
        else:
            # Display a message in the GUI indicating no solution
            self.arrow_label.configure(text="No Solution")

    def bfs(self, initial_state, goal_state):
        start_node = PuzzleState(initial_state)
        goal_node = PuzzleState(goal_state)

        queue = deque([start_node])
        visited = set()

        while queue:
            current_node = queue.popleft()

            if current_node == goal_node:
                print("Amount of nodes visited by BFS = " + str(len(visited)))
                path = self.get_path(current_node)
                print("Amount of nodes in Path by Bfs = " + str(len(path)))
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
        start_node = PuzzleState(initial_state)
        goal_node = PuzzleState(goal_state)

        stack = [start_node]
        visited = set()

        while stack:
            current_node = stack.pop()

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
                        stack.append(neighbor_node)

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
                print("Amount of nodes visited by A* = " + str(len(visited)))
                path = self.get_path(current_node)
                print("Amount of nodes in Path by A* = " + str(len(path)))
                print("Cost by A* = " + str(current_node.cost))
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
            self.arrow_label.configure(text="→")
        elif move == (1, 0):
            self.arrow_label.configure(text="↓")
        elif move == (0, -1):
            self.arrow_label.configure(text="←")
        elif move == (-1, 0):
            self.arrow_label.configure(text="↑")
        else:
            self.arrow_label.configure(text="Start")

    def update_gui_with_solution_path(self):
        if self.solution_path:
            current_state, current_move = self.solution_path.pop(0)
            self.update_gui_with_arrow(current_state, current_move)
            self.root.after(1000, self.update_gui_with_solution_path)

game = Game()
