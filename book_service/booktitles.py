import random

# Lists of words to create book titles
adjectives = [
    "Mysterious", "Forgotten", "Enchanted", "Lost", "Dark", "Silent",
    "Hidden", "Secret", "Ancient", "Eternal", "Cursed", "Invisible",
    "Broken", "Whispering", "Glorious", "Fading", "Rising", "Fallen",
    "Infinite", "Wandering"
]

nouns = [
    "Forest", "Kingdom", "City", "Dream", "Night", "Star", "River",
    "Mountain", "Castle", "Ocean", "Valley", "Garden", "Labyrinth",
    "Empire", "Chronicle", "Journey", "Saga", "Legacy", "Odyssey",
    "Quest"
]

themes = [
    "of Shadows", "of Time", "of Destiny", "of Hope", "of Fire",
    "of Ice", "of Light", "of Darkness", "of Dreams", "of Secrets",
    "of Legends", "of the Past", "of the Future", "of Magic",
    "of the Lost", "of the Brave", "of the Fallen", "of the Stars",
    "of the Abyss", "of the Unknown"
]

def generate_random_title():
    # Randomly select words from the lists
    adjective = random.choice(adjectives)
    noun = random.choice(nouns)
    theme = random.choice(themes)
    # Construct the title
    title = f"The {adjective} {noun} {theme}"
    return title