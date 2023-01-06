import actions
import enemies
import items
import sounds
import utils
import world


class MapTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.beenThere = False

    def intro_text(self):
        raise NotImplementedError()

    def modify_player(self, player):
        raise NotImplementedError()

    def adjacent_moves(self):
        """Returns all move actions for adjacent tiles."""
        moves = []
        if world.tile_exists(self.x + 1, self.y):
            moves.append(actions.MoveEast())
        if world.tile_exists(self.x - 1, self.y):
            moves.append(actions.MoveWest())
        if world.tile_exists(self.x, self.y - 1):
            moves.append(actions.MoveNorth())
        if world.tile_exists(self.x, self.y + 1):
            moves.append(actions.MoveSouth())
        return moves

    def available_actions(self):
        """Returns all of the available actions in this room."""
        moves = self.adjacent_moves()
        moves.append(actions.ViewInventory())
        moves.append(actions.Equip())
        moves.append(actions.Heal())
        moves.append(actions.Status())

        return moves


class StartingShuttle(MapTile):
    # override the intro_text method in the superclass
    def intro_text(self):
        if self.beenThere:
            return "Oh no not again at the starting point"
        else:
            self.beenThere=True
            return """
                    You find yourself in a space shuttle with lots of monsters inside the spaceship.
                    you have to find self-destructing button and destroy the Spaceship to save the Kasol.
                    """

    def modify_player(self, player):
        # Room has no action on player
        pass


class LootRoom(MapTile):
    def __init__(self, x, y, item, beenThere):
        self.item = item
        self.beenThere = beenThere
        super().__init__(x, y)

    def add_loot(self, player):
        player.inventory.append(self.item)

    def modify_player(self, player):
        self.add_loot(player)


class EnemyRoom(MapTile):
    def __init__(self, x, y, enemy):
        self.enemy = enemy
        super().__init__(x, y)

    def modify_player(self, the_player):
        if self.enemy.is_alive():
            sounds.enemy_attack()
            the_player.hp = the_player.hp - self.enemy.damage
            utils.text_to_speech(f"Enemy does {self.enemy.damage} damage.")
            utils.text_to_speech(f"You have {the_player.hp} HP remaining.")
            print("Enemy does {} damage. You have {} HP remaining.".format(self.enemy.damage, the_player.hp))

    def available_actions(self):
        if self.enemy.is_alive():
            return [actions.Flee(tile=self), actions.Attack(enemy=self.enemy), actions.Equip(), actions.Heal(),
                    actions.Status()]
        else:
            moves = self.adjacent_moves()
            moves.append(actions.Equip())
            moves.append(actions.Heal())
            moves.append(actions.Status())

            return moves


class EmptySpaceShuttle(MapTile):
    def intro_text(self):
        if self.beenThere:
            return """Oh again at the same empty shuttle! Have to concentrate this time"""
        else:
            self.beenThere = True
            return """Ah! Empty shuttle ha, This time for sure I'll find a person who is responsible for this 
            destruction. """

    def modify_player(self, player):
        # Room has no action on player
        pass


class AlienRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.Alien())

    def intro_text(self):
        if self.enemy.is_alive():
            utils.alien_ascii()
            sounds.alien()
            return """
            Single alien is approaching you, don't let your guard down!
            """
        else:
            return """
            The corpse of a dead alien laying on the ground.
            """


class WolfMonsterShuttle(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.WolfMonster())

    def intro_text(self):
        if self.enemy.is_alive():
            utils.wolf_monster_ascii()
            sounds.wolf_monster()
            return """A wolf monster jumps down in front of you! I guess someone must turn a human into monster. Now 
            focus and you must win."""
        else:
            return """
             The corpse of a dead wolf monster is on the ground.
             """


class CyborgShuttle(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.Cyborg())

    def intro_text(self):
        if self.enemy.is_alive():
            utils.cyborg_ascii()
            sounds.cyborg()
            return """A vicious cyborg jumps down in front of you! One wrong move and you'll be dead."""
        else:
            return """The dead cyborg laying on the ground. Today must be my lucky day because even I am not 
            sure How I killed this son of a bitch! """


class DemonShuttle(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.Demon())

    def intro_text(self):
        if self.enemy.is_alive():
            utils.demon_ascii()
            sounds.demon()
            return """Demon approaching you! He has insatiable hunger for blood so don't let your guard down even for a 
            moment. """
        else:
            return """The demons dead body is fading away slowly! I'm feeling good watching this badass getting 
            erased slowly. """


class GarauMainVillainShuttle(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.GarauMainVillain())

    def intro_text(self):
        if self.enemy.is_alive():
            utils.garau_ascii()
            sounds.main_villain()
            return """Look carefully! Garau is coming! he is responsible for this havoc. Now it's time 
            give him punishment he deserves. """
        else:
            return """Garau is laying on the ground! this suits him the best!. """


class FindSwordRoom(LootRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.Sword(), beenThere=False)

    def intro_text(self):
        if self.beenThere:
            return """
            You've been here before...
            This is where you found a sword"""
        else:
            utils.sword_ascii()
            self.beenThere = True
            sounds.pulling_out_sword()
            return """
                    Your notice something shiny in the corner.
                    It's a Sword! You pick it up.
                    """


class MedicalShuttle(LootRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.MagicPotion(), beenThere=False)

    def intro_text(self):
        if self.beenThere:
            return """
            You've been here before...
            This is where you found health potions"""
        else:
            return """
                    This looks like a some advance medical shuttle. I must search some medicine to regain my health.
                    Today surely is my lucky day! I found magic potion here!
                    """


class SelfDestructionShuttle(MapTile):
    def intro_text(self):
        utils.text_to_speech("""Great! See that red button on main machine that is self destruction button can 
        destroy whole spaceship and monsters inside it with a single click... ... Now click it and get rid of these 
        monsters. Victory is yours!""")
        sounds.nuke()
        sounds.win()
        return """Great! See that red button on main machine that is self destruction button can destroy whole 
        spaceship and monsters inside it with a single click... ... Now click it and get rid of these monsters. 
 
 
        Victory is yours!
        """

    def modify_player(self, player):
        player.victory = True
