"""
Decorators Module
"""
import os
import sys
import numpy as np
from datetime import datetime
from ka_uts_uts.utils.fnc import Fnc
from ka_uts_log.log import Log


def timer(fnc):
    """
    Timer Decorator
    """
    def __wrapper(*args, **kwargs):
        start = datetime.now()
        fnc(*args, **kwargs)
        _fnc_name = Fnc.sh_fnc_name(fnc)
        end = datetime.now()
        elapse_time = end.timestamp() - start.timestamp()
        np_elapse_time = np.format_float_positional(elapse_time, trim='k')
        msg = f"{_fnc_name} elapse time [sec] = {np_elapse_time}"
        Log.info(msg, stacklevel=2)
    return __wrapper


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    Log.critical(exc_value.message, exc_info=(exc_type, exc_value, exc_traceback))


def handle_error(fnc):
    """
    Error Decorator
    """
    def __wrapper(*args, **kwargs):
        try:
            fnc(*args, **kwargs)
            os._exit(0)
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            handle_exception(exc_type, exc_value, exc_traceback)
            os._exit(1)
    return __wrapper
