from ursina import *
import random

def update():
    global offset, collision, score
    offset += time.dt * .3
    setattr(track, "texture_offset", (0, offset))

    if not collision:  # Only update the car's position if no collision has occurred
        car0.x += held_keys['d'] * time.dt * .2
        car0.x -= held_keys['a'] * time.dt * .2

        # Road boundary adjustment
        if car0.x >= .37:  # Right boundary
            car0.x = .37
        if car0.x <= -.33:  # Left boundary
            car0.x = -.33

        for car in cars:
            if car.rotation_y == 0:  # Move car1 and car2
                new_z = car.z - time.dt * random.uniform(.1, .15)  # Increased speed
            else:  # Move car3 and car4
                new_z = car.z - time.dt * random.uniform(.2, .25)  # Increased speed

            # Check for collisions with other NPC cars
            too_close = False
            for other_car in cars:
                if other_car != car and abs(car.x - other_car.x) < .1 and abs(new_z - other_car.z) < .1:
                    too_close = True
                    break

            if too_close:
                car.x += random.choice([-0.01, 0.01])
            else:
                if car.z > car0.z and new_z <= car0.z:
                    score += 1
                    score_text.text = f"Score: {score}"  # Update score display
                car.z = new_z

            if car.z < -0.5:
                car.z = .4
                car.x = random.uniform(-.3, .3)

            if abs(car0.x - car.x) < .05 and abs(car0.z - car.z) < .05:
                collision = True
                game_over_text.enabled = True
                restart_text.enabled = True

class Car(Entity):
    scale_y = .0001
    scale_z = .06
    def __init__(self, img, scale_x, position, angle):
        super().__init__()
        self.parent = track
        self.model = "cube"
        self.texture = img
        self.scale = (scale_x, self.scale_y, self.scale_z)
        self.position = position
        self.collider = "box"
        self.rotation_y = angle

def restart_game():
    global collision, score, offset
    collision = False
    score = 0
    offset = 0
    game_over_text.enabled = False
    restart_text.enabled = False
    score_text.text = f"Score: {score}"

    car0.position = initial_car0_position
    for car in cars:
        car.z = random.uniform(0, .4)
        car.x = random.uniform(-.3, .3)

app = Ursina()
window.color = color.white
offset = 0
collision = False
score = 0

initial_car0_position = (.05, 1, -.12)

cars_img = ["assets/car0.png", "assets/car1.png", "assets/car2.png", "assets/car3.png", "assets/car4.png"]
track = Entity(model='cube', color=color.white, scale=(10, .5, 60), position=(0, 0), texture="assets/track.png")

car0 = Car(cars_img[0], 0.15, initial_car0_position, 0)
car0.scale *= 2

cars = []
for i in range(5):
    scale_x = random.uniform(0.07, 0.1)
    position = (random.uniform(-.3, .3), 1, random.uniform(0, .4))
    car = Car(cars_img[i % len(cars_img)], scale_x, position, 0)
    car.scale *= 3
    cars.append(car)

game_over_text = Text(
    text="GAME OVER",
    origin=(0, 0),
    scale=2.0,
    color=color.red,
    background=True,
    position=(0, 0.2)
)
game_over_text.enabled = False

score_text = Text(
    text=f"Score: {score}",
    position=(-0.5, 0.4),  # Adjusted for visibility
    scale=0.5,  # Larger size for visibility
    color=color.black,
    background=True
)

restart_text = Text(
    text="Press R to Restart",
    origin=(0, -0.2),
    scale=0.2,
    color=color.black,
    position=(0, -0.3)
)
restart_text.enabled = False

camera.position = (0, 8, -26)
camera.rotation_x = 20

def input(key):
    if key == 'r' and collision:
        restart_game()

app.run()
