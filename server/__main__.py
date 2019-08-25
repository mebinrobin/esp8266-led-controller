import logging as log
import numpy as np
import yaml
from server.device import Effects, Controller as DeviceController
from server.audio import Microphone

with open("../server_config.yml", 'r') as config_file:
    config = yaml.load(config_file)

log.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=log.DEBUG)

# Configuring device controller
dc = DeviceController(ips=config['device']['ips'], port=config['device']['port'])


# TODO: Move this to an other file
def process_samples(raw):
    raw = np.frombuffer(buffer=raw, dtype=np.int16)
    strength = int((np.abs(np.max(raw) - np.min(raw)) / 2**15)*10)

    log.info("Strength: %i", strength)

    # if display_bars < config.BAR_SUPER_THRESHOLD:
    #     display_bars *= config.BAR_MIN_AMPLIFIER

    if strength > config['led_pixels']:
        strength = config['led_pixels']

    dc.send_all(Effects.RAINBOW_WAVE.value + [100])
    # if strength >= config['super_bar_threshold']:
    #     dc.send_to(0, [1, 1])  # Desk
    #     dc.send_to(1, [1, 1])  # Window
    # else:
    #     dc.send_to(0, [1, 1])  # Desk
    #     dc.send_to(1, [1, 0])  # Window


if __name__ == '__main__':
    try:
        # TODO: Implement this correctly

        buffer_size = int(config['microphone']['sample_rate']/config['microphone']['refresh_rate'])
        with Microphone(config['microphone']['sample_rate'], config['microphone']['refresh_rate']) as (mic, stream):
            mic.start()
            while stream.is_active():
                process_samples(stream.read(buffer_size))

    except KeyboardInterrupt:
        exit()
