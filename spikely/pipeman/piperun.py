import json
import os
import sys

from spikely import config as cfg


def run(elem_list_str):

    elem_jdict_list = json.loads(elem_list_str)
    elem_list = [cfg.cvt_dict_to_elem(elem_jdict)
                 for elem_jdict in elem_jdict_list]

    payload = None
    last_index = len(elem_list) - 1
    for index, elem in enumerate(elem_list):
        if index == last_index:
            next_elem = None
        else:
            next_elem = elem_list[index + 1]
        payload = elem.run(payload, next_elem)


def main():
    run(sys.argv[1])

    # Turns out that this is a very important call
    os._exit(1)

if __name__ == '__main__':
    main()
