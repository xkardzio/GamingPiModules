from . import KeyBinder
import json

example_config = '''
{
    "KeyConfig": [
        {
            "gpio_pin": 23,
            "profiles": [
                {
                    "name": "default",
                    "trigger": "w"
                }
            ]
        },
        {
            "gpio_pin": 24,
            "profiles": [
                {
                    "name": "default",
                    "trigger": "s"
                }
            ]
        },
        {
            "gpio_pin": 25,
            "profiles": [
                {
                    "name": "default",
                    "trigger": "a"
                }
            ]
        },
        {
            "gpio_pin": 12,
            "profiles": [
                {
                    "name": "default",
                    "trigger": "d"
                }
            ]
        },
        {
            "gpio_pin": 4,
            "profiles": [
                {
                    "name": "default",
                    "trigger": "1"
                }
            ]
        },
        {
            "gpio_pin": 27,
            "profiles": [
                {
                    "name": "default",
                    "trigger": "2"
                }
            ]
        },
        {
            "gpio_pin": 22,
            "profiles": [
                {
                    "name": "default",
                    "trigger": "3"
                }
            ]
        },
        {
            "gpio_pin": 6,
            "profiles": [
                {
                    "name": "default",
                    "trigger": "4"
                }
            ]
        },
        {
            "gpio_pin": 5,
            "profiles": [
                {
                    "name": "default",
                    "trigger": "5"
                }
            ]
        },
        {
            "gpio_pin": 26,
            "profiles": [
                {
                    "name": "default",
                    "trigger": "6"
                }
            ]
        }
    ]
}
'''

if __name__ == '__main__':
    print("****************\n")
    print('Module KeyBinder\n')
    print("****************\n\n")
    
    
    config = json.loads(example_config)
    kb = KeyBinder(config)
    kb.run()
