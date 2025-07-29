from collections import deque
import pygame
from pygame.locals import *
from enum import Enum
from typing import Callable
from threading import Thread, Lock

LOCK = Lock()

class InputType(Enum):
    BUTTON_DOWN = JOYBUTTONDOWN
    BUTTON_UP = JOYBUTTONUP
    STICK_MOVE = JOYAXISMOTION
    DPAD_MOVE = JOYHATMOTION

class Controller:
    def __init__(self, mapping=None, DEBUG=False):
        self.mapping = {} if mapping is None else mapping
        self.DEBUG = DEBUG
        self._current_events = deque()
        self._values = deque()
    
    def add_mapping(self, input_type: InputType, id: int, callback: Callable):
        self.mapping[(input_type, id)] = callback
        
    def listen(self, controller_number: int):
        thd = Thread(target=lambda: self.__runtime(controller_number), daemon=True)
        thd.start()

    def read(self):
        with LOCK:
            ret = zip(list(self._current_events), list(self._values))
            self._current_events.clear()
            self._values.clear()
            return ret

    def __runtime(self, controller_number: int):
        pygame.init()
        pygame.joystick.init()

        if pygame.joystick.get_count() == 0:
            if self.DEBUG: print("WARNING: No controllers connected.")
            return

        joystick = pygame.joystick.Joystick(controller_number)
        joystick.init()

        if self.DEBUG:
            print(f"Controller Name: {joystick.get_name()}")

        try:
            while True:
                for event in pygame.event.get():
                    key = None
                    if event.type == JOYBUTTONDOWN:
                        key = (InputType.BUTTON_DOWN, event.button)
                        if key in self.mapping:
                            self.mapping[key]()
                        if self.DEBUG:
                            print(f"PRESSED BUTTON {event.button}")
                    elif event.type == JOYBUTTONUP:
                        key = (InputType.BUTTON_UP, event.button)
                        if key in self.mapping:
                            self.mapping[key]()
                        if self.DEBUG:
                            print(f"RELEASED BUTTON {event.button}")
                    elif event.type == JOYAXISMOTION:
                        key = (InputType.STICK_MOVE, event.axis)
                        if key in self.mapping:
                            self.mapping[key](event.value)
                        if self.DEBUG:
                            print(f"MOVED STICK AXIS {event.axis} {event.value}")
                    elif event.type == JOYHATMOTION:
                        key = (InputType.DPAD_MOVE, event.hat)
                        if key in self.mapping:
                            self.mapping[key](event.value)
                        if self.DEBUG:
                            print(f"MOVED HAT {event.hat} {event.value}")
                    if key:
                        with LOCK:
                            self._current_events.append(key)
                            self._values.append(event.value if event.type in {JOYAXISMOTION, JOYHATMOTION} else None)

        except KeyboardInterrupt:
            pass

        finally:
            pygame.joystick.quit()
            pygame.quit()