from ursina import *
import time
import random

game = Ursina()

# Player
texture_path = 'textures/basket.jpg'  
player = Entity(model='sphere', texture=texture_path, position=(0, 3, -2000), scale=(5, 5, 5), collider='box')
camera.z = -15
camera.add_script(SmoothFollow(target=player, offset=(0, 5, -30)))

#Jalanan
road = Entity(model='plane', scale=(50, 10, 1000000), color=color.gray)
median_r = Entity(model='cube', collider='box', position=(25, 2, 0), scale=(5, 10, 1000000), color=color.orange)
median_l = Entity(model='cube', collider='box', position=(-25, 2, 0), scale=(5, 10, 1000000), color=color.orange)

# Garis putih di jalan raya
stripe_length = 50
stripe_width = 1
for i in range(-2000, 1000000, 100):
    stripe = Entity(model='cube', position=(0, 0.1, i), scale=(stripe_width, 0.1, stripe_length), color=color.white)

# Rows and score
rows = [-15, -10, -5, 0, 5, 10, 15]
score_label = Text(text="Score:", scale=3, x=-0.85, y=0.45, color=color.black)
score_board = Text(text=str(0), scale=3, x=-0.63, y=0.45, color=color.black)
speed = 80
is_paused = False
initial_z_position = player.z
score = 0
game_over = False 

#fungsi pause
pause_indicator = Text(text='PAUSE', scale=6, color=color.yellow, origin=(0.7, 0), x=0.3, y=-0.0)
pause_indicator.enabled = False

#BAMBANG
game_over_panel = Panel(model='quad', scale=(0.5, 0.3), color=color.white33, enabled=False)
game_over_text = Text(parent=game_over_panel, text='GAME OVER', scale=5, color=color.red, origin=(0.0, 0.5), y=0.2)
restart_button = Button(parent=game_over_panel, text='Restart', color=color.green, scale=0.4, origin=(-0.6, 0.0), y=-0.3)
quit_button = Button(parent=game_over_panel, text='Exit', color=color.red, scale=0.4, origin=(0.6, 0.0), y=-0.3)
game_over_panel.enabled = False

# Functions
def update():
    if not is_paused and not game_over:  
        player_movement()
        update_score()
        check_collision()

def player_movement():
    if game_over:  
        return

    player.z += lerp(time.dt * speed, 0, 0.1)  
    player.rotation_x += time.dt * 50

    if held_keys['d']:
        player.x += lerp(time.dt * 30, 0, 0.1)
        player.rotation_z += time.dt * 100
    if held_keys['a']:
        player.x -= lerp(time.dt * 30, 0, 0.1)
        player.rotation_z -= time.dt * 100
    if held_keys['w']:
        player.z += lerp(time.dt * 350, 0, 0.1)
        player.rotation_x += time.dt * 600

def update_score():
    global score
    
    scale_factor = 0.1
    score_val = (player.z - initial_z_position) * scale_factor
    score = int(score_val)
    score_board.text = str(score)

#HAFIZI
def check_collision():
    if player.intersects().hit or median_r.intersects().hit or median_l.intersects().hit:
        show_game_over_dialog()

def show_game_over_dialog():
    global game_over
    game_over_panel.enabled = True
    game_over = True  

def restart_game():
    global is_paused, initial_z_position, score, game_over
    player.position = (0, 3, -2000)
    player.rotation = (0, 0, 0)
    initial_z_position = player.z
    score = 0
    is_paused = False
    game_over = False  
    game_over_panel.enabled = False

def exit_game():
    application.quit()

#ALDI
def toggle_pause():
    global is_paused
    is_paused = not is_paused

    pause_indicator.enabled = is_paused

    if is_paused:
        time.dt = 0
    else:
        time.dt = 1 / 60  

def input(key):
    if key == 'escape':
        application.quit()
    elif key == 'space':
        toggle_pause()
        
restart_button.on_click = restart_game
quit_button.on_click = exit_game

for i in range(0, 10000, 100):
    enemy = Entity(model='cube', collider='box', position=(random.choice(rows), 6, i), color=color.random_color())
    enemy.scale = (10, 10, 10)

# jalanin game
window.fullscreen = 1
sky = Sky()
game.run()
