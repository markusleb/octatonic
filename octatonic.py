def generate_combinations(n, k):
    def cross_sum (bit_string):
        cs = 0
        for j in range(len(bit_string)):
            if bit_string[j] == '1':
                cs += 1
        return cs

    result = []
    for i in range(2**n):
        b_string_size_n = str(bin(i)[2:].zfill(n))
#        print ("checking",i, b_string_size_n, end="")
        if cross_sum(b_string_size_n)==k:
            result.append(b_string_size_n)
#            print(" *")
#        else:
#            print("")
    return result


def normalize_bit_string(bit_string):
    # convert to int value
    value = int(bit_string, base=2)
    # find largest rotated value
    largest_rotation = max(int(bit_string[i:]+bit_string[:i], base=2) for i in range(len(bit_string)))
    return str(bin(largest_rotation))[2:]
    
def remove_rotated_bit_strings(bit_strings):
    seen = set()
    unique_bit_strings = []
    for bit_string in bit_strings:
        normalized = normalize_bit_string(bit_string)
        if normalized not in seen:
            seen.add(normalized)
            unique_bit_strings.append(normalized)
    return sorted(unique_bit_strings)

# Create combinations for 8 notes witihin chromatic scale
n = 12
k = 8
combinations = sorted(generate_combinations(n, k))

print ("Summary:")
print ("\t", len(combinations),"combinations")
unique_combinations = sorted(remove_rotated_bit_strings(combinations))
print ("\t", len(unique_combinations), "unique combinations")

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
Scale_list = []

print ("\n\n=====================================================\nAll Scale Patterns with upper and lower constructor chords:\n")

for A in unique_combinations:
    U,L = generate_U_L(A)
    Scale_list.append(A)
    U_list.append(U)
    L_list.append(L)
    print(f"A: {A}, U: {U}, L: {L}")
    assert int(U, 2) | int(L, 2) == int(A, 2)

U_unique_list = sorted(list(set(U_list)))
L_unique_list = sorted(list(set(L_list)))

print ("\nUnique upper constructor chords:\n",U_unique_list)
print ("\nUnique lower constructor chords:\n",L_unique_list)

# create list of unique constructor chords
U_unique_list.extend(L_unique_list)
constructor_chords = remove_rotated_bit_strings(U_unique_list)

def remove_trailing_zero_rotate(pattern):
    a = pattern
    while a[0] == '0':
        a = a[1:] + a[:1]
    return a;

for i in range(0,len(constructor_chords)):
    constructor_chords[i] = remove_trailing_zero_rotate(constructor_chords[i])

print("\nAll constructor chords combined:\n", constructor_chords, "\n")

note_names = ["C", "C#/Db", "D", "D#/Eb", "E", "F", "F#/Gb", "G", "G#/Ab", "A", "A#/Bb", "B"]
simple_note_names = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]



# common chord types
common_chords = [
        [ "major",       "100010010000" ],
        [ "major7",      "100010010001" ],
        [ "dominant7",   "100010010010" ],
        [ "dom7/b9",     "110010010010" ],
        [ "dom7/#9",     "100110010010" ],
        [ "dom7sus4",    "100001010010" ],
        [ "dom7/11",     "100011010010" ],
        [ "5 add7/11",   "100001010010" ],
        [ "major9",      "101010010001" ],
        [ "maj add9",    "101010010000" ],
        [ "dom9",        "101010010010" ],
        [ "major11",     "101011010001" ],
        [ "maj add11",   "100011010000" ],
        [ "major7/11",   "100011010001" ],
        [ "major7/#11",  "100010110001" ],
        [ "major6",      "100010010100" ],
        [ "dom13",       "101010010110" ],
        [ "dom7add13",   "100010010110" ],
        [ "lydian", 	 "100000110000" ],
        [ "lyd maj7",    "100000110001" ],
        [ "lyd 9",       "101000110001" ],

        [ "minor",       "100100010000" ],
        [ "minor6", 	 "100100010100" ],
        [ "minor7",      "100100010010" ],
        [ "minor7b9",    "110100010010" ],
        [ "minor9",      "101100010010" ],
        [ "minor b9", 	 "110100010010" ],
        [ "min add9",    "101100010000" ],
        [ "minor11",     "101101010010" ],
        [ "min7add11",   "100101010010" ],
        [ "min add11",   "100101010000" ],
        [ "min add9/11", "101101010000" ],
        [ "min maj7",	 "100100010001" ],
        [ "min maj9", 	 "101100010001" ],
        [ "min maj11", 	 "101101010001" ],
        
        [ "dim", 	 "100100100000" ],
        [ "dim7",        "100100100100" ],
        [ "min7b5",	 "100100100010" ],
        [ "dim b6",      "100100101000" ],

        [ "aug",         "100010001000" ],
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

def find_first_chord_name (pattern):
    # across all pattern rotations
    for j in range(0, len(str(pattern))):
        # compare to all common chords
        for i in range(0, len(common_chords)):
            if pattern[j:] + pattern[:j] == common_chords[i][1]:
                return common_chords[i][0]

def find_root_note (pattern):
    for i in range(len(str(pattern))):
        if pattern[i] == '1':
            return simple_note_names[i]


# print notation for all constructor chords
print ("\nAll constructor chords notated:")

print ("-------------------------------------")
# for all constructor chords in order 
for c in range(0, len(constructor_chords)): 
    print(c, "-", constructor_chords[c], ":")
    # print note names for canonical chord
    for i in range(0,len(note_names)):
        if constructor_chords[c][i] == '1':
            print (note_names[i],end="\t")
    print ()
    print (find_chord_names(constructor_chords[c]))
    print ("-------------------------------------")


# align scales to the leftmost note

for S in range (len(Scale_list)):
    for R in range (len(Scale_list[S])):
        if Scale_list[S][0] == '0':
            Scale_list[S] = Scale_list[S][1:] + Scale_list[S][:1]
            U_list[S] = U_list[S][1:] + U_list[S][:1]
            L_list[S] = L_list[S][1:] + L_list[S][:1]

def hamming_distance (x,y):
    d = 0
    for i in range(len(x)):
        if x[i] != y[i]:
            d += 1
    return d

def minimal_distance (a,b):
    min_d = hamming_distance (a,b)
    for i in range(1,len(b)):
        dist = hamming_distance(a, b[i:] + b[:i])
        if dist < min_d:
            min_d = dist
    return min_d

Major_scale = "101011010101"
Harm_minor_scale = "101101011001"
Melod_minor_scale = "101101010101"

print ("\n\n\n=====================================================================================================================")
print ("Scale ID\t", "Scale Pattern\t", "Upper Chord\tName\t\t", "Lower Chord\tName\t\t", "Norm. Musical Dist.")
print ("\t\t\t\t\t\t\t\t\t\t\t\tMaj\tHmin\tMmin")
print ("---------------------------------------------------------------------------------------------------------------------")
for S in range(len(Scale_list)):
    U_chord = U_list[S]
    L_chord = L_list[S]
    print ("ID:", int(Scale_list[S], base=2), "\t", Scale_list[S], "\t", 
        U_chord, "\t", find_root_note(U_chord), find_first_chord_name(U_chord), "\t", 
        L_chord, "\t", find_root_note(L_chord), find_first_chord_name(L_chord), "\t",
	minimal_distance(Major_scale, Scale_list[S]), "\t",
        minimal_distance(Harm_minor_scale, Scale_list[S]), "\t",
        minimal_distance(Melod_minor_scale, Scale_list[S]))

print ("=====================================================================================================================")
