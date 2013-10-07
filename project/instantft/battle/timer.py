# coding: utf-8 
from __future__ import division
import numpy

class Train(object):
    def __init__(self, distance, speed, rounds):
        """
        """

        self.stations = numpy.ceil(distance / (speed / rounds))
        self.locus = 0

    def move(self):
        """
        """

        self.locus += 1

        return self.locus >= self.stations

    def stop(self):
        """

        """

        return self.locus >= self.stations

class Lateral(object):
    def __init__(self, distance, speed, rounds, face_to):
        self.step = numpy.ceil(speed / rounds)
        self.distance = numpy.ceil(distance)
        self.face_to = face_to
        self.locus = 0
        
    def move(self):
        """
        """

        locus = self.locus + self.step
        diff = max(min(locus - self.locus, self.distance), 0)
        self.locus = locus
        self.distance -= self.step

        moves = []
        quot, rem = divmod(diff, 3)
        
        step = quot * 3

        if step:
            moves.append((step, step * self.face_to))

        if rem:
            moves.append((rem, rem * self.face_to))

        return moves

    def stop(self):
        """
        """

        return self.distance <= 0

class Meteor(object):
    def __init__(self, speed, rounds):
        """
        """

        self.step = speed / rounds
        self.speed = speed
        self.rounds = rounds
        self.counter = 0
        self.line = 0
        self.locus = 0

    def across(self):
        """
        """

        self.line += self.step
        new_line = numpy.ceil(self.line)
        moves = 0

        if new_line <= self.speed:
            moves = new_line - self.locus

        self.counter += 1

        return moves

    def is_die(self):
        """
        """

        return self.counter > self.rounds

class MoveRound(object):
    def __init__(self, speed, rounds):
        self.speed = speed
        self.rounds = rounds
        self.step = speed / rounds
        self.init()

    def init(self):
        self.locus = 0
        self.offset = 0
        self.prev = 0
        self.value = numpy.floor(self.locus + self.step)
        self.counter = 0

    def move(self):
        """
        """

        return max(self.value - self.prev, 0)

    def moved(self, line, moves):
        if len(line) != moves:
            return 0

        self.locus += self.step
        self.prev = self.value
        self.value = numpy.floor(self.locus + self.step)
        self.counter += 1

        return 1

class AttackRound(object):
    def __init__(self, speed, rounds):
        """
        """

        self.raw_rounds = rounds / speed
        self.step = speed / rounds
        self.rounds = numpy.ceil(self.raw_rounds)
        self.offset = self.rounds - self.raw_rounds
        self.counter = 1
        self.cd_counter = 1
        self.status = True

    def init(self):
        """
        """

        if self.counter == self.rounds:
            self.rounds = numpy.ceil(self.raw_rounds - self.offset)
        else:
            self.rounds = numpy.ceil(self.raw_rounds)

        self.counter = 1
        self.cd_counter = 1
        self.status = True
        self.offset = self.rounds - self.raw_rounds

    def circle(self, attacked):
        """
        """

        init = attacked and self.cd_counter >= self.rounds
        status = False

        if init:
            self.init()
            status = True
        elif attacked:
            self.cd_counter += 1
            self.status = False

        self.counter += 1

        return status

    def able_to(self):
        """
        """

        return self.status

if __name__ == "__main__":
    mvround = MoveRound(3, 10)
    print mvround.move()
    print mvround.move()
    print mvround.move()
    print mvround.move()
    print mvround.move()
    print mvround.move()
    print mvround.move()
    print mvround.move()
    print mvround.move()
    print mvround.move()
    print mvround.move()
