from random import choice, uniform

def noiseFCurves(fcurves):
    for k in fcurves:
        if choice(range(0,10)) == 5:
            modifier = k.modifiers.new(type="NOISE")
            modifier.strength = uniform(0,1)

