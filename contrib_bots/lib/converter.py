# See readme.md for instructions on running this code.

from __future__ import division
from past.utils import old_div

import copy
from math import log10, floor

# A dictionary allowing the conversion of each unit to its base unit.
# An entry consists of the unit's name, a constant number and a constant
# factor that need to be added and multiplied to convert the unit into
# the base unit in the last parameter.
UNITS = {'bit': [0, 1, 'bit'],
         'byte': [0, 8, 'bit'],
         'cubic-centimeter': [0, 0.000001, 'cubic-meter'],
         'cubic-decimeter': [0, 0.001, 'cubic-meter'],
         'liter': [0, 0.001, 'cubic-meter'],
         'cubic-meter': [0, 1, 'cubic-meter'],
         'cubic-inch': [0, 0.000016387064, 'cubic-meter'],
         'fluid-ounce': [0, 0.000029574, 'cubic-meter'],
         'cubic-foot': [0, 0.028316846592, 'cubic-meter'],
         'cubic-yard': [0, 0.764554857984, 'cubic-meter'],
         'teaspoon': [0, 0.0000049289216, 'cubic-meter'],
         'tablespoon': [0, 0.000014787, 'cubic-meter'],
         'cup': [0, 0.00023658823648491, 'cubic-meter'],
         'gram': [0, 1, 'gram'],
         'kilogram': [0, 1000, 'gram'],
         'ton': [0, 1000000, 'gram'],
         'ounce': [0, 28.349523125, 'gram'],
         'pound': [0, 453.59237, 'gram'],
         'kelvin': [0, 1, 'kelvin'],
         'celsius': [273.15, 1, 'kelvin'],
         'fahrenheit': [255.372222, 0.555555, 'kelvin'],
         'centimeter': [0, 0.01, 'meter'],
         'decimeter': [0, 0.1, 'meter'],
         'meter': [0, 1, 'meter'],
         'kilometer': [0, 1000, 'meter'],
         'inch': [0, 0.0254, 'meter'],
         'foot': [0, 0.3048, 'meter'],
         'yard': [0, 0.9144, 'meter'],
         'mile': [0, 1609.344, 'meter'],
         'nautical-mile': [0, 1852, 'meter'],
         'square-centimeter': [0, 0.0001, 'square-meter'],
         'square-decimeter': [0, 0.01, 'square-meter'],
         'square-meter': [0, 1, 'square-meter'],
         'square-kilometer': [0, 1000000, 'square-meter'],
         'square-inch': [0, 0.00064516, 'square-meter'],
         'square-foot': [0, 0.09290304, 'square-meter'],
         'square-yard': [0, 0.83612736, 'square-meter'],
         'square-mile': [0, 2589988.110336, 'square-meter'],
         'are': [0, 100, 'square-meter'],
         'hectare': [0, 10000, 'square-meter'],
         'acre': [0, 4046.8564224, 'square-meter']}

PREFIXES = {'atto': -18,
            'femto': -15,
            'pico': -12,
            'nano': -9,
            'micro': -6,
            'milli': -3,
            'centi': -2,
            'deci': -1,
            'deca': 1,
            'hecto': 2,
            'kilo': 3,
            'mega': 6,
            'giga': 9,
            'tera': 12,
            'peta': 15,
            'exa': 18}

ALIASES = {'a': 'are',
           'ac': 'acre',
           'c': 'celsius',
           'cm': 'centimeter',
           'cm2': 'square-centimeter',
           'cm3': 'cubic-centimeter',
           'cm^2': 'square-centimeter',
           'cm^3': 'cubic-centimeter',
           'dm': 'decimeter',
           'dm2': 'square-decimeter',
           'dm3': 'cubic-decimeter',
           'dm^2': 'square-decimeter',
           'dm^3': 'cubic-decimeter',
           'f': 'fahrenheit',
           'fl-oz': 'fluid-ounce',
           'ft': 'foot',
           'ft2': 'square-foot',
           'ft3': 'cubic-foot',
           'ft^2': 'square-foot',
           'ft^3': 'cubic-foot',
           'g': 'gram',
           'ha': 'hectare',
           'in': 'inch',
           'in2': 'square-inch',
           'in3': 'cubic-inch',
           'in^2': 'square-inch',
           'in^3': 'cubic-inch',
           'k': 'kelvin',
           'kg': 'kilogram',
           'km': 'kilometer',
           'km2': 'square-kilometer',
           'km^2': 'square-kilometer',
           'l': 'liter',
           'lb': 'pound',
           'm': 'meter',
           'm2': 'square-meter',
           'm3': 'cubic-meter',
           'm^2': 'square-meter',
           'm^3': 'cubic-meter',
           'mi': 'mile',
           'mi2': 'square-mile',
           'mi^2': 'square-mile',
           'nmi': 'nautical-mile',
           'oz': 'ounce',
           't': 'ton',
           'tbsp': 'tablespoon',
           'tsp': 'teaspoon',
           'y': 'yard',
           'y2': 'square-yard',
           'y3': 'cubic-yard',
           'y^2': 'square-yard',
           'y^3': 'cubic-yard'}

HELP_MESSAGE = ('Converter usage:\n'
                '`@convert <number> <unit_from> <unit_to>`\n'
                'Converts `number` in the unit <unit_from> to '
                'the <unit_to> and prints the result\n'
                '`number`: integer or floating point number, e.g. 12, 13.05, 0.002\n'
                '<unit_from> and <unit_to> are two of the following units:\n'
                '* square-centimeter (cm^2, cm2), square-decimeter (dm^2, dm2), '
                'square-meter (m^2, m2), square-kilometer (km^2, km2),'
                ' square-inch (in^2, in2), square-foot (ft^2, ft2), square-yard (y^2, y2), '
                ' square-mile(mi^2, mi2),  are (a), hectare (ha), acre (ac)\n'
                '* bit, byte\n'
                '* centimeter (cm), decimeter(dm), meter (m),'
                ' kilometer (km), inch (in), foot (ft), yard (y),'
                ' mile (mi), nautical-mile (nmi)\n'
                '* Kelvin (K), Celsius(C), Fahrenheit (F)\n'
                '* cubic-centimeter (cm^3, cm3), cubic-decimeter (dm^3, dm3), liter (l), '
                'cubic-meter (m^3, m3), cubic-inch (in^3, in3), fluid-ounce (fl-oz), '
                'cubic-foot (ft^3, ft3), cubic-yard (y^3, y3)\n'
                '* gram (g), kilogram (kg), ton (t), ounce (oz), pound(lb)\n'
                '* (metric only, U.S. and imperial units differ slightly:) teaspoon (tsp), tablespoon (tbsp), cup\n\n\n'
                'Allowed prefixes are:\n'
                '* atto, pico, femto, nano, micro, milli, centi, deci\n'
                '* deca, hecto, kilo, mega, giga, tera, peta, exa\n\n\n'
                'Usage examples:\n'
                '* `@convert 12 celsius fahrenheit`\n'
                '* `@convert 0.002 kilomile millimeter`\n'
                '* `@convert 31.5 square-mile ha`\n'
                '* `@convert 56 g lb`\n')

QUICK_HELP = 'Enter `@convert help` for help on using the converter.'

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

# Rounds the number 'x' to 'digits' significant digits.
# A normal 'round()' would round the number to an absolute amount of
# fractional decimals, e.g. 0.00045 would become 0.0.
# 'round_to()' rounds only the digits that are not 0.
# 0.00045 would then become 0.0005.
def round_to(x, digits):
    return round(x, digits-int(floor(log10(abs(x)))))

class ConverterHandler(object):
    '''
    This plugin allows users to make conversions between various units,
    e.g. Celsius to Fahrenheit, or kilobytes to gigabytes.
    It looks for messages of the format
    '@convert <number> <unit_from> <unit_to>'
    The message '@convert help' posts a short description of how to use
    the plugin, along with a list of all supported units.
    '''

    def usage(self):
        return '''
               This plugin allows users to make conversions between
               various units, e.g. Celsius to Fahrenheit,
               or kilobytes to gigabytes. It looks for messages of
               the format '@convert <number> <unit_from> <unit_to>'
               The message '@convert help' posts a short description of
               how to use the plugin, along with a list of
               all supported units.
               '''

    def triage_message(self, message, client):
        return '@convert' in message['content']

    def handle_message(self, message, client, state_handler):
        content = message['content']

        words = content.lower().split()
        convert_indexes = [i for i, word in enumerate(words) if word == "@convert"]
        results = []

        for convert_index in convert_indexes:
            if (convert_index + 1) < len(words) and words[convert_index + 1] == 'help':
                results.append(HELP_MESSAGE)
                continue
            if (convert_index + 3) < len(words):
                number = words[convert_index + 1]
                unit_from = ALIASES.get(words[convert_index + 2], words[convert_index + 2])
                unit_to = ALIASES.get(words[convert_index + 3], words[convert_index + 3])
                exponent = 0

                if not is_float(number):
                    results.append(number + ' is not a valid number. ' + QUICK_HELP)
                    continue

                number = float(number)
                number_res = copy.copy(number)

                for key, exp in PREFIXES.items():
                    if unit_from.startswith(key):
                        exponent += exp
                        unit_from = unit_from[len(key):]
                    if unit_to.startswith(key):
                        exponent -= exp
                        unit_to = unit_to[len(key):]

                uf_to_std = UNITS.get(unit_from, False)
                ut_to_std = UNITS.get(unit_to, False)

                if uf_to_std is False:
                    results.append(unit_from + ' is not a valid unit. ' + QUICK_HELP)
                if ut_to_std is False:
                    results.append(unit_to + ' is not a valid unit.' + QUICK_HELP)
                if uf_to_std is False or ut_to_std is False:
                    continue

                base_unit = uf_to_std[2]
                if uf_to_std[2] != ut_to_std[2]:
                    unit_from = unit_from.capitalize() if uf_to_std[2] == 'kelvin' else unit_from
                    results.append(unit_to.capitalize() + ' and ' + unit_from +
                                   ' are not from the same category. ' + QUICK_HELP)
                    continue

                # perform the conversion between the units
                number_res *= uf_to_std[1]
                number_res += uf_to_std[0]
                number_res -= ut_to_std[0]
                number_res /= ut_to_std[1]

                if base_unit == 'bit':
                    number_res *= 1024 ** (old_div(exponent, float(3)))
                else:
                    number_res *= 10 ** exponent
                number_res = round_to(number_res, 7)

                results.append('{} {} = {} {}'.format(number,
                                                      words[convert_index + 2],
                                                      number_res,
                                                      words[convert_index + 3]))

            else:
                results.append('Too few arguments given. ' + QUICK_HELP)

        new_content = ''
        for idx, result in enumerate(results, 1):
            new_content += ((str(idx) + '. conversion: ') if len(results) > 1 else '') + result + '\n'

        client.send_message(dict(
            type='stream',
            to=message['display_recipient'],
            subject=message['subject'],
            content=new_content,
        ))

handler_class = ConverterHandler
