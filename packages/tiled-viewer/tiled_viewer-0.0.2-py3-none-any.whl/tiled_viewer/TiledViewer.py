# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class TiledViewer(Component):
    """A TiledViewer component.
ExampleComponent is an example component.
It takes a property, `label`, and
displays it.
It renders an input with the property `value`
which is editable by the user.

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- backgroundClassName (string; optional):
    The class name for the background.

- closeOnSelect (boolean; optional):
    Whether to close the viewer on select.

- contentClassName (string; optional):
    The class name for the content.

- enableStartupScreen (boolean; optional):
    Whether to enable the startup screen.

- isPopup (boolean; optional):
    Whether the viewer is a popup.

- selectedLinks (boolean | number | string | dict | list; optional):
    The content sent into the callback function from Tiled.

- singleColumnMode (boolean; optional):
    Whether to use single column mode.

- size (string; optional):
    The size of the viewer. 'small', 'medium', 'large'.

- tiledBaseUrl (string; optional):
    The base URL for the tiled viewer."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'tiled_viewer'
    _type = 'TiledViewer'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, backgroundClassName=Component.UNDEFINED, closeOnSelect=Component.UNDEFINED, contentClassName=Component.UNDEFINED, enableStartupScreen=Component.UNDEFINED, isPopup=Component.UNDEFINED, selectedLinks=Component.UNDEFINED, singleColumnMode=Component.UNDEFINED, tiledBaseUrl=Component.UNDEFINED, size=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'backgroundClassName', 'closeOnSelect', 'contentClassName', 'enableStartupScreen', 'isPopup', 'selectedLinks', 'singleColumnMode', 'size', 'tiledBaseUrl']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'backgroundClassName', 'closeOnSelect', 'contentClassName', 'enableStartupScreen', 'isPopup', 'selectedLinks', 'singleColumnMode', 'size', 'tiledBaseUrl']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(TiledViewer, self).__init__(**args)
