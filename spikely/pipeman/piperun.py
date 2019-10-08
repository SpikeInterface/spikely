import json
import sys

from spikely import config as cfg


def run(elem_list_str):

    elem_jdict_list = json.loads(elem_list_str)
    elem_list = [cfg.cvt_dict_to_elem(elem_jdict)
                 for elem_jdict in elem_jdict_list]

    payload = None
    last_elem_index = len(elem_list) - 1
    for count, elem in enumerate(elem_list):
        next_elem = elem_list[count + 1] \
            if count < last_elem_index else None
        payload = elem.run(payload, next_elem)


def main():
    run(sys.argv[1])
    sys.exit()


if __name__ == '__main__':
    main()
