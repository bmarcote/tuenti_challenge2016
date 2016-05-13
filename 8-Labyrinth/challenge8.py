# IT  DOES NOT WORD........
import sys
import telnetlib

outputfile = open(sys.argv[1], 'w')

hostname, port = "52.49.91.111", "1986"
session = telnetlib.Telnet(hostname, port=port)

#| The Labyrinth:
#|  # #####
#|  #   #
#|  ##  # #
#|  # #x#
#|  # # ###
#|  #   # #
#|  ##### #

# Two states: # (wall)  or ' ' (corridor)
# the objective: x
def play_round():
    lab = str(session.read_very_eager())[2:-1] # deleting chars from conversion
    labyrinth = []
    rows = lab.split('\\n')
    if rows[-1] == '':
        rows = rows[:-1]
    for a_row in rows:
        labyrinth.append(list(a_row))

    # let's find the x!!!
    session.write(bytes(find_x(labyrinth)))
    # session.write(b'\\n')



session.close()
