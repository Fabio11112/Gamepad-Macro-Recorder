# Gamepad Macro Recorder & Replayer

A high-precision gamepad input recorder and replayer that captures controller inputs from physical gamepads (like PlayStation DualSense) and replays them as a virtual Xbox 360 controller using precise timing.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [How It Works](#how-it-works)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Controller Schemes](#controller-schemes)
- [Usage Guide](#usage-guide)
- [Technical Details](#technical-details)
- [Troubleshooting](#troubleshooting)

---

## 🎮 Overview

This tool allows you to:
1. **Record** gamepad inputs with precise timestamps (button presses, releases, analog stick movements, trigger pulls)
2. **Replay** the recorded inputs on a virtual Xbox 360 controller with accurate timing
3. **Loop** recordings indefinitely for automated tasks

The system uses:
- **Pygame** to read physical controller inputs
- **vgamepad** to create a virtual Xbox 360 controller for output
- **High-precision timing** (125Hz polling for axes, event-driven for buttons)
- **JSON-based recordings** for easy storage and sharing

---

## ✨ Features

### Recording Features
- ✅ **High-precision input capture** at 125Hz polling rate (8ms intervals)
- ✅ **Button events** - Captures press and release with timestamps
- ✅ **Analog inputs** - Records left/right stick movements
- ✅ **Trigger inputs** - Records left/right trigger positions
- ✅ **Dead zone handling** - Filters out controller drift
- ✅ **Thread-based polling** - Separate threads for buttons and axes
- ✅ **Real-time recording** - Start/stop with Ctrl+C

### Playback Features
- ✅ **Precise timing reproduction** - Uses busy-waiting for sub-millisecond accuracy
- ✅ **Virtual controller output** - Appears as Xbox 360 controller to games/apps
- ✅ **Single or infinite loop** - Replay once or indefinitely
- ✅ **Controller mapping** - Translates any gamepad to Xbox layout
- ✅ **Configurable delays** - Adjust timing between replays

### Configuration
- ✅ **JSON-based config** - Easy to modify without touching code
- ✅ **Multiple controller support** - Add custom controller schemes
- ✅ **Adjustable thresholds** - Fine-tune dead zones and timing
- ✅ **Flexible paths** - Customize recording and scheme locations

---

## 🔧 How It Works

### Recording Process
1. **Initialization**: Pygame detects your connected gamepad
2. **Dual capture system**:
   - **Buttons**: Event-driven capture (press/release events)
   - **Axes**: Continuous polling at 125Hz (8ms intervals) in separate thread
3. **Timestamp tracking**: All inputs get precise timestamps using `time.perf_counter()`
4. **Dead zone filtering**: Small movements below threshold are ignored
5. **JSON storage**: Inputs saved with ID, type, value, and timestamp

### Replay Process
1. **Loading**: Reads recorded inputs from JSON file
2. **Virtual controller**: Creates Xbox 360 controller using vgamepad + ViGEmBus driver
3. **Input mapping**: Translates your controller layout to Xbox 360 layout
4. **Precise timing**:
   - Calculates target time for each input
   - Sleeps for most of the wait time
   - Uses busy-waiting for final 2ms for precision
5. **Execution**: Presses buttons/moves sticks at exact recorded times
6. **Looping**: Can restart immediately or wait 5 seconds between loops

---

## 📦 Installation

### Prerequisites

**Windows Only** - This tool requires Windows due to ViGEmBus driver dependency.

### Step 1: Install ViGEmBus Driver

The virtual controller requires the ViGEmBus driver:

1. Download latest release from: https://github.com/nefarius/ViGEmBus/releases
2. Run the installer (`ViGEmBus_*_x64_x86_arm64.exe`)
3. Restart your computer after installation

### Step 2: Install Python Dependencies

```bash
pip install pygame vgamepad
```

Or if you have a `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Step 3: Verify Installation

Run this Python code to test:

```python
import pygame
import vgamepad

print("✓ Pygame installed:", pygame.version.ver)
print("✓ vgamepad installed successfully")

# Test virtual controller creation
gamepad = vgamepad.VX360Gamepad()
print("✓ Virtual Xbox 360 controller created successfully!")
```

---

## 📁 Project Structure

```
my_implementation/
├── main.py                          # Main entry point - run this!
│
├── config/
│   └── config.json                  # Configuration file (paths, thresholds)
│
├── configuration_manager/
│   └── config_manager.py            # Handles loading/saving config
│
├── controller_schemes/
│   └── dualsense.json               # Button/axis mapping for DualSense controller
│
├── gamepad/
│   ├── gamepad_reader.py            # Records inputs from physical gamepad
│   ├── gamepad_repeater.py          # Replays inputs to virtual gamepad
│   ├── gamepad_super.py             # Base class with shared logic
│   └── gamepad_to_vg_mapper.py      # Maps inputs to Xbox 360 layout
│
├── input_classes/
│   ├── input.py                     # Data class for single input
│   ├── input_type.py                # Enum (BUTTON or AXIS)
│   ├── input_collection.py          # Container for multiple inputs
│   └── input_iterator.py            # Iterator for input playback
│
├── json_classes/
│   ├── json_recorder.py             # Saves inputs to JSON file
│   └── json_loader.py               # Loads inputs from JSON file
│
└── recordings/
    └── dualsense_inputs.json        # Example: recorded inputs
```

---

## ⚙️ Configuration

### Configuration File: `config/config.json`

```json
{
  "paths": {
    "recording_folder_location": "recordings/",
    "controller_scheme_folder": "controller_schemes/"
  },
  "gamepad": {
    "dead_zone": 0.06,
    "name": "dualsense"
  },
  "repetition": {
    "offset": 0.008,
    "busy_waiting_time": 0.002
  }
}
```

### Configuration Parameters Explained

#### 🗂️ Paths Section
| Parameter | Description | Default |
|-----------|-------------|---------|
| `recording_folder_location` | Where JSON recordings are saved | `recordings/` |
| `controller_scheme_folder` | Where controller mapping files are stored | `controller_schemes/` |

#### 🎮 Gamepad Section
| Parameter | Description | Default | Notes |
|-----------|-------------|---------|-------|
| `dead_zone` | Threshold for axis inputs | `0.06` | Range: 0.0 to 1.0. Increase if you see drift, decrease for more sensitivity |
| `name` | Controller scheme name | `dualsense` | Must match a `.json` file in `controller_schemes/` folder |

**Dead Zone Explained**: 
- Axes report values from `-1.0` to `1.0`
- If absolute value < `dead_zone`, it's treated as `0.0`
- Example: with `dead_zone=0.06`, input of `0.05` becomes `0.0`
- Prevents controller drift from being recorded/replayed

#### ⏱️ Repetition Section
| Parameter | Description | Default | Purpose |
|-----------|-------------|---------|---------|
| `offset` | Polling interval for axes | `0.008` | 8ms = 125Hz polling rate |
| `busy_waiting_time` | Pre-busy-wait threshold | `0.002` | Last 2ms uses busy-waiting for precision |

**Timing Mechanism**:
1. Calculate time until next input
2. If time > `busy_waiting_time` (2ms), use `time.sleep()`
3. Final 2ms uses busy-waiting loop for sub-millisecond precision
4. Achieves accurate timing even at microsecond level

---

## 🎯 Controller Schemes

### What is a Controller Scheme?

A controller scheme maps your physical controller's buttons and axes to standardized names. This allows the program to:
- Know which button is "X" or "Circle"
- Identify left/right sticks
- Map to Xbox 360 layout for replay

### DualSense Scheme: `controller_schemes/dualsense.json`

```json
{
  "axis": {
    "left_stick": {
      "x": 0,    // Pygame axis ID for left stick X
      "y": 1     // Pygame axis ID for left stick Y
    },
    "right_stick": {
      "x": 2,    // Pygame axis ID for right stick X
      "y": 3     // Pygame axis ID for right stick Y
    },
    "triggers": {
      "left": 4,   // Pygame axis ID for L2 trigger
      "right": 5   // Pygame axis ID for R2 trigger
    }
  },
  "button": {
    "bottom_action": 0,              // Cross (X) button
    "right_action": 1,               // Circle button
    "left_action": 2,                // Square button
    "top_action": 3,                 // Triangle button
    "select_or_share": 4,            // Share button
    "system_home": 5,                // PS button
    "start_menu": 6,                 // Options button
    "left_stick_click": 7,           // L3 (left stick press)
    "right_stick_click": 8,          // R3 (right stick press)
    "left_bumper": 9,                // L1 button
    "right_bumper": 10,              // R1 button
    "dpad_up": 11,                   // D-pad up
    "dpad_down": 12,                 // D-pad down
    "dpad_left": 13,                 // D-pad left
    "dpad_right": 14,                // D-pad right
    "aux_center_or_touchpad": 15     // Touchpad press
  }
}
```

### Xbox 360 Virtual Controller Mapping

During replay, inputs are mapped to Xbox 360 layout:

| Generic Name | Xbox 360 Button | DualSense Equivalent |
|--------------|----------------|---------------------|
| bottom_action | A | Cross (X) |
| right_action | B | Circle |
| left_action | X | Square |
| top_action | Y | Triangle |
| select_or_share | Back | Share |
| system_home | Guide | PS Button |
| start_menu | Start | Options |
| left_stick_click | Left Thumb | L3 |
| right_stick_click | Right Thumb | R3 |
| left_bumper | LB | L1 |
| right_bumper | RB | R1 |

### Creating Custom Controller Schemes

To add support for another controller:

1. **Find Pygame IDs**:
```python
import pygame
pygame.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Press each button and check which ID it reports
for event in pygame.event.get():
    if event.type == pygame.JOYBUTTONDOWN:
        print(f"Button {event.button} pressed")

# Move each axis and check IDs
for i in range(joystick.get_numaxes()):
    print(f"Axis {i}: {joystick.get_axis(i)}")
```

2. **Create JSON file**: `controller_schemes/your_controller.json`

3. **Map all buttons/axes** using the IDs you found

4. **Update config.json**: Set `"gamepad.name": "your_controller"`

---

## 🚀 Usage Guide

### Running the Program

```bash
python main.py
```

### Menu Options Explained

When you run `main.py`, you'll see:

```
What do you want to do?
0 - Record
1 - Repeat once your recording
2 - Repeat Indefinitely your recording
>>>
```

---

### Option 0: Record New Macro

**What it does**: Records all your controller inputs to a JSON file.

#### Step-by-Step Process:

1. **Enter `0` and press Enter**

2. **Recording starts automatically**:
   ```
   The gamepad Wireless Controller is being recorded. Start using your controller
   ```

3. **Use your controller**:
   - Press any buttons
   - Move analog sticks
   - Pull triggers
   - All inputs are captured with timestamps

4. **Watch real-time feedback** (if enabled in code):
   - Button presses/releases logged
   - Axis movements tracked

5. **Stop recording**:
   - Press `Ctrl+C` on your keyboard
   - Recording saves automatically to:
     ```
     recordings/dualsense_inputs.json
     ```

#### What Gets Recorded:

**Example Recording File** (`recordings/dualsense_inputs.json`):
```json
[
    {
        "id": 0,
        "type": 0,
        "value": 0,
        "timestamp": 0.5234567
    },
    {
        "id": 0,
        "type": 1,
        "value": 0.3456,
        "timestamp": 0.5314892
    }
]
```

**Field Breakdown**:
- `id`: Button number or axis number (from controller scheme)
- `type`: `0` = BUTTON, `1` = AXIS
- `value`: 
  - Buttons: `0` (pressed) or `1` (released)
  - Axes: Float from `-1.0` to `1.0`
- `timestamp`: Time in seconds from recording start

#### Recording Technical Details:

**Button Recording**:
- Event-driven (immediate capture)
- Captures separate press (DOWN) and release (UP) events
- Timestamp: Exact moment event occurred

**Axis Recording**:
- Polled at 125Hz (every 8ms)
- Only records if value changed by > 0.01
- Dead zone applied: values < 0.06 become 0.0
- Simultaneous tracking of:
  - Left stick X/Y
  - Right stick X/Y
  - Left trigger
  - Right trigger

**Thread Architecture**:
```
Main Thread:          Button event loop
Background Thread:    Axis polling loop (125Hz)
Both write to:        Shared JsonRecorder (thread-safe append)
```

---

### Option 1: Replay Once

**What it does**: Creates a virtual Xbox 360 controller and replays your recording exactly once.

#### Step-by-Step Process:

1. **Enter `1` and press Enter**

2. **Get ready prompt**:
   ```
   ENTER to start
   ```
   - Press Enter when you're ready
   - This gives you time to focus the target application

3. **Playback begins**:
   - Virtual Xbox 360 controller created
   - Inputs replayed with precise timing
   - Console shows each action (if debug enabled)

4. **Automatic completion**:
   - Plays through entire recording once
   - Program exits when finished

#### What Happens During Replay:

1. **Virtual controller creation**:
   - Windows sees a new Xbox 360 controller
   - Check "Devices and Printers" - you'll see "Xbox 360 Controller"

2. **Timing precision**:
   ```python
   # Example: Input recorded at timestamp 1.5 seconds
   # Program waits exactly 1.5 seconds from start
   # Then executes the input
   ```

3. **Input execution**:
   - **Buttons**: Press or release based on recorded value
   - **Sticks**: Set X/Y position to recorded values
   - **Triggers**: Set pressure from 0.0 (not pressed) to 1.0 (fully pressed)

4. **Update cycle**:
   - After each input: `gamepad.update()` sends to virtual controller
   - Games/applications receive input immediately

#### Use Cases for Replay Once:

- ✅ Testing recordings
- ✅ Executing a specific action sequence
- ✅ Speedrunning practice (replay perfect inputs)
- ✅ Demonstration or tutorial playback

---

### Option 2: Replay Indefinitely

**What it does**: Loops your recording continuously with a 5-second pause between each cycle.

#### Step-by-Step Process:

1. **Enter `2` and press Enter**

2. **Get ready prompt**:
   ```
   ENTER to start
   ```

3. **Infinite loop begins**:
   ```
   [DEBUG] START REPLAY
   ... (recording plays) ...
   [DEBUG] END OF REPLAY AND WAITING
   ... (5 second pause) ...
   [DEBUG] END OF WAITING
   [DEBUG] START REPLAY
   ... (recording plays again) ...
   ```

4. **Stop the loop**:
   - Press `Ctrl+C` to stop
   - Virtual controller releases all inputs safely

#### Loop Timing:

```
┌─────────────────────────────────────────────┐
│ Cycle 1                                     │
├─────────────────────────────────────────────┤
│ [Replay recording - variable duration]     │
│ [Wait 5 seconds]                            │
├─────────────────────────────────────────────┤
│ Cycle 2                                     │
├─────────────────────────────────────────────┤
│ [Replay recording]                          │
│ [Wait 5 seconds]                            │
├─────────────────────────────────────────────┤
│ ... continues forever ...                   │
└─────────────────────────────────────────────┘
```

**Customizing Wait Time**:

Edit `main.py`, line 37:
```python
time.sleep(5)  # Change 5 to any number of seconds
```

#### Use Cases for Infinite Replay:

- ✅ **Grinding/Farming**: Repeat actions in games
- ✅ **Automated testing**: Loop through test sequence
- ✅ **Demonstration loop**: Trade show displays
- ✅ **Endurance testing**: Stress test applications

#### Important Notes:

⚠️ **Anti-Cheat Warning**: Many online games detect and ban macro/bot usage. Only use this for:
- Offline games
- Testing your own applications
- Environments where automation is allowed

⚠️ **Resource Usage**: 
- Program runs continuously
- Virtual controller active indefinitely
- Monitor CPU usage if running for hours

⚠️ **Safe Stopping**:
- Always use `Ctrl+C` to stop gracefully
- Allows cleanup of virtual controller
- Prevents stuck inputs

---

## 🔬 Technical Details

### Input Recording Architecture

```
Physical Controller (via USB/Bluetooth)
          ↓
   Pygame Library
          ↓
   ┌─────────────────────┐
   │  GamepadReader      │
   │  ┌───────────────┐  │
   │  │ Main Thread   │←─┼─── Button Events (JOYBUTTONDOWN/UP)
   │  │ Event Loop    │  │
   │  └───────────────┘  │
   │                     │
   │  ┌───────────────┐  │
   │  │ Poll Thread   │←─┼─── Axis Polling (125Hz)
   │  │ Continuous    │  │
   │  └───────────────┘  │
   └──────────┬──────────┘
             ↓
      JsonRecorder
             ↓
      JSON File Storage
```

### Input Replay Architecture

```
      JSON File
          ↓
     JsonLoader
          ↓
   InputCollection
          ↓
   ┌─────────────────────────────┐
   │  GamepadRepeater            │
   │  ┌───────────────────────┐  │
   │  │ Timing Loop           │  │
   │  │ • Calculate target    │  │
   │  │ • Sleep (coarse)      │  │
   │  │ • Busy-wait (precise) │  │
   │  └─────────┬─────────────┘  │
   │            ↓                 │
   │  ┌────────────────────────┐ │
   │  │ GamepadToVGamepadMapper│ │
   │  │ • Map button IDs       │ │
   │  │ • Convert axis values  │ │
   │  │ • Track stick states   │ │
   │  └─────────┬──────────────┘ │
   └────────────┼─────────────────┘
               ↓
        VX360Gamepad
               ↓
        ViGEmBus Driver
               ↓
    Virtual Xbox 360 Controller
               ↓
    OS/Game sees real controller
```

### Classes Explained

#### 1. `ConfigManager` (`configuration_manager/config_manager.py`)

**Purpose**: Centralized configuration loading and access.

**Key Methods**:
```python
config = ConfigManager()  # Loads config/config.json
value = config.get("gamepad.dead_zone")  # Returns 0.06
```

**Features**:
- Loads JSON config on initialization
- Creates default config if missing
- Dot-notation access: `"path.to.value"`
- Type safety with defaults

---

#### 2. `GamepadReader` (`gamepad/gamepad_reader.py`)

**Purpose**: Records inputs from physical controller.

**Key Methods**:
```python
reader.record()  # Start recording
reader.stop()    # Stop and save to JSON
```

**Internal Process**:
1. `record()`: Initializes joystick, starts threads
2. `_read_button_events()`: Main thread processes button events
3. `_poll_axes()`: Background thread samples axes at 125Hz
4. `stop()`: Joins threads, saves to JSON

**Threading Safety**:
- `isRecording` flag controls both threads
- `JsonRecorder.append()` is thread-safe (Python GIL)
- Clean shutdown with `thread.join()`

---

#### 3. `GamepadRepeater` (`gamepad/gamepad_repeater.py`)

**Purpose**: Replays recorded inputs to virtual controller.

**Key Methods**:
```python
repeater.replay()  # Play recording once
```

**Timing Logic**:
```python
# For each input:
target_time = start_time + input.timestamp
remaining = target_time - current_time

if remaining > 0.002:  # More than 2ms left
    time.sleep(remaining - 0.002)  # Sleep most

while current_time < target_time:  # Busy-wait final 2ms
    pass

execute_input(input)  # Execute at exact time
```

**Why Busy-Waiting?**:
- `time.sleep()` only accurate to ~15ms on Windows
- Busy-waiting achieves sub-millisecond precision
- Only used for final 2ms to minimize CPU usage

---

#### 4. `GamepadSuper` (`gamepad/gamepad_super.py`)

**Purpose**: Base class with shared utility methods.

**Key Methods**:
```python
_is_left_stick(input)   # Returns True if input is left stick
_is_right_stick(input)  # Returns True if input is right stick
_is_left_trigger(input) # Returns True if input is left trigger
_is_right_trigger(input)# Returns True if input is right trigger
```

**Why Needed?**:
- Axes are identified only by number (0, 1, 2, 3...)
- These methods map numbers to semantic meaning
- Both Reader and Repeater inherit this logic

---

#### 5. `GamepadToVGamepadMapper` (`gamepad/gamepad_to_vg_mapper.py`)

**Purpose**: Translates controller inputs to Xbox 360 format.

**Key Features**:

1. **Button Mapping**:
   ```python
   # DualSense "Cross" (button 0) → Xbox "A" button
   dualsense_button_0 → XUSB_GAMEPAD_A
   ```

2. **Axis Conversion**:
   ```python
   # Pygame: -1.0 (left/up) to 1.0 (right/down)
   # Xbox: -1.0 (left/up) to 1.0 (right/down) [same range]
   
   # Triggers special case:
   # Pygame: -1.0 (not pressed) to 1.0 (fully pressed)
   # Xbox: 0.0 (not pressed) to 1.0 (fully pressed)
   trigger_value = (pygame_value + 1) / 2  # Conversion
   ```

3. **Y-Axis Inversion**:
   ```python
   # Pygame: positive Y = down
   # Xbox: positive Y = up
   # Solution: Invert Y axes
   mapped_y = -original_y
   ```

4. **Stick State Tracking**:
   - Sticks have separate X and Y axes
   - Must track last X when Y updates (and vice versa)
   - Sends both X and Y together: `left_joystick_float(x, y)`

---

#### 6. `Input` (`input_classes/input.py`)

**Purpose**: Data class representing single input event.

**Structure**:
```python
input = Input(
    id=0,           # Button/axis number
    type=Type.BUTTON,  # BUTTON or AXIS
    value=0,        # 0/1 for buttons, -1.0 to 1.0 for axes
    timestamp=1.523 # Time in seconds
)
```

**Serialization**:
```python
dict = input.to_dict()  # Convert to JSON-serializable dict
input = Input(dict)     # Reconstruct from dict
```

---

#### 7. `InputCollection` & `InputIterator`

**Purpose**: Container and iterator for recorded inputs.

**Usage**:
```python
collection = InputCollection([input1, input2, input3])
iterator = collection.get_iterator()

while iterator.hasNext():
    current_input = iterator.next()
    # Process input
```

**Why Custom Iterator?**:
- Provides `hasNext()` method for safer iteration
- Abstracts input list iteration
- Could add features like reverse playback, filtering

---

#### 8. `JsonRecorder` & `JsonLoader`

**Purpose**: Save and load recordings from JSON files.

**Recording Flow**:
```python
recorder = JsonRecorder("recordings/my_recording.json")
recorder.append(input1)  # Add inputs
recorder.append(input2)
recorder.save()          # Write to file at end
```

**Loading Flow**:
```python
loader = JsonLoader("recordings/my_recording.json")
loader.load()           # Read and parse JSON
inputs = loader.getInputs()  # Get Input objects
```

---

### Timing Precision Analysis

**Challenge**: Replicate timing with microsecond accuracy.

**Solution**:
```python
# Record: High-precision timestamps
timestamp = time.perf_counter()  # Nanosecond precision

# Replay: Hybrid sleep approach
target = start + timestamp
remaining = target - current

if remaining > 0.002:
    time.sleep(remaining - 0.002)  # Coarse sleep

while current < target:  # Busy-wait (<2ms)
    current = time.perf_counter()
```

**Accuracy Results**:
- `time.sleep()` alone: ±15ms error
- Hybrid approach: ±0.1ms error
- Good enough for frame-perfect inputs (60fps = 16.67ms)

---

### Dead Zone Implementation

**Problem**: Controllers always have slight analog drift.

**Solution**:
```python
# Recording phase
for axis_id in range(joystick.get_numaxes()):
    value = joystick.get_axis(axis_id)
    
    if abs(value) < dead_zone:  # 0.06 by default
        value = 0
    
    # Only record if changed significantly
    if abs(value - last_value) > 0.01:
        record(value)
```

**Replay phase**:
```python
# Same dead zone applied during mapping
if abs(input.value) <= dead_zone:
    input.value = 0
```

**Benefits**:
- Prevents recording of drift/noise
- Smaller JSON files
- Cleaner playback

---

## 🐛 Troubleshooting

### Issue: "No joystick connected"

**Symptom**: Program exits with error during recording.

**Solutions**:
1. Verify controller is connected (USB or Bluetooth)
2. Check Windows "Devices and Printers" - you should see your controller
3. Test controller in "Set up USB game controllers" (Windows+R → `joy.cpl`)
4. Reconnect controller and try again

**Debugging**:
```python
import pygame
pygame.init()
print(f"Controllers detected: {pygame.joystick.get_count()}")
```

---

### Issue: Virtual controller not appearing

**Symptom**: Replay runs but game doesn't see controller.

**Solutions**:
1. **Install ViGEmBus driver**: https://github.com/nefarius/ViGEmBus/releases
2. **Restart computer** after driver installation
3. **Check Device Manager**:
   - Open Device Manager (Windows+R → `devmgmt.msc`)
   - Look for "Nefarius Virtual Gamepad Emulation Bus"
   - Should have no yellow warning icons
4. **Run as administrator** (sometimes needed)

**Verification**:
```python
import vgamepad
gamepad = vgamepad.VX360Gamepad()  # Should not raise error
# Check "Devices and Printers" → see "Xbox 360 Controller"
```

---

### Issue: Inputs not matching recording

**Symptoms**:
- Actions happen too fast/slow
- Buttons pressed at wrong times
- Sticks moving incorrectly

**Solutions**:

1. **Timing too fast/slow**:
   - Check system load - high CPU usage affects timing
   - Close background applications
   - Increase `busy_waiting_time` if too fast: `0.002` → `0.005`

2. **Controller mapping wrong**:
   - Your controller might not be DualSense
   - Create custom controller scheme (see "Creating Custom Controller Schemes")
   - Verify button IDs match in `controller_schemes/your_controller.json`

3. **Axis inverted**:
   - Some controllers have inverted Y axes
   - Edit `GamepadToVGamepadMapper._map_axis()` to remove `-` from Y inversion

---

### Issue: Recording file not found

**Symptom**: `FileNotFoundError` when replaying.

**Solutions**:
1. Check `recordings/` folder exists
2. Verify filename matches: `{gamepad_name}_inputs.json`
3. Ensure you recorded before trying to replay
4. Check `config.json` → `"gamepad.name"` matches your controller scheme

---

### Issue: Controller drift in recording

**Symptom**: Sticks/triggers moving when they shouldn't.

**Solutions**:
1. **Increase dead zone**:
   - Edit `config/config.json`
   - Change `"dead_zone": 0.06` to `0.10` or higher
   - Record again

2. **Controller calibration**:
   - Windows: "Set up USB game controllers" → Properties → Settings → Calibrate

---

### Issue: High CPU usage during replay

**Symptom**: CPU at 100% during playback.

**Explanation**: Busy-waiting intentionally uses CPU for timing precision.

**Solutions**:
1. Normal behavior - only uses CPU during active replay
2. To reduce CPU (at cost of timing accuracy):
   - Edit `configuration_manager/config_manager.py`
   - Increase `"busy_waiting_time": 0.002` to `0.010`
   - More sleep, less busy-waiting

---

### Issue: Program won't stop with Ctrl+C

**Symptom**: Pressing Ctrl+C doesn't stop recording/replay.

**Solutions**:
1. Press Ctrl+C multiple times
2. If frozen, close terminal window
3. Task Manager → End process: `python.exe`
4. For recording: Ensure `isRecording` flag is being checked frequently

---

### Issue: Inputs feel "choppy" or "stuttery"

**Symptoms**:
- Replayed movements not smooth
- Stick movements jerky

**Solutions**:

1. **Recording too sparse**:
   - Decrease `poll_interval` in `GamepadReader`:
   ```python
   self.poll_interval = 0.004  # 250Hz instead of 125Hz
   ```

2. **Value change threshold too high**:
   - In `GamepadReader._poll_axes()`:
   ```python
   if abs(value - last_value) > 0.01:  # Lower this to 0.005
   ```

3. **System lag**:
   - Close background applications
   - Disable V-Sync in games if testing

---

## 📝 Additional Notes

### File Locations

All relative paths are from the `my_implementation/` directory:

```
my_implementation/
├── config/config.json              ← Configuration
├── controller_schemes/
│   └── dualsense.json              ← Controller mappings
├── recordings/
│   └── dualsense_inputs.json      ← Your recordings
└── main.py                         ← Run this!
```

### Supported Controllers

**Officially supported**:
- ✅ PlayStation 5 DualSense (included scheme)

**Can be added**:
- ⚙️ PlayStation 4 DualShock
- ⚙️ Xbox One/Series controller
- ⚙️ Nintendo Switch Pro Controller
- ⚙️ Generic USB gamepad

To add: Create JSON scheme file with button/axis mapping.

### Limitations

1. **Windows only** - ViGEmBus driver is Windows-exclusive
2. **Single controller** - Records first detected controller only
3. **Xbox 360 output** - Virtual controller always Xbox 360 layout
4. **No real-time editing** - Must stop recording to save
5. **No playback speed control** - Timing is 1:1 from recording

### Future Enhancement Ideas

- 🔮 **Recording editor** - GUI to trim/merge recordings
- 🔮 **Multiple controller support** - Record several gamepads
- 🔮 **Playback speed control** - 0.5x slow-mo, 2x fast forward
- 🔮 **Conditional replay** - "Press buttons until X happens"
- 🔮 **Hotkey trigger** - Press F9 to start replay
- 🔮 **Linux support** - Alternative to ViGEmBus (uinput)

---

## 📄 License

[Add your license here]

---

## 🤝 Contributing

[Add contribution guidelines here]

---

## ⚠️ Disclaimer

This tool is for legitimate automation, testing, and accessibility purposes only. 

**DO NOT USE** for:
- ❌ Cheating in online games
- ❌ Violating terms of service
- ❌ Gaining unfair advantages in competitive multiplayer

**ONLY USE** for:
- ✅ Offline single-player games
- ✅ Testing your own applications
- ✅ Accessibility assistance
- ✅ Content creation/demonstrations
- ✅ Speedrunning practice

The authors are not responsible for misuse of this software.

---

## 📧 Contact

Email: fabioandrajar@gmail.com

---

**Happy Recording! 🎮**
