import json
import os


# ---------------------------------------
# GET API & SECRET KEYS FROM RES FOLDER
# ---------------------------------------
def get_key(name):
    keyfile = os.path.join(os.getcwd(), 'res', 'keys.json')
    try:
        with open(keyfile, 'r', encoding='utf-8') as kf:
            data = json.load(kf)
        return data[name]
    except KeyError as ke:
        return f'*** Error: Attribute {ke} not found.'
    except Exception as ex:
        return f'*** Error: {ex}.'


if __name__ == "__main__":
    print('This is not main!')
