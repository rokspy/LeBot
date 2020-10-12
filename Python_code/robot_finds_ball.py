from Vision import ImageProcessing
from TempMovement import MainBoardMovement

See = ImageProcessing
Move = MainBoardMovement
x_mid = 1280
x_range = 10
rot_quickness = 5


print('Starting orientation...')

while True:
    BallCentroid = See.return_basket_centroid # Centroid
    if x_mid - x_range > BallCentroid[0] > x_mid + x_range: # If not withing horizontal range
        dif = BallCentroid - x_mid
        if dif > 0:     # Ball is to the right
            Move.rotate_right(rot_quickness)
        elif dif < 0:   # Ball is to the left
            Move.rotate_left(rot_quickness)
        continue
    else:
        break

print("Orientation done")
