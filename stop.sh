#!/bin/bash

# Define the terminal title
TERMINAL_TITLE="tictactoebackend"

# Find the terminal window with the specified title and close it
WINDOW_ID=$(xdotool search --name "$TERMINAL_TITLE")

if [ -n "$WINDOW_ID" ]; then
    # Close the terminal window
    xdotool windowclose "$WINDOW_ID"
    echo "Terminal with title '$TERMINAL_TITLE' has been closed."
else
    echo "No terminal with title '$TERMINAL_TITLE' found."
fi
