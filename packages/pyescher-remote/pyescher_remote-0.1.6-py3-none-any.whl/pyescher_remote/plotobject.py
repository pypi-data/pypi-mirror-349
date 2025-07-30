from enum import Enum
from typing import Any, Literal, Union
from numpy import ndarray
from numpy import min as npmin
from numpy import max as npmax


class PlotCall3D(Enum):
    QUIVER = 'quiver'
    LINE = 'line'
    MESH = 'mesh'
    PLOT = 'plot'
    SCATTER = 'scatter'
    SURF = 'surf'

class PlotCall2D(Enum):
    LINE = 'line'
    SCATTER = 'scatter'
    HIST = 'hist'

def _parse_data_to_summary(data: Union[float, complex, int, str, ndarray, tuple, list]) -> tuple[str, str]:
    if isinstance(data, (float, complex, int)):
        return 'Number', f'{data:.2f}'
    elif isinstance(data, ndarray):
        if data.size <= 10:
            return 'Array', f'{data}'
        return 'Array', f'{data.shape}[{npmin(data):.2f} - {npmax(data):.2f}] dtype = {data.dtype}'
    elif isinstance(data, str):
        return 'String', data
    elif isinstance(data, list):
        return 'List', str(data[:10])
    elif isinstance(data, tuple):
        return 'Tuple', str(data[:10])
    else:
        return 'Aux', str(data)

class PlotItem:

    def __init__(self, pc: Union[PlotCall3D, PlotCall2D], 
                 args: tuple, 
                 kwargs: dict, 
                 summarized_args: list[tuple[int, str]] = None, 
                 summarized_kwargs: dict[str, Any] = None,
                 aux_data: list[tuple[Any, str]] = None):

        if summarized_args is None:
            summarized_args = ()
        if summarized_kwargs is None:
            summarized_kwargs = dict()
        if aux_data is None:
            aux_data = []
        self.plot_call = pc
        self.args: tuple = args
        self.kwargs: dict[str, Any] = kwargs
        self.summarized_args: tuple[int] = summarized_args
        self.summarized_kwargs: dict[str, Any] = summarized_kwargs
        self.aux_data: list[tuple[Any, str]] = aux_data

    @staticmethod
    def from_data(data: dict):
        dim = data['DIM']
        call = data['CALL']
        args = data['ARGS']
        kwargs = data['KWARGS']
        summarized_args: tuple[tuple[int, str]] = data['SUMMARIZED_ARGS']
        summarized_kwargs: tuple[str] = data['SUMMARIZED_KWARGS']
        aux_data: list = data['AUX_DATA']

        if dim == '3D':
            plotcall = PlotCall3D(call)
        else:
            plotcall = PlotCall2D(call)
        return PlotItem(plotcall, args, kwargs, summarized_args, summarized_kwargs, aux_data)

    
    def to_data(self) -> dict:
        return {
            'DIM': '3D' if isinstance(self.plot_call, PlotCall3D) else '2D',
            'CALL': self.plot_call.value,
            'ARGS': self.args,
            'KWARGS': self.kwargs,
            'SUMMARIZED_ARGS': self.summarized_args,
            'SUMMARIZED_KWARGS': self.summarized_kwargs,
            'AUX_DATA': self.aux_data,
        }
    
    def summarized_data(self) -> list[tuple[str, str, str]]:
        data = []
        for key, value in self.summarized_kwargs.items():
            typename, datastring = _parse_data_to_summary(value)
            data.append((key, typename, datastring))
        for index, name in self.summarized_args:
            typename, datastring = _parse_data_to_summary(self.args[index])
            data.append((name, typename, datastring))
        for auxdata, name in self.aux_data:
            typename, datastring = _parse_data_to_summary(auxdata)
            data.append((name, typename, datastring))
        return data
    
    
class PlotObject:

    def __init__(self, 
                 name: str,
                 plottype: str,
                 dim: str,
                 plotitems: list[PlotItem]):
        self.active: bool = True
        self.name = name
        self.plottype: str = plottype
        self.dim: Literal['3D','2D'] = dim
        self.plotitems = plotitems
    
    @staticmethod
    def from_data(data: dict):
        name = data['NAME']
        dim = data['DIM']
        plottype = data['PLOTTYPE']
        plotitems = [PlotItem.from_data(item) for item in data['ITEMS']]
        return PlotObject(name, plottype, dim, plotitems)
    
    def to_data(self) -> dict:
        return {
            'NAME': self.name,
            'PLOTTYPE': self.plottype,
            'DIM': self.dim,
            'ITEMS': [item.to_data() for item in self.plotitems]
        }
    
    def table_items(self) -> list[tuple[str, str, str]]:
        summarized_data = []
        for item in self.plotitems:
            summarized_data.extend(item.summarized_data())
        return summarized_data
    
class PlotGroup:

    def __init__(self, 
                 name: str,
                 dim: Literal['3D','2D'],
                 plotobjects: list[PlotObject]):
        self.name = name
        self.dim: Literal['3D', '2D'] = dim
        self.plotobjects = plotobjects

    @staticmethod
    def from_data(data: dict):
        name = data['NAME']
        dim = data['DIM']
        plotobjects = [PlotObject.from_data(item) for item in data['ITEMS']]
        return PlotGroup(name, dim, plotobjects)
    
    def add_object(self, plotobj: PlotObject) -> None:
        self.plotobjects.append(plotobj)

    def to_data(self) -> dict:
        return {
            'NAME': self.name,
            'DIM': self.dim,
            'ITEMS': [item.to_data() for item in self.plotobjects]
        }
    
    def tree_data(self) -> list[tuple[str, str]]:
        summarized_data = []
        for item in self.plotobjects:
            summarized_data.append((item.name, item.plottype))
        return summarized_data
    
    def plot_items(self) -> list[PlotItem]:
        items = []
        for item in self.plotobjects:
            items.extend(item.plotitems)
        return items