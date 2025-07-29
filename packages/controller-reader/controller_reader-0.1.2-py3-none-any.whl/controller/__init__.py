import pygame
from pygame.locals import *
from enum import Enum
from typing import Callable
from threading import Thread

class InputType(Enum):
    BUTTON_DOWN = JOYBUTTONDOWN
    BUTTON_UP = JOYBUTTONUP
    STICK_MOVE = JOYAXISMOTION
    DPAD_MOVE = JOYHATMOTION

class Controller:
    def __init__(self, mapping:dict[tuple[InputType, int], Callable[[float|tuple[int, int]], None]|Callable[[], None]]|None = None, DEBUG:bool = False):
        self.mapping = {} if mapping is None else mapping
        self.DEBUG = DEBUG
        self._current_events:list[tuple[InputType, int]] = []
        self._values = []
    
    def add_mapping(self, input_type:InputType, id:int, callback:Callable[[float|tuple[int, int]], None]|Callable[[], None]):
        self.mapping[(input_type, id)] = callback
        
    def listen(self, controller_number:int):
        thd = Thread(target=lambda:self.__runtime(controller_number), daemon=True)
        thd.start()

    def consume_events(self):
        ret = self._current_events
        self._current_events = []
        return ret
    
    def consume_values(self):
        ret = self._values
        self._values = []
        return ret

    def __runtime(self, controller_number:int):
        # Initialize pygame
        pygame.init()

        # Initialize the joystick module
        pygame.joystick.init()

        # Check if any controllers are connected
        if pygame.joystick.get_count() == 0:
            if self.DEBUG:print("WARNING: No controllers connected.")
            return

        # Get the first connected joystick
        joystick = pygame.joystick.Joystick(controller_number)
        joystick.init()

        # Print controller information
        if self.DEBUG:
            print(f"Controller Name: {joystick.get_name()}")
            print(f"Number of Axes: {joystick.get_numaxes()}")
            print(f"Number of Buttons: {joystick.get_numbuttons()}")
            print(f"Number of Hats: {joystick.get_numhats()}")


        try:
            while True:
                # Process events
                key = None
                for event in pygame.event.get():
                    if event.type == JOYBUTTONDOWN:
                        key = (InputType.BUTTON_DOWN, event.button)
                        if key in self.mapping:
                            self.mapping[key]()
                        if self.DEBUG:
                            print(f"PRESSED BUTTON {event.button}")
                    elif event.type == JOYBUTTONUP:
                        key = (InputType.BUTTON_UP, event.button)
                        if key in self.mapping:
                            self.mapping[(InputType.BUTTON_UP, event.button)]()
                        if self.DEBUG:
                            print(f"RELEASED BUTTON {event.button}")
                    elif event.type == JOYAXISMOTION:
                        key = (InputType.STICK_MOVE, event.axis)
                        if key in self.mapping:
                            self.mapping[(InputType.STICK_MOVE, event.axis)](event.value)
                        if self.DEBUG:
                            print(f"MOVED STICK AXIS {event.axis} {event.value}")
                        self._values.append(event.value)
                    elif event.type == JOYHATMOTION:
                        key = (InputType.STICK_MOVE, event.hat)
                        if key in self.mapping:
                            self.mapping[(InputType.STICK_MOVE, event.hat)](event.value)
                        if self.DEBUG:
                            print(f"MOVED HAT {event.hat} {event.value}")
                        self._values.append(event.value)
                    if key:
                        self._current_events.append(key)
                

        except KeyboardInterrupt:
            pass

        finally:
            # Clean up
            pygame.joystick.quit()
            pygame.quit()