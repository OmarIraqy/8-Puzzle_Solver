import time
import tkinter as tk
from collections import deque
from heapq import heapify, heappush, heappop
import math

class PuzzleState:
    # Each Puzzle State has:
    # state : which is the shape of the puzzle
    # parent : which is the node that added this state in the frontier list
    # action : the move made to get from the parent to this node
    # costType : to indicate which heuristic to use in case of A* (0--> no cost , 1--> Manhattan , 2--> Euclidean)
    def __init__(self, state, parent=None, action=None, costType=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.costType = costType
        if costType == 1:
            self.cost = self.get_manhattan_distance(self.state) + parent.cost if parent else self.get_manhattan_distance(self.state)
        elif costType == 2:
            self.cost = self.get_euclidean_distance(self.state) + parent.cost if parent else self.get_euclidean_distance(self.state)

    # overriding equality function so that two nodes are equal if they have the same puzzle shape
    def __eq__(self, other):
        return self.state == other.state

    def __hash__(self):
        return hash(str(self.state))

    def __str__(self):
        return str(self.state)

    def __repr__(self):
        return self.state

   # Overriding the less than function that's used by the heap
    def __lt__(self, other):
        return self.cost < other.cost

    # Calculating Euclidean Distance from node to goal
    def get_euclidean_distance(self, matrix1):
        cost = 0
        for i in range(3):
            for j in range(3):
                tile = matrix1[i][j]
                goal_row, goal_col = divmod(tile, 3)
                cost += math.sqrt((i - goal_row) ** 2 + (j - goal_col) ** 2)
        return cost

    # Calculating Manhattan Distance from node to goal
    def get_manhattan_distance(self, matrix1):
        cost = 0
        for i in range(3):
            for j in range(3):
                tile = matrix1[i][j]
                goal_row, goal_col = divmod(tile , 3)
                cost += abs(i - goal_row) + abs(j - goal_col)
        return cost

    # Decreasing the cost of a state in case the parent is changed
    def decreaseKey(self,node):
        if self.costType == 1:
            self.cost = self.get_manhattan_distance(self.state) + node.cost
        elif self.costType == 2:
            self.cost = self.get_euclidean_distance(self.state) + node.cost

        self.parent = node



class Game:
    # Initializing the game's GUI and stating the goal state
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("8-Puzzle Solver")
        self.random_initial_state = None
        self.goal_state = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        self.solution_path = None

        self.cell_var = [[tk.StringVar() for _ in range(3)] for _ in range(3)]

        for i in range(3):
            for j in range(3):
                label = tk.Label(self.root, textvariable=self.cell_var[i][j], width=10, height=5, relief="solid",
                                 borderwidth=1, font=("Helvetica", 16), bg="lightblue", fg="darkblue")
                label.grid(row=i, column=j, padx=5, pady=5)

        self.initial_state_entry = tk.Entry(self.root, font=("Helvetica", 12), justify="center")
        self.initial_state_entry.grid(row=3, columnspan=3, pady=10)

        submit_button = tk.Button(self.root, text="Submit Initial State", command=self.submit_initial_state,
                                  bg="gray", fg="white", font=("Helvetica", 12), relief="raised")
        submit_button.grid(row=4, columnspan=3, pady=10)

        self.arrow_label = tk.Label(self.root, text="", font=("Arial", 20), bg="lightgreen", fg="darkgreen")
        self.arrow_label.grid(row=5, columnspan=3, pady=10, sticky='nsew')

        bfs_button = tk.Button(self.root, text="BFS", command=lambda: self.run_algorithm(1), bg="orange", fg="white",
                               font=("Helvetica", 14), relief="raised")
        bfs_button.grid(row=6, column=0, padx=10, pady=10, sticky='nsew')

        dfs_button = tk.Button(self.root, text="DFS", command=lambda: self.run_algorithm(2), bg="purple", fg="white",
                               font=("Helvetica", 14), relief="raised")
        dfs_button.grid(row=6, column=1, padx=10, pady=10, sticky='nsew')

        a_star_manhattan_button = tk.Button(self.root, text="A* Manhattan", command=lambda: self.run_algorithm(3),
                                            bg="green", fg="white", font=("Helvetica", 14), relief="raised")
        a_star_manhattan_button.grid(row=6, column=2, padx=10, pady=10, sticky='nsew')

        a_star_euclidean_button = tk.Button(self.root, text="A* Euclidean", command=lambda: self.run_algorithm(4),
                                            bg="blue", fg="white", font=("Helvetica", 14), relief="raised")
        a_star_euclidean_button.grid(row=6, column=3, padx=10, pady=10, sticky='nsew')

        for i in range(7):
            self.root.grid_rowconfigure(i, weight=1)
            self.root.grid_columnconfigure(i, weight=1)

        self.root.mainloop()

    # taking initial state from user
    def submit_initial_state(self):
        input_text = self.initial_state_entry.get()
        try:
            self.random_initial_state = [[int(char) for char in row] for row in input_text.split(',')]
            self.update_gui_with_state(self.random_initial_state)
        except ValueError:
            print("Invalid input. Please enter a valid comma-separated 3x3 matrix.")

    # Updating the gui with a state
    def update_gui_with_state(self, state):
        for i in range(3):
            for j in range(3):
                self.cell_var[i][j].set(state[i][j])

    # Calling of Searching Algorithms and calculating the time taken.
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
            self.arrow_label.config(text="No Solution")

    # BFS Search
    def bfs(self, initial_state, goal_state):
        start_node = PuzzleState(initial_state)
        goal_node = PuzzleState(goal_state)

        queue = deque([start_node])
        visited = set()

        nodes_in_memory = []
        while queue:
            current_node = queue.popleft()
            nodes_in_memory.append(len(queue)+len(visited))
            if current_node == goal_node:
                print("Number of nodes visited by BFS = " + str(len(visited)))
                print("Max Number of nodes in memory = " + str(max(nodes_in_memory)))
                path = self.get_path(current_node)
                print("Number of nodes in Path by Bfs = " + str(len(path)))
                return path

            if current_node not in visited:
                visited.add(current_node)

                neighbors = self.get_neighbors(current_node.state)
                for last_move, new_position, neighbor_state, move in neighbors:
                    neighbor_node = PuzzleState(neighbor_state, current_node, move)
                    if neighbor_node not in visited:
                        queue.append(neighbor_node)

        return None

    # DFS Search
    def dfs(self, initial_state, goal_state):
        start_node = PuzzleState(initial_state)
        goal_node = PuzzleState(goal_state)

        stack = [start_node]
        visited = set()

        nodes_in_memory = []
        while stack:
            current_node = stack.pop()

            nodes_in_memory.append(len(stack) + len(visited))
            if current_node == goal_node:
                print("Number of nodes visited = " + str(len(visited)))
                print("Max Number of nodes in memory = " + str(max(nodes_in_memory)))
                path = self.get_path(current_node)
                print("Number of nodes in Path = " + str(len(path)))
                return path

            if current_node not in visited:
                visited.add(current_node)

                neighbors = self.get_neighbors(current_node.state)
                for last_move, new_position, neighbor_state, move in neighbors:
                    neighbor_node = PuzzleState(neighbor_state, current_node, move)
                    if neighbor_node not in visited:
                        stack.append(neighbor_node)

        return None

    # A* search
    def A_star(self, initial_state, goal_state, cost):
        start_node = PuzzleState(initial_state, costType=cost)
        goal_node = PuzzleState(goal_state, costType=cost)

        heap = [start_node]
        heapify(heap)
        visited = set()

        nodes_in_memory = []
        while heap:
            current_node = heappop(heap)

            nodes_in_memory.append(len(heap) + len(visited))
            if current_node == goal_node:
                print("Number of nodes visited by A* = " + str(len(visited)))
                print("Max Number of nodes in memory = " + str(max(nodes_in_memory)))
                path = self.get_path(current_node)
                print("Number of nodes in Path by A* = " + str(len(path)))
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
                        heapify(heap)

        return None

    # Finding the blank tile position
    def get_blank_position(self, state):
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    return i, j

    # Getting neighbors of a state
    def get_neighbors(self, state):
        i, j = self.get_blank_position(state)
        neighbors = []

        # All possible moves
        moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        for move in moves:
            new_i, new_j = i + move[0], j + move[1]

            # Checking that it's not out of border
            if 0 <= new_i < 3 and 0 <= new_j < 3:
                new_state = [row.copy() for row in state]
                new_state[i][j], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[i][j]
                neighbors.append(((i, j), (new_i, new_j), new_state, move))

        return neighbors

    # Getting the solution path
    def get_path(self, current_node):
        path = []
        while current_node.parent:
            path.insert(0, (current_node.state, current_node.action))
            current_node = current_node.parent
        path.insert(0, (current_node.state, None))
        return path

    # Updating the arrow in the GUI
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

    # Displaying the states of the solution path
    def update_gui_with_solution_path(self):
        if self.solution_path:
            current_state, current_move = self.solution_path.pop(0)
            self.update_gui_with_arrow(current_state, current_move)
            self.root.after(1000, self.update_gui_with_solution_path)

# Starting the Game
game = Game()