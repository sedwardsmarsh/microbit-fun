from microbit import *
import music
from time import ticks_ms

def transform_range(old_value, old_max, old_min, new_max, new_min):
    # https://stackoverflow.com/questions/929103/convert-a-number-range-to-another-range-maintaining-ratio
    old_range = old_max - old_min
    new_range = new_max - new_min  
    return (((old_value - old_min) * new_range) / old_range) + new_min

x_avg = 0
x_working_sum = 0
while True:
    x_raw_tilt, y_raw_tilt, _ = accelerometer.get_values()
    # print('x_raw_tilt=', x_raw_tilt)
        
    # average the x values to make them smoother
    if ticks_ms() % 1000 == 0:
        x_avg = x_working_sum/1000
        print('x_avg=', x_avg)
        x_working_sum = 0
    x_working_sum += x_raw_tilt

    # flip y axis
    y_raw_tilt *= -1
    
    # transform raw tilt values in the range [-1000, 1000] to respective ranges for pitch and volume
    transformed_x = int(transform_range(old_value=x_avg, old_max=1000, old_min=-1000, new_max=1000, new_min=100))
    transformed_y = int(transform_range(old_value=y_raw_tilt, old_max=1000, old_min=-1000, new_max=255, new_min=100))
    
    # play sound when b button is pressed
    if button_b.is_pressed():
        speaker.on()
        set_volume(transformed_y)
        music.pitch(transformed_x)
    else:
        speaker.off()
