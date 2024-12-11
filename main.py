import random
import json
import os
from collections import deque

# ANSI color codes
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
GRAY = "\033[90m"

def handle_monster():
    print(RED + "\nYou encounter a fearsome monster!" + RESET)
    print("           (    )")
    print("          ((((()))")
    print("          |o\\ /o)|")
    print("          ( (  _') ")
    print("           (._.  /\\")
    print("          ,/___,/  \\")
    print("          `-----'   " + RESET)
    print("You must decide:")
    print("- Fight the monster (F)")
    print("- Scare it away (S)")
    print("- Sneak past it (N)")

    while True:
        choice = input("> ").strip().lower()
        if choice == "f":
            print(GREEN + "You bravely fight the monster and defeat it!" + RESET)
            break
        elif choice == "s":
            print(CYAN + "You scare the monster away with a loud roar!" + RESET)
            break
        elif choice == "n":
            print(YELLOW + "You successfully sneak past the monster." + RESET)
            break
        else:
            print("Invalid choice. Please choose F, S, or N.")


def handle_witches():
    print(MAGENTA + "\nYou stumble upon a coven of witches brewing potions!" + RESET)
    print(MAGENTA + "       /\\         /\\\n"
                    "      {  `---'  }\n"
                    "      {  O   O  }\n"
                    "      ~~>  V  <~~\n"
                    "       \\  \\|/  /\n"
                    "        `-----'__\n"
                    "        /     \\  `^\n"
                    "       {       } |\n"
                    "       |  \\_/  |/ |\n"
                    "        \\__/  /(_/\n"
                    "          (__/ " + RESET)
    print("One witch approaches and says, 'Answer this riddle correctly, and we’ll let you pass.'")
    print(YELLOW + "Riddle: I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?" + RESET)

    attempts = 0
    while attempts < 2:
        answer = input("> ").strip().lower()
        if answer == "echo":
            print(GREEN + "Correct! The witches let you pass." + RESET)
            break
        else:
            print("Wrong answer. Try again.")
            attempts += 1
    else:
        print("Hint: It's something you hear in a canyon or valley.")
        while True:
            answer = input("> ").strip().lower()
            if answer == "echo":
                print(GREEN + "Correct! The witches let you pass." + RESET)
                break
            else:
                print("Incorrect. Try again.")


def handle_pirates():
    print(CYAN + "\nYou encounter a band of pirates! They block your way and demand treasure." + RESET)
    print(CYAN + "      _~\n   _~ )_)_~\n   \\_~_\\_\\~_\n    ~  \\_)  " + RESET)
    print("- Give them treasure (T)")
    print("- Fight them off (F)")

    while True:
        choice = input("> ").strip().lower()
        if choice == "t":
            print(GREEN + "You give the pirates treasure, and they let you pass." + RESET)
            break
        elif choice == "f":
            print(RED + "You fight bravely and defeat the pirates!" + RESET)
            break
        else:
            print("Invalid choice. Please choose T or F.")


def handle_tribe():
    print(YELLOW + "\nYou meet a peaceful tribe deep in the jungle. They challenge you with a riddle." + RESET)
    print(YELLOW + "      /^\\    /^\\ \n     {  O}  {  O}\n      \\ /    \\ / \n       X      X  " + RESET)
    print("Riddle: The more you take, the more you leave behind. What am I?")

    answer = input("> ").strip().lower()
    if answer == "footsteps":
        print(GREEN + "Correct! The tribe welcomes you and gives you a blessing." + RESET)
    else:
        print(WHITE + "Incorrect. The tribe allows you to leave unharmed." + RESET)


def generate_maze(rows, cols):
    # Initialize the grid with walls (0)
    maze = [[0 for _ in range(cols)] for _ in range(rows)]

    # Starting cell
    start_x, start_y = 0, 0
    maze[start_x][start_y] = 1  # Mark as a passage

    # Use a stack for DFS
    stack = [(start_x, start_y)]

    # Directions for carving paths: (dx, dy)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while stack:
        x, y = stack[-1]

        neighbors = []
        for dx, dy in directions:
            nx, ny = x + 2 * dx, y + 2 * dy
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 0:
                if maze[x + dx][y + dy] == 0:
                    neighbors.append((nx, ny, dx, dy))

        if neighbors:
            nx, ny, dx, dy = random.choice(neighbors)
            maze[x + dx][y + dy] = 1
            maze[nx][ny] = 1
            stack.append((nx, ny))
        else:
            stack.pop()

    # Place the goal:
    goal_x, goal_y = find_farthest_cell(maze, start_x, start_y)
    maze[goal_x][goal_y] = 2

    # Add special encounters
    add_special_encounters(maze, count=5)

    return maze


def find_farthest_cell(maze, sx, sy):
    rows = len(maze)
    cols = len(maze[0])
    queue = deque([(sx, sy, 0)])
    visited = set([(sx, sy)])
    farthest_cell = (sx, sy)
    max_dist = 0

    while queue:
        x, y, dist = queue.popleft()
        if dist > max_dist:
            max_dist = dist
            farthest_cell = (x, y)

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                if maze[nx][ny] == 1 and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny, dist + 1))
    return farthest_cell


def add_special_encounters(maze, count=5):
    rows = len(maze)
    cols = len(maze[0])
    passages = [(i, j) for i in range(rows) for j in range(cols) if maze[i][j] == 1 and not (i == 0 and j == 0)]
    random.shuffle(passages)
    encounter_types = [3, 4, 5, 6]
    for _ in range(count):
        if passages:
            x, y = passages.pop()
            maze[x][y] = random.choice(encounter_types)


class Game:
    def __init__(self, map_files, maze_rows=20, maze_cols=50, load_state=None):
        self.map_files = map_files
        self.num_file_maps = len(map_files)
        self.maze_rows = maze_rows
        self.maze_cols = maze_cols

        if load_state:
            # Load from saved state
            self.current_map_index = load_state['current_map_index']
            self.map = load_state['map']
            self.x = load_state['x']
            self.y = load_state['y']
            self.goal = tuple(load_state['goal'])
            self.visited = load_state['visited']
            self.riddle_answered = load_state['riddle_answered']
            self.use_random_maps = load_state['use_random_maps']
        else:
            self.current_map_index = 0
            self.use_random_maps = False
            self.map = self.load_current_map()
            self.x, self.y = 0, 0
            self.goal = self.find_goal()
            self.visited = [[False for _ in range(len(self.map[0]))] for _ in range(len(self.map))]
            self.riddle_answered = False

    def load_map(self, filename: str) -> list[list[int]]:
        with open(filename, 'r') as file:
            rows, cols = map(int, file.readline().split())
            return [[int(char) for char in line.strip()] for line in file]

    def load_current_map(self):
        # If we still have file-based maps, load from file, else generate a random map
        if self.current_map_index < self.num_file_maps:
            return self.load_map(self.map_files[self.current_map_index])
        else:
            self.use_random_maps = True
            return generate_maze(self.maze_rows, self.maze_cols)

    def find_goal(self) -> tuple:
        for i, row in enumerate(self.map):
            for j, cell in enumerate(row):
                if cell == 2:
                    return i, j
        return None

    def get_current_location(self) -> tuple:
        return self.x, self.y

    def check_escape(self) -> bool:
        return self.x < 0 or self.x >= len(self.map) or self.y < 0 or self.y >= len(self.map[0])

    def set_location(self, x: int, y: int) -> bool:
        if 0 <= x < len(self.map) and 0 <= y < len(self.map[0]) and self.map[x][y] != 0:
            self.x, self.y = x, y
            return True
        return False

    def goal_reached(self) -> bool:
        if self.get_current_location() == self.goal:
            print(GREEN + "Congratulations! You've reached the goal!" + RESET)
            self.current_map_index += 1
            if self.use_random_maps:
                # Generate another random map indefinitely
                print(CYAN + "Generating a new random maze..." + RESET)
                self.map = generate_maze(self.maze_rows, self.maze_cols)
                self.goal = self.find_goal()
                self.x, self.y = 0, 0
                self.visited = [[False for _ in range(len(self.map[0]))] for _ in range(len(self.map))]
                return False
            else:
                if self.current_map_index < self.num_file_maps:
                    print(YELLOW + f"Loading map {self.current_map_index + 1}..." + RESET)
                    self.map = self.load_current_map()
                    self.goal = self.find_goal()
                    self.x, self.y = 0, 0
                    self.visited = [[False for _ in range(len(self.map[0]))] for _ in range(len(self.map))]
                    return False
                else:
                    print(GREEN + "You have completed all file-based maps! Moving on to random maps..." + RESET)
                    self.map = generate_maze(self.maze_rows, self.maze_cols)
                    self.goal = self.find_goal()
                    self.x, self.y = 0, 0
                    self.visited = [[False for _ in range(len(self.map[0]))] for _ in range(len(self.map))]
                    self.use_random_maps = True
                    return False
        return False

    def can_move(self, direction: str) -> bool:
        dx, dy = {"north": (-1, 0), "south": (1, 0), "east": (0, 1), "west": (0, -1)}.get(direction, (0, 0))
        nx, ny = self.x + dx, self.y + dy
        return 0 <= nx < len(self.map) and 0 <= ny < len(self.map[0]) and self.map[nx][ny] != 0

    def move(self, direction: str) -> bool:
        dx, dy = {"north": (-1, 0), "south": (1, 0), "east": (0, 1), "west": (0, -1)}.get(direction, (0, 0))
        nx, ny = self.x + dx, self.y + dy
        if self.set_location(nx, ny):
            cell_value = self.map[self.x][self.y]
            if cell_value == 3:
                handle_monster()
            elif cell_value == 4:
                handle_witches()
            elif cell_value == 5:
                handle_pirates()
            elif cell_value == 6:
                handle_tribe()
            return True
        return False

    def print_map(self):
        # Colorize the map
        for i in range(len(self.map)):
            row_str = ""
            for j in range(len(self.map[i])):
                if (i, j) == (self.x, self.y):
                    # Player
                    row_str += BLUE + 'P' + RESET
                else:
                    cell = self.map[i][j]
                    if cell == 0:
                        # Wall
                        row_str += GRAY + '#' + RESET
                    elif cell == 1:
                        # Path
                        row_str += '.'  # Default color (white)
                    elif cell == 2:
                        # Goal
                        row_str += GREEN + 'G' + RESET
                    elif cell == 3:
                        # Monster
                        row_str += RED + 'M' + RESET
                    elif cell == 4:
                        # Witches
                        row_str += MAGENTA + 'W' + RESET
                    elif cell == 5:
                        # Pirates
                        row_str += CYAN + 'R' + RESET
                    elif cell == 6:
                        # Tribe
                        row_str += YELLOW + 'T' + RESET
            print(row_str)
        print()

    def answer_riddle(self):
        riddle = "I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?"
        print("\n" + MAGENTA + "A mysterious figure blocks your way and asks the following riddle:" + RESET)
        print(YELLOW + f"\"{riddle}\"" + RESET)
        while True:
            answer = input("Answer: ").strip().lower()
            if answer == "echo":
                print(GREEN + "Correct! The path is now open." + RESET)
                self.riddle_answered = True
                return True
            else:
                print(RED + "Incorrect. Try again." + RESET)

    def save_game(self):
        # Prompt for save file name
        filename = input("Enter a filename to save your game: ").strip()
        if not filename:
            filename = "savegame.json"
        state = {
            'current_map_index': self.current_map_index,
            'map': self.map,
            'x': self.x,
            'y': self.y,
            'goal': self.goal,
            'visited': self.visited,
            'riddle_answered': self.riddle_answered,
            'use_random_maps': self.use_random_maps,
            'map_files': self.map_files,
            'maze_rows': self.maze_rows,
            'maze_cols': self.maze_cols
        }
        with open(filename, 'w') as f:
            json.dump(state, f)
        print(GREEN + f"Game saved to {filename}." + RESET)


def load_game():
    filename = input("Enter the saved game filename: ").strip()
    if not os.path.exists(filename):
        print(RED + "No such save file." + RESET)
        return None
    with open(filename, 'r') as f:
        state = json.load(f)
    return state


def main():
    # Initially defined map files
    map_files = ['map1.txt', 'map2.txt', 'map3.txt']

    # At startup, give the option to start a new game or load one
    choice = ''
    while choice not in ['n', 'l']:
        choice = input("Do you want to start a New game (N) or Load a saved game (L)? ").strip().lower()

    if choice == 'l':
        load_state = load_game()
        if load_state is None:
            print("Starting a new game instead.")
            load_state = None
    else:
        load_state = None

    game = Game(map_files=map_files, maze_rows=20, maze_cols=50, load_state=load_state)

    print("Welcome to the adventure game!")
    game.print_map()

    if not game.riddle_answered:
        while not game.answer_riddle():
            pass

    while True:
        game.print_map()
        direction = input("Which direction? (north/south/east/west) or type 'save' to save: ").strip().lower()
        if direction == 'save':
            game.save_game()
            continue
        if direction in ['north', 'south', 'east', 'west']:
            if not game.move(direction):
                print(RED + "You can't move that way." + RESET)
            else:
                if game.goal_reached():
                    # infinite random mazes continue
                    pass
        else:
            print(RED + "Invalid input. Try again." + RESET)


if __name__ == "__main__":
    main()
