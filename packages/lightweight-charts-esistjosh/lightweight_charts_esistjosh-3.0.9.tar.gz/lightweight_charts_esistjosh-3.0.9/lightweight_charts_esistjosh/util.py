import asyncio
import json
from datetime import datetime
from random import choices
from typing import Literal, Union
from numpy import isin
import pandas as pd


class Pane:
    def __init__(self, window):
        from lightweight_charts_esistjosh import Window
        self.win: Window = window
        self.run_script = window.run_script
        self.bulk_run = window.bulk_run
        if hasattr(self, 'id'):
            return
        self.id = Window._id_gen.generate()


class IDGen(list):
    ascii = 'abcdefghijklmnopqrstuvwxyz'

    def generate(self) -> str:
        var = ''.join(choices(self.ascii, k=8))
        if var not in self:
            self.append(var)
            return f'window.{var}'
        self.generate()



def parse_event_message(window, string):
    """
    Parses messages of the form "handlerName_~_arg1;;;arg2;;;…"
    and safely looks up the handler, ignoring any undefined names.
    """
    name, args = string.split('_~_')
    args = args.split(';;;')

    # safe lookup—if there's no handler for this name, just no-op
    func = window.handlers.get(name)
    if func is None:
        import logging
        logging.getLogger(__name__).debug(
            "parse_event_message: no handler for '%s', ignoring", name
        )
        # return a no-op plus empty args
        return (lambda *a, **kw: None, ())

    return func, args


#def js_data(data: Union[pd.DataFrame, pd.Series]) -> str:
#    """
#    Convert a pandas DataFrame or Series into a JSON-formatted string.
#    For DataFrames, if a 'close' column exists, a 'value' column is created identical to 'close'.
#    Filters out None and NaN values for DataFrames.
#
#    Parameters:
#    - data: Union[pd.DataFrame, pd.Series]
#        The pandas DataFrame or Series to convert.
#
#    Returns:
#    - str
#        A JSON-formatted string representing the cleaned data.
#    """
#    try:
#        if isinstance(data, pd.DataFrame):
#            df = data.copy()  # Create a copy to avoid modifying the original DataFrame
#
#            # Step 1: Check for 'close' column and create 'value' column if it exists
#            if 'close' in df.columns:
#                df['value'] = df['close']
#                print("Added 'value' column based on 'close' column.")
#
#            # Step 2: Convert DataFrame to list of records (dictionaries)
#            records = df.to_dict(orient='records')
#
#            # Step 3: Filter out None and NaN values from each record
#            filtered_records = [
#                {k: v for k, v in record.items() if v is not None and not pd.isna(v)}
#                for record in records
#            ]
#
#            # Optional: If 'value' column was added and you want to ensure it's present,
#            # you can add additional checks or processing here.
#
#            # Convert the filtered records to JSON
#            json_output = json.dumps(filtered_records, indent=2)
#            return json_output
#
#        elif isinstance(data, pd.Series):
#            # Convert Series to dictionary
#            series_dict = data.to_dict()
#
#            # Optional: If needed, you can add a 'value' field based on the Series values
#            # For example, if the Series represents 'close' values:
#            # series_dict['value'] = series_dict.get('close', series_dict)
#
#            # Currently, no filtering is applied to Series
#            json_output = json.dumps(series_dict, indent=2)
#            return json_output
#
#        else:
#            raise ValueError("Input data must be a pandas DataFrame or Series.")
#
#    except Exception as e:
#        raise ValueError(f"Error converting data to JSON: {e}")

def js_data(data: Union[pd.DataFrame, pd.Series]):
    if isinstance(data, pd.DataFrame):
        d = data.to_dict(orient='records')
        filtered_records = [{k: v for k, v in record.items() if v is not None and not pd.isna(v)} for record in d]
    else:
        d = data.to_dict()
        filtered_records = {k: v for k, v in d.items()}
    return json.dumps(filtered_records, indent=2)


def snake_to_camel(s: str):
    components = s.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

def js_json(d: dict):
    filtered_dict = {}
    for key, val in d.items():
        if key in ('self') or val in (None,):
            continue
        if '_' in key:
            key = snake_to_camel(key)
        filtered_dict[key] = val
    return f"JSON.parse('{json.dumps(filtered_dict)}')"


def jbool(b: bool): return 'true' if b is True else 'false' if b is False else None


LINE_STYLE = Literal['solid', 'dotted', 'dashed', 'large_dashed', 'sparse_dotted']

MARKER_POSITION = Literal['above', 'below', 'inside']

MARKER_SHAPE = Literal['arrow_up', 'arrow_down', 'circle', 'square']

CROSSHAIR_MODE = Literal['normal', 'magnet', 'hidden']

PRICE_SCALE_MODE = Literal['normal', 'logarithmic', 'percentage', 'index100']

TIME = Union[datetime, pd.Timestamp, str, float]

NUM = Union[float, int]

FLOAT = Literal['left', 'right', 'top', 'bottom']

CANDLE_SHAPE = Literal['Rectangle','Rounded','Ellipse','Arrow','Polygon','Bar','3d']

TOOLBOX_MODE = Literal['default', 'legacy', 'disabled']

def as_enum(value, string_types):
    types = string_types.__args__
    return -1 if value not in types else types.index(value)


def marker_shape(shape: MARKER_SHAPE):
    return {
        'arrow_up': 'arrowUp',
        'arrow_down': 'arrowDown',
    }.get(shape) or shape


def marker_position(p: MARKER_POSITION):
    return {
        'above': 'aboveBar',
        'below': 'belowBar',
        'inside': 'inBar',
    }.get(p)


class Emitter:
    def __init__(self):
        self._callable = None

    def __iadd__(self, other):
        self._callable = other
        return self

    def _emit(self, *args):
        if self._callable:
            if asyncio.iscoroutinefunction(self._callable):
                asyncio.create_task(self._callable(*args))
            else:
                self._callable(*args)


class JSEmitter:
    def __init__(self, chart, name, on_iadd, wrapper=None):
        self._on_iadd = on_iadd
        self._chart = chart
        self._name = name
        self._wrapper = wrapper

    def __iadd__(self, other):
        def final_wrapper(*arg):
            other(self._chart, *arg) if not self._wrapper else self._wrapper(other, self._chart, *arg)
        async def final_async_wrapper(*arg):
            await other(self._chart, *arg) if not self._wrapper else await self._wrapper(other, self._chart, *arg)

        self._chart.win.handlers[self._name] = final_async_wrapper if asyncio.iscoroutinefunction(other) else final_wrapper
        self._on_iadd(other)
        return self


class Events:
    def __init__(self, chart):
        self.new_bar = Emitter()
        self.search = JSEmitter(chart, f'search{chart.id}',
            lambda o: chart.run_script(f'''
            Lib.Handler.makeSpinner({chart.id})
            {chart.id}.search = Lib.Handler.makeSearchBox({chart.id})
            ''')
        )
        salt = chart.id[chart.id.index('.')+1:]
        self.range_change = JSEmitter(chart, f'range_change{salt}',
            lambda o: chart.run_script(f'''
            let checkLogicalRange{salt} = (logical) => {{
                {chart.id}.chart.timeScale().unsubscribeVisibleLogicalRangeChange(checkLogicalRange{salt})
                
                let barsInfo = {chart.id}.series.barsInLogicalRange(logical)
                if (barsInfo) window.callbackFunction(`range_change{salt}_~_${{barsInfo.barsBefore}};;;${{barsInfo.barsAfter}}`)
                    
                setTimeout(() => {chart.id}.chart.timeScale().subscribeVisibleLogicalRangeChange(checkLogicalRange{salt}), 50)
            }}
            {chart.id}.chart.timeScale().subscribeVisibleLogicalRangeChange(checkLogicalRange{salt})
            '''),
            wrapper=lambda o, c, *arg: o(c, *[float(a) for a in arg])
        )

        self.click = JSEmitter(chart, f'subscribe_click{salt}',
            lambda o: chart.run_script(f'''
            let clickHandler{salt} = (param) => {{
                if (!param.point) return;
                const time = {chart.id}.chart.timeScale().coordinateToTime(param.point.x)
                const price = {chart.id}.series.coordinateToPrice(param.point.y);
                window.callbackFunction(`subscribe_click{salt}_~_${{time}};;;${{price}}`)
            }}
            {chart.id}.chart.subscribeClick(clickHandler{salt})
            '''),
            wrapper=lambda func, c, *args: func(c, *[float(a) if a != 'null' else None for a in args])
        )
        self.save_defaults = Emitter()
        self.save_script = Emitter()
class BulkRunScript:
    def __init__(self, script_func):
        self.enabled = False
        self.scripts = []
        self.script_func = script_func

    def __enter__(self):
        self.enabled = True

    def __exit__(self, *args):
        self.enabled = False
        self.script_func('\n'.join(self.scripts))
        self.scripts = []

    def add_script(self, script):
        self.scripts.append(script)
