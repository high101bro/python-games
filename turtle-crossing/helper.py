from turtle import Turtle
import random
import time
import queue
import os
import copy
import pickle

UP = 90
DOWN = 270
LEFT = 180
RIGHT = 0

ALIGNMENT = 'center'
FONT = 'Arial'
SIZE = 18
TYPE = 'normal'


class Game(Turtle):
    def __init__(self):
        super().__init__()
        self.pet_list = []
        self.vehicles_driving_left_queue = queue.Queue()
        self.vehicles_driving_left_list = []
        self.vehicles_driving_right_queue = queue.Queue()
        self.vehicles_driving_right_list = []
        self.turtle_splats = 0
        self.food_queue = queue.Queue()
        self.food_list = []
        self.candy_queue = queue.Queue()
        self.candy_list = []
        self.poop_list = []


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.color("black")
        self.hideturtle()
        self.penup()
        self.goto(0, -350)
        self.score = 0
        
        if os.path.exists("high_score.pkl"):
            print('file exists')
            with open("high_score.pkl", "rb") as file:
                self.high_score = pickle.load(file)
        else:
            self.high_score = 0
            
        if os.path.exists("turtle_squishes.pkl"):
            print('file exists')
            with open("turtle_squishes.pkl", "rb") as file:
                self.turtle_squishes = pickle.load(file)
        else:
            self.turtle_squishes = 0
        self.update_score()

    def increase_score(self):
        self.score += 1
        self.update_score()

    def decrease_score(self):
        self.score -= 1
        self.update_score()

    def update_score(self):
        self.clear()
        if self.score > self.high_score:
            self.high_score = self.score
            with open("high_score.pkl", "wb") as file:
                pickle.dump(self.high_score, file)
        self.write(f"Score: {self.score}     High Score: {self.high_score}     Squishes: {self.turtle_squishes}", align=ALIGNMENT, font=(FONT, SIZE, TYPE))

    def game_over(self):
        self.goto(0, 0)
        self.write(f"Game Over!", align=ALIGNMENT, font=(FONT, SIZE, TYPE))


class Vehicle(Turtle):

    def __init__(self):
        super().__init__()
        self.stamp()
        self.count = 0

    def spawn(self, file, xcor, ycor, direction):
        super().__init__()
        self.color('black')
        self.shape(file)
        # self.shapesize(stretch_wid=0.01, stretch_len=0.01)
        self.penup()
        self.hideturtle()
        self.goto(xcor, ycor)
        self.direction = direction
        self.moving = False

    def reset(self, direction, screen_width):
        if self.direction == 'left':
            xcor = ((screen_width + 300) / 2)
            ycor = 35
        elif self.direction == 'right':
            xcor = -((screen_width + 300) / 2)
            ycor = -26
        self.goto(xcor, ycor)
        self.showturtle()
        self.moving = False

    def drive(self):
        self.speed(1)
        if self.direction == 'left':
            xcor = self.xcor() - 3
            self.goto(xcor, self.ycor())
        elif self.direction == 'right':
            xcor = self.xcor() + 3
        self.goto(xcor, self.ycor())


class Splat(Turtle):
    def __init__(self, pet, file, direction):
        super().__init__()
        self.penup()
        self.shape(file)
        ran_splat = random.randint(-3,3)
        if direction == 'right':
            self.goto(pet.xcor() + 45 + ran_splat, pet.ycor() - 3 + ran_splat)
        elif direction == 'left':
            self.goto(pet.xcor() - 45 + ran_splat, pet.ycor() - 3 + ran_splat)


class Pet(Turtle):
    def __init__(self, color, xcor, ycor, screen_width, screen_height):
        super().__init__()
        self.direction = None
        self.stamp()
        self.color(color)
        self.shape('turtle')
        self.penup()
        self.goto((xcor, ycor))
        self.stomach = 0
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.shapesize(stretch_wid=1, stretch_len=1, outline=0)

    def reset(self, scoreboard):
        self.hideturtle()
        self.goto(-4, 280)
        self.setheading(DOWN)
        self.showturtle()
        with open("turtle_squishes.pkl", "wb") as file:
            pickle.dump(scoreboard.turtle_squishes, file)
            scoreboard.update_score()
        self.shapesize(stretch_wid=1, stretch_len=1, outline=0)

    def move_up(self):
        if self.ycor() + 20 > ((self.screen_height / 2) - 20):
            self.setheading(DOWN)
            self.forward(20)
        else:
            self.setheading(UP)
            self.forward(20)

    def move_down(self):
        if self.ycor() - 20 < ((self.screen_height / 2) - 20) * -1:
            self.setheading(UP)
            self.forward(20)
        else:
            self.setheading(DOWN)
            self.forward(20)

    def move_left(self):
        if self.xcor() - 20 < ((self.screen_width / 2) - 20) * -1:
            self.setheading(RIGHT)
            self.forward(20)
        else:
            self.setheading(LEFT)
            self.forward(20)

    def move_right(self):
        if self.xcor() + 20 > ((self.screen_width / 2) - 20):
            self.setheading(LEFT)
            self.forward(20)
        else:
            self.setheading(RIGHT)
            self.forward(20)

    def move_towards_closest_candy(self, game):
        closest_candy = None
        min_distance = float('inf')

        # Find the closest candy
        for candy in game.candy_list:
            distance = self.distance(candy)
            if distance < min_distance:
                min_distance = distance
                closest_candy = candy

        # Determine direction towards the closest candy
        if closest_candy is not None:
            angle_to_candy = self.towards(closest_candy)
            direction = self.get_closest_cardinal_direction(angle_to_candy)
            self.setheading(direction)
            self.forward(20)  # Adjust the distance moved per step as needed

    def get_closest_cardinal_direction(self, angle):
        # Define cardinal directions
        up, right, down, left = 90, 0, 270, 180

        # Calculate the difference between the angle and each cardinal direction
        diff_up = abs(angle - up)
        diff_right = abs(angle - right)
        diff_down = abs(angle - down)
        diff_left = abs(angle - left)

        # Find the closest cardinal direction
        closest_direction = min([diff_up, diff_right, diff_down, diff_left], key=abs)

        # Return the corresponding cardinal direction
        if closest_direction == diff_up:
            return up
        elif closest_direction == diff_right:
            return right
        elif closest_direction == diff_down:
            return down
        elif closest_direction == diff_left:
            return left

    def move_randomly(self, screen_width, screen_height):
        directions = {
            'up': 90,
            'down': 270,
            'left': 180,
            'right': 0,
        }
        chance_of_moving = random.randint(1,100)
        if chance_of_moving > 99:
            direction = random.choice(['up', 'down', 'left', 'right', 'forward', 'forward', 'forward', 'forward', 'forward', 'forward'])
            if direction == 'forward':
                pass
            else:
                self.setheading(directions[direction])
            if   self.xcor() + 20 > ((screen_width/2) - 20):
                self.setheading(directions['left'])
                self.forward(20)
            elif self.xcor() - 20 < ((screen_width / 2) - 20) * -1:
                self.setheading(directions['right'])
                self.forward(20)
            elif self.ycor() + 20 > ((screen_height / 2) - 20):
                self.setheading(directions['down'])
                self.forward(20)
            elif self.ycor() - 20 < ((screen_height / 2) - 20) * -1:
                self.setheading(directions['up'])
                self.forward(20)
            else:
                # screen_height
                self.forward(20)



    def eat_food(self, game, scoreboard):
        for index, food in enumerate(game.food_list):
            if self.distance(food) < 15:
                print('That food was yummy!')
                food.hideturtle()
                # food.clear()
                game.food_list.remove(food)
                self.stomach += 1
                scoreboard.increase_score()

    def eat_candy(self, game, scoreboard):
        for candy in list(game.candy_list):
            if self.distance(candy) < 15:
                print(f'{self.color()} pet ate candy!')
                candy.hideturtle()
                game.candy_list.remove(candy)
                self.stomach += 1
                current_size = self.shapesize()
                self.shapesize(stretch_wid=current_size[0] + 0.1, stretch_len=current_size[1] + 0.1)
                scoreboard.increase_score()

    def eat_pet(self, pets, scoreboard):
        if self.shapesize()[0] >= 1.1:
            for pet in list(pets):
                if self.distance(pet) < 15:
                    print('Player ate a pet!')
                    pet.reset(scoreboard)
                    scoreboard.decrease_score()
                    current_size = self.shapesize()
                    self.shapesize(stretch_wid=current_size[0] / 1.1, stretch_len=current_size[1] / 1.1)

    def poop(self, game):
        poop_dist = 10
        poop = None
        if self.heading() == UP:
            poop = Poop(xcor=self.xcor(), ycor=self.ycor() - poop_dist)
        elif self.heading() == DOWN:
            poop = Poop(xcor=self.xcor(), ycor=self.ycor() + poop_dist)
        elif self.heading() == LEFT:
            poop = Poop(xcor=self.xcor() + poop_dist, ycor=self.ycor())
        elif self.heading() == RIGHT:
            poop = Poop(xcor=self.xcor() - poop_dist, ycor=self.ycor())
        game.poop_list.append(poop)

    def push_ball(self, ball):
        if self.distance(ball) < 15:
            print('Pushing Ball!')
            angle = self.heading()
            ball.setheading(angle)
            ball.forward(20)



class Ball(Turtle):
    def __init__(self, file, xcor, ycor, screen_width, screen_height):
        super().__init__()
        self.direction = None
        self.stamp()
        self.shape(file)
        self.penup()
        self.goto((xcor, ycor))
        self.screen_width = screen_width
        self.screen_height = screen_height

    def move_up(self):
        if self.ycor() + 20 > ((self.screen_height / 2) - 20):
            self.setheading(DOWN)
            self.forward(20)
        else:
            self.setheading(UP)
            self.forward(20)

    def move_down(self):
        if self.ycor() - 20 < ((self.screen_height / 2) - 20) * -1:
            self.setheading(UP)
            self.forward(20)
        else:
            self.setheading(DOWN)
            self.forward(20)

    def move_left(self):
        if self.xcor() - 20 < ((self.screen_width / 2) - 20) * -1:
            self.setheading(RIGHT)
            self.forward(20)
        else:
            self.setheading(LEFT)
            self.forward(20)

    def move_right(self):
        if self.xcor() + 20 > ((self.screen_width / 2) - 20):
            self.setheading(LEFT)
            self.forward(20)
        else:
            self.setheading(RIGHT)
            self.forward(20)


class Candy(Turtle):
    def __init__(self):
        super().__init__()
        self.stamp()
        self.hideturtle()
        self.color('red')
        self.penup()
        self.shape('circle')
        self.shapesize(0.5)

    def spawn(self, xcor, ycor):
        self.goto(xcor, ycor)
        self.showturtle()


class Food(Turtle):
    def __init__(self):
        super().__init__()
        self.stamp()
        self.count = 0

    def spawn(self, xcor, ycor):
        self.hideturtle()
        self.color('green')
        self.penup()
        self.shape('circle')
        self.shapesize(0.5)
        self.goto((xcor, ycor))
        self.showturtle()


class Poop(Turtle):

    def __init__(self, xcor, ycor):
        super().__init__()
        self.stamp()
        self.hideturtle()
        self.speed(1)
        self.color('brown')
        self.penup()
        self.shape('circle')
        self.shapesize(0.25)
        self.goto((xcor, ycor))
        self.showturtle()
