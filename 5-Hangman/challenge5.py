# IT  DOES NOT WORD........
import sys
import telnetlib

words = [ w.replace('\n', '') for w in open('words.txt', 'r').readlines()]
outputfile = open(sys.argv[1], 'w')

hostname, port = "52.49.91.111", "9988"
session = telnetlib.Telnet(hostname, port=port)

# Congratulations, Noob!
#
# Your test key is: 9cb4afde731e9eadcda4506ef7c65fa2
# Get ready for next level!
#
# Well done!
#
#     O/
#    /|
#    / \
#
#
# M A N I A
#
# Get ready for next level!
#
#


def current_state(data):
    print(data)
    index1 = data.index('|\\n\\n')+5
    index2 = index1+data[index1:].index('\\n\\n>')
    return data[index1:index2].split(' ')

def get_known_chars(word):
    chars = []
    for ind, a_char in enumerate(word):
        if a_char != '_':
            chars.append((ind, a_char))
    return chars

def get_possible_words(case, discarted):
    known_chars = get_known_chars(case)
    compatible_words = []
    # char_discarted = list(discarted)
    for a_word in words:
        could_be = True
        for a_discarted in discarted:
            if a_discarted.upper() in a_word:
                could_be = False
        if could_be and len(a_word)==len(case.replace(' ', '')):
            for i,char in known_chars:
                if a_word[i] != char:
                    could_be = False
                    break
            if could_be:
                compatible_words.append(a_word)
    return compatible_words

# data = session.read_very_eager()
# session.write(b'a')

def play_round():
    possible_words = []
    discarting = ''
    first_attempts = ['e', 'a', 'o', 's', 'm', 'c', 'i', 'u']
    output = str(session.read_very_eager())
    session.write(b'\\n')
    print(output)
    last_char = None
    while 'GAME OVER' not in output or last_char == None or 'Congratulations' not in output:
        output = str(session.read_very_eager())
        outputfile.write(output)
        outputfile.write('\n---------------------------\n')
        print(output)
        the_word = current_state(output)
        if last_char not in the_word and last_char != None:
            discarting += last_char
        n_char = len(the_word)
        known_chars = get_known_chars(the_word)
        if len(known_chars) <= 2:
            #attempting characters
            last_char = first_attempts.pop(0)
            session.write(bytes(char, 'utf8'))
        else:
            possible_words = get_possible_words(the_word, discarting)
            session.write(bytes(possible_words[0], 'utf8'))
#
# n_case = 0
# for line in path:#sys.stdin:
#     if n_case != 0:
#
#
#         output.write('Case #{}: {:0d}\n'.format(n_case, tables))
#     n_case += 1
#
# path.close()
# output.close()
# session.close()
