import turtle
import random
import math

SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 900
X_MARGIN = 100
Y_MARGIN = 80

SCHOOL_NUMBER = 5
SCHOOL_FISH_MIN = 5
SCHOOL_FISH_MAX = 10
FISH_POPULATION_MAX = 50
INITIAL_SIZE = 0.2
EATING_DISTANCE = 10
FISH_MAX_SCALE_SIZE = 3
FISH_SIZE_TO_GIVE_BIRTH = 1
FISH_BIRTH_COUNT_MAX = 3
FISH_NUMBER_TO_BE_BORN_MIN = 1
FISH_NUMBER_TO_BE_BORN_MAX = 4
FOOD_EATEN_TO_MAKE_BABY = 2 #20

TURNING_ANGLE_INCREMENT = 1
SPEED_VARIATION = 0.15  # Slight variation in speed for dynamic movement

COLLISION_RADIUS_SWIM = 6  # Detection radius for avoiding other fish
COLLISION_RADIUS_FEED = 3  # Detection radius for avoiding other fish
AVOIDANCE_TURN_INCREMENT = 5  # Gradual turn increment for smoother avoidance

SCHOOL_SEPARATION_DISTANCE = 100  # Desired distance between schools
MAX_STRAY_DISTANCE = 200
PERSONAL_SPACE_MIN = 2  # Minimum personal space
PERSONAL_SPACE_MAX = 4  # Maximum personal space

autofeeder_enabled = False
FOOD_DROPPED = 25
FOOD_DROP_RADIUS = 100
FOOD_ACTIVE_HEIGHT = SCREEN_HEIGHT // 2 - 100  # Food becomes active when it's 100 units down from the top
food_particles = []

WATER_LEVEL_TO_APPLY_BAIT = SCREEN_HEIGHT // 2 - 55
fishing_line_bait = None

caught_fish = None
line_toggle = False


FISH_SPEED = 0.35
SUCKER_FISH_SPEED = 0.5
FOOD_SPEED = 0.20
CHASE_SPEED = FISH_SPEED * 3  # For some reason they slowed down... this addresses that
POOP_SPEED = 0.20
BOAT_SPEED = 1
LINE_SPEED = 15

FISH_CAUGHT_MY_PERSON_MIN = 25

CLEANING_RADIUS = 100  # Define how close a click needs to be to clean the poop

# Shark variables
SHARK_EATING_DISTANCE = 20  # Define how close the shark needs to be to eat the fish
SHARK_SPEED_MULTIPLIER = 5 #10
FISH_SIZE_TO_BE_EATEN = 1.2

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


# Create a turtle for displaying the fish count
fish_counter_display = turtle.Turtle()
fish_counter_display.hideturtle()
fish_counter_display.penup()
fish_counter_display.goto(-SCREEN_WIDTH // 2 + 50, -SCREEN_HEIGHT // 2 + 20)
fish_counter_display.color("black")

def update_fish_count_display():
    fish_counter_display.clear()
    total_fish = len(fishes)
    fish_counter_display.write(f"Fish: {total_fish}", align="left", font=("Arial", 16, "normal"))


# Initial update call
update_fish_count_display()

def get_random_point_near(center_x, center_y, min_distance, max_distance):
    angle = random.uniform(0, 360)
    distance = random.uniform(min_distance, max_distance)
    offset_x = distance * math.cos(math.radians(angle))
    offset_y = distance * math.sin(math.radians(angle))
    return center_x + offset_x, center_y + offset_y

class Tank:
    @staticmethod
    def total_fish():
        return len(fishes)



school_directions = [0 for _ in range(SCHOOL_NUMBER)]  # Initialize with a direction for each school

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
        self.personal_space = random.randint(PERSONAL_SPACE_MIN, PERSONAL_SPACE_MAX)
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

        self.update_stomach_display()

        self.min_speed = random.uniform(2, 5)
        self.max_speed = random.uniform(6, 9)
        self.current_speed = self.min_speed

    #
    # def swim_in_school(self):
    #     global school_directions
    #
    #     # Boundaries for clockwise movement with a margin
    #     margin = 10  # Margin to prevent overshooting
    #     left_bound = -SCREEN_WIDTH // 2 + 150 + margin
    #     right_bound = SCREEN_WIDTH // 2 - 150 - margin
    #     top_bound = SCREEN_HEIGHT // 2 - 150 - margin
    #     bottom_bound = -SCREEN_HEIGHT // 2 + 150 + margin
    #
    #     # Check if this fish hits any boundary
    #     if self.xcor() >= right_bound and school_directions[self.school_index] == 0:
    #         school_directions[self.school_index] = 270  # Change to down
    #     elif self.ycor() <= bottom_bound and school_directions[self.school_index] == 270:
    #         school_directions[self.school_index] = 180  # Change to left
    #     elif self.xcor() <= left_bound and school_directions[self.school_index] == 180:
    #         school_directions[self.school_index] = 90   # Change to up
    #     elif self.ycor() >= top_bound and school_directions[self.school_index] == 90:
    #         school_directions[self.school_index] = 0    # Change to right
    #
    #     # Set the fish's heading to the school's direction
    #     self.setheading(school_directions[self.school_index])
    #
    #     # Randomly adjust speed
    #     self.adjust_speed()
    #
    #     # Move the fish forward with its current speed
    #     self.forward(self.current_speed)
    #
    # def adjust_speed(self):
    #     if random.random() < 0.1:  # 10% chance to change speed
    #         # Determine whether to increase or decrease the speed
    #         speed_change = 0.5 if random.random() < 0.5 else -0.5
    #         new_speed = self.current_speed + speed_change
    #
    #         # Ensure the new speed is within the min-max range
    #         self.current_speed = max(self.min_speed, min(new_speed, self.max_speed))
    #

    ##################################################################
    def check_boundary_hit(self):
        # Check if this fish hits any of the boundaries
        if self.xcor() >= SCREEN_WIDTH // 2 - 150 or self.xcor() <= -SCREEN_WIDTH // 2 + 150:
            return True
        if self.ycor() >= SCREEN_HEIGHT // 2 - 150 or self.ycor() <= -SCREEN_HEIGHT // 2 + 150:
            return True
        return False


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

        self.avoid_collision(COLLISION_RADIUS_SWIM)

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




    def check_and_remove_near_person(self):
        if self.distance(person) < FISH_CAUGHT_MY_PERSON_MIN:
            self.remove_fish()

    def update_stomach_display(self):
        self.stomach_display.clear()  # Clear the previous text
        display_position_y = self.ycor() + 20  # Adjust the Y-offset to display above the fish
        self.stomach_display.goto(self.xcor(), display_position_y)
        self.stomach_display.write(len(self.stomach), align="center", font=("Arial", 8, "normal"))

    def hide_stomach_display(self):
        self.stomach_display.hideturtle()
        self.stomach_display.clear()

    def show_stomach_display(self):
        self.stomach_display.showturtle()

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
        if self.size_scale >= FISH_SIZE_TO_GIVE_BIRTH and self.birth_count <= FISH_BIRTH_COUNT_MAX and len(self.stomach) == STOMACH_SIZE and Tank.total_fish <= FISH_POPULATION_MAX:  # Check size and birth count
            school_members = [fish for fish in fishes if fish.school_index == self.school_index]
            if len(school_members) >= 2:  # Check if there are at least 2 fishes in the school
                fish_to_be_born = random.randint(FISH_NUMBER_TO_BE_BORN_MIN, FISH_NUMBER_TO_BE_BORN_MAX)
                for _ in range(fish_to_be_born):  # Create 3 new fishes
                    new_fish = Fish(self.xcor(), self.ycor(), self.school_index)
                    fishes.append(new_fish)
                    new_fish.size_scale = INITIAL_SIZE  # Set the size of the new fish
                    new_fish.shapesize(stretch_wid=INITIAL_SIZE, stretch_len=INITIAL_SIZE, outline=None)
                self.birth_count += 1  # Increment the birth count
                if self.birth_count == 1:
                    self.outline_color("black")  # Change the border to black on second birth

    def outline_color(self, color):
        self.shapesize(stretch_wid=self.size_scale, stretch_len=self.size_scale, outline=1)
        self.pencolor(color)

    def get_dynamic_eating_distance(self):
        base_eating_distance = EATING_DISTANCE
        return base_eating_distance * self.size_scale / INITIAL_SIZE

    def get_dynamic_personal_space(self):
        # Scale up the personal space as the fish grows
        return PERSONAL_SPACE_MIN * self.size_scale / INITIAL_SIZE

    def eat_food(self, closest_food):
        global caught_fish

        if len(self.stomach) < STOMACH_SIZE and closest_food.ycor() < FOOD_ACTIVE_HEIGHT:
            distance_to_food = self.distance(closest_food)
            if distance_to_food < self.get_dynamic_eating_distance():
                self.stomach.append(closest_food)  # Add the food to the stomach
                self.food_eaten += 1  # Increment the food eaten counter
                closest_food.hideturtle()  # Hide the food particle
                try:
                    food_particles.remove(closest_food)  # Remove the food from the list
                except ValueError:
                    pass  # Handle the exception if the food is already removed

                if closest_food == fishing_line_bait and not closest_food.is_eaten:
                    closest_food.get_eaten()
                    caught_fish = self  # Set the caught fish
                    self.penup()  # To allow free movement
                    self.hide_stomach_display()  # Hide the stomach display

                # Increase the size of the fish if the stomach is full
                if len(self.stomach) == STOMACH_SIZE:
                    self.size_scale += 0.1  # Increment size scale
                    if self.size_scale > FISH_MAX_SCALE_SIZE:
                        self.size_scale = FISH_MAX_SCALE_SIZE
                    self.shapesize(stretch_wid=self.size_scale, stretch_len=self.size_scale, outline=None)

                self.update_stomach_display()  # Update display
                if self in attracted_fish:
                    attracted_fish.remove(self)  # Remove from attracted_fish list

        # Update display (if you have the display feature implemented)
        self.update_stomach_display()
        if self in attracted_fish:
            attracted_fish.remove(self)  # Remove from attracted_fish list

        if closest_food == fishing_line_bait and not closest_food.is_eaten:
            closest_food.get_eaten()
            caught_fish = self  # Set the caught fish
            self.penup()  # To allow free movement

    def give_up_chase(self):
        if self in attracted_fish:
            attracted_fish.remove(self)  # Remove from attracted_fish list


    def adjust_movement(self):
        # Use dynamic personal space calculation
        dynamic_personal_space = self.get_dynamic_personal_space()

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


    def set_school_direction(self, new_direction):
        global school_directions
        school_directions[self.school_index] = new_direction
        self.setheading(new_direction)

    def swim_towards_food_or_bait(self):
        closest_food = self.find_closest_food()
        closest_bait = self.find_closest_bait()

        if closest_food:
            if self.distance(closest_food) < self.get_dynamic_eating_distance():
                self.eat_food(closest_food)  # Consume the target
            else:
                # Adjust heading towards the target
                angle_to_target = math.atan2(closest_food.ycor() - self.ycor(), closest_food.xcor() - self.xcor())
                angle_to_target = math.degrees(angle_to_target)
                self.setheading(angle_to_target)
                self.forward(CHASE_SPEED)
        elif closest_bait and not closest_bait.is_eaten:
            # Only chase the bait if it's not eaten
            distance_to_bait = self.distance(closest_bait)
            if distance_to_bait < self.get_dynamic_eating_distance():
                self.eat_food(closest_bait)
            else:
                angle_to_bait = math.atan2(closest_bait.ycor() - self.ycor(), closest_bait.xcor() - self.xcor())
                angle_to_bait = math.degrees(angle_to_bait)
                self.setheading(angle_to_bait)
                self.forward(CHASE_SPEED)
        else:
            # Continue with other behavior (like swimming in school) if no target is found
            self.swim_in_school()


    def find_closest_food(self):
        closest_target = None
        min_distance = float('inf')

        # Check for closest food particle
        for food in food_particles:
            if food.isvisible():
                distance = self.distance(food)
                if distance < min_distance:
                    min_distance = distance
                    closest_target = food
        return closest_target

    def find_closest_bait(self):
        closest_target = None
        min_distance = float('inf')

        # Check for closest bait
        distance = self.distance(fishing_line_bait)
        if distance < min_distance:
            min_distance = distance
            closest_target = fishing_line_bait
        return closest_target

    def avoid_collision(self, collision_radius):
        close_fish = [other_fish for other_fish in fishes if other_fish != self and self.distance(other_fish) < collision_radius]
        if close_fish:
            # Calculate average angle away from close fish
            away_angles = [math.atan2(self.ycor() - fish.ycor(), self.xcor() - fish.xcor()) for fish in close_fish]
            avg_away_angle = sum(away_angles) / len(away_angles)
            avg_away_angle = math.degrees(avg_away_angle)
            self.setheading(avg_away_angle)

    def forward(self, distance):
        if line_toggle:
            self.pendown()
        else:
            self.penup()
            self.clear()
        super().forward(distance)
        self.update_stomach_display()
        self.distance_swam += distance

        if self.distance_swam >= SWIM_POOP_DISTANCE and self.stomach:
            self.poop()

    def poop(self):
        # Only allow pooping if the stomach is full
        if len(self.stomach) >= STOMACH_SIZE:
            poop = Poop(self.xcor(), self.ycor())
            poops.append(poop)  # Add to the list of poop objects
            self.stomach.clear()  # Clear the stomach contents
            self.distance_swam = 0  # Reset the distance swum
            self.update_stomach_display()  # Update the display to reflect the empty stomach

    def check_and_give_birth(self):
        global fishes
        if self.size_scale >= FISH_SIZE_TO_GIVE_BIRTH and self.birth_count <= FISH_BIRTH_COUNT_MAX and len(
                self.stomach) == STOMACH_SIZE:
            if Tank.total_fish() + FISH_NUMBER_TO_BE_BORN_MAX <= FISH_POPULATION_MAX:  # Ensure adding new fish won't exceed max population
                school_members = [fish for fish in fishes if fish.school_index == self.school_index]
                if len(school_members) >= 2:  # Check if there are at least 2 fishes in the school
                    fish_to_be_born = random.randint(FISH_NUMBER_TO_BE_BORN_MIN, FISH_NUMBER_TO_BE_BORN_MAX)
                    for _ in range(fish_to_be_born):
                        new_fish = Fish(self.xcor(), self.ycor(), self.school_index)
                        fishes.append(new_fish)
                        new_fish.size_scale = INITIAL_SIZE
                        new_fish.shapesize(stretch_wid=INITIAL_SIZE, stretch_len=INITIAL_SIZE, outline=None)
                    self.stomach.clear()  # Clear the stomach after giving birth
                    self.update_stomach_display()  # Update the display
                    self.birth_count += 1  # Increment the birth count
                    if self.birth_count == 1:
                        self.outline_color("black")  # Change the border to black on second birth

    def remove_fish(self):
        """Remove the fish from the tank, including its stomach display."""
        self.stomach_display.clear()
        self.stomach_display.hideturtle()
        self.hideturtle()
        if self in fishes:
            fishes.remove(self)

class SuckerFish(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("square")
        self.color("darkgreen")
        self.penup()
        # Raise the sucker fish by 10 units
        self.goto(random.randint(-SCREEN_WIDTH//2, SCREEN_WIDTH//2), -SCREEN_HEIGHT//2 + 85)
        self.setheading(0)
        self.speed = SUCKER_FISH_SPEED  # Set a speed for the sucker fish
        # Stretch the sucker fish into a long rectangle
        self.shapesize(0.5, 2.25)  # Adjust the first parameter for height, second for length

    def move(self):
        # Move forward continuously
        self.forward(self.speed)

        # Turn around if it hits the tank boundaries
        if abs(self.xcor()) > SCREEN_WIDTH//2 - X_MARGIN:
            self.setheading(180 - self.heading())

    def clean_poop(self):
        # Check for nearby poop and remove it
        for poop in poops[:]:
            if self.distance(poop) < 20:  # Adjust cleaning radius as needed
                poop.remove()

class Food(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("square")
        self.color("chocolate")
        self.penup()
        self.shapesize(0.30, 0.10)
        self.is_moving = False
        self.arc_height = 50  # Maximum height of the arc
        self.gravity = -0.25  # Gravity effect
        self.x_speed = 0.5  # Horizontal speed
        self.y_speed = 5  # Initial vertical speed

        # Ensure food spawns within the specified horizontal bounds
        x_pos = random.randint(-SCREEN_WIDTH // 2 + 100, SCREEN_WIDTH // 2 - 100)
        y_pos = SCREEN_HEIGHT // 2

        self.goto(x_pos, y_pos)
        self.setheading(270)

    def start_moving(self, start_x, start_y, target_x):
        self.goto(start_x, start_y)
        self.is_moving = True
        self.x_speed = (target_x - start_x) / 40.0  # Adjust the number for arc length

    def move(self):
        if self.is_moving:
            new_x = self.xcor() + self.x_speed
            new_y = self.ycor() + self.y_speed
            self.y_speed += self.gravity
            self.goto(new_x, new_y)

            if self.ycor() <= FOOD_ACTIVE_HEIGHT:
                self.is_moving = False  # Stop arcing when reaching the water surface


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
        self.goto(-SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)
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


class Wave(turtle.Turtle):
    def __init__(self, x, y):
        super().__init__()
        self.penup()
        self.shape("circle")
        self.color("lightblue")
        self.shapesize(stretch_wid=1, stretch_len=2)
        self.goto(x, y)
        self.dy = random.uniform(0.1, 0.15)  # Speed of the wave's vertical movement

    def move(self):
        self.sety(self.ycor() + self.dy)
        if self.ycor() > SCREEN_HEIGHT // 2 - 80 or self.ycor() < SCREEN_HEIGHT // 2 - 90:
            self.dy *= -1  # Reverse direction



class Person(turtle.Turtle):
    def __init__(self, boat):
        super().__init__()
        self.boat = boat
        self.shape("square")  # Or use a custom shape
        self.shapesize(stretch_wid=1, stretch_len=0.25, outline=1)
        self.color("pink")
        self.penup()
        self.goto(boat.xcor(), boat.ycor() + 20)  # Position the person on the boat
        self.fishing_pole = FishingPole(self)
        self.fishing_line = FishingLine(self.fishing_pole)  # Pass the fishing_pole object
        self.fish_caught = 0  # Initialize fish caught count
        self.fish_caught_display = turtle.Turtle(visible=False)  # Create a turtle for displaying the fish count
        self.fish_caught_display.penup()
        self.fish_caught_display.goto(self.xcor(), self.ycor() + 30)  # Position above the person
        self.update_fish_caught_display()


    def update_fish_caught_display(self):
        self.fish_caught_display.clear()
        self.fish_caught_display.write(f"Caught: {self.fish_caught}", align="center", font=("Arial", 12, "normal"))

    def update_fishing_pole_direction(self):
        # Update the fishing pole's direction based on the boat's movement
        self.fishing_pole.update_direction(self.boat.last_movement_direction)


class FishingPole(turtle.Turtle):

    def __init__(self, person):
        super().__init__()
        self.person = person
        self.shape("square")
        self.shapesize(stretch_wid=0.1, stretch_len=1, outline=1)
        self.color('black')
        self.penup()
        self.goto(person.xcor(), person.ycor())
        self.setheading(0)  # Initial direction


    def update_pole_position(self):
        global caught_fish

        # Position the fishing pole relative to the person
        self.goto(self.person.xcor(), self.person.ycor() - 20)  # Adjust offset as needed

        # Calculate the new position and orientation of the fishing pole
        if self.person.boat.direction != 0:
            offset_x = 10 if self.person.boat.last_movement_direction < 0 else -10
            offset_y = 8  # Raise the pole by 10 units
            angle = 35 if self.person.boat.last_movement_direction < 0 else -35
        else:
            offset_x = 0
            offset_y = 10  # Raise the pole by 10 units
            angle = 90  # Vertical when the boat is not moving

        # Position the fishing pole relative to the person
        self.goto(self.person.xcor() + offset_x, self.person.ycor() + offset_y)
        self.setheading(angle)

        # Ensure that the line position is updated whenever the pole position is updated
        self.person.fishing_line.update_line_position()

        if caught_fish:
            tip_x, tip_y = self.person.fishing_line.get_bait_coordinates()
            caught_fish.goto(tip_x, tip_y)

    def update_direction(self, boat_direction):
        # Point the fishing pole in the opposite direction of the boat's last movement
        if boat_direction != 0:
            self.setheading(180 if boat_direction < 0 else 0)


class Boat(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("square")  # You can use a custom shape for a more boat-like appearance
        self.color("brown")
        self.shapesize(1, 4)  # Adjust the size as needed
        self.penup()
        self.goto(0, SCREEN_HEIGHT // 2 - 80)  # Lower the boat by 20 units
        self.direction = 0  # 0 for no movement, -1 for left, 1 for right
        self.last_movement_direction = 0  # Track the last movement direction
        self.person = None  # Initialize with None and set later

    def start_moving_left(self):
        self.direction = - BOAT_SPEED

    def start_moving_right(self):
        self.direction = BOAT_SPEED

    def stop(self):
        self.direction = 0

    def move(self):
        global caught_fish

        new_x = self.xcor() + self.direction
        if new_x < -SCREEN_WIDTH // 2 + X_MARGIN or new_x > SCREEN_WIDTH // 2 - X_MARGIN:
            self.direction *= -1  # Reverse direction if at the tank boundary
        else:
            self.setx(new_x)
            person.goto(self.xcor(), self.ycor() + 20)  # Update person's position with boat

        # Update last movement direction
        self.last_movement_direction = self.direction
        person.update_fishing_pole_direction()

        if self.person is not None:
            self.person.fishing_line.bait.update_bait_position()

        if self.person:
            self.person.fishing_line.update_line_position()

        if caught_fish:
            tip_x, tip_y = person.fishing_line.get_bait_coordinates()
            caught_fish.goto(tip_x, tip_y)

    def adjust_vertical_position(self, waves):
        # Get the x-coordinates of the boat
        boat_x_left = self.xcor() - self.shapesize()[1] * 10  # 10 is half the size of the turtle's default size
        boat_x_right = self.xcor() + self.shapesize()[1] * 10

        # Find waves under the boat
        waves_under_boat = [wave for wave in waves if boat_x_left <= wave.xcor() <= boat_x_right]

        # Calculate the average y-coordinate of these waves
        if waves_under_boat:
            avg_y = sum(wave.ycor() for wave in waves_under_boat) / len(waves_under_boat)
            self.sety(avg_y + 15)  # 20 is an offset to place the boat above the waves

        # Update person's vertical position
        person.goto(self.xcor(), self.ycor() + 20)

        # Update fishing pole's position
        person.fishing_pole.update_pole_position()


class FishingLine(turtle.Turtle):
    def __init__(self, fishing_pole):
        super().__init__()
        super().__init__()
        self.fishing_pole = fishing_pole
        self.color("gray")
        self.hideturtle()
        self.penup()
        self.line_length = 15
        self.is_extended = True
        self.bait = Bait(self)
        global fishing_line_bait
        fishing_line_bait = self.bait

    def get_bait_coordinates(self):
        return self.bait.xcor(), self.bait.ycor()

    def update_line_position(self):
        self.clear()
        self.penup()

        # Get the position and orientation of the fishing pole
        pole_x, pole_y = self.fishing_pole.position()
        pole_heading = self.fishing_pole.heading()
        pole_length = 10  # Length of the fishing pole

        # Adjust pole_heading for rightward movement
        # If the boat is moving right, the pole's heading should be adjusted by 180 degrees
        if self.fishing_pole.person.boat.direction > 0:
            pole_heading = (pole_heading + 180) % 360

        # Calculate the tip of the pole using trigonometry
        heading_radians = math.radians(pole_heading)
        tip_x = pole_x + pole_length * math.cos(heading_radians)
        tip_y = pole_y + pole_length * math.sin(heading_radians)

        # Position the line at the tip of the pole
        self.goto(tip_x, tip_y)
        self.pendown()

        # Draw line based on whether it's extended
        if self.is_extended:
            # Line casted
            self.goto(tip_x, tip_y - self.line_length)
        else:
            # Line reeled in
            self.goto(tip_x, tip_y)
        self.penup()

        # Update bait position
        self.bait.update_bait_position()

    def extend_line(self):
        global caught_fish
        # Increase the line length by a fixed amount
        if self.ycor() > -SCREEN_HEIGHT // 2 + 130:
            self.line_length += LINE_SPEED

        self.bait.update_bait_position()
        if caught_fish:
            tip_x, tip_y = self.get_bait_coordinates()
            caught_fish.goto(tip_x, tip_y)

    def retract_line(self):
        global caught_fish
        # Decrease the line length by a fixed amount
        if self.ycor() < self.fishing_pole.ycor() - 15:
            self.line_length -= LINE_SPEED
        # fishing_line_bait.update_bait_position()

        self.bait.update_bait_position()
        if caught_fish:
            tip_x, tip_y = self.get_bait_coordinates()
            caught_fish.goto(tip_x, tip_y)

class Bait(turtle.Turtle):
    def __init__(self, fishing_line):
        super().__init__()
        self.fishing_line = fishing_line
        self.shape("circle")
        self.color("brown")  # You can choose any color or shape
        self.shapesize(0.1, 0.25)  # Adjust size as needed
        self.penup()
        self.update_bait_position()
        self.is_eaten = False  # Add this line

    def get_eaten(self):
        self.is_eaten = True
        self.hideturtle()

    def update_bait_position(self):
        # Get the end position of the fishing line
        line_end_x, line_end_y = self.fishing_line.position()
        self.goto(line_end_x, line_end_y)

    def reset_bait(self):
        self.showturtle()  # Make the bait visible again
        self.update_bait_position()  # Update its position to the end of the line


def reset_the_bait():
    # Check if the end of the fishing line is above the water level
    if fishing_line_bait.fishing_line.ycor() > WATER_LEVEL_TO_APPLY_BAIT:
        fishing_line_bait.reset_bait()
        fishing_line_bait.is_eaten = False  # Reset the eaten status

# # Create the boat
boat = Boat()

# Create wave objects
waves = [Wave(x, SCREEN_HEIGHT // 2 - 80) for x in range(-SCREEN_WIDTH // 2, SCREEN_WIDTH // 2, 30)]

# Create the boat and person objects
person = Person(boat)  # Pass the existing boat object to the person
boat.person = person   # Assign the person to the boat's attribute


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


# Define coordinates for the shark
shark_x = random.randint(-SCREEN_WIDTH//4, SCREEN_WIDTH//4)
shark_y = random.randint(-SCREEN_HEIGHT//4, SCREEN_HEIGHT//4)
shark = Fish(shark_x, shark_y, school_index, predator=True)

# Create the tank top
tank_top = Tank_Top()

# Create the floor of the tank
floor = Floor()

# Create a sucker fish
sucker_fish = SuckerFish()


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
    # Get the current x-coordinate of the boat
    boat_x = boat.xcor()
    boat_y = boat.ycor()

    # Define the range for food spawning
    food_spawn_min_x = boat_x - 200
    food_spawn_max_x = boat_x + 200

    # Adjust the range if it exceeds the screen boundaries
    if food_spawn_min_x < -SCREEN_WIDTH // 2 + X_MARGIN:
        food_spawn_min_x = -SCREEN_WIDTH // 2 + X_MARGIN
        food_spawn_max_x = food_spawn_min_x + 400  # Maintain a 400 unit range

    if food_spawn_max_x > SCREEN_WIDTH // 2 - X_MARGIN:
        food_spawn_max_x = SCREEN_WIDTH // 2 - X_MARGIN
        food_spawn_min_x = food_spawn_max_x - 400  # Maintain a 400 unit range

    for _ in range(FOOD_DROPPED):
        food_x = random.randint(boat_x - FOOD_DROP_RADIUS, boat_x + FOOD_DROP_RADIUS)
        # Ensure food doesn't spawn outside the tank boundaries
        food_x = max(min(food_x, SCREEN_WIDTH // 2 - X_MARGIN), -SCREEN_WIDTH // 2 + X_MARGIN)

        food = Food()
        food.start_moving(boat_x, boat_y, food_x)  # Start moving from boat's position
        food_particles.append(food)


def drop_food_on_keypress():
    drop_food()


def on_screen_click(x, y):
    clean_nearby_poop(x, y)
    global school_directions
    for fish in fishes:
        # Calculate the angle towards the click from the fish's current position
        angle = math.atan2(y - fish.ycor(), x - fish.xcor())
        angle = math.degrees(angle)
        fish.set_school_direction(angle)


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
    global FISH_SPEED, SUCKER_FISH_SPEED, FOOD_SPEED, POOP_SPEED, CHASE_SPEED, BOAT_SPEED, LINE_SPEED
    FISH_SPEED += SPEED_INCREMENT
    SUCKER_FISH_SPEED += SPEED_INCREMENT
    FOOD_SPEED += SPEED_INCREMENT
    POOP_SPEED += SPEED_INCREMENT
    CHASE_SPEED = FISH_SPEED * 3
    BOAT_SPEED += SPEED_INCREMENT
    LINE_SPEED += SPEED_INCREMENT


def decrease_speed():
    global FISH_SPEED, FOOD_SPEED, POOP_SPEED, CHASE_SPEED
    FISH_SPEED = max(0.25, FISH_SPEED - SPEED_INCREMENT)
    FOOD_SPEED = max(0.35, FOOD_SPEED - SPEED_INCREMENT)
    POOP_SPEED = max(0.35, POOP_SPEED - SPEED_INCREMENT)
    CHASE_SPEED = max(FISH_SPEED * 3, CHASE_SPEED - SPEED_INCREMENT)

def release_fish():
    global caught_fish
    if caught_fish and caught_fish.distance(person) < FISH_CAUGHT_MY_PERSON_MIN:
        caught_fish.remove_fish()  # Remove the fish from the game
        person.fish_caught += 1  # Increment the fish caught count
        person.update_fish_caught_display()  # Update the display
        caught_fish = None
    elif caught_fish:
        caught_fish.update_stomach_display()  # Show the stomach display again if the fish is not close enough
        caught_fish = None

def toggle_line_display():
    global line_toggle
    line_toggle = not line_toggle


# Fishing line tip coordinates
# Create a turtle for displaying the fishing line tip coordinates
coord_display = turtle.Turtle()
coord_display.hideturtle()
coord_display.penup()
coord_display.goto(SCREEN_WIDTH // 2 - 150, -SCREEN_HEIGHT // 2 + 50)


# Bind key events
screen.listen()
screen.onkey(increase_speed, "+")
screen.onkey(decrease_speed, "-")
screen.onkey(drop_food_on_keypress, "f")
screen.onkey(toggle_line_display, "l")
screen.onkey(toggle_autofeeder, "a")
screen.onkey(release_fish, "r")
screen.onkey(reset_the_bait, "b")
screen.onkey(boat.stop, "/")
screen.onkey(boat.start_moving_left, "Left")
screen.onkey(boat.start_moving_right, "Right")
screen.onkey(person.fishing_line.retract_line, "Up")
screen.onkey(person.fishing_line.extend_line, "Down")
screen.onclick(on_screen_click)


# Main game loop
while True:
    # Update the fish count display
    update_fish_count_display()

    # Fishing line tip coordinates
    tip_x, tip_y = person.fishing_line.get_bait_coordinates()
    coord_display.clear()  # Clear the previous coordinates
    coord_display.write(f"Line Tip: ({tip_x:.2f}, {tip_y:.2f})", align="left", font=("Arial", 12, "normal"))

    # Assign each food particle to the two closest fish
    food_assignments = {}
    for food in food_particles:
        closest_two_fish = find_two_closest_fish_for_food(food)
        for fish, _ in closest_two_fish:
            food_assignments.setdefault(fish, []).append(food)

    # Assign bait to the two closest fish
    closest_two_fish = find_two_closest_fish_for_food(fishing_line_bait)
    for fish, _ in closest_two_fish:
        food_assignments.setdefault(fish, []).append(fishing_line_bait)

    if fish.distance(fishing_line_bait) < EATING_DISTANCE and not fishing_line_bait.is_eaten:
        fishing_line_bait.get_eaten()
        fish.eat_food(fishing_line_bait)  # Assuming you have a method for fish to eat food
        # break

    # Move the caught fish with the fishing line
    if caught_fish:
        tip_x, tip_y = person.fishing_line.get_bait_coordinates()
        caught_fish.goto(tip_x, tip_y)
        caught_fish.hide_stomach_display()

    # Update fish and check for birth conditions
    for fish in fishes[:]:  # Use a copy of the list as it may be modified
        if fish != caught_fish:  # Skip the caught fish
            assigned_food = food_assignments.get(fish, [])
            active_assigned_food = [f for f in assigned_food if f.ycor() < FOOD_ACTIVE_HEIGHT]
            if active_assigned_food:
                # Let the fish swim towards the closest active assigned food
                closest_food = min(active_assigned_food, key=lambda x: fish.distance(x))
                fish.swim_towards_food_or_bait()
            else:
                fish.swim_in_school()

            fish.check_and_remove_near_person()  # Add this line

            fish.check_and_give_birth()

            # fish.hide_stomach_display()  # Keep updating position for other fishes


    # Move the shark
    if 'shark' in globals():  # Check if the shark exists
        shark.random_movement()

    # Move the food particles
    for food in food_particles[:]:
        if food.is_moving:
            food.move()
        else:
            if food.isvisible():
                food.descend()
            else:
                try:
                    food_particles.remove(food)
                except ValueError:
                    pass  # Handle the error if the food is already removed

    # Update poop particles
    for poop in poops[:]:
        if poop.isvisible():
            poop.descend()
        else:
            poops.remove(poop)

    # Move and clean with the sucker fish
    sucker_fish.move()
    sucker_fish.clean_poop()

    # Update the fishing line's position
    person.fishing_line.update_line_position()

    # Move the waves
    for wave in waves:
        wave.move()


    # Move the boat and adjust its vertical position
    boat.move()
    boat.adjust_vertical_position(waves)

    # Update the person's position based on the boat's position
    person.goto(boat.xcor(), boat.ycor() + 20)


    # Call autofeeder function if enabled
    autofeeder()

    # Refresh the screen
    screen.update()
