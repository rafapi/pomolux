#!/usr/bin/env python
'''
Pomodoro timer.

The program is invoked with a "work duration", a "rest duration",
the "number of cycles" and a "long rest duration".
It plays a random playlist from `musicforprogramming` (or a ticking
sound if we are offline) for the work duration (specified in minutes)
and then an alarm. After that it plays another tick for the `rest`
duration (also specified in minutes). This is done for a number of
cycles and at the end a default track is played for the long rest
duration (also specified in  minutes) to mark the end of the work cycle.

If the `pync` library is available, it will use it to display messages
on the screen. Otherwise, it simply prints them out to stdout.

The Luxafor Flag, if present, will be used aligned with the 'busy state'.

Type ./pomodoro --help for useage instructions

For details on the Pomodoro technique refer http://www.pomodorotechnique.com/
'''

import argparse
import feedparser
import os
import random
import socket
import subprocess
import sys

from simple_timer import countdown_timer as timer

try:
    from python_luxafor import LuxaforDev
except ImportError:
    has_luxafor = False
else:
    has_luxafor = True

try:
    from pync import Notifier
except ImportError:
    has_pync = False
else:
    has_pync = True


workdir = os.getcwd()
audiodir = workdir + '/' + 'audio'
work_tick = audiodir + '/' + 'clock-ticking-4.mp3'
rest_tick = audiodir + '/' + 'clock-ticking-5.mp3'
cycle_end = audiodir + '/' + 'relax_sequence.mp3'
alarm_cycle = audiodir + '/' + 'game-sound-correct.mp3'
alarm_end = audiodir + '/' + 'game-sound-incorrect.mp3'
dev_null = subprocess.DEVNULL


def is_reachable(url):
    try:
        host = socket.gethostbyname(url)
        socket.create_connection((host, 80), 2)
        return True
    except socket.error:
        pass
        return False


def select_music():
    url = 'musicforprogramming.net'
    feed_url = 'http://' + url + '/' + 'rss.php'
    if is_reachable(url):
        feed = feedparser.parse(feed_url)
        playlist = feed.entries[random.randint(0, len(feed.entries)-1)].id
        return playlist
    else:
        return work_tick


def notify(title, content, force=False):
    if not has_pync or force:
        sys.stdout.write(str(content)+"\n")
    else:
        Notifier.notify(content, title=title)


def play_track(track, duration=None, repeat='-1'):
    "Plays a `track` for a `duration` amount of time"
    cmd = ["mpg123", "-b", "2048", "--loop", repeat, track]
    try:
        proc = subprocess.Popen(
                cmd, stdout=dev_null, stderr=subprocess.STDOUT)
        if duration:
            timer(duration)
        else:
            proc.wait()
    except subprocess.TimeoutExpired:
        pass
    except OSError as err:
        print(err)
    except KeyboardInterrupt:
        notify('Pomodoro', 'Interrupting')
    proc.kill()


def use_luxafor(mode):
    if has_luxafor:
        lux = LuxaforDev()
        if mode in lux.modes:
            led_mode = lux.modes[mode]
            lux.select_led_mode(led_mode)
    else:
        print('No Luxafor')
        pass


def pomodoro(**args):
    use_luxafor('off')
    twork, trest, long_rest, repeat = (
            args['w']*60, args['r']*60, args['l']*60, args['n'])
    notify('Banner', 'Note: press `s` to mute/unmute', force=True)
    for _ in range(repeat-1):
        notify('Pomodoro', 'Work now')
        use_luxafor('work')
        play_track(select_music(), twork)
        play_track(alarm_cycle, repeat='1')
        notify('Pomodoro', 'Rest now')
        use_luxafor('rest')
        play_track(rest_tick, trest)
        play_track(alarm_cycle, repeat='1')
    notify('Pomodoro', 'Work now')
    use_luxafor('work')
    play_track(select_music(), twork)
    play_track(alarm_cycle, repeat='1')
    notify('Pomodoro', 'Rest now')
    use_luxafor('rest')
    play_track(cycle_end, long_rest)
    play_track(alarm_end, repeat='1')
    notify('Pomodoro', 'Cycle complete', force=True)
    use_luxafor('long_rest')
    return 0


def cli_parser():
    parser = argparse.ArgumentParser(
            description='Pomodoro timer (Music from musicforprogramming.net)',
            conflict_handler='resolve',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-w', type=int, default=25,
                        help='Work time in minutes')
    parser.add_argument('-r', type=int, default=5,
                        help='Rest time in minutes')
    parser.add_argument('-l', type=int, default=20,
                        help='Long rest time in minutes')
    parser.add_argument('-n', type=int, default=4,
                        help='Numer of cycles')

    return parser


if __name__ == "__main__":
    args = cli_parser().parse_args()
    pomodoro(**vars(args))
