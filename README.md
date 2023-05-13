# iterm2_auto_mode

This script automatically changes the color scheme of your iTerm2 terminal based on your system's light/dark theme and can be set up to run automatically every time iTerm2 is launched.

## Description

The script monitors your system's theme and updates iTerm2's color scheme accordingly. When the system's theme is dark, it sets iTerm2's color scheme to "Dark Background". When the system's theme is light, it sets iTerm2's color scheme to "Light Background".

## Setup

1. Make sure you have Python 3 installed. You can check your Python version by running `python3 --version` in your terminal.

2. You will need to install the `iterm2` Python package. You can do this by running `pip3 install iterm2`.

3. Clone this repository or download the script to your local machine.

4. You will also need to change the log file path at `logging.basicConfig` varable.

4. To set up the script to run automatically on iTerm2 launch, move the script to the `~/Library/ApplicationSupport/iTerm2/Scripts/AutoLaunch/` directory. If the `AutoLaunch` directory doesn't exist, create it.

## Usage

Once the script is placed in the `AutoLaunch` directory, it will run automatically every time iTerm2 is launched.

## Troubleshooting

If the script is not updating your iTerm2 color scheme as expected, make sure the "Dark Background" and "Light Background" color schemes exist in your iTerm2 presets. If you encounter errors or the script isn't behaving as expected, check the Script Console in iTerm2. You can access this by selecting Scripts > Script Console in iTerm2.

## Contributing

If you would like to contribute to this project, feel free to fork the repository, make your changes, and open a pull request. We appreciate your help!
