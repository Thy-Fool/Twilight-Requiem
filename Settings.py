# Screen size
width = 896
height = 640
# Frames per second
fps = 60
# General size of obstacles
obstacles_size = 64

# Weapons
Weapon_choice = {'Sword': {'cooldown': 434, 'melee_time': 0.15, 'damage': 10, 'Knockback': 6},
                 'Axe': {'cooldown': 800, 'melee_time': 0.15, 'damage': 25, 'Knockback': 5},
                 'Spear': {'cooldown': 560, 'melee_time': 0.15, 'damage': 8, 'Knockback': 4}}

# Magic
Magic_choice = {'Heal': {'Mana_usage': 35, 'Effect': 40},
                'Fire': {'Mana_usage': 20, 'Effect': 45},
                'Lightning': {'Mana_usage': 25, 'Effect': 40}}

# Beast data
Beast_data = {
    'Bane_of_destiny': {'Health': 100, 'Attack': 6, 'Speed': 4, 'Exp_drop': 25, 'knock_resistance': 3, 'Range': 300,
                        'Notice_range': 500, 'Cooldown': 400, 'Separation': 10},
    'Worm_of_spirit': {'Health': 50, 'Attack': 17, 'Speed': 3, 'Exp_drop': 30, 'knock_resistance': 2, 'Range': 250,
                       'Notice_range': 430, 'Cooldown': 550, 'Separation': 10},
    'Dark_Knight': {'Health': 110, 'Attack': 16, 'Speed': 4, 'Exp_drop': 35, 'knock_resistance': 3, 'Range': 200,
                    'Notice_range': 520, 'Cooldown': 600, 'Separation': 100}}

# Health info
Healthbar_length = 200
Healthbar_width = 15

# Mana info
Manabar_length = 150
Manabar_width = 10

# Color
Health_color1 = 'red'
Health_color2 = (255, 173, 51)
Mana_color = (33, 107, 255)
bar_color = (61, 62, 63)

# Font
Main_font = 'Game_font.ttf'
text_color = (255, 255, 255)
