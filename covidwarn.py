from gpiozero import LED
from time import sleep
import requests
import json

def get_data():
    r = requests.get('https://api.covidtracking.com/v1/states/ny/current.json', allow_redirects=True)
    j = json.loads(r.content)

    positivity_rate = float(j["positiveIncrease"]) / float(j["totalTestResultsIncrease"])

    return positivity_rate

if __name__ == '__main__':
    yellow_led = LED(2)
    red_led = LED(3)

    warning_threshold = 0.02
    danger_threshold = 0.05
    seconds_in_day = 86400

    yellow_led.off()
    red_led.off()

    while True:
        p_rate = get_data()

        print("Positivity rate: %f" % p_rate)

        if p_rate > danger_threshold:
            yellow_led.off()
            red_led.on()
        elif p_rate > warning_threshold:
            red_led.off()
            yellow_led.on()
        else:
            red_led.off()
            yellow_led.off()

        sleep(seconds_in_day)
