import random
from collections import Counter

players_inventory ={
    'weapons':[],
    'armor':[],
    'potions':[],
}

def add_item_to_inventory(category, name, effect_value, quantity):
    if category in players_inventory:
        item = {'name': name, 'value': effect_value, 'quantity': quantity}
        for existing_item in players_inventory[category]:
            if existing_item['name'] == name:
                existing_item['quantity'] += quantity
                return
        players_inventory[category].append(item)
    else:
        print(f"Invalid item category: {category}")

def remove_item_from_inventory(category, name):
    if category in players_inventory:
        players_inventory[category] = [item for item in players_inventory[category] if item['name'] != name]
    else:
        print(f"Invalid item category: {category}")

def display_inventory():
    print("\n--- Inventory ---")
    for category, items in players_inventory.items():
        print(f"\n{category}:")
        if items:
            for item in items:
                print(f"  {item['name']} (Value: {item['value']}, Quantity: {item['quantity']})")
        else:
            print("  None")

def track_item(category, name):
    if category in players_inventory:
        for item in players_inventory[category]:
            if item['name'] == name:
                return item
    return None







def generate_enemies():
    enemy_names = ["Goblin", "Orc", "Troll", "Dragon", "Vampire"]
    enemies = []
    
    for _ in range(3):
        name = random.choice(enemy_names)
        strength = random.randint(5, 15)  
        health = random.randint(20, 60)    
        enemies.append({'name': name, 'strength': strength, 'health': health})
    
    return enemies

def display_enemies(enemies):
    print("\n--- Enemies ---")
    for enemy in enemies:
        print(f"{enemy['name']} - Strength: {enemy['strength']}, Health: {enemy['health']}")



player_health = 100
defeated_count = 0
total_damage_dealt = 0
weapon_usage = Counter()
unique_enemies = set()


def choose_weapon():
    weapons = players_inventory['weapons']
    if not weapons:
        print("No weapons available! You fight barehanded with 1 damage.")
        return {'name': 'Fist', 'value': 1}
    print("\nChoose a weapon:")
    for idx, w in enumerate(weapons, 1):
        print(f"{idx}. {w['name']} (Damage: {w['value']}, Quantity: {w['quantity']})")
    choice = int(input("Enter choice: ")) - 1
    weapon = weapons[choice]
    weapon_usage[weapon['name']] += 1
    return weapon

def use_potion():
    potions = players_inventory['potions']
    if potions:
        potion = potions[0]  
        global player_health
        player_health = min(100, player_health + potion['value'])
        potion['quantity'] -= 1
        if potion['quantity'] == 0:
            remove_item_from_inventory('potions', potion['name'])
        print(f"Healed with {potion['name']}! New health: {player_health}")


def battle(enemy, weapon):
    global player_health, defeated_count, total_damage_dealt
    print(f"\n\nBattle starts with {enemy['name']}!")
    for round_num in range(1, 4):
        if player_health <= 0:
            print("You were defeated!")
            return

        print(f"\n-- Round {round_num} --")
        damage = weapon['value']
        enemy['health'] -= damage
        total_damage_dealt += damage
        print(f"You attacked {enemy['name']} for {damage} damage.")

        if enemy['health'] <= 0:
            print(f"{enemy['name']} defeated!")
            defeated_count += 1
            unique_enemies.add(enemy['name'])
            return

        enemy_attack = random.randint(1, enemy['strength'])
        player_health -= enemy_attack
        print(f"{enemy['name']} attacked you for {enemy_attack} damage. \nYour health: {player_health}")

        if round_num < 3 and player_health > 0:
            use = input("Use potion? (y/n): ").strip().lower()
            if use == 'y':
                use_potion()

def  Post_Battle():
    print("\n--- Post-Battle ---")
    print(f"Total enemies defeated: {defeated_count}")
    print(f"Total damage dealt: {total_damage_dealt}")
    print(f"Current Player health: {player_health}")
    if weapon_usage:
        most_used = weapon_usage.most_common(1)[0][0]
        print(f"Most used weapon: {most_used}")
    for enemy in unique_enemies:
        print(f"Unique enemy faced: {enemy}")
    


def main():
    print("Welcome to Dungeon Quest!")

    add_item_to_inventory('weapons', 'Sword', 10, 1)
    add_item_to_inventory('weapons', 'Axe', 12, 1)
    add_item_to_inventory('armor', 'Shield', 5, 1)
    add_item_to_inventory('potions', 'Healing Potion', 20, 3)

    display_inventory()
    enemies = generate_enemies()
    display_enemies(enemies)

    for enemy in enemies:
        if player_health <= 0:
            break
        weapon = choose_weapon()
        battle(enemy, weapon)

    Post_Battle()

if __name__ == "__main__":
    main()