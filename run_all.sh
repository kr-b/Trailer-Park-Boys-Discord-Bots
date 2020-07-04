#!/usr/bin/bash

# Run new tmux session for each bot
tmux new -d -s dcbot_lahey "python3 ./lahey.py"
tmux new -d -s dcbot_ricky "python3 ./ricky.py"
tmux new -d -s dcbot_bubbles "python3 ./bubbles.py"