import json
import random
import re

TAXONS = ["genus", "subtribe", "subfamily", "family", "superfamily", "parvorder", "infraorder", "suborder"]

def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return " ".join(text.split())

def load_primate_data(json_filepath: str) -> tuple[list, dict]:
    with open(json_filepath, "r", encoding='utf-8') as a_file:
        species = json.load(a_file)    

    lookup = {}
    for specie in species:
        names = [specie["scientific"], specie["common"]] + specie.get("aliases", [])
        for name in names:
            key = normalize(name)
            if key:
                lookup[key] = specie

    return species, lookup

def mystery_select(species: list) -> dict:
    return random.choice(species)

def evaluate(answer: dict, user_guess: str, lookup: dict) -> dict:
    guess = lookup.get(normalize(user_guess))
    if not guess:
        return {"status": "INVALID", "message": "Species not recognized in database."}

    if guess["id"] == answer["id"]:
        return {"status": "CORRECT", "guess": guess}

    target_tax = answer.get("taxonomy", {})
    guess_tax = guess.get("taxonomy", {})

    shared_rank = None
    shared_group_name = None

    for rank in TAXONS:
        t_val = target_tax.get(rank)
        g_val = guess_tax.get(rank)
        if t_val and g_val and t_val == g_val:
            shared_rank = rank
            shared_group_name = t_val
            break  # Stop at narrowest matching rank

    return {
        "status": "INCORRECT",
        "guessed_animal": guess,
        "shared_rank": shared_rank,
        "shared_group": shared_group_name
    }

def game():
    moves = 20
    hints = 3
    print("Thus begins a game of Metaprima.")
    while moves > 0:
        guess = input(">> ")
        if guess == "q":
            keybinds()
        elif guess == "c":
            if hints > 0:
                print("Hint demo")
                hints -= 1
            else:
                print("You're out of hints!")
        elif guess == "g":
            print("")
        elif guess == "x":
            print("Goodbye!")
            exit()
        else:
            evaluate()

def menu():
    print("===========================================================================")
    print("Welcome to Metaprima! c(o.o)ↄ꠹")
    print("===========================================================================")
    print()
    print("Metaprima is a hobby project directly based on Metazooa, a popular website ")
    print("game by Trainwreck Labs. This game is a more simplistic version of Metazooa")
    print("that focuses only on primate species and has no GUI (because I'm not that  ")
    print("advanced yet, LOL.) Type one of the letters below and enter it to continue.")
    print()
    print("===========================================================================")
    print()
    print(">> a ------------------------------------------------------- start the game")
    print(">> h ---------------------------------------------------- game instructions")
    print(">> x ----------------------------------------------------- exit the program")
    print()
        
def instructions():
    print("===========================================================================")
    print("Below is an overview on how to play the game Metaprima.")
    print("===========================================================================")
    print()
    print("When you start a game, the program randomly selects one of roughly 500")
    print("primate species. The name of this species is not revealed to you. As the")
    print("player, it is your objective to guess the exact species secretly selected")
    print("by the game engine in the background. You play each turn by typing in the")
    print("name -- common or scientific -- of your guess, and clicking 'enter'. Each")
    print("time you get it wrong, the game will notify you, and you get another turn.")
    print("You recieve 20 total guesses per game. If you don't guess the mystery")
    print("species by your 20th guess, you lose! If you can guess it in 20 or under")
    print("turns, you win! 1 win = 1 point -- these are just for bragging rights.")
    print()
    print("Sound hard? Don't worry -- the game gives you hints! It's very unlikely")
    print("that you get the correct species on the first guess. But, at the end of")
    print("the day, all animals are genetically related, and they all share last")
    print("common ancestors. This game is organized around primate phylogeny -- as")
    print("such, with every wrong guess, the game informs you how closely your guess")
    print("is taxonomically related to the mystery animal. For example, if the mystery")
    print("primate is a Human (H. sapiens), and you enter the guess Sumatran Orangutan")
    print("(P. abelii), you will receive the following message:")
    print()
    print(">> Incorrect. You have guessed down to the mystery family, Hominidae.")
    print()
    print("Hominidae is the closest shared taxonomic ranking between humans and")
    print("Sumatran orangutans. This notification helps you narrow down your choices,")
    print("as you now know that the mystery species must belong to the family")
    print("Hominidae, but cannot be an orangutan.")
    print("Note: At any time, you can choose to get a hint, which automatically moves")
    print("you down 1 rank towards the mystery species in the taxonomic tree. One hint")
    print("costs 3 turns. You can use up to 3 hints per game. Additionally, you can")
    print("choose to give up and have the game display the answer if you so wish.")
    print()
    print("Finally, here are a series of specific keybinds necessary to play the game.")
    print("These can be entered into the terminal at any time while playing Metaprima.")
    print()
    keybinds()
    print()
    print("===========================================================================")
    print()
    print(">> a ------------------------------------------------------- start the game")
    print(">> m ------------------------------------------------------- return to menu")
    print(">> x ----------------------------------------------------- exit the program")
    print()
    action = input(">> ").strip().lower()
    if action != "a" and action != "m" and action != "x":
        print("Invalid operation.")
    else:
        if action == "a":
            game()
        elif action == "m":
            menu()
        else:
            print("Goodbye!")
            exit()

def keybinds():
    print(">> q -------------------------------------------------------- list keybinds")
    print(">> c ------------------------------------------------------- provide a hint")
    print(">> g -------------------------------------------------------------- give up")
    print(">> x ----------------------------------------------------- exit the program")

def main():
    menu()
    while True:
        action = input(">> ").strip().lower()
        if action != "a" and action != "h" and action != "x":
            print("Invalid operation.")
        else:
            if action == "a":
                game()
            elif action == "h":
                instructions()
            else:
                print("Goodbye!")
                break

if __name__ == "__main__":
    main()