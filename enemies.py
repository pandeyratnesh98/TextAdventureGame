class Enemy:
    def __init__(self, name, hp, damage, experience):
        self.name = name
        self.hp = hp
        self.damage = damage
        self.experience = experience

    def is_alive(self):
        return self.hp > 0


class Cyborg(Enemy):
    def __init__(self):
        super().__init__(name="Cyborg", hp=200, damage=85, experience=340)


class Alien(Enemy):
    def __init__(self):
        super().__init__(name="Alien", hp=30, damage=25, experience=30)


class WolfMonster(Enemy):
    def __init__(self):
        super().__init__(name="Wolf Monster", hp=65, damage=35, experience=60)


class Demon(Enemy):
    def __init__(self):
        super().__init__(name="Demon", hp=145, damage=55, experience=125)


class GarauMainVillain(Enemy):
    def __init__(self):
        super().__init__(name="Garau", hp=350, damage=100, experience=550)
