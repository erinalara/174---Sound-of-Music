# Erina Lara
# 018182630
# Homework 3 - Sound of Music

import musicbox  # Imports musicbox

my_music = musicbox.MusicBox()  # Assigns my_music to musicbox

NOTES = [("C", 60), ("D", 62), ("E", 64), ("F", 65), ("G", 67), ("A", 69), ("B", 71)]
# Tuple of notes with their given MIDI value
MAJOR_INTERVALS = [2, 2, 1, 2, 2, 2, 1]  # List of major intervals, 7 integers
MINOR_INTERVALS = [2, 1, 2, 2, 1, 2, 2]  # List of minor intervals, 7 integers


def note_to_int(note):  # Converts note (letter) to their integer/midi value (integer)
    added_value = 0  # Gives total value of add-ons, meaning if there is a flat (b) or # or ^ (octave)
    total_integer = 0  # Gives total note value
    octave = 12  # An octave is 12 notes higher
    for i in range(len(note)):  # Scans note
        if "^" in note:
            added_value = ((note.rfind("^") + 1) * octave)  # 1 is added to note.rfind because the index starts at 0
        if "b" == note[i]:
            added_value -= 1  # Decrements 1 from MIDI value of note because of the flat (b)
        if "#" == note[i]:
            added_value += 1  # Increments 1 to MIDI value of note because of the #
        if note[i].isalpha() is False and note[i] != '^' and note[i] != 'b' and note[i] != '#':
            total_integer = -1  # Total note value is assigned -1, which means invalid, IF has invalid char/not alpha

    for i in range(len(NOTES)):  # Scans notes list, NOTE: NOTES[i] = (Letter, midi integer)
        note_letters, midi = NOTES[i]  # Assigns note_letters to first value in NOTES[i]
        #  and assigns midi integer to second value in NOTES[i]
        if note_letters in note and total_integer != -1:        # If user note is in NOTE list; is valid
            total_integer = midi + added_value      # Variable added_value is added to midi/note integer value for total
    if total_integer == 0:  # If letter is not a valid note, returns -1
        total_integer = -1

    return total_integer


def print_menu():  # Prints menu
    print("Main menu: \n1. Play scale \n2. Play song \n3. Quit")


def get_menu_choice():  # Gets menu choice from user
    user_choice = 0     # User choice
    while user_choice != 1 and user_choice != 2 and user_choice != 3:   # Validates user choice
        user_choice = int(input("Please enter a selection: "))
    return user_choice


def get_scale():  # Gets scale choice from user
    scale_choice = ' '  # Sets scale_choice as a string
    integer_value = -1  # Sets initial integer value as -1 (invalid)
    scale_split = ''  # Sets scale split as string
    while (integer_value == -1) or ("major" not in scale_choice and "Major" not in scale_choice and
                                    "Minor" not in scale_choice and "minor" not in scale_choice):
        scale_choice = input("Please enter a scale: ")  # Validates user choice to ensure 'major' or 'minor'
        if " " not in scale_choice:  # If 'major' or 'minor' not in choice -> loops
            integer_value = -1
        else:  # Checks if note is valid by calling note_to_int
            scale_split = scale_choice.split(" ")
            note_letter = str(scale_split[0])
            integer_value = note_to_int(note_letter)  # If -1 is returned, user choice is invalid -> loops

    scale = scale_split[1]  # Gives word; either 'major' or 'minor'
    choice = (integer_value, scale)  # Stores tuple in variable choice
    return choice  # Returns scale choice as tuple


def scale_to_ints(scale):  # Converts scale to integers
    notes_list = [scale[0]]  # Notes list is assigned as a list, with the scale note in first position

    if scale[1] == 'major' or scale[1] == 'Major':  # Path for a major scale
        for i in range(len(MAJOR_INTERVALS)):  # MAJOR_INTERVALS = [2, 2, 1, 2, 2, 2, 1]
            initial = notes_list[i]     # Initial value is set to the value of notes_list[i]
            if initial < notes_list[i]:     # Makes sure that next note is calculated based off the integer before it
                initial = scale[0] + MAJOR_INTERVALS[i]     # Increments initial by major interval value
            notes_list.append(initial + (MAJOR_INTERVALS[i]))   # Appends notes_list
        return notes_list   # Returns list of notes as integers

    elif scale[1] == 'minor' or scale[1] == 'Minor':  # Path for a minor scale
        for i in range(len(MINOR_INTERVALS)):  # MINOR_INTERVALS = [2, 1, 2, 2, 1, 2, 2]
            initial = notes_list[i]         # Initial value is set to the value of notes_list[i]
            if initial < notes_list[i]:     # Makes sure that next note is calculated based off the integer before it
                initial = scale[0] + MINOR_INTERVALS[i]     # Increments initial by minor interval value
            notes_list.append(initial + (MINOR_INTERVALS[i]))       # Appends notes_list
        return notes_list       # Returns list of notes as integers


def menu_play_scale():      # Plays scale
    a = get_scale()         # Calls get scale, returns list of note integers in variable a
    play = scale_to_ints(a)     # Calls scale_to_ints
    for i in range(len(play)):
        my_music.play_note(play[i], 500)


def get_song_file():    # Gets song name
    user_song = input("Enter the song file name: ")         # Gets user input for song file name
    return user_song         # Returns user_song as string


def play_song(file_name):       # Plays song
    for line in open(file_name):  # Scans lines in text file
        if '//' in line:        # If line has '//', ignores line and continues
            continue
        line_split = line.split(" ")    # splits line at space

        if len(line_split) > 2:  # is a chord when it has more than 2 values (ex. [G,A,Bb,400] has length 4)
            chord_list = []  # Chord is set as empty list
            time = 0        # Sets initial time as 0
            for i in range(len(line_split)):        # Scans line_split list, from 0 to len of line
                time = int(line_split[-1])          # Sets time equal to last value in line_split list
                if line_split[i] != line_split[-1]:        # Ensures that time is not called/ run through
                    letter = line_split[i]                  # Sets letter of note equal to line_split[i]
                    note_integer = note_to_int(letter)     # Calls note_to_int of letter and stores integer
                    chord_list.append(note_integer)         # Appends note_integer to chord list

            my_music.play_chord(chord_list, time)   # Plays chord

        elif len(line_split) == 2:  # Single note if has 2 values (ex. length of [Ab,500] is 2)
            letter = line_split[0]    # First value is set as letter
            duration = int(line_split[1])   # Time duration is set as an integer of the value in the second position
            # (bc it's initially a string)
            if letter == 'P':       # Letter is a Pause, calls musicbox's pause function
                my_music.pause(duration)
            elif letter == 'I':     # Letter means Instrument change, changes instrument through musicbox
                instrument = duration       # Duration value is equal to instrument number
                my_music.change_instrument(instrument)
            else:
                midi_value = note_to_int(letter)    # Calls note_to_int to convert note to MIDI
                my_music.play_note(midi_value, duration)    # Plays note/integer


def menu_play_song():   # Plays selected song
    song = get_song_file()  # Calls song_file to get user song choice
    play_song(song)         # Calls play_song to play song


def main():         # Main function
    x = 0           # X initially set to 0 to loop
    while x != 3:   # Loops until x = 3, if x = 3, program quits
        print_menu()
        x = get_menu_choice()
        if x == 1:          # Initiates option 1, scale
            menu_play_scale()
        elif x == 2:        # Initiates option 2, song
            menu_play_song()


main()
my_music.close()
