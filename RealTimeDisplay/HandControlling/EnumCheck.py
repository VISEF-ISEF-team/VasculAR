from enum import IntEnum

# Gesture Encodings 
class Gest(IntEnum):
    # Binary Encoded
    FIST = 0
    PINKY = 1
    RING = 2
    MID = 4
    LAST3 = 7
    INDEX = 8
    FIRST2 = 12
    LAST4 = 15
    THUMB = 16    
    PALM = 31
    
    # Extra Mappings
    V_GEST = 33
    TWO_FINGER_CLOSED = 34
    PINCH_MAJOR = 35
    PINCH_MINOR = 36

# Create an instance of Gest with the value of MID
gesture = Gest(4)
# Print the name and value of the gesture
print(gesture.name)

print(gesture.value)

# Check if the gesture contains the index finger using bitwise and operation
print(gesture & Gest.INDEX)

# Check if the gesture is equal to another Gest member using == operator
print(gesture == Gest.MID)
