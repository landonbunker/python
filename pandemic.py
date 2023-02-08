import tkinter
import random

WIDTH = 80                  # How many cells wide the neighborhood is
HEIGHT = 60                 # How many cells tall the neighborhood is
                            # Note that going larger makes each day take longer.
                            # If you want to go bigger than 150 x 100 or so,
                            # do it in steps so that you can gauge how slow your
                            # computer gets
CELL_PIXEL_SIZE = 12        # Size of each cell on screen, in pixels

SCREEN_UPDATE_FREQUENCY = 1 # How often to redraw the screen.  Making this 5 or 10
                            # will cause the screen to redraw only every 5 or 10
                            # days, speeding up the run-time, slightly.

STARTING_INFECTED = 4       # How many "patient zero"s are there in your population?

POPULATION_DENSITY = .2    # Fraction of cells have a person in them

SYMPTOM_CHANCE = .3        # Chance that people who are infected will develop
                           # symptoms (per day)

SYMPTOM_MORTALITY_RATE = .05 # Fraction of people with symptoms will die from it
    
INFECTION_LENGTH = 6       # How many days the infection lasts

CONTAGION_FACTOR = .1       # If you come into contact with someone who is contagious,
                            # how likely are you to get it?

class Person:
    # There are five states a person can be in:
    #   Susceptable:  They've never had it, and can get it
    #   Infected:   They have it and are contagious, but don't know it
    #   Symptomatic: They have it, and have symptoms, so they move around less
    #   Recovered:  They're over it, no longer contagious, and can't get it again
    #   Dead:  They died of the virus
    
    # Each person object needs to "know" (have stored) their neighborhood, and
    # where in their neighborhood (row, column) they are located
    def __init__(self, neighborhood, row, col):
        self.state = "susceptable"
        self.neighborhood = neighborhood
        self.my_row = row
        self.my_col = col
    
    # How many neighbors within a certain distance are infected or symptomatic?
    # Rather than pythagorian distance, I'm just doing an n x n square from
    # the grid.  So, if distance is 2, I'm counting how many people in the two
    # rows above, two rows below, two columns to the left, and two-columns to 
    # the right are contagious.    
    def count_infected_neighbors(self, distance):
        infected_neighbors = 0
        for r in range(self.my_row - distance, self.my_row + distance + 1):
            for c in range(self.my_col - distance, self.my_col + distance + 1):
                # Check if the neighbor I'm looking at is off the grid
                if r < 0 or c < 0 or r >= HEIGHT or c >= WIDTH:
                    continue
                # Check if the "neighbor" I'm looking at is actually me
                if r == self.my_row and c == self.my_col:
                    continue
                # Only check if that location in the grid is contagious if it's 
                # not "empty". (Because, if it's the string "empty", it won't 
                # have a .state variable to check, and trying would cause an 
                # error.)
                if self.neighborhood.grid[r][c] != "empty" \
                        and self.neighborhood.grid[r][c].state in ["infected", "symptomatic"]:
                    infected_neighbors += 1
        return infected_neighbors
        
        
    # This function gets called once per clock (day) for each person object
    def update(self):
        
        # Move around (How far? based on how healthy you feel.)
        if self.state == "susceptable" or self.state == "infected"  or \
                    self.state == "recovered":
            # Healthy-feeling people move 5 "steps"
            for i in range(5):
                self.move()
        elif self.state == "symptomatic":
            # Sick-feeling people mostly stay home -- move 1 step
            for i in range(1):
                self.move()
        
        # If you're sick, you're one day closer to getting better
        if self.state == "infected" or self.state == "symptomatic":
            self.days_left -= 1
            
            # If you're sick but have no days left to be sick, you're recovered.
            # Congratulations!
            if self.days_left <= 0:
                self.state = "recovered"

        # If you're infected, you have a chance of developing symptoms
        if self.state == "infected":
            if random.random() < SYMPTOM_CHANCE:
                self.state = "symptomatic"
                
        # If you're symptomatic, you have a chance of dying.
        if self.state == "symptomatic":
            if random.random() < (SYMPTOM_MORTALITY_RATE / INFECTION_LENGTH):
                self.state = "dead"
            
        # If you're susceptable, you have a chance of getting infected
        if self.state == "susceptable":
            # x is how likely you are to get it from someone at a given distance.
            # We're assuming that the chance of getting it is cut in half with 
            # each additional step away.  That is, if you have a 30% chance of 
            # getting it if you're next to an infected person, you'll have a 15% 
            # chance of getting it for each infected person 2 steps away
            # and a 7.5% chance for each infected person 3 steps away, etc...
            contagion_chance = CONTAGION_FACTOR
            # Calculating for up to 4 places out.  Kind of arbitrary how far to check.
            for distance in range(4):
                # count how many infected people are within a certain distance
                num_infected_people = self.count_infected_neighbors(distance)
                for i in range(num_infected_people):
                    if random.random() < contagion_chance:
                        self.state = "infected"
                        self.days_left = INFECTION_LENGTH
                        
                # Divide chance of contagion by 2 for each step away from the
                # nearest infected person
                contagion_chance = contagion_chance / 2
    
    def move(self):
        # Make a list of all of the blank cells around me, then pick one to 
        # move to (if any)
        empty_neighbors = []
        for r in range(self.my_row - 1, self.my_row + 2):
            for c in range(self.my_col - 1, self.my_col + 2):
                # If the neighbor I'm looking at is off the grid, skip to the next one
                if r < 0 or c < 0 or r >= HEIGHT or c >= WIDTH:
                    continue
                # If the "neighbor" I'm looking at is me, skip to the next one
                if r == self.my_row and c == self.my_col:
                    continue
                
                if self.neighborhood.grid[r][c] == "empty":
                    empty_neighbors.append( (r,c) )
        
        if len(empty_neighbors) > 0:
            
            # Pick an empty neighboring cell at random
            new_row, new_col = random.choice(empty_neighbors)
        
            # To "move" there, replace my current spot in the grid with 
            # "empty", and insert myself in the new, previously empty
            # spot, then update my own record of where I am.
            self.neighborhood.grid[self.my_row][self.my_col] = "empty"
            self.neighborhood.grid[new_row][new_col] = self
            self.my_row = new_row
            self.my_col = new_col

class Neighborhood:
    def __init__(self):
        # Need a "master" window.  tkinter.Tk is a class that makes and 
        # controls an on-screen window for us.
        self.master = tkinter.Tk()
        
        # Make a clock to keep track of how many turns (days) the
        # simulation has run
        self.clock = 0
        
        # Update the window title (at top of window) to show time
        self.master.title("Pandemic Day " + str(self.clock))

        # Create a Canvas object on the window.  The beauty of abstraction
        # is that you don't have to understand what this really means to 
        # be able to use it!  (A "canvas" is an object for putting other
        # visible objects on, so they show up on the screen.)
        self.canvas = tkinter.Canvas(self.master, width=WIDTH*CELL_PIXEL_SIZE, height=HEIGHT*CELL_PIXEL_SIZE)
        self.canvas.pack()

        # A list of people objects
        self.person_list = []
        
        # Create a grid (2-D list) of where the people are
        self.grid = []
        for row in range(HEIGHT):
            self.grid.append([])
            for col in range(WIDTH):
                if random.random() < POPULATION_DENSITY:
                    person = Person(self, row, col)
                    self.grid[row].append(person)
                    self.person_list.append(person)
                else:
                    self.grid[row].append("empty")
        
        # Start off with a handful a "patient zero"s.
        for x in range(STARTING_INFECTED):
            unlucky_person = random.choice(self.person_list)
            unlucky_person.state = "infected"
            unlucky_person.days_left = INFECTION_LENGTH
            
        # A parallel grid (2-D list) for storing "canvas rectangle" objects.
        # Again, you don't need to understand this part very well to use it.
        # It will paint each "cell" on the screen
        self.canvas_grid = []
        for row in range(HEIGHT):
            self.canvas_grid.append([])
            for col in range(WIDTH):
                rectangle = self.canvas.create_rectangle(col*CELL_PIXEL_SIZE,row*CELL_PIXEL_SIZE,\
                    (col+1)*CELL_PIXEL_SIZE,(row+1)*CELL_PIXEL_SIZE, fill="grey", outline="black")
                self.canvas_grid[row].append(rectangle)
        self.canvas.update()

    def update_grid(self):
        # Want to update the people in random order each time.
        # (Otherwise, if they're always getting updated starting in the
        # upper-left corner, they tend to all drift up and to the left over 
        # time.)
        random.shuffle(self.person_list)
        
        # Go through all of the person objects and call their update method.
        # This will check all of the things that can happen to a person
        # (Get better, develop symptoms, die, get infected, move around)
        for p in self.person_list:
            p.update()
    
    def update_canvas_grid(self):
        # This function goes through each entry in the grid (either 
        # the string "empty" or a Person object) and paints the associated
        # cell the correct color based on their status.
    
        for row in range(HEIGHT):
            for col in range(WIDTH):
                if self.grid[row][col] == "empty":
                    color = "black"
                else:
                    state = self.grid[row][col].state
                    if state == "infected":
                        color = "red"
                    elif state == "symptomatic":
                        color = "brown"
                    elif state == "recovered":
                        color = "green"
                    elif state == "dead":
                        color = "yellow"
                    else:
                        color = "white"
                # Now that I know what color, I can update the "rectangle" object
                # I created in the __init__ method to show up that color on 
                # the canvas.  You don't need to understand this part to use it.
                self.canvas.itemconfig(self.canvas_grid[row][col], \
                                  fill=color, outline=color)
        self.canvas.update()

    def update_loop(self):
        # update the clock
        self.clock += 1
        self.master.title("Pandemic Day " + str(self.clock))
        
        # Call the update_grid method to go through each person object and 
        # update their status, move around, etc...
        self.update_grid()
        
        # Setting Screen_update_frequency (at top) to 5 or 10 will make it run
        # (slightly) faster, for large simulations, but then you can't see
        # the daily changes
        if self.clock % SCREEN_UPDATE_FREQUENCY == 0:
            self.update_canvas_grid()
        
        # This function will ask the canvas to call the update_loop function
        # again in 10 milliseconds.  It's a GUI way of entering an infinite 
        # loop.  If you want to exit the program after a while, put this line 
        # in an if statement so that it only runs while the clock is less than
        # some amount, or while there are still infected people, etc...
        self.canvas.after(10, self.update_loop)

# Create the neighborhood (call its init method), which will also create
# the list of Person objects.
n = Neighborhood()

# Call the update_loop function for the first time, which will then take care 
# of scheduling the next update call.
n.update_loop()

# This line asks the Window to enter a "waiting loop", which will wait until 
# you close the application window, allowing on-screen updates to keep 
# occuring until you do.  Without this, the window would update the first
# time, and then exit the program.
tkinter.mainloop()