import json
import os

MEMORY_FILE = "memory.json"


# LOAD MEMORY
def load_memory():

    if os.path.exists(MEMORY_FILE):

        with open(MEMORY_FILE, "r") as f:

            return json.load(f)

    return {}


# SAVE MEMORY
def save_memory(memory):

    with open(MEMORY_FILE, "w") as f:

        json.dump(memory, f, indent=4)


# ADD MEMORY
def remember(key, value):

    memory = load_memory()

    memory[key] = value

    save_memory(memory)


# GET MEMORY
def recall(key):

    memory = load_memory()

    return memory.get(key)