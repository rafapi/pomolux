#!/usr/bin/env python

'''
Define the interaction with the Luxafor Flag.
Primarly aimed to be used along the pomodory app,
but it can also be used as a standalone app.
'''

import hid
import argparse


class LuxaforDev(object):
    '''
    Contains the functionallity for the Luxafor Flag
    '''

    # Main LED combinations. All performed with fading.
    green = [2, 255, 0, 255, 0, 20, 0]
    red = [2, 255, 255, 0, 0, 20, 0]
    blue = [2, 255, 0, 0, 255, 20, 0]
    orange = [2, 255, 255, 100, 0, 20, 0]
    turn_off = [2, 255, 0, 0, 0, 20, 0]

    def __init__(self):
        self.dev = hid.device(0x04d8, 0xf372)

    def setup_device(self):
        try:
            self.dev.open(0x04d8, 0xf372)
        except OSError as err:
            print('Exiting device with error: {}'.format(err))
        return self.dev

    def write(self, values):
        '''
        Send values to the device.

        - setPattern:
            write([6,PATTERN,REPEAT,0,0,0,0])

        - setWave:
            write([4,WAVE,RED,GREEN,BLUE,0,REPEAT,SPEED])

        - setStrobe:
            write([3,LED,RED,GREEN,BLUE,SPEED,0,REPEAT])

        - setFade:
            write([2,LED,RED,GREEN,BLUE,SPEED,0])

        - setColor:
            write([1,LED,RED,GREEN,BLUE,0,0])

        Examples:
        - Police pattern ([6, 5, 1, 0, 0, 0, 0])
        - Green wave ([4,4,0,255,0,0,1,10])

        '''
        device = self.setup_device()
        device.write(values)
        device.close()

    def off(self):
        '''
        Turn off all LEDs
        '''
        self.write(self.turn_off)

    def work(self):
        self.write(self.red)

    def rest(self):
        self.write(self.orange)

    def long_rest(self):
        self.write(self.green)

    commands = {
            'off': off,
            'work': work,
            'rest': rest,
            'long_rest': long_rest
            }

    @staticmethod
    def command_line_parser():
        parser = argparse.ArgumentParser(
                description='Luxafor Flag controller',
                conflict_handler='resolve')
        parser.add_argument(
                'mode', help='Flag colour. It represents the busy state',
                choices=['work', 'rest', 'long_rest', 'off'])
        parser.add_argument(
                '-m', '--minutes', '--min', type=int,
                help='additional amount of minutes to wait for')
        parser.add_argument(
                '-h', '--hours', type=int,
                help='additional amount of hours to wait for')
        return parser

    def select_args(self, arg):
        if arg in self.commands:
            func = self.commands[arg]
            func(self)


if __name__ == '__main__':
    luxdev = LuxaforDev()
    arg = luxdev.command_line_parser().parse_args()
    arg = arg.mode
    luxdev.select_args(arg)
