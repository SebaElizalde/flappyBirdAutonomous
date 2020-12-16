import numpy as np
import pygame

from agent import Agent

bird = pygame.Rect(105, 245, 50, 50)
wallWidth = 98
wallHeight = 500
gap = 130
wallx = 100
offset = 130

agent = Agent()
positions = np.array([
    [wallx,
     290 + gap - offset + 10,
     wallWidth - 10,
     wallHeight
     ],
    [wallx,
     0 - gap - offset - 10,
     wallWidth - 10,
     wallHeight
     ],
    [
        bird[0],
        bird[1],
        bird[2],
        bird[3]
    ]
])