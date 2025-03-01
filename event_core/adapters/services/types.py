from typing import Dict, List, TypeAlias, Union

ScalarT: TypeAlias = Union[None, str, int, float, bool]

JsonT: TypeAlias = Union[
    None,
    str,
    int,
    bool,
    float,
    List["JsonT"],
    Dict["JsonT", "JsonT"],
]
