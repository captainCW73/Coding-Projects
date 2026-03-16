class Enemy:
    def __init__(self, name, health, damage):
        self.name = name
        self.health = health
        self.damage = damage
        self.position = (0, 0)

    def patrol(self):
        # Logic for patrolling behavior
        pass

    def attack(self, player):
        # Logic for attacking the player
        pass

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.die()

    def die(self):
        # Logic for enemy death
        pass