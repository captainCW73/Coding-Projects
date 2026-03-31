class Player:
    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.health = 100

    def move(self, direction):
        # Update the player's position based on the direction
        if direction == "left":
            self.position[0] -= 1
        elif direction == "right":
            self.position[0] += 1
        elif direction == "up":
            self.position[1] += 1
        elif direction == "down":
            self.position[1] -= 1

    def jump(self):
        # Implement jump logic
        print(f"{self.name} jumps!")

    def attack(self):
        # Implement attack logic
        print(f"{self.name} attacks!")