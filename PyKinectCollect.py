from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime

import ctypes
import _ctypes
import pygame
import sys

import random

if sys.hexversion >= 0x03000000:
    import _thread as thread
else:
    import thread

# colors for drawing different bodies 
SKELETON_COLORS = [pygame.color.THECOLORS["red"], 
                  pygame.color.THECOLORS["blue"], 
                  pygame.color.THECOLORS["green"], 
                  pygame.color.THECOLORS["orange"], 
                  pygame.color.THECOLORS["purple"], 
                  pygame.color.THECOLORS["yellow"], 
                  pygame.color.THECOLORS["violet"]]

# Represents a ball object; derived from the "Sprite" class in PyGame
class Ball(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__() # calls the parent class (Sprite) constructor

        ## TODO: pass the below 2 as arguments for bounds instead
        # ALSO IN PyKinectCollect CLASS
        self._kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body)
        self._frame_surface = pygame.Surface((self._kinect.color_frame_desc.Width, self._kinect.color_frame_desc.Height), 0, 32)
        

        self.image = pygame.Surface([width,height]) # creates a blank image
        self.image.fill((255,255,255)) # white
        self.image.set_colorkey((255,255,255)) # makes background transparent after fill
        ### Note: to use a bit-mapped graphic instead,
        ### self.image = pygame.image.load("example.png").convert()

        # Draw the ellipse
        pygame.draw.ellipse(self.image, color, [0, 0, width, height])

        # Fetch the rectangle object.
        # This rectangle represents the dimesions of the sprite; it has attributes x and y,
        #   so to move this sprite, use `mySprite.rect.x` and `mySprite.rect.y`
        # Update the position of this image by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()

    def update(self):
        # Move ball object down 1 pixel
        self.rect.y += 1
        # If ball disappears at bottom of the screen, re-spawn it at the top
        if self.rect.y > self._frame_surface.get_height():
            self.rect.y = random.randrange(-50, -20)
            self.rect.x = self.rect.x

class PyKinectCollect(object):
    def __init__(self):
        pygame.init()

        # Used to manage how fast the screen updates
        self._clock = pygame.time.Clock()

        # Set the width and height of the screen [width, height]
        self._infoObject = pygame.display.Info()
        self._screen = pygame.display.set_mode((self._infoObject.current_w >> 1, self._infoObject.current_h >> 1), 
                                               pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)

        pygame.display.set_caption("Send help")

        # Loop until the user clicks the close button.
        self._done = False

        # Kinect runtime object, we want only color and body frames 
        self._kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body)

        # back buffer surface for getting Kinect color frames, 32bit color, width and height equal to the Kinect color frame size
        self._frame_surface = pygame.Surface((self._kinect.color_frame_desc.Width, self._kinect.color_frame_desc.Height), 0, 32)

        # here we will store skeleton data 
        self._bodies = None

        #self._randObjects = []

        # List of ball sprite, managed by a class called Group
        # This also holds all the objects that the player can collide with
        self.ballList = pygame.sprite.Group()


    def draw_body_bone(self, joints, jointPoints, color, joint0, joint1):
        joint0State = joints[joint0].TrackingState;
        joint1State = joints[joint1].TrackingState;

        # both joints are not tracked
        if (joint0State == PyKinectV2.TrackingState_NotTracked) or (joint1State == PyKinectV2.TrackingState_NotTracked): 
            return

        # both joints are not *really* tracked
        if (joint0State == PyKinectV2.TrackingState_Inferred) and (joint1State == PyKinectV2.TrackingState_Inferred):
            return

        # ok, at least one is good 
        start = (jointPoints[joint0].x, jointPoints[joint0].y)
        end = (jointPoints[joint1].x, jointPoints[joint1].y)

        try:
            pygame.draw.line(self._frame_surface, color, start, end, 8)
        except: # need to catch it due to possible invalid positions (with inf)
            pass

    def draw_body(self, joints, jointPoints, color):
        # Torso
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_Head, PyKinectV2.JointType_Neck);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_Neck, PyKinectV2.JointType_SpineShoulder);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_SpineMid);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineMid, PyKinectV2.JointType_SpineBase);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_ShoulderRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_ShoulderLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineBase, PyKinectV2.JointType_HipRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineBase, PyKinectV2.JointType_HipLeft);
    
        # Right Arm    
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ShoulderRight, PyKinectV2.JointType_ElbowRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ElbowRight, PyKinectV2.JointType_WristRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristRight, PyKinectV2.JointType_HandRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HandRight, PyKinectV2.JointType_HandTipRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristRight, PyKinectV2.JointType_ThumbRight);

        # Left Arm
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ShoulderLeft, PyKinectV2.JointType_ElbowLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ElbowLeft, PyKinectV2.JointType_WristLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristLeft, PyKinectV2.JointType_HandLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HandLeft, PyKinectV2.JointType_HandTipLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristLeft, PyKinectV2.JointType_ThumbLeft);

        # Right Leg
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HipRight, PyKinectV2.JointType_KneeRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_KneeRight, PyKinectV2.JointType_AnkleRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_AnkleRight, PyKinectV2.JointType_FootRight);

        # Left Leg
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HipLeft, PyKinectV2.JointType_KneeLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_KneeLeft, PyKinectV2.JointType_AnkleLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_AnkleLeft, PyKinectV2.JointType_FootLeft);


    def draw_color_frame(self, frame, target_surface):
        target_surface.lock()
        address = self._kinect.surface_as_array(target_surface.get_buffer())
        ctypes.memmove(address, frame.ctypes.data, frame.size)
        del address
        target_surface.unlock()

    def spawnObjects(self):
        if random.randrange(0, 100) < 1: # 1% chance every frame
            # Randomly spawn up to N objects at frame
            for i in range(1, random.randint(1, 2)):
                # Set random color for object
                color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
                # Set random size
                width = int(self._frame_surface.get_width()) / random.randint(8, 16)
                height = int(self._frame_surface.get_height()) / random.randint(8, 16)

                obj = Ball(color, width, height)
                # Set random starting horizontal location; spawn objects from top
                obj.rect.x = random.randrange(0, int(self._frame_surface.get_width()))
                obj.rect.y = random.randrange(-50, -20)

                # Add to list of objects
                self.ballList.add(obj)

        self.ballList.draw(self._frame_surface)
        self.ballList.update()

        '''
        if random.randrange(0, 100) < 1: # 1% chance every frame
            # Randomly spawn up to N objects at frame
            for i in range(1, random.randint(1, 2)):
                # Set random color for object
                randRGB = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
                # Set random size
                randWidth = int(self._frame_surface.get_width()) / random.randint(8, 16)
                randHeight = int(self._frame_surface.get_height()) / random.randint(8, 16)
                # Set random starting location
                randX = random.randrange(0, int(self._frame_surface.get_width()))
                # TODO: fix height to start at top outside of frame & add gravity for it to drop down
                randY = random.randrange(0, int(self._frame_surface.get_height()))
                randRect = (randX, randY, randWidth, randHeight)

                self._randObjects.append((randRGB, randRect))

        for color, rect in self._randObjects:
            rect.y += 1
            pygame.draw.ellipse(self._frame_surface, color, rect)
        '''

        # TODO delete object condition (reaches bottom of surface)

    def run(self):
        # -------- Main Program Loop -----------
        while not self._done:
            # --- Main event loop
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    self._done = True # Flag that we are done so we exit this loop

                elif event.type == pygame.VIDEORESIZE: # window resized
                    self._screen = pygame.display.set_mode(event.dict['size'], 
                                               pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
                    
            # --- Game logic should go here

            # --- Getting frames and drawing  
            # --- Woohoo! We've got a color frame! Let's fill out back buffer surface with frame's data 
            if self._kinect.has_new_color_frame():
                frame = self._kinect.get_last_color_frame()
                self.draw_color_frame(frame, self._frame_surface)
                frame = None

            self.spawnObjects()

            # --- Cool! We have a body frame, so can get skeletons
            if self._kinect.has_new_body_frame(): 
                self._bodies = self._kinect.get_last_body_frame()

            # --- draw skeletons to _frame_surface
            if self._bodies is not None: 
                for i in range(0, self._kinect.max_body_count):
                    body = self._bodies.bodies[i]
                    if body.is_tracked:
                        joints = body.joints 
                        # convert joint coordinates to color space 
                        joint_points = self._kinect.body_joints_to_color_space(joints)
                        self.draw_body(joints, joint_points, SKELETON_COLORS[i])

            # --- copy back buffer surface pixels to the screen, resize it if needed and keep aspect ratio
            # --- (screen size may be different from Kinect's color frame size) 

            h_to_w = float(self._frame_surface.get_height()) / self._frame_surface.get_width()
            target_height = int(h_to_w * self._screen.get_width())
            #### shows up here
            #### pygame.draw.ellipse(self._frame_surface, (255,0,0), (80, 80, 80, 80), 5)
            surface_to_draw = pygame.transform.scale(self._frame_surface, (self._screen.get_width(), target_height));
            #### disappears here
            #### pygame.draw.ellipse(surface_to_draw, (255,0,0), (80, 80, 80, 80), 5)
            self._screen.blit(surface_to_draw, (0,0))
            surface_to_draw = None
            pygame.display.update()

            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

            # --- Limit to 60 frames per second
            self._clock.tick(60)

        # Close our Kinect sensor, close the window and quit.
        self._kinect.close()
        pygame.quit()


__main__ = "Kinect v2 Body Game"
game = PyKinectCollect();
game.run();

