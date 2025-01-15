def generate_combinations(n, k):
    def backtrack(current, ones):
        if len(current) == n:
            if ones == k:
                result.append(current)
            return
        backtrack(current + '0', ones)
        backtrack(current + '1', ones + 1)

    result = []
    backtrack('', 0)
    return result

def normalize_bit_string(bit_string):
    # Convert bit_string to a list for easier manipulation
    bit_list = list(bit_string)
    # Find the lexicographically largest rotation
    largest_rotation = max(bit_list[i:] + bit_list[:i] for i in range(len(bit_string)))
    return ''.join(largest_rotation)

def remove_rotated_bit_strings(bit_strings):
    seen = set()
    unique_bit_strings = []
    for bit_string in bit_strings:
        normalized = normalize_bit_string(bit_string)
        if normalized not in seen:
            seen.add(normalized)
            unique_bit_strings.append(bit_string)
    return sorted(unique_bit_strings)

# Create combinations for 8 notes witihin chromatic scale
n = 12
k = 8
combinations = sorted(generate_combinations(n, k))

print(len(combinations),"combinations")
unique_combinations = sorted(remove_rotated_bit_strings(combinations))
print(len(unique_combinations), "unique combinations")

# generate "upper" and "lower" constructor chords
# currently the rule is: 
# - assign notes in an alternating way to upper and lower constructor
# - this is consistent with Barry Harris' use of them
#
# Note though that one could choose other constructors, e.g. by using two maj7 chords one whole tone shifted
# or two dom7 chords a fifth apart.

def generate_U_L(A):
    U = ['0'] * len(A)
    L = ['0'] * len(A)
    u_assigned = False  # Flag to track if U has been assigned a 1
    
    for i in range(len(A)):
        if A[i] == '1':
            if not u_assigned:
                U[i] = '1'
                u_assigned = True
            else:
                L[i] = '1'
                u_assigned = False  # Reset for next 1
    
    return ''.join(U), ''.join(L)

U_list = []
L_list = []

for A in unique_combinations:
    U,L = generate_U_L(A)
    U_list.append(U)
    L_list.append(L)
    print(f"A: {A}, U: {U}, L: {L}")
    assert int(U, 2) | int(L, 2) == int(A, 2)

U_unique_list = sorted(list(set(U_list)))
L_unique_list = sorted(list(set(L_list)))

print(U_unique_list)
print(L_unique_list)

# create list of unique constructor chords
U_unique_list.extend(L_unique_list)
constructor_chords = remove_rotated_bit_strings(U_unique_list)

for i in range(0,len(constructor_chords)):
    a = constructor_chords[i]
    while a[0] == '0':
        a = a[1:] + a[:1]
    constructor_chords[i] = a
  
print("All constructor chords:", constructor_chords)

note_names = ["C", "C#/Db", "D", "D#/Eb", "E", "F", "F#/Gb", "G", "G#/Ab", "A", "A#/Bb", "B"]

# common chord types
common_chords = [
        [ "major triad", "100010010000" ],
        [ "major7",      "100010010001" ],
        [ "dominant7",   "100010010010" ],
        [ "dom7/b9",     "110010010010" ],
        [ "dom7/#9",     "100110010010" ],
        [ "dom7sus4",    "100001010010" ],
	[ "dom7/11",     "100011010010" ],
	[ "5 add7/11",   "100001010010" ],
        [ "major9",      "101010010001" ],
        [ "major add9",  "101010010000" ],
        [ "dom9",        "101010010010" ],
        [ "major11",     "101011010001" ],
        [ "major add11", "100011010000" ],
        [ "major7/11",   "100011010001" ],
        [ "major7/#11",  "100010110001" ],
        [ "major6",      "100010010100" ],
        [ "dom13",       "101010010110" ],
        [ "dom7add13",   "100010010110" ],
	[ "lydian", 	 "100000110000" ],
	[ "lydian maj7", "100000110001" ],
	[ "lydian 9",    "101000110001" ],

        [ "minor triad", "100100010000" ],
	[ "minor6", 	 "100100010100" ],
        [ "minor7",      "100100010010" ],
        [ "minor7b9",    "110100010010" ],
        [ "minor9",      "101100010010" ],
	[ "minor b9", 	 "110100010010" ],
	[ "minor add9",  "101100010000" ],
	[ "minor11",     "101101010010" ],
	[ "minor7add11", "100101010010" ],
	[ "minor add11", "100101010000" ],
	[ "min add9/11", "101101010000" ],
	[ "min maj7",	 "100100010001" ],
	[ "min maj9", 	 "101100010001" ],
	[ "min maj11", 	 "101101010001" ],

	[ "dim triad", 	 "100100100000" ],
	[ "diminished7", "100100100100" ],
	[ "min7b5",	 "100100100010" ],
	[ "diminished b6", "100100101000" ],

	[ "augmented",   "100010001000" ],
	[ "aug m7", 	 "100010001010" ],
	[ "aug maj7",	 "100010001001" ],
	[ "aug 6",       "100010001100" ],
	[ "aug 9",       "101010001001" ],

	[ "sus2",	 "101000010000" ],
	[ "sus4", 	 "100001010000" ]
    ]


def find_chord_names (pattern):
    # across all pattern rotations
    namelist = [] 
    for j in range(0, len(str(pattern))):
        # compare to all common chords
        for i in range(0, len(common_chords)):
            if pattern[j:] + pattern[:j] == common_chords[i][1]:
                namelist.append(note_names[j] +" "+ common_chords[i][0])
    return namelist




# print notation for all constructor chords
print ("-----------------------------")
# for all constructor chords in order 
for c in range(0, len(constructor_chords)): 
    print(c, "-", constructor_chords[c], ":")
    # print note names for canonical chord
    for i in range(0,len(note_names)):
        if constructor_chords[c][i] == '1':
            print (note_names[i],end="\t")
    print ()
    chordnames =print (find_chord_names(constructor_chords[c]))
    print ("-----------------------------")









