#!/usr/bin/python

import argparse
from colorama import Fore, Back

# Scale dictionary
SCALEDICT = {

    'Scale': {
        'Chromatic': '1,b2,2,b3,3,4,b5,5,b6,6,b7,7',
        'Major': '1,2,3,4,5,6,7',
        'Minor Natural': '1,2,b3,4,5,b6,b7',
        'Minor Harmonic': '1,2,b3,4,5,b6,7',
        'Major Pentatonic': '1,2,3,5,6',
        'Minor Pentatonic': '1,b3,4,5,b7',
        'Blues Pentatonic': '1,b3,4,b5,5,b7',
        'Wtf': '1,b2,b3,3,4,5,b6,6,7'
        # 'Wtf': '1,b2,3,4,b5,5,7'
        # '1', '#1', '2', '#2', '3', '4', '#4', '5', '#5', '6', '#6', '7'
    },
    'Mode': {
        'Ionian': '1,2,3,4,5,6,7',
        'Dorian': '1,2,b3,4,5,6,b7',
        'Phrygian': '1,b2,b3,4,5,b6,b7',
        'Lydian': '1,2,3,#4,5,6,7',
        'Mixolydian': '1,2,3,4,5,6,b7',
        'Aeolian': '1,2,b3,4,5,b6,b7',
        'Locrian': '1,b2,b3,4,b5,b6,b7',
        'Phrygian Dominant': '1,b2,3,4,5,b6,b7'
    },
    'Chords': {
        'Major': '1,3,5',
        'Minor': '1,b3,5',
        '7th': '1,3,5,b7',
        'Major 7th': '1,3,5,7',
        'Minor 7th': '1,b3,5,b7',
        '6th': '1,3,5,6',
        'Augmented': '1,3,#5',
        'Diminished': '1,b3,b5'
    }

}


class Doctrina:
    def __init__(self, key, scale, type, notes):

        # Make first letter uppercase
        self.key = key.title()
        self.scale = scale.title()
        self.type = type
        self.notes = notes

    def check_key(self):

        if self.key not in self.notes:
            print('This key no exist in these notes')
            exit()

    def check_scale(self):
        match self.type:
            case 'scale':
                if not SCALEDICT['Scale'].get(self.scale):
                    if SCALEDICT['Mode'].get(self.scale):
                        self.scale = SCALEDICT['Mode'].get(self.scale)
                        return
                    print("Scale not in the list")
                    exit()
                self.scale = SCALEDICT['Scale'].get(self.scale)
            case 'chords':
                if SCALEDICT['Chords'].get(self.scale):
                    self.scale = SCALEDICT['Chords'].get(self.scale)
                    return
                print("Chords not in the list")
                exit()
        return

    def check_bemol(self):

        # Try if we have bemol in key or scale
        for index, item in enumerate(self.notes):
            if self.scale.find('b') >= 0 or self.key.find('b') >= 0:
                if '#' in self.notes[index]:
                    try:
                        self.notes[index] = f'{self.notes[index + 1]}b'
                    except IndexError:
                        self.notes[index] = f'{self.notes[0]}b'

    @staticmethod
    def interval_to_notes(key, scale, notes):

        interval_flat = ['1', 'b2', '2', 'b3', '3', '4', 'b5', '5', 'b6', '6', 'b7', '7']
        interval_sharp = ['1', '#1', '2', '#2', '3', '4', '#4', '5', '#5', '6', '#6', '7']

        interval = interval_sharp
        if scale.find('b') >= 0:
            interval = interval_flat

        conversion = [interval.index(i) for i in scale.split(',')]
        scale_conversion = [(x + notes.index(key)) % 12 for x in conversion]
        return [notes[index] for index in scale_conversion]

    @staticmethod
    def description():
        return 'Doctrina by Lilian Boinard'


class Fretboard:
    def __init__(self, key, notes, scale, tuning, frets):
        self.key = key
        self.notes = notes
        self.scale = scale
        self.tuning = list(tuning)[::-1]
        for index, item in enumerate(self.tuning):
            if item == '#' or item == 'b':
                self.tuning[index + 1] = self.tuning[index + 1] + self.tuning[index]
                self.tuning.pop(index)
        print(self.tuning)
        # We add the empty note
        self.frets = frets + 1
        self.fretboard = None

    def construct(self):

        fretboard = [[i for i in Doctrina.interval_to_notes(item, '1,b2,2,b3,3,4,b5,5,b6,6,b7,7', self.notes)] for item
                     in self.tuning]

        for index, item in enumerate(fretboard):
            notes_to_add_multiplicator = int((self.frets - 11) / 11)
            notes_to_add_modulo = int((self.frets - 11) % 11)
            fretboard[index] += (item * notes_to_add_multiplicator)
            if notes_to_add_modulo > 1:
                fretboard[index] += item[:(notes_to_add_modulo - 2)]
            item.pop(0)

        self.fretboard = fretboard

        return

    def print_scale(self):
        for index, item in enumerate(self.tuning):

            if item in self.scale:
                if item == self.key:
                    string = Back.GREEN + Fore.BLACK + f'{item}' + Back.LIGHTWHITE_EX
                else:
                    string = Back.LIGHTBLUE_EX + Fore.BLACK + f'{item}' + Back.LIGHTWHITE_EX
            else:
                string = Back.LIGHTWHITE_EX + Fore.BLACK + f'{item}'
            if len(item) > 1:
                string += '||'
            else:
                string += ' ||'
            for note in self.fretboard[index]:
                if note not in self.scale:
                    string += f'-----|'
                    continue
                if len(note) > 1:
                    if note == self.key:
                        string += '-(' + Back.GREEN + f'{note}' + Back.LIGHTWHITE_EX + ')|'
                        continue
                    string += '--' + Back.LIGHTBLUE_EX + f'{note}' + Back.LIGHTWHITE_EX + '-|'
                    continue
                if note == self.key:
                    string += '-(' + Back.GREEN + f'{note}' + Back.LIGHTWHITE_EX + ')-|'
                    continue
                string += '--' + Back.LIGHTBLUE_EX + f'{note}' + Back.LIGHTWHITE_EX + '--|'

            string += Back.RESET
            print(string)
        frets_count = [f'{Fore.LIGHTWHITE_EX + str(i) + Back.LIGHTBLACK_EX if i % 2 != 0 and i != 1 else " "}     ' for
                       i in range(0, 10)]
        frets_count += [
            f'{Fore.LIGHTWHITE_EX + str(i) + Back.LIGHTBLACK_EX if i % 2 != 0 and i != 11 and i != 13 or i == 12 else "  "}    '
            for i in range(10, self.frets - 1)]
        frets_count += f'{self.frets}  '
        print(Back.LIGHTBLACK_EX + ''.join(frets_count) + Back.RESET + Fore.RESET)


def main():
    parser = argparse.ArgumentParser(
        description=Doctrina.description(),
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('key', type=str, help='The key')
    parser.add_argument('scale', type=str, help='The scale')
    parser.add_argument('type', type=str, help='scale / chords')
    parser.add_argument('--notes', default=['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'], type=list,
                        help='The notes')
    parser.add_argument('--tuning', '-t', help='String tuning', default='EADGBE', type=str)
    parser.add_argument('--frets', '-f', help='Number of frets (minimum = 12)', default='24', type=int)
    args = parser.parse_args()

    Brain = Doctrina(key=args.key, scale=args.scale, type=args.type, notes=args.notes)

    Brain.check_bemol()
    Brain.check_key()
    Brain.check_scale()
    Brain.scale = Doctrina.interval_to_notes(Brain.key, Brain.scale, Brain.notes)
    
    print(f'Key: {Brain.key}')
    print(f'Scale notes: {Brain.scale}')

    FRETBOARD = Fretboard(key=Brain.key, scale=Brain.scale, notes=Brain.notes, tuning=args.tuning, frets=args.frets)
    FRETBOARD.construct()
    print('\n')
    FRETBOARD.print_scale()


if __name__ == '__main__':
    main()
