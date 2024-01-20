import turtle
import random
import math

SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 900
X_MARGIN = 100
Y_MARGIN = 80

SCHOOL_NUMBER = 5
SCHOOL_FISH_MIN = 2
SCHOOL_FISH_MAX = 6
INITIAL_SIZE = 0.25 #1.5
FISH_SPEED = 0.25
EATING_DISTANCE = 20
FISH_MAX_SCALE_SIZE = 10
FISH_SIZE_TO_GIVE_BIRTH = 2
FOOD_EATEN_TO_MAKE_BABY = 2 #20

TURNING_ANGLE_INCREMENT = 1
SPEED_VARIATION = 0.1  # Slight variation in speed for dynamic movement

COLLISION_RADIUS = 30  # Detection radius for avoiding other fish
AVOIDANCE_TURN_INCREMENT = 5  # Gradual turn increment for smoother avoidance

SCHOOL_SEPARATION_DISTANCE = 150  # Desired distance between schools
MAX_STRAY_DISTANCE = 200
PERSONAL_SPACE_MIN = 20  # Minimum personal space
PERSONAL_SPACE_MAX = 100  # Maximum personal space

FOOD_DROPPED = 25
FOOD_ACTIVE_HEIGHT = SCREEN_HEIGHT // 2 - 100  # Food becomes active when it's 100 units down from the top
FOOD_SPEED = 0.35
CHASE_SPEED = FISH_SPEED * 3  # For some reason they slowed down... this addresses that
POOP_SPEED = 0.35
CLEANING_RADIUS = 100  # Define how close a click needs to be to clean the poop
autofeeder_enabled = False

SHARK_EATING_DISTANCE = 20  # Define how close the shark needs to be to eat the fish
SHARK_SPEED_MULTIPLIER = 10
FISH_SIZE_TO_BE_EATEN = 1.9

STOMACH_SIZE = 5
SWIM_POOP_DISTANCE = 1000  #10000  # Distance after which the fish will poop

SPEED_INCREMENT = 0.25  # Adjust the speed increment as needed

attracted_fish = []  # List of fish that are currently attracted to food

poops = []  # Global list to keep track of poop objects


# Define different colors for the schools
school_colors = ["red", "green", "blue", "yellow", "purple", "black", "magenta", "orange", "pink", "yellow"]

# Global variables for school directions and distances
school_directions = [random.randint(0, 360) for _ in range(5)]
school_distances = [random.randint(1000, 2000) for _ in range(5)]

# Declare the global list of fishes
fishes = []

# Setup the screen
screen = turtle.Screen()
screen.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
screen.bgcolor("lightblue")
screen.title("Fish Tank Game")
screen.tracer(0)  # Turn off automatic screen updates

class Fish(turtle.Turtle):
    def __init__(self, center_x, center_y, school_index, predator=False):
        super().__init__()
        self.school_index = school_index
        self.color(school_colors[school_index])  # Assign color based on school index
        self.shape("triangle")
        self.shapesize(INITIAL_SIZE, INITIAL_SIZE)
        self.penup()
        self.hideturtle()

        # Get a random starting position near the central point
        start_x, start_y = get_random_point_near(center_x, center_y, 20, 80)
        self.goto(start_x, start_y)

        self.showturtle()
        self.setheading(school_directions[school_index])
        self.avoidance_turn = 0
        self.personal_space = random.uniform(PERSONAL_SPACE_MIN, PERSONAL_SPACE_MAX)
        self.distance_swam = 0
        self.size_scale = INITIAL_SIZE
        self.birth_count = 0
        self.school_index = school_index

        self.food_eaten = 0
        self.stomach = []
        self.predator = predator  # Set the predator attribute before calling update_stomach_display

        if self.predator:
            self.color("gray")
            self.pencolor("darkgray")
            self.size_scale = 3
            self.new_heading = random.randint(0, 360)
            self.eaten_fish_count = 0
        else:
            self.color(school_colors[school_index])
            self.size_scale = INITIAL_SIZE

        self.shapesize(self.size_scale, self.size_scale)
        self.stomach_display = turtle.Turtle(visible=False)
        self.stomach_display.penup()
        self.stomach_display.hideturtle()

        self.update_stomach_display()  # Now safe to call this method

    def update_stomach_display(self):
        self.stomach_display.clear()  # Clear the previous text
        display_position_y = self.ycor() + 20  # Adjust the Y-offset to display above the fish
        self.stomach_display.goto(self.xcor(), display_position_y)
        self.stomach_display.write(len(self.stomach), align="center", font=("Arial", 8, "normal"))

    def random_movement(self):
        if self.predator:
            # Look for target fish
            target, distance_to_target = self.find_target_fish()

            # Shark Eating
            if target and distance_to_target < EATING_DISTANCE:
                # Eat the target fish
                fishes.remove(target)
                target.remove_fish()
                target.hideturtle()
                self.eaten_fish_count += 1  # Increment the eaten fish count
                self.update_stomach_display()  # Update the display to show the new count
            elif target:
                # Move towards the target fish
                angle_to_target = math.atan2(target.ycor() - self.ycor(), target.xcor() - self.xcor())
                angle_to_target = math.degrees(angle_to_target)
                self.setheading(angle_to_target)
            else:
                # Decrease the frequency of direction changes
                if random.random() < 0.02:  # 5% chance to change direction
                    self.new_heading = random.randint(0, 360)

                if hasattr(self, 'new_heading'):
                    angle_difference = (self.new_heading - self.heading() + 360) % 360
                    if angle_difference > 180:
                        angle_difference -= 360

                    if angle_difference != 0:
                        # Smaller turn angle for smoother turning
                        turn_angle = min(abs(angle_difference), 3)  # Reduce max turn angle
                        turn_angle *= abs(angle_difference) / angle_difference
                        self.setheading(self.heading() + turn_angle)

            # Increase the speed of the shark
            shark_speed = FISH_SPEED * SHARK_SPEED_MULTIPLIER  # Adjust the multiplier as needed

            # Move the shark forward
            self.forward(shark_speed)

            # Keep the shark within screen bounds
            max_x = SCREEN_WIDTH // 2 - X_MARGIN
            max_y = SCREEN_HEIGHT // 2 - Y_MARGIN
            if self.xcor() > max_x or self.xcor() < -max_x or self.ycor() > max_y or self.ycor() < -max_y:
                self.new_heading = math.degrees(math.atan2(-self.ycor(), -self.xcor()))


    def update_stomach_display(self):
        # Clear and update the stomach display with the new count
        self.stomach_display.clear()
        display_position_y = self.ycor() + 20
        self.stomach_display.goto(self.xcor(), display_position_y)
        if self.predator:
            display_text = f"Kills: {self.eaten_fish_count}"
        else:
            display_text = str(len(self.stomach))
        self.stomach_display.write(display_text, align="center", font=("Arial", 8, "normal"))

    def find_target_fish(self):
        if self.predator:
            target_fish = None
            min_distance = float('inf')
            for fish in fishes:
                if fish.size_scale >= FISH_SIZE_TO_BE_EATEN:
                    distance = self.distance(fish)
                    if distance < min_distance:
                        min_distance = distance
                        target_fish = fish
            return target_fish, min_distance

    def check_and_give_birth(self):
        global fishes
        if self.size_scale >= 2 and self.birth_count < 2:  # Check size and birth count
            school_members = [fish for fish in fishes if fish.school_index == self.school_index]
            if len(school_members) >= 2:  # Check if there are at least 2 fishes in the school
                for _ in range(3):  # Create 3 new fishes
                    new_fish = Fish(self.xcor(), self.ycor(), self.school_index)
                    fishes.append(new_fish)
                    new_fish.size_scale = 1  # Set the size of the new fish
                    new_fish.shapesize(stretch_wid=1, stretch_len=1, outline=None)
                self.birth_count += 1  # Increment the birth count
                if self.birth_count == 2:
                    self.outline_color("black")  # Change the border to black on second birth

    def outline_color(self, color):
        self.shapesize(stretch_wid=self.size_scale, stretch_len=self.size_scale, outline=1)
        self.pencolor(color)

    def eat_food(self, closest_food):
        MAX_STOMACH_CONTENT = 5  # Maximum number of food pieces in stomach

        if len(self.stomach) < MAX_STOMACH_CONTENT and closest_food.ycor() < FOOD_ACTIVE_HEIGHT:
            distance_to_food = self.distance(closest_food)
            if distance_to_food < EATING_DISTANCE:
                self.stomach.append(closest_food)  # Add the food to the stomach
                self.food_eaten += 1  # Increment the food eaten counter
                closest_food.hideturtle()  # Hide the food particle
                try:
                    food_particles.remove(closest_food)  # Remove the food from the list
                except ValueError:
                    pass  # Handle the exception if the food is already removed

                # Increase the size of the fish if needed
                self.size_scale += 0.1  # Increment size scale
                self.shapesize(stretch_wid=self.size_scale, stretch_len=self.size_scale, outline=None)

                if self.size_scale > FISH_MAX_SCALE_SIZE:
                    self.size_scale = FISH_MAX_SCALE_SIZE
                    self.shapesize(stretch_wid=FISH_MAX_SCALE_SIZE, stretch_len=FISH_MAX_SCALE_SIZE, outline=None)

        # Update display (if you have the display feature implemented)
        self.update_stomach_display()
        if self in attracted_fish:
            attracted_fish.remove(self)  # Remove from attracted_fish list

    def give_up_chase(self):
        if self in attracted_fish:
            attracted_fish.remove(self)  # Remove from attracted_fish list


    def adjust_movement(self):
        # Collision avoidance and maintaining personal space
        for other_fish in fishes:
            if other_fish != self and self.distance(other_fish) < COLLISION_RADIUS:
                # Calculate angle away from the other fish
                away_angle = math.atan2(self.ycor() - other_fish.ycor(), self.xcor() - other_fish.xcor())
                away_angle = math.degrees(away_angle)
                self.setheading(away_angle)


        # Check if there are other fish to compare distances with
        other_fishes = [fish for fish in fishes if fish != self]
        if other_fishes:
            closest_fish_distance = min(self.distance(fish) for fish in fishes if fish != self)
            if closest_fish_distance < self.personal_space:
                # If too close to another fish, slow down or slightly turn away
                self.setheading(self.heading() + random.uniform(-10, 10))
                self.forward(FISH_SPEED * 0.5)
            elif closest_fish_distance > self.personal_space:
                # If too far from other fish, speed up to catch up
                self.forward(FISH_SPEED * 1.5)
            else:
                # Maintain current speed and direction
                self.forward(FISH_SPEED)
        else:
            closest_fish_distance = None  # Or handle it in another appropriate way


        # Check if the fish has strayed too far from the school center
        school_center_x, school_center_y = calculate_school_center(self.school_index)
        distance_to_center = math.sqrt((self.xcor() - school_center_x) ** 2 + (self.ycor() - school_center_y) ** 2)
        if distance_to_center > MAX_STRAY_DISTANCE:
            # Get a random point near the school center to head towards
            target_x, target_y = get_random_point_near(school_center_x, school_center_y, 20, 100)
            angle_to_target = math.atan2(target_y - self.ycor(), target_x - self.xcor())
            angle_to_target = math.degrees(angle_to_target)
            self.setheading(angle_to_target)
            self.forward(FISH_SPEED * 1.5)  # Move faster towards the target
        else:
            self.forward(FISH_SPEED)  # Continue with normal movement if within range


        # Additional logic for maintaining distance from other schools
        own_school_center_x, own_school_center_y = calculate_school_center(self.school_index)
        for other_school_index in range(len(school_colors)):
            if other_school_index != self.school_index:
                other_school_center_x, other_school_center_y = calculate_school_center(other_school_index)
                distance_to_other_school = math.sqrt((own_school_center_x - other_school_center_x) ** 2 +
                                                     (own_school_center_y - other_school_center_y) ** 2)
                if distance_to_other_school < SCHOOL_SEPARATION_DISTANCE:
                    # Calculate angle away from the other school center
                    away_angle = math.atan2(own_school_center_y - other_school_center_y,
                                            own_school_center_x - other_school_center_x)
                    away_angle = math.degrees(away_angle)
                    self.setheading(away_angle)
                    break  # Once a direction away from a close school is set, no need to check others

        self.forward(FISH_SPEED)

        # Stay away from the sides
        max_x = SCREEN_WIDTH // 2 - X_MARGIN
        max_y = SCREEN_HEIGHT // 2 - Y_MARGIN
        min_x = -max_x
        min_y = -max_y

        if not (min_x < self.xcor() < max_x and min_y < self.ycor() < max_y):
            angle_to_center = math.atan2(-self.ycor(), -self.xcor())
            angle_to_center = math.degrees(angle_to_center)
            self.setheading(angle_to_center)

        self.forward(FISH_SPEED)

    def swim_in_school(self):
        global school_directions, school_distances

        margin = 60  # Margin from the edge of the screen
        max_x = SCREEN_WIDTH // 2 - margin
        max_y = SCREEN_HEIGHT // 2 - margin

        # If the fish is near the edge of the screen, turn it around and move it forward
        if self.xcor() > max_x or self.xcor() < -max_x or self.ycor() > max_y or self.ycor() < -max_y:
            self.setheading(self.heading() + 180)  # Turn around by 180 degrees
            self.forward(10)  # Move forward by 100 units

        # Initialize new_direction with the current direction
        new_direction = self.heading()

        # Check and turn around if at the edge
        current_direction = self.heading()
        target_direction = school_directions[self.school_index]
        if self.xcor() > max_x or self.xcor() < -max_x:
            target_direction = 180 - target_direction
        if self.ycor() > max_y or self.ycor() < -max_y:
            target_direction = -target_direction

        # Gradually adjust direction towards target direction
        if current_direction != target_direction:
            # Calculate the smallest angle difference
            angle_difference = (target_direction - current_direction + 360) % 360
            if angle_difference > 180:
                angle_difference -= 360

            if angle_difference != 0:  # Check to prevent division by zero
                # Turn by the smaller of the angle difference or the defined increment
                turn_angle = min(abs(angle_difference), TURNING_ANGLE_INCREMENT)
                turn_angle *= abs(angle_difference) / angle_difference  # Retain the sign of the angle difference
                new_direction = current_direction + turn_angle

        self.setheading(new_direction)

        school_directions[self.school_index] = new_direction

        # Update the school direction and distance if needed
        school_distances[self.school_index] -= 1
        if school_distances[self.school_index] <= 0:
            school_directions[self.school_index] = random.randint(0, 360)
            school_distances[self.school_index] = random.randint(200, 500)

        # Randomly adjust distance if needed
        if school_distances[self.school_index] <= 0:
            school_directions[self.school_index] = random.randint(0, 360)
            school_distances[self.school_index] = random.randint(20, 100)  # Random distance between 20 and 100

        # Randomly vary direction within a small angle to simulate natural movement
        variation_angle = random.uniform(-10, 10)  # Variation angle range
        self.setheading(self.heading() + variation_angle)


        # Detect if the fish is near the edge and adjust its heading
        if abs(self.xcor()) > SCREEN_WIDTH * 0.75 or abs(self.ycor()) > SCREEN_HEIGHT * 0.75:
            angle_to_center = math.atan2(-self.ycor(), -self.xcor())
            angle_to_center = math.degrees(angle_to_center)
            self.setheading(self.heading() + 0.25 * ((angle_to_center - self.heading() + 360) % 360 - 180))
            self.forward(1000)

        # self.forward(FISH_SPEED)

        self.adjust_movement()

        self.avoid_collision()

        # Gradually apply avoidance turn
        if self.avoidance_turn != 0:
            new_heading = self.heading() + self.avoidance_turn
            self.setheading(new_heading)
            self.avoidance_turn *= 0.1  # Reduce avoidance turn over time for smoother movement

        # Vary speed slightly for more natural movement
        speed = FISH_SPEED + random.uniform(-SPEED_VARIATION, SPEED_VARIATION)
        self.forward(speed)

        # Update the distance left to swim in this direction
        school_distances[self.school_index] -= FISH_SPEED

    def set_school_direction(self, new_direction):
        global school_directions
        school_directions[self.school_index] = new_direction
        self.setheading(new_direction)

    def swim_towards_food(self, closest_food):
        if len(self.stomach) < STOMACH_SIZE and closest_food.ycor() < FOOD_ACTIVE_HEIGHT:  # Use STOMACH_SIZE
            distance_to_food = self.distance(closest_food)
            if distance_to_food < EATING_DISTANCE:
                self.eat_food(closest_food)
            else:
                # Adjust heading towards the food
                angle_to_food = math.atan2(closest_food.ycor() - self.ycor(), closest_food.xcor() - self.xcor())
                angle_to_food = math.degrees(angle_to_food)
                self.setheading(angle_to_food)

                # Call avoid_collision to adjust the heading if needed
                self.avoid_collision()

                # Increase speed when chasing food
                self.forward(CHASE_SPEED)


    def find_closest_food(self):
        min_distance = float('inf')
        closest_food = None
        for food in food_particles:
            if food.isvisible():
                distance = self.distance(food)
                if distance < min_distance:
                    min_distance = distance
                    closest_food = food
        return closest_food

    def avoid_collision(self):
        close_fish = [other_fish for other_fish in fishes if other_fish != self and self.distance(other_fish) < COLLISION_RADIUS]
        if close_fish:
            # Calculate average angle away from close fish
            away_angles = [math.atan2(self.ycor() - fish.ycor(), self.xcor() - fish.xcor()) for fish in close_fish]
            avg_away_angle = sum(away_angles) / len(away_angles)
            avg_away_angle = math.degrees(avg_away_angle)
            self.setheading(avg_away_angle)

    def forward(self, distance):
        super().forward(distance)
        self.update_stomach_display()  # Update the display position as the fish moves
        self.distance_swam += distance  # Track the distance swum
        if self.distance_swam >= SWIM_POOP_DISTANCE and self.stomach:
            self.poop()

    def poop(self):
        if self.stomach:
            # Create a poop object at the fish's current location
            poop = Poop(self.xcor(), self.ycor())
            poops.append(poop)  # Add to the list of poop objects
            self.stomach.clear()  # Clear the stomach contents
            self.distance_swam = 0  # Reset the distance swum

    def check_and_give_birth(self):
        if self.size_scale >= FISH_SIZE_TO_GIVE_BIRTH and self.food_eaten >= FOOD_EATEN_TO_MAKE_BABY:  # Reproduce after eating 20 foods

            global fishes
            if self.size_scale >= 2:  # Check if the fish is big enough
                self.outline_color("black")
                school_members = [fish for fish in fishes if fish.school_index == self.school_index]
                if len(school_members) >= 2:  # Check if there are at least 2 fishes in the school
                    for _ in range(3):  # Create 3 new fishes
                        new_fish = Fish(self.xcor(), self.ycor(), self.school_index)
                        fishes.append(new_fish)
                        new_fish.size_scale = INITIAL_SIZE  # Set the size of the new fish
                        new_fish.shapesize(stretch_wid=INITIAL_SIZE, stretch_len=INITIAL_SIZE, outline=None)
                    self.food_eaten = 0  # Reset food eaten counter after reproduction

    def remove_fish(self):
        """Remove the fish from the tank, including its stomach display."""
        self.stomach_display.clear()
        self.stomach_display.hideturtle()
        self.hideturtle()
        if self in fishes:
            fishes.remove(self)

class Food(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("square")
        self.color("chocolate")
        self.penup()
        self.shapesize(0.30, 0.10)

        # Ensure food spawns within the specified horizontal bounds
        x_pos = random.randint(-SCREEN_WIDTH // 2 + 100, SCREEN_WIDTH // 2 - 100)
        y_pos = SCREEN_HEIGHT // 2

        self.goto(x_pos, y_pos)
        self.setheading(270)


    def descend(self):
        stop_y = -SCREEN_HEIGHT // 2 + 90  # Y-coordinate to stop descending
        if self.ycor() > stop_y:
            self.forward(FOOD_SPEED)
        else:
            # Stop moving when the food reaches near the bottom
            self.sety(stop_y)  # Optional: Adjust position to exact stop point

class Poop(turtle.Turtle):
    def __init__(self, x, y):
        super().__init__()
        self.shape("circle")
        self.color("brown")  # Poop color
        self.penup()
        self.shapesize(0.2, 0.2)  # Smaller than food
        self.goto(x, y)  # Initial position set to the fish's position
        self.setheading(270)  # Downwards

    def descend(self):
        stop_y = -SCREEN_HEIGHT // 2 + 90  # Y-coordinate to stop descending
        if self.ycor() > stop_y:
            self.forward(POOP_SPEED)
        else:
            self.sety(stop_y)  # Stop moving when reaching near the bottom

    def remove(self):
        self.hideturtle()
        if self in poops:
            poops.remove(self)

class Tank_Top(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.color("white")  # Set the color of the tank top
        self.begin_fill()
        self.goto(-SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 +20)
        self.pendown()
        self.forward(SCREEN_WIDTH)
        self.right(90)
        self.forward(100)  # Height of the tank top
        self.right(90)
        self.forward(SCREEN_WIDTH)
        self.right(90)
        self.forward(100)  # Height of the tank top
        self.right(90)
        self.end_fill()

tank_top = Tank_Top()
class Floor(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.color("gray")  # Set floor color
        self.begin_fill()
        self.goto(-SCREEN_WIDTH // 2, -SCREEN_HEIGHT // 2)
        self.pendown()
        self.forward(SCREEN_WIDTH)
        self.left(90)
        self.forward(100)  # Height of the floor
        self.left(90)
        self.forward(SCREEN_WIDTH)
        self.left(90)
        self.forward(100)  # Height of the floor
        self.left(90)
        self.end_fill()

# Create the floor of the tank
floor = Floor()

# List to keep track of food particles
food_particles = []


# Function to toggle autofeeder
def toggle_autofeeder():
    global autofeeder_enabled
    autofeeder_enabled = not autofeeder_enabled
    print("Autofeeder " + ("enabled" if autofeeder_enabled else "disabled"))

# Function to check if autofeeder should drop food
def autofeeder():
    if autofeeder_enabled:
        # Check if any fish's stomach is not full
        any_stomach_not_full = any(len(fish.stomach) < STOMACH_SIZE for fish in fishes)

        # Check if there is no visible food on the screen
        no_food_present = all(not food.isvisible() for food in food_particles)

        if any_stomach_not_full and no_food_present:
            drop_food()

def clean_nearby_poop(x, y):
    for poop in poops[:]:  # Iterate over a copy of the list as it may be modified
        if poop.distance(x, y) < CLEANING_RADIUS:
            poop.remove()



def drop_food():
    for _ in range(FOOD_DROPPED):  # Drop 10 pieces of food
        food = Food()
        food_particles.append(food)


def drop_food_on_keypress():
    drop_food()


def get_random_point_near(center_x, center_y, min_distance, max_distance):
    angle = random.uniform(0, 360)
    distance = random.uniform(min_distance, max_distance)
    offset_x = distance * math.cos(math.radians(angle))
    offset_y = distance * math.sin(math.radians(angle))
    return center_x + offset_x, center_y + offset_y


def on_screen_click(x, y):
    clean_nearby_poop(x, y)
    global school_directions
    for fish in fishes:
        # Calculate the angle towards the click from the fish's current position
        angle = math.atan2(y - fish.ycor(), x - fish.xcor())
        angle = math.degrees(angle)
        fish.set_school_direction(angle)


# Create 5 schools of fishes with random populations between 5 and 10
for school_index in range(SCHOOL_NUMBER):
    central_x = random.randint(-SCREEN_WIDTH//4, SCREEN_WIDTH//4)
    central_y = random.randint(-SCREEN_HEIGHT//4, SCREEN_HEIGHT//4)
    number_of_fish_in_school = random.randint(SCHOOL_FISH_MIN, SCHOOL_FISH_MAX)
    for _ in range(number_of_fish_in_school):
        fish = Fish(central_x, central_y, school_index)
        # fish.size_scale = 1
        # fish.shapesize(stretch_wid=1, stretch_len=1, outline=None)
        # fish.pencolor("white")  # Set the initial border color
        fishes.append(fish)

def calculate_school_center(school_index):
    members = [fish for fish in fishes if fish.school_index == school_index]
    if not members:
        return 0, 0  # Return a default position if there are no members in the school

    avg_x = sum(fish.xcor() for fish in members) / len(members)
    avg_y = sum(fish.ycor() for fish in members) / len(members)
    return avg_x, avg_y


def find_two_closest_fish_for_food(food):
    if food.ycor() >= FOOD_ACTIVE_HEIGHT:  # Only consider food below the active height
        return []

    distances = [(fish, fish.distance(food)) for fish in fishes if len(fish.stomach) < STOMACH_SIZE and fish not in attracted_fish]
    distances.sort(key=lambda x: x[1])
    return distances[:2] if len(distances) >= 2 else distances


def increase_speed():
    global FISH_SPEED, FOOD_SPEED, POOP_SPEED, CHASE_SPEED
    FISH_SPEED += SPEED_INCREMENT
    FOOD_SPEED += SPEED_INCREMENT
    POOP_SPEED += SPEED_INCREMENT
    CHASE_SPEED += SPEED_INCREMENT


def decrease_speed():
    global FISH_SPEED, FOOD_SPEED, POOP_SPEED, CHASE_SPEED
    FISH_SPEED = max(0.25, FISH_SPEED - SPEED_INCREMENT)
    FOOD_SPEED = max(0.35, FOOD_SPEED - SPEED_INCREMENT)
    POOP_SPEED = max(0.35, POOP_SPEED - SPEED_INCREMENT)
    CHASE_SPEED = max(FISH_SPEED * 3, CHASE_SPEED - SPEED_INCREMENT)


# Define coordinates for the shark
shark_x = random.randint(-SCREEN_WIDTH//4, SCREEN_WIDTH//4)
shark_y = random.randint(-SCREEN_HEIGHT//4, SCREEN_HEIGHT//4)
shark = Fish(shark_x, shark_y, school_index, predator=True)


screen.listen()
screen.onkey(increase_speed, "+")
screen.onkey(decrease_speed, "-")
screen.onkey(drop_food_on_keypress, "f")
screen.onkey(toggle_autofeeder, "a")
screen.onclick(on_screen_click)


# Main game loop
while True:
    # Assign each food particle to the two closest fish
    food_assignments = {}
    for food in food_particles:
        closest_two_fish = find_two_closest_fish_for_food(food)
        for fish, _ in closest_two_fish:
            food_assignments.setdefault(fish, []).append(food)

    # Update fish and check for birth conditions
    for fish in fishes[:]:  # Use a copy of the list as it may be modified
        assigned_food = food_assignments.get(fish, [])
        active_assigned_food = [f for f in assigned_food if f.ycor() < FOOD_ACTIVE_HEIGHT]
        if active_assigned_food:
            # Let the fish swim towards the closest active assigned food
            closest_food = min(active_assigned_food, key=lambda x: fish.distance(x))
            fish.swim_towards_food(closest_food)
        else:
            fish.swim_in_school()

        fish.check_and_give_birth()

    # Move the shark
    if 'shark' in globals():  # Check if the shark exists
        shark.random_movement()

    # Update food particles
    for food in food_particles[:]:
        if food.isvisible():
            food.descend()
        else:
            try:
                food_particles.remove(food)
            except ValueError:
                pass  # for some reason a ValueError occurs saying 'x not in list'

    # Update poop particles
    for poop in poops[:]:
        if poop.isvisible():
            poop.descend()
        else:
            poops.remove(poop)

    # Call autofeeder function if enabled
    autofeeder()

    # Refresh the screen
    screen.update()
