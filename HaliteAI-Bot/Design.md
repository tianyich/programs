# Design

## Tasks
    Eric:
        Create a simple model for genetic bot
            -class Bot
            -Array: [23,4,5,6,7,0.49]
            -Behavior
                -
                -
                -

    Jason:
        Find solution to genetic evolution

## Run_game.bat mechanics
```batch
halite.exe --replay-directory replays/ -vv --no-logs --width 32 --height 32 "python MyBot1.py" "python MyBot.py"
```
### Python command
    Command line parameter input: "python MyBot1.py arg1 arg2 arg3"
    Retrieving info from python: 
```python
import sys
print(sys.argv)
```