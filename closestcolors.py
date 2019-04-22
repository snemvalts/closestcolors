import sys
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

lines = [line.rstrip('\n') for line in open(sys.argv[1])]

def delta_e_perceptiveness(a):
    if(a >= 100):
        return 'Colors are exact opposite'
    elif(100 >= a > 49):
        return 'Colors are more different than similar'
    elif(49 >= a >= 11):
        return 'Colors are more similar than different'
    elif(11 > a > 2):
        return 'Color difference is visible at a glance'
    elif(2 >= a > 1):
        return 'Color difference visible through close observation'
    elif(a <= 1):
        return 'Color difference not perceptible with human eyes'


name_to_value = {}

for i in lines:
    split = i.split(':')
    if(len(split) == 2):
        name_to_value[split[0]] = sRGBColor.new_from_rgb_hex(split[1].upper())


for i in name_to_value:
    min_diff = 101.0
    min_diff_name = ''
    for j in name_to_value:
        if(i == j): continue

        lab_i = convert_color(name_to_value[i], LabColor)
        lab_j = convert_color(name_to_value[j], LabColor)

        delta_e = delta_e_cie2000(lab_i, lab_j)

        if(delta_e < min_diff):
            min_diff = delta_e
            min_diff_name = j

    print()
    print('Closest color to %s is %s with ΔE of %.3f.' % (i, min_diff_name, min_diff))
    print('Perceptiveness rating: ' + str(delta_e_perceptiveness(min_diff)))
    print()
