# AUTO GENERATED FILE - DO NOT EDIT

import typing  # noqa: F401
import numbers # noqa: F401
from typing_extensions import TypedDict, NotRequired, Literal # noqa: F401
from dash.development.base_component import Component, _explicitize_args
try:
    from dash.development.base_component import ComponentType # noqa: F401
except ImportError:
    ComponentType = typing.TypeVar("ComponentType", bound=Component)


class Mviewer(Component):
    """A Mviewer component.


Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- box (dict; optional):
    Box region selected (returned).

    `box` is a dict with keys:

    - xmin (number; required)

    - ymin (number; required)

    - dx (number; required)

    - dy (number; required)

    - screenXmin (number; required)

    - screenYmin (number; required)

    - screenDx (number; required)

    - screenDy (number; required)

- cmdStr (string; optional):
    Command string (returned).

- cutoutDesc (string; optional):
    Command string.

- height (number; optional):
    App window height.

- img (string; required):
    Main image.

- imgHeight (number; required):
    Main image height.

- imgWidth (number; required):
    Main image width.

- inset (string; required):
    Inset image (to show region of main image) currently being
    displayed.

- insetHeight (number; required):
    Inset image height.

- insetWidth (number; required):
    Inset image width.

- pick (dict; optional):
    Location of a location pick (returned).

    `pick` is a dict with keys:

    - x (number; required)

    - y (number; required)

- width (number; optional):
    App window width.

- zoombox (dict; optional):
    Visible window box and zoom factor.

    `zoombox` is a dict with keys:

    - zoom (number; required)

    - width (number; required)

    - height (number; required)

    - xmin (number; required)

    - ymin (number; required)

    - dx (number; required)

    - dy (number; required)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'mviewer'
    _type = 'Mviewer'
    Zoombox = TypedDict(
        "Zoombox",
            {
            "zoom": typing.Union[int, float, numbers.Number],
            "width": typing.Union[int, float, numbers.Number],
            "height": typing.Union[int, float, numbers.Number],
            "xmin": typing.Union[int, float, numbers.Number],
            "ymin": typing.Union[int, float, numbers.Number],
            "dx": typing.Union[int, float, numbers.Number],
            "dy": typing.Union[int, float, numbers.Number]
        }
    )

    Box = TypedDict(
        "Box",
            {
            "xmin": typing.Union[int, float, numbers.Number],
            "ymin": typing.Union[int, float, numbers.Number],
            "dx": typing.Union[int, float, numbers.Number],
            "dy": typing.Union[int, float, numbers.Number],
            "screenXmin": typing.Union[int, float, numbers.Number],
            "screenYmin": typing.Union[int, float, numbers.Number],
            "screenDx": typing.Union[int, float, numbers.Number],
            "screenDy": typing.Union[int, float, numbers.Number]
        }
    )

    Pick = TypedDict(
        "Pick",
            {
            "x": typing.Union[int, float, numbers.Number],
            "y": typing.Union[int, float, numbers.Number]
        }
    )

    @_explicitize_args
    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        img: typing.Optional[str] = None,
        imgWidth: typing.Optional[typing.Union[int, float, numbers.Number]] = None,
        imgHeight: typing.Optional[typing.Union[int, float, numbers.Number]] = None,
        inset: typing.Optional[str] = None,
        insetWidth: typing.Optional[typing.Union[int, float, numbers.Number]] = None,
        insetHeight: typing.Optional[typing.Union[int, float, numbers.Number]] = None,
        width: typing.Optional[typing.Union[int, float, numbers.Number]] = None,
        height: typing.Optional[typing.Union[int, float, numbers.Number]] = None,
        cutoutDesc: typing.Optional[str] = None,
        zoombox: typing.Optional["Zoombox"] = None,
        box: typing.Optional["Box"] = None,
        pick: typing.Optional["Pick"] = None,
        cmdStr: typing.Optional[str] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'box', 'cmdStr', 'cutoutDesc', 'height', 'img', 'imgHeight', 'imgWidth', 'inset', 'insetHeight', 'insetWidth', 'pick', 'width', 'zoombox']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'box', 'cmdStr', 'cutoutDesc', 'height', 'img', 'imgHeight', 'imgWidth', 'inset', 'insetHeight', 'insetWidth', 'pick', 'width', 'zoombox']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['img', 'imgHeight', 'imgWidth', 'inset', 'insetHeight', 'insetWidth']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(Mviewer, self).__init__(**args)
