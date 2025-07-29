from typing import Any

from newby.storage.storage import Storage


def retrieve(arguments: Any, storage: Storage, arg: str, tmp: bool = False) -> Any:
    _arg = getattr(arguments, arg)
    if _arg is not None:
        if tmp:
            if not getattr(arguments, arg + "_tmp"):
                storage.update({arg: _arg}, store=True)
        else:
            storage.update({arg: _arg}, store=True)
        return _arg
    elif getattr(storage, arg) is not None:
        return getattr(storage, arg)
    else:
        _arg = input(f"Please enter {arg}: \n")
        storage.update({arg: _arg}, store=True)

        return _arg
