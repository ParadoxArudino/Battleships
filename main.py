#Imports
import pygame
import random
import time
import math
from typing import Callable, Optional, Tuple
from collections import deque

from simple_objects import *
from game_objects import *
from menu_objects import *
from utils import *

class Engine:
    def __init__(self, maxFPS):
        
        #init colours
        self.background_colour = (0, 0, 0)
        
        #init window
        self.surface = pygame.display.set_mode((1280, 920), pygame.RESIZABLE)
        pygame.display.set_caption('Battleships')

        #init runtime variables
        self.maxFPS = maxFPS #Max FPS 
        self.clock = pygame.time.Clock() #Clock instance
        self.startTime = time.time() #Start time
        self.runTime = 0 #Run time
        self.frameCount = 0 #Frame count
        self.exited = False #Exit flag
        self.recent_frame_times = deque(maxlen=10) #Queue of frame times

        #init objects
        self.mode = 0 #0 = menu, 1 = game, 2 = card game
        self.objectsG: list[GameObject] = [] #List of mage gamemode game objects
        self.objectsM: list[MenuObject] = [] #List of menu objects
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

        if self.frameCount % 60 == 0: #Every second, update the background colour to a random colour
            self.background_colour = RandColour()
            print("FPS: " + str(self.clock.get_fps()))
    
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

    def run(self):
        #Main loop
        while not self.exited:
            self.clock.tick(self.maxFPS)
            self.recent_frame_times.append(self.clock.get_time())
            self.runTime = time.time() - self.startTime
            self.frameCount += 1

            if self.mode == 0:
                self.execute_menutick()
            elif self.mode == 1:
                self.execute_gametick()
            #elif self.mode == 2:
            #    self.execute_cardtick()
            else:
                print("Invalid mode")
            self.execute_render()
        
        pygame.quit()
    
instance = Engine(60)
instance.run() 