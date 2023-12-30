#Imports
import pygame
import random
import time
import math
from typing import Callable, Optional, Tuple
from collections import deque

#Objects
class Box:
    def __init__(self, x1: float, y1: float, x2: float, y2: float):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self.width = x2 - x1
        self.height = y2 - y1

    @property
    def top(self) -> float:
        return self.y1

    @property
    def bottom(self) -> float:
        return self.y2

    @property
    def left(self) -> float:
        return self.x1

    @property
    def right(self) -> float:
        return self.x2

    def center(self) -> Tuple[float, float]:
        """Calculates the coordinates of the center of the box"""
        center_x = self.left + self.width / 2
        center_y = self.top + self.height / 2

        return (center_x, center_y)

    def is_inside(self, outer_box: Box, allowed_margin=0.0) -> bool:
        is_within_x = (
            outer_box.left - self.left <= allowed_margin
            and self.right - outer_box.right <= allowed_margin
        )

        is_within_y = (
            outer_box.top - self.top <= allowed_margin
            and self.bottom - outer_box.bottom <= allowed_margin
        )

        return is_within_x and is_within_y

    def intersects_with_point(self, coordinates: Tuple[float, float]):
        other_x, other_y = coordinates
        is_within_x = self.x1 <= other_x <= self.x2
        is_within_y = self.y1 <= other_y <= self.y2
        return is_within_x and is_within_y

    def is_outside(self, other_box: Box) -> bool:
        is_outside_x = self.right < other_box.left or self.left > other_box.right

        is_outside_y = self.bottom < other_box.top or self.top > other_box.bottom

        return is_outside_x or is_outside_y


#Instances
class engine:
    def __init__(self, maxFPS):
        
        #init colours
        self.background_colour = (0, 0, 0)

        #init window
        self.surface = pygame.display.set_mode((1280, 920))
        pygame.display.set_caption('Battleships')

        #init components
        self.maxFPS = maxFPS #Max FPS 
        self.clock = pygame.time.Clock() #Clock instance
        self.exited = False #Exit flag
        self.recent_frame_times = deque(maxlen=10) #Queue of frame times
        self.mode = 0 #0 = menu, 1 = game, 2 = card game
        self.objectsG: list[gameObjects] = [] #List of mage gamemode game objects
        self.objectsM: list[menuObjects] = [] #List of menu objects
        #self.objectsC: list[cardgameObjects] = [] #List of card gamemode objects
    
    #Window properties
    def width(self) -> int:
        return self.surface.get_width()
    def height(self) -> int:
        return self.surface.get_height()
    def box(self) -> Box:
        self.surface.get_rect()

    #Event handlers
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.exited = True
        #TBD key handeling
        #TBD click handeling
    
    #Graphics unit
    def milliseconds_per_frame(self):
        #Returns average time taken to compute, render, and draw the last 10 frames
        times = self.recent_frame_times

        if not len(times):
            # Default to 0 if we haven't recorded any frame times yet
            return 0

        sum = 0
        for time in times:
            sum += time
        average = sum / len(times)
        return average
    
    def execute_gametick(self):
        #Updates state and position of all game objects. Called once per frame
        for event in pygame.event.get():
            self.on_event(event)
    
    def execute_menutick(self):
        #Updates state and position of all menu objects. Called once per frame
        for event in pygame.event.get():
            self.on_event(event)
    
    #def execute_cardtick(self):
    #    #Updates state and position of all card game objects. Called once per frame
    #    for event in pygame.event.get():
    #        self.on_event(event)

    def execute_render(self):
        #Draws all game objects to the screen. Called once per frame
        self.surface.fill(self.background_colour)
        
        if self.mode == 0:
            for obj in self.objectsM:
                obj.draw(self.surface)
        elif self.mode == 1:
            for obj in self.objectsG:
                obj.draw(self.surface)
        elif self.mode == 2:
            for obj in self.objectsC:
                obj.draw(self.surface)
        else:
            print("Invalid mode")

        pygame.display.flip()
    
        
    

        

