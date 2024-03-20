import math
import random
import tkinter as tk

# Initialize Tkinter
root = tk.Tk()
root.title("Space Invader")
canvas = tk.Canvas(root, width=800, height=600)
canvas.pack()

# Background
background_image = tk.PhotoImage(file = 'background.png')
canvas.create_image(0, 0, anchor=tk.NW, image=background_image)

# Player
player_image = tk.PhotoImage(file = 'player.png')
player_id = canvas.create_image(370, 480, anchor=tk.NW, image=player_image)
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemy_images = []
enemy_ids = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_image = tk.PhotoImage(file = 'enemy.png')
    enemy_images.append(enemy_image)
    enemy_id = canvas.create_image(random.randint(0, 736), random.randint(50, 150), anchor=tk.NW, image=enemy_image)
    enemy_ids.append(enemy_id)
    enemyX.append(canvas.coords(enemy_id)[0])
    enemyY.append(canvas.coords(enemy_id)[1])
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet
bullet_image = tk.PhotoImage(file = 'bullet.png')
bullet_id = None
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score
score_value = 0
font = ("Arial", 32, "bold")
score_id = canvas.create_text(10, 10, anchor=tk.NW, text="Score : " + str(score_value), fill="white", font=font)

# High Score
high_score_file = "high_score.txt"

def read_high_score():
    try:
        with open(high_score_file, "r") as file:
            return int(file.read().strip())
    except FileNotFoundError:
        return 0

def write_high_score(score):
    with open(high_score_file, "w") as file:
        file.write(str(score))

high_score = read_high_score()

def show_score():
    canvas.itemconfig(score_id, text="Score : " + str(score_value))

# Game Over
over_font = ("Arial", 64, "bold")

def game_over_text():
    global high_score
    canvas.create_text(200, 250, text="GAME OVER", fill="white", font=over_font)
    if score_value > high_score:
        high_score = score_value
        write_high_score(high_score)
        canvas.create_text(200, 350, text="New High Score: " + str(high_score), fill="white", font=over_font)

def player_motion(event):
    global playerX, playerX_change
    if event.keysym == 'Left':
        playerX_change = -5
    elif event.keysym == 'Right':
        playerX_change = 5
    elif event.keysym == 'space':
        fire_bullet(playerX)

def player_stop_motion(event):
    global playerX_change
    if event.keysym in ['Left', 'Right']:
        playerX_change = 0

def fire_bullet(x):
    global bullet_id, bulletX, bulletY, bullet_state
    if bullet_state == "ready":
        bullet_id = canvas.create_image(x + 16, 480 + 10, anchor=tk.NW, image=bullet_image)
        bulletX = x
        bulletY = 480
        bullet_state = "fire"

def isCollision(enemyX, enemyY, bulletX, bulletY):
    enemy_left = enemyX
    enemy_right = enemyX + 64  # Assuming enemy width is 64
    enemy_top = enemyY
    enemy_bottom = enemyY + 64  # Assuming enemy height is 64

    bullet_left = bulletX
    bullet_right = bulletX + 16  # Assuming bullet width is 16
    bullet_top = bulletY
    bullet_bottom = bulletY + 16  # Assuming bullet height is 16

    if (bullet_right >= enemy_left and bullet_left <= enemy_right) and \
       (bullet_bottom >= enemy_top and bullet_top <= enemy_bottom):
        return True
    return False

# Initial speeds
bullet_speed = 10
enemy_speed = 4

def bullet_motion():
    global bulletY, bullet_state, score_value
    if bullet_state == "fire":
        bulletY -= bullet_speed
        canvas.move(bullet_id, 0, -bullet_speed)
        if bulletY <= 0:
            canvas.delete(bullet_id)
            bullet_state = "ready"
        else:
            for i in range(num_of_enemies):
                if isCollision(enemyX[i], enemyY[i], bulletX, bulletY):
                    canvas.delete(bullet_id)
                    bullet_state = "ready"
                    # Update score when collision happens
                    score_value += 1
                    show_score()
                    # Move enemy to a new random position
                    enemyX[i] = random.randint(0, 736)
                    enemyY[i] = random.randint(50, 150)
                    canvas.coords(enemy_ids[i], enemyX[i], enemyY[i])



def enemy_motion():
    global enemyX, enemyY, enemy_ids, enemy_speed
    for i in range(num_of_enemies):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = enemy_speed
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -enemy_speed
            enemyY[i] += enemyY_change[i]
        canvas.move(enemy_ids[i], enemyX_change[i], 0)  # Update enemy position on the canvas

def increase_speed():
    global bullet_speed, enemy_speed
    # Increase speeds based on score
    bullet_speed = 10 + score_value * 0.1
    enemy_speed = 4 + score_value * 0.05

def game_loop():
    global playerX, playerX_change
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    canvas.move(player_id, playerX - canvas.coords(player_id)[0], 0)
    bullet_motion()
    enemy_motion()
    increase_speed()  # Call to adjust speeds
    root.after(50, game_loop)

def restart_game(event):
    global score_value, playerX, playerY, playerX_change
    score_value = 0
    show_score()
    for i in range(num_of_enemies):
        canvas.delete(enemy_ids[i])
        enemy_ids[i] = canvas.create_image(random.randint(0, 736), random.randint(50, 150),
                                           anchor=tk.NW, image=enemy_images[i])
    playerX = 370
    playerY = 480
    playerX_change = 0
    canvas.coords(player_id, playerX, playerY)
    canvas.bind("<KeyPress>", player_motion)
    canvas.bind("<KeyRelease>", player_stop_motion)

root.bind("<KeyPress>", player_motion)
root.bind("<KeyRelease>", player_stop_motion)
root.bind("<r>", restart_game)

game_loop()

root.mainloop()


