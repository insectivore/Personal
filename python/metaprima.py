import json
import random
import re
import sys

# Taxonomic ranks ordered from narrowest (species level) to broadest
TAXONOMIC_RANKS = ["genus", "subtribe", "tribe", "subfamily", "family", "superfamily", "parvorder", "infraorder", "suborder"]

# Hierarchy ordered from broadest to narrowest for Progressive Hints
HINT_RANK_ORDER = ["suborder", "infraorder", "parvorder", "superfamily", "family", "subfamily", "tribe", "subtribe", "genus"]

def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return ' '.join(text.split())

class PrimateGameEngine:
    def __init__(self, json_filepath: str):
        with open(json_filepath, 'r', encoding='utf-8') as file:
            self.species_list = json.load(file)
        
        self.lookup = {}
        for animal in self.species_list:
            # Handles key names from both 'scientific'/'common' and 'scientific_name'/'common_name'
            sci = animal.get('scientific') or animal.get('scientific_name') or ""
            com = animal.get('common') or animal.get('common_name') or ""
            aliases = animal.get('aliases', [])
            
            names = [sci, com] + aliases
            for name in names:
                if name:
                    key = normalize(name)
                    if key:
                        self.lookup[key] = animal

    def get_random_animal(self) -> dict:
        """Selects a target primate for the round."""
        return random.choice(self.species_list)

    def evaluate_guess(self, target_animal: dict, guess_str: str) -> dict:
        """Evaluates user guess against the target animal."""
        guessed_animal = self.lookup.get(normalize(guess_str))
        
        if not guessed_animal:
            return {"status": "INVALID", "message": "Animal not recognized in database."}

        if guessed_animal['id'] == target_animal['id']:
            return {"status": "CORRECT", "guessed_animal": guessed_animal}

        # Compare taxonomy ranks from narrowest to broadest
        target_tax = target_animal.get("taxonomy", {})
        guess_tax = guessed_animal.get("taxonomy", {})

        shared_rank = None
        shared_group_name = None

        for rank in TAXONOMIC_RANKS:
            t_val = target_tax.get(rank)
            g_val = guess_tax.get(rank)
            if t_val and g_val and t_val == g_val:
                shared_rank = rank
                shared_group_name = t_val
                break  # Stop at narrowest match

        return {
            "status": "INCORRECT",
            "guessed_animal": guessed_animal,
            "shared_rank": shared_rank,
            "shared_group": shared_group_name
        }

def get_name(animal: dict) -> str:
    """Helper to format species display names."""
    com = animal.get('common') or animal.get('common_name', 'Unknown Common Name')
    sci = animal.get('scientific') or animal.get('scientific_name', 'Unknown Scientific Name')
    return f"{com} ({sci})"

def keybinds():
    print(">> q -------------------------------------------------------- list keybinds")
    print(">> c ------------------------------------------------------- provide a hint")
    print(">> g -------------------------------------------------------------- give up")
    print(">> x ----------------------------------------------------- exit the program")

def game(engine: PrimateGameEngine):
    target = engine.get_random_animal()
    moves = 20
    hints = 3
    hint_rank_idx = 0  # Tracks progress through HINT_RANK_ORDER

    print("\n===========================================================================")
    print("Thus begins a game of Metaprima.")
    print("A mystery primate has been selected! Type a common or scientific name to guess.")
    print("Type 'q' to view keybinds.")
    print("===========================================================================\n")

    while moves > 0:
        user_input = input(f"[{moves} turns left] >> ").strip()
        if not user_input:
            continue

        cmd = user_input.lower()

        if cmd == "q":
            keybinds()
            continue
        elif cmd == "c":
            if hints <= 0:
                print(">> You are out of hints for this game!")
            elif moves <= 3:
                print(">> You don't have enough turns remaining to buy a hint.")
            else:
                target_tax = target.get("taxonomy", {})
                hint_found = False
                
                # Find the next populated rank from broad to narrow
                while hint_rank_idx < len(HINT_RANK_ORDER):
                    rank = HINT_RANK_ORDER[hint_rank_idx]
                    val = target_tax.get(rank)
                    hint_rank_idx += 1
                    if val:
                        hints -= 1
                        moves -= 3
                        print(f">> [HINT] The mystery primate belongs to the {rank.capitalize()}: {val} (-3 turns, {hints} hints left)")
                        hint_found = True
                        break
                if not hint_found:
                    print(">> No further taxonomic hints available for this species!")
        elif cmd == "g":
            print(f"\n>> You gave up! The mystery primate was: {get_name(target)}\n")
            break
        elif cmd == "x":
            print("Goodbye!")
            sys.exit()
        else:
            result = engine.evaluate_guess(target, user_input)

            if result["status"] == "INVALID":
                print(">> Animal not recognized in the database. Check spelling -- no turns spent.")
            elif result["status"] == "CORRECT":
                turns_taken = 20 - moves + 1
                print("\n===========================================================================")
                print(f"CORRECT! You identified the mystery primate in {turns_taken} turn(s)!")
                print(f"Species: {get_name(target)}")
                print("===========================================================================")
                break
            elif result["status"] == "INCORRECT":
                moves -= 1
                guessed_name = get_name(result["guessed_animal"])
                if result["shared_rank"]:
                    rank_str = result["shared_rank"].capitalize()
                    group_str = result["shared_group"]
                    print(f">> Incorrect. You have guessed down to the mystery {rank_str}: {group_str}.")
                else:
                    print(f">> Incorrect. They share no standard taxonomic subgroup with the target.")
                if moves == 0:
                    print("\n===========================================================================")
                    print(f"GAME OVER! Out of turns. The mystery primate was: {get_name(target)}")
                    print("===========================================================================")

def menu(engine: PrimateGameEngine):
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

    action = input(">> ").strip().lower()
    if action == "a":
        game(engine)
    elif action == "h":
        instructions(engine)
    elif action == "x":
        print("Goodbye!")
        sys.exit()
    else:
        print("\nInvalid operation.\n")
        
def instructions(engine: PrimateGameEngine):
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

    while True:
        action = input(">> ").strip().lower()
        if action == "a":
            game(engine)
            break
        elif action == "m":
            break
        elif action == "x":
            print("Goodbye!")
            sys.exit()
        else:
            print("Invalid operation.")

def main():
    # Initialize the engine once with JSON data file
    try:
        engine = PrimateGameEngine('primates.json')
    except FileNotFoundError:
        print("Error: 'primates.json' not found in the working directory.")
        sys.exit(1)

    menu(engine)

if __name__ == "__main__":
    main()