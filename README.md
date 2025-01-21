# MicroPython Simulation in Wokwi for VS Code

MicroPython project for an ESP32 that detects motion and displays the next bus departures (with delays) near my home.
 
![](https://i.imgur.com/1HAYWK4.png)

## Prerequisites

1. Install the [Wokwi for VS Code](https://marketplace.visualstudio.com/items?itemName=Wokwi.wokwi-vscode) extension.
2. Install the [mpremote](https://docs.micropython.org/en/latest/reference/mpremote.html) tool, e.g. `pip install mpremote`.

## Usage

1. Clone this project and open it in VS Code.
2. From the command palette, select "Wokwi: Start Simulator". You may need to activate your license first.
3. Select the "esp32-c3-lcd" folder.
4. While the simulator is running, open a command prompt, and type:

   ```python
   python3 -m mpremote connect port:rfc2217://localhost:4000 fs cp scripts/* :/ + run scripts/main.py
   ```

   This will connect to the simulator, copy all the scripts and run the `main.py` file on the board.
   Note: keep the simulator tab visible while running the command, otherwise the simulator will pause and the command will timeout.

#### Advanced usage

You can also use the `mpremote` tool to upload files to the simulator, install libraries, and open a REPL session. For example, the following command will connect to the simulator, upload the `main.py` file, install the `ssd1306` library, and then open a REPL session:

```python
python -m mpremote connect port:rfc2217://localhost:4000 fs cp main.py :main.py + mip install ssd1306 + repl
```

See the [mpremote documentation](https://docs.micropython.org/en/latest/reference/mpremote.html) for more details.

## What is used? 

### API
BVG schedules is using [bvg-rest](https://github.com/derhuerst/bvg-rest?tab=readme-ov-file) wrapper API. 

### Board and components
- The ESP-C3 board was chosen as it has the lowest power consumption, making it ideal for batttery-powered, wall-hang gadget.
- Screen and sensor are for the moment simulated. The diagram of the circuit can be found [here](https://wokwi.com/projects/417541800209963009).

## License

Licensed under the MIT license. See [LICENSE](LICENSE) for details.
