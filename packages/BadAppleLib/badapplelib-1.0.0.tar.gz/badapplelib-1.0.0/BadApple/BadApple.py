import sys
import time
import os
import blessed

terminal = blessed.Terminal() # intiialize blessed

def Play(ignoreResolution=False,fps=1/30): # fps=1/30 means that it defaults to 30 fps if nothing is supplied, does the computation beforehand
    os.chdir(__file__.replace("BadApple.py", ""))
    os.chdir("frames") # get into the frames folder
    frames_list = os.listdir() # list all frames
    if not ignoreResolution:
        #Get columns and lines of terminal
        x = os.get_terminal_size().columns
        y = os.get_terminal_size().lines
        if x < 144:
            print(f"Columns number is too small! {x}, expecting x >= 144")
            return False
        if y < 36:
            print(f"Lines number is too small! {y}, expecting x >= 36")
            return False
    try:
        for frames in frames_list: # loops throught all of the frames
            with open(frames, "r") as frame: # opens each frame
                sys.stdout.write(frame.read()+terminal.move_yx(0, 0)) # prints contents of frames
                sys.stdout.flush() # flushes stdout
                time.sleep(fps) # waits for 30 "frames"
    except KeyboardInterrupt:
        os.system("clear")
        return False
    return True
