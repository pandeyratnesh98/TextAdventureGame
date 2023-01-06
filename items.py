# Base class for all items
import sounds


class Item:
    # __init__ is the contructor method
    def __init__(self, name, description, value):
        self.name = name  # attribute of the Item class and any subclasses
        self.description = description  # attribute of the Item class and any subclasses
        self.value = value  # attribute of the Item class and any subclasses

    # __str__ method is used to print the object
    def __str__(self):
        return "{}\n=====\n{}\nValue: {}\n".format(self.name, self.description, self.value)


# Extend the Items class
# Gold class will be a child or subclass of the superclass Item
class Gold(Item):
    # __init__ is the contructor method
    def __init__(self, amt):
        self.amt = amt  # attribute of the Gold class
        super().__init__(name="Gold",
                         description="A round coin with {} stamped on the front.".format(str(self.amt)),
                         value=self.amt)


class Potions(Item):
    def __init__(self, name, description, value, amt, health):
        self.amt = amt
        self.health = health
        super().__init__(name, description, value)


class SmallPotion(Potions):
    def __init__(self):
        super().__init__(
            name="Small Potion",
            description="A small potion",
            value=5,
            amt=1,
            health=75
        )


class MagicPotion(Potions):
    def __init__(self):
        super().__init__(
            name="Magic Potion",
            description="A magic potion",
            value=5,
            amt=1,
            health=150
        )


class Weapon(Item):
    def __init__(self, name, description, value, damage):
        self.damage = damage
        super().__init__(name, description, value)

    def sound(self):
        pass

    def __str__(self):
        return "{}\n=====\n{}\nValue: {}\nDamage: {}".format(self.name, self.description, self.value, self.damage)


class Pistol(Weapon):
    def __init__(self):
        super().__init__(name="Pistol",
                         description="A small size hand pistol.",
                         value=0,
                         damage=50)

    def sound(self):
        sounds.pistol()


class Sword(Weapon):
    def __init__(self):
        super().__init__(name="Sword",
                         description="A fine sharped sword.",
                         value=10,
                         damage=35)

    def sound(self):
        sounds.sword()


class Bazooka(Weapon):
    def __init__(self):
        super().__init__(name="Bazooka",
                         description="A big shoulder needed to fire this weapon. this can destroy small-size monsters "
                                     "in one blow",
                         value=10,
                         damage=100)

    def sound(self):
        sounds.bazooka()


class LaserBeam(Weapon):
    def __init__(self):
        super().__init__(name="Laser Beam",
                         description="a small size gun but most effective.",
                         value=10,
                         damage=75)

    def sound(self):
        sounds.laser_beam()
