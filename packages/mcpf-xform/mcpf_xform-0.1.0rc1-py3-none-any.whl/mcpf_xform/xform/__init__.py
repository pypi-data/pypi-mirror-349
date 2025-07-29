from typing import Any

import mcpf_core.core.routines as routines
from mcpf_core.func import constants


def set_default_input_from_variable(data: dict[str, Any]) -> dict[str, Any]:
    """
    It sets the value of the label constants.DEFAULT_IO_DATA_LABEL in "data"
    Yaml args:
             'input_label': It is a label in "data", whose value will be referenced by
             the other label constants.DEFAULT_IO_DATA_LABEL as well.
    """
    iterator = routines.pop_loop_iterator()
    meta = routines.get_meta_data(data)
    # default_arguments_values
    arg = {"input_label": constants.DEFAULT_IO_DATA_LABEL}
    # merging default values with current argument values
    if meta[constants.ARGUMENTS]:
        arg = arg | meta[constants.ARGUMENTS]
    # if the function part of a loop
    if iterator:
        arg["input_label"] = iterator

    data[constants.DEFAULT_IO_DATA_LABEL] = data[arg["input_label"]]
    routines.set_meta_in_data(data, meta)
    return data


def remove_data(data: dict[str, Any]) -> dict[str, Any]:
    """
    It removes a label (with its referenced value) from "data"
    Yaml args:
             'input':   It is a label in "data", which will be removed from "data",
                        by default it is constants.DEFAULT_IO_DATA_LABEL.
    """
    iterator = routines.pop_loop_iterator()
    meta = routines.get_meta_data(data)
    # default_arguments_values
    arg = {"input": constants.DEFAULT_IO_DATA_LABEL}
    # merging default values with current argument values
    if meta[constants.ARGUMENTS]:
        arg = arg | meta[constants.ARGUMENTS]
    # if the function part of a loop
    if iterator:
        arg["input"] = iterator
    del data[arg["input"]]

    routines.set_meta_in_data(data, meta)
    return data
