class Game:
    def __init__(self, map_files):
        self.map_files = map_files
        self.current_map_index = 0
        self.map = self.load_map(self.map_files[self.current_map_index])  # Load the first map
        self.x, self.y = 0, 0  # Starting position
        self.goal = self.find_goal()  # Dynamically find goal position
        self.visited = [[False for _ in range(len(self.map[0]))] for _ in range(len(self.map))]  # Track visited locations
        self.riddle_answered = False  # To track if the player has successfully answered the riddle

    def load_map(self, filename: str) -> list[list[int]]:
        with open(filename, 'r') as file:
            # Read dimensions of the map (in the first line)
            rows, cols = map(int, file.readline().split())

            # Read the map and convert each row into a list of integers
            game_map = []
            for line in file:
                game_map.append([int(char) for char in line.strip()])
        return game_map

    def find_goal(self) -> tuple:
        for i, row in enumerate(self.map):
            for j, cell in enumerate(row):
                if cell == 2:  # Goal cell
                    return i, j
        return None  # Fallback if no goal is found

    def getCurrentLocation(self) -> tuple:
        return self.x, self.y

    def check_escape(self) -> bool:
        if self.x < 0 or self.x >= len(self.map) or self.y < 0 or self.y >= len(self.map[0]):
            return True
        return False

    def set_location(self, x: int, y: int) -> bool:
        if 0 <= x < len(self.map) and 0 <= y < len(self.map[0]) and self.map[x][y] != 0:
            self.x, self.y = x, y
            return True
        return False

    def goal_reached(self) -> bool:
        if self.check_escape():  # Escape the map to win
            print("You escaped the map and won!")
            exit()
        return self.getCurrentLocation() == self.goal

    def can_move(self, direction: str) -> bool:
        if direction == 'north' and self.x > 0 and self.map[self.x - 1][self.y] != 0:
            return True
        elif direction == 'south' and self.x < len(self.map) - 1 and self.map[self.x + 1][self.y] != 0:
            return True
        elif direction == 'east' and self.y < len(self.map[0]) - 1 and self.map[self.x][self.y + 1] != 0:
            return True
        elif direction == 'west' and self.y > 0 and self.map[self.x][self.y - 1] != 0:
            return True
        return False

    def move(self, direction: str) -> bool:
        if direction == 'north':
            return self.set_location(self.x - 1, self.y)
        elif direction == 'south':
            return self.set_location(self.x + 1, self.y)
        elif direction == 'east':
            return self.set_location(self.x, self.y + 1)
        elif direction == 'west':
            return self.set_location(self.x, self.y - 1)
        return False

    def print_map(self):
        """Display the current game map with player's position marked."""
        for i in range(len(self.map)):
            row = ''
            for j in range(len(self.map[i])):
                if (i, j) == (self.x, self.y):
                    row += 'P'  # Player's position
                elif self.map[i][j] == 0:
                    row += '#'  # Obstacle
                elif self.map[i][j] == 2:
                    row += 'G'  # Goal
                else:
                    row += '.'  # Walkable space
            print(row)
        print()  # New line for better formatting

    def answer_riddle(self):
        """Ask the player a riddle they must answer to proceed."""
        riddle = "I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?"
        print("\nA mysterious figure blocks your way and asks the following riddle:")
        print(f"\"{riddle}\"")
        answer = input("Answer: ").strip().lower()
        if answer == "echo":
            print("Correct! The path is now open.")
            self.riddle_answered = True
            return True
        else:
            print("Incorrect. The path remains blocked.")
            return False

def main():
    map_files = ['map1.txt', 'map2.txt', 'map3.txt']  # Add your map files here
    game = Game(map_files)

    # Print the initial game map first
    print("Starting the game! Here's the initial map:")
    game.print_map()

    # Ask the riddle if at starting location
    if (game.x, game.y) == (0, 0) and not game.riddle_answered:
        if not game.answer_riddle():
            # Prevent movement until the player answers the riddle
            while not game.riddle_answered:
                game.answer_riddle()

    while True:  # Main game loop
        # Print the game map for the player
        game.print_map()

        # Prompt player for movement
        direction = input("Which way do you want to go? (north/south/east/west): ").strip().lower()
        if direction not in ['north', 'south', 'east', 'west']:
            print("Invalid direction. Try again.")
            continue

        # Attempt the move
        if game.move(direction):
            if game.goal_reached():
                print("Congratulations! You've reached the goal!")
                break
            if game.check_escape():
                print("You escaped the map and won!")
                exit()
        else:
            print("You can't go that way.")


if __name__ == "__main__":
    main()

