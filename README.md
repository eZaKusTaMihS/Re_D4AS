# D4AS
A script for autoplaying D4DJ Groovy Mix (JP only).

*Author: ゼカツまし*

## LOGS
### TODOs
- Pack the script into exe
- Add UI (maybe won't)
- Add more settings that can be set automatically other than manually in game

### Recent Updates
#### Oct 26, 2024
- Add support for event type: raid
- Voltage supplement fixed

## Requirements
- Get your simulator ready. [MuMu Player 12](https://mumu.163.com) is recommended.
- Download [the latest version of python](https://www.python.org/downloads/) and follow the instructions to install.
- Install environment: run `pip install opencv-python==4.10.0.84` in cmd.
- Make sure you've got adb installed (usually comes with the simulator).
For MuMu user, adb can be found at `MuMuPlayer-12.0\shell\adb.exe`.

## Preparations
Set your simulator and make sure the resolution is set to 1280*720.
![](doc_res/01.png)

Install D4DJ and log into your account.

Test adb.
Run `adb devices` in cmd to show the devices that are currently connected to adb.
![](doc_res/02.png)

Then fill the address into `serial` field in `config.json`.
For those with multiple devices, figure out which device D4DJ is running on
and fill in that address.

## Usage
### General
Run `python main.py` under root directory to start the script.
(Planning to pack it into exe in near future)

Normally you should change the config to make the script run properly.
You may refer to [Customization](#customization) to customize the script.

Also make sure to read the [Cautions](#cautions) before running the script.

### Customization
In `config.json`, there are two fields under `tasks` you can change.
- `event_type`: valued among `raid`, `poker`, `yell` and `battle`,
depending on which event type you are running the script for.
- `mode`: valued among `single`, `multi` and `sp`.
Some events may not have sp lives and the script may not work under that situation.

More settings, such as voltage recognition, will be added later (probably this year?).

The `res` folder stores buttons or features for opencv to recognize.
Under experiencing failure in recognizing a specific button or status (see the `res/stat` folder),
you may screenshot and add or replace the original png files with yours.
File names are not considered but make sure all you put are png files.

If you want to deactivate some of the buttons or status,
you may just place a `_` at the beginning of the file name,
then it will be ignored.

### Cautions
Make sure that:
- Auto mode is switched on within the game
- Proper voltage usage is set
- Under some circumstances you may need to get your room selected in advance when there are multiple choices

before starting the script.

By the way you are recommended to set your background static
(disable club motion/skill window/groovy effect, set bg to music jacket/character, etc.)
and screenshot a static part of your live screen and replace the image in the `res/stat/live` folder with it
to help the script to recognize the live status. Loop time recorder based on live screen may be provided in later updates.
You may delete the old images in the `live` folder since that's my background.

## Finally
Enjoy your playing D4DJ.
You are welcome to contact me if you have any problems with the script
(since it's highly uncompleted).