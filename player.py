import random

import items
import sounds
import world
import utils


class Player:

    def __init__(self, name):
        self.inventory = [items.Gold(15), items.Pistol(), items.SmallPotion(),
                          items.SmallPotion(), ]  # Inventory on startup
        self.name = name
        self.hp = 200  # Health Points
        self.maxHp = 200
        self.location_x, self.location_y = world.starting_position  # (0, 0)
        self.currentWpn = self.inventory[1]
        self.experience = 0
        self.level = 1
        self.attackPower = 100
        self.nextLevelUp = 30
        self.victory = False  # no victory on start up

    def flee(self, tile):
        """Moves the player randomly to an adjacent tile"""
        available_moves = tile.adjacent_moves()
        r = random.randint(0, len(available_moves) - 1)
        self.do_action(available_moves[r])

    # is_alive method
    def is_alive(self):
        return self.hp > 0  # Greater than zero value then you are still alive

    def print_inventory(self):
        for item in self.inventory:
            sounds.equip()
            print(item, '\n')

    def move(self, dx, dy):
        sounds.walking()
        self.location_x += dx
        self.location_y += dy
        print(world.tile_exists(self.location_x, self.location_y).intro_text())

    def move_north(self):
        self.move(dx=0, dy=-1)

    def move_south(self):
        self.move(dx=0, dy=1)

    def move_east(self):
        self.move(dx=1, dy=0)

    def move_west(self):
        self.move(dx=-1, dy=0)

    def attack(self, enemy):
        self.currentWpn.sound()
        print("You use {} against {}!".format(self.currentWpn.name, enemy.name))
        enemy.hp -= self.currentWpn.damage
        if not enemy.is_alive():
            self.experience += enemy.experience
            print("You killed {}!".format(enemy.name))
            self.is_level_up(enemy)
        else:
            print("{} HP is {}.".format(enemy.name, enemy.hp))

    def equip(self):
        print("\n These are the weapons you currently possess:\n")
        weapon_list = []
        for item in self.inventory:
            if isinstance(item, items.Weapon):
                weapon_list.append(item)
        i = 1
        for weapon in weapon_list:
            print(i, ",", weapon.name, sep=" ")
            i += 1
        while True:
            item_choice = utils.get_int_input("\n Select the weapon you want to equip:\n") - 1
            if item_choice not in range(0, len(weapon_list)):
                print("\n Invalid weapon choice")
                continue
            break

        print("\n")
        sounds.equip()
        print(weapon_list[item_choice].name, "equipped.\n")
        self.currentWpn = weapon_list[item_choice]

    def heal(self):
        print("\n These are the potions you currently possess:\n")
        potion_list = []
        for potion in self.inventory:
            if isinstance(potion, items.Potions):
                if potion.amt <= 0:
                    self.inventory.remove(potion)
                    continue
                else:
                    potion_list.append(potion)
        i = 1
        for potion in potion_list:
            print(i, potion.name, sep=" ")
            i += 1
        while True:
            if len(potion_list) == 0:
                print("you have no potions")
                return None
            item_choice = utils.get_int_input("\n Select a Potion.\n")
            if item_choice not in range(0, len(potion_list)):
                print("\n Invalid Choice.")
                continue
            break
        self.heal_to_player(item_choice, potion_list)

    def heal_to_player(self, item_choice, potion_list):
        chosen_potion = potion_list[item_choice]
        sounds.drinking()
        sounds.healed()
        print("\nYou were healed for {} ".format(chosen_potion.health))
        self.hp = self.hp + chosen_potion.health
        chosen_potion.amt = chosen_potion.amt - 1
        if chosen_potion.amt == 0:
            self.inventory.remove(chosen_potion)

        if self.maxHp < self.hp:
            self.hp = self.maxHp

    def status(self):
        print("\nYou are a level {} \n".format(self.level))
        print(" * Current HP: {} /".format(self.hp), "{}\n".format(self.maxHp))
        print(" * Attack Power: {} \n".format(self.attackPower))
        print(" * Total XP: {} \n".format(self.experience))

    def do_action(self, action, **kwargs):
        action_method = getattr(self, action.method.__name__)
        if action_method:
            action_method(**kwargs)

    def is_level_up(self, enemy):
        if self.nextLevelUp <= self.experience:
            self.level += 1
            self.maxHp += 20
            self.attackPower += 30
            self.nextLevelUp *= 2
            print("*********************")
            print("\n* Level Upgraded! *\n")
            print("*********************")
            print("\nYou are at level {} now\n".format(self.level))
            print("* Maximum HP increased to: {}".format(self.maxHp))
            print("* Attack Power increased to: {} \n".format(self.attackPower))
            print("* Your XP increased to: {} \n".format(self.experience))
            sounds.level_up()
            utils.text_to_speech(f"Level Upgraded! You are at level {self.level} now")
