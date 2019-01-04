from source.config.attribute.types import *


def convert_attributes_to_num(attributes, target):
    if target is AttributeKey.gender.value:
        converted = []
        for atr_id in range(0, len(attributes)):
            if (attributes[atr_id] == 'F'):
                converted.append(0)
            elif (attributes[atr_id] == 'M'):
                converted.append(1)
        return converted
    else:
        return attributes


def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False