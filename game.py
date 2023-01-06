import sounds
import utils
import world
from player import Player


def play():
    world.load_tiles()
    name = input("Whats Your name?: \t")
    player = Player(name)
    # These lines load the starting room and display the text
    room = world.tile_exists(player.location_x, player.location_y)
    sounds.phone_ringing()
    utils.text_to_speech(f"Hello {name}")
    intro_text="""As you remember,  in 2003, Rohit Mehra's son sent some signals to space and made aliens meet him 
    personally, people don't believe it, but it's true. In this process, an alien just forgot to catch his spaceship 
    because the spaceship driver was very punctual, so he left him on earth to teach him the value of time. In the 
    meantime, Rohit and the alien became friends, and Rohit helped the alien catch his flight, and the alien 
    reciprocated by giving him some powers. The whole incident was happened in Kasol, India. 20 Years later, 
    Rohit received the same signals stating that they would capture Kasol because of its resources. It could happen 
    any minute, so get ready to defend and fight. """
    print(intro_text)
    utils.text_to_speech(intro_text)
    sounds.spaceship_coming()
    utils.spaceship_ascii()
    print(room.intro_text())
    while player.is_alive() and not player.victory:
        room = world.tile_exists(player.location_x, player.location_y)
        room.modify_player(player)
        # Check again since the room could have changed the player's state
        if player.is_alive() and not player.victory:
            print("Choose an action:\n")
            available_actions = room.available_actions()
            for action in available_actions:
                print(action)
            action_input = input('Action: ')
            for action in available_actions:
                if action_input == action.hotkey:
                    player.do_action(action, **action.kwargs)
                    break
    if player.is_alive() and player.victory:
        print("You won!")
        sounds.win()

    print("Game Over you Lost!")
    sounds.game_over()
    utils.text_to_speech("Game Over you Lost!")


if __name__ == "__main__":
    play()
