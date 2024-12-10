def handle_monster():
    print("\nYou encounter a fearsome monster! You must decide:")
    print("- Fight the monster (F)")
    print("- Scare it away (S)")
    print("- Sneak past it (N)")

    while True:
        choice = input("> ").strip().lower()
        if choice == "f":
            print("You bravely fight the monster and defeat it!")
            break
        elif choice == "s":
            print("You scare the monster away with a loud roar!")
            break
        elif choice == "n":
            print("You successfully sneak past the monster.")
            break
        else:
            print("Invalid choice. Please choose F, S, or N.")


def handle_witches():
    print("\nYou stumble upon a coven of witches brewing potions!")
    print("One witch approaches and says, 'Answer this riddle correctly, and we’ll let you pass.'")
    print(
        "Riddle: I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?")

    attempts = 0
    while attempts < 2:
        answer = input("> ").strip().lower()
        if answer == "echo":
            print("Correct! The witches let you pass.")
            break
        else:
            print("Wrong answer. Try again.")
            attempts += 1
    else:
        print("Hint: It's something you hear in a canyon or valley.")
        while True:
            answer = input("> ").strip().lower()
            if answer == "echo":
                print("Correct! The witches let you pass.")
                break
            else:
                print("Incorrect. Try again.")


def handle_pirates():
    print("\nYou encounter a band of pirates! They block your way and demand treasure.")
    print("- Give them treasure (T)")
    print("- Fight them off (F)")

    while True:
        choice = input("> ").strip().lower()
        if choice == "t":
            print("You give the pirates treasure, and they let you pass.")
            break
        elif choice == "f":
            print("You fight bravely and defeat the pirates!")
            break
        else:
            print("Invalid choice. Please choose T or F.")


def handle_tribe():
    print("\nYou meet a peaceful tribe deep in the jungle. They challenge you with a riddle.")
    print("Riddle: The more you take, the more you leave behind. What am I?")

    answer = input("> ").strip().lower()
    if answer == "footsteps":
        print("Correct! The tribe welcomes you and gives you a blessing.")
    else:
        print("Incorrect. The tribe allows you to leave unharmed.")


class Game:
    def __init__(self, map_files):
        self.map_files = map_files
        self.current_map_index = 0
        self.map = self.load_map(self.map_files[self.current_map_index])
        self.x, self.y = 0, 0
        self.goal = self.find_goal()
        self.visited = [[False for _ in range(len(self.map[0]))] for _ in range(len(self.map))]
        self.riddle_answered = False

    def load_map(self, filename: str) -> list[list[int]]:
        with open(filename, 'r') as file:
            rows, cols = map(int, file.readline().split())
            return [[int(char) for char in line.strip()] for line in file]

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
            print("Congratulations! You've reached the goal!")
            if self.current_map_index < len(self.map_files) - 1:
                self.current_map_index += 1
                self.map = self.load_map(self.map_files[self.current_map_index])
                self.goal = self.find_goal()
                self.x, self.y = 0, 0
                self.visited = [[False for _ in range(len(self.map[0]))] for _ in range(len(self.map))]
                print(f"Moving to map {self.current_map_index + 1}!")
                return False
            else:
                print("You've completed all maps! Well done!")
                return True
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
        for i in range(len(self.map)):
            row = ''
            for j in range(len(self.map[i])):
                if (i, j) == (self.x, self.y):
                    row += 'P'
                elif self.map[i][j] == 0:
                    row += '#'
                elif self.map[i][j] == 2:
                    row += 'G'
                else:
                    row += '.'
            print(row)
        print()

    def answer_riddle(self):
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
    map_files = ['map1.txt', 'map2.txt', 'map3.txt']
    game = Game(map_files)

    print("Welcome to the adventure game!")
    game.print_map()

    if not game.riddle_answered:
        while not game.answer_riddle():
            pass

    while True:
        game.print_map()
        direction = input("Which direction? (north/south/east/west): ").strip().lower()
        if direction in ['north', 'south', 'east', 'west']:
            if not game.move(direction):
                print("You can't move that way.")
            elif game.goal_reached():
                break
        else:
            print("Invalid input. Try again.")


if __name__ == "__main__":
    main()
