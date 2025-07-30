from .communicator import Sender
import numpy as np
from typing import Callable
from functools import partial
from enum import Enum
from .plotobject import PlotCall2D, PlotCall3D, PlotGroup, PlotItem, PlotObject

class MeshType(Enum):
    surface = 'surface'
    wireframe = 'wireframe'
    points = 'points'
    mesh = 'mesh'
    fancymesh = 'fancymesh'

class RemoteView3D:
    def __init__(self, sender: Sender = None):
        if sender is None:
            self.sender = Sender()
        else:
            self.sender = sender
        self.active_group: PlotGroup = None
        self.clear()

    def new_plot_group(self, name: str = 'NewPlotGroup'):
        new_group = PlotGroup(name, '3D',[])
        self.active_group = new_group

    def new_group(self, name: str):
        self.new_plot_group(name)
        return self

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.update()
    
    def send_plotgroup(self):
        self.sender.send_data(('plot',self.active_group.to_data()))

    def clear(self):
        self.sender.send_data(('clear',None))
        
    def quiver3d(self, x, y, z, u, v, w, color=(1,0,0)):
        kwargs = dict(color=color)
        pitem = PlotItem(PlotCall3D.QUIVER, (x,y,z,u,v,w),kwargs,((0,'x'),(1,'y'),(2,'z'),(3,'u'),(4,'v'),(5,'w')),dict())
        pobj = PlotObject('Quiver','quiver plot','3D',[pitem])
        self.active_group.add_object(pobj)

    def cs(self, origin: np.ndarray, basis: np.ndarray, length=1.0):
        x0, y0, z0 = origin
        xhat = basis[0,:]
        yhat = basis[1,:]
        zhat = basis[2,:]
        xx, xy, xz = basis[0,:]
        yx, yy, yz = basis[1,:]
        zx, zy, zz = basis[2,:]
        xax = PlotItem(PlotCall3D.QUIVER, (x0, y0, z0,x0+xx,y0+xy,z0+xz),{'color': (1,0,0), 'scale_mode':'scalar','scale_factor': length}, aux_data=[(xhat,'X')])
        yax = PlotItem(PlotCall3D.QUIVER, (x0, y0, z0,x0+yx,y0+yy,z0+yz),{'color': (0,1,0), 'scale_mode':'scalar','scale_factor': length}, aux_data=[(yhat,'Y')])
        zax = PlotItem(PlotCall3D.QUIVER, (x0, y0, z0,x0+zx,y0+zy,z0+zz),{'color': (0,0,1), 'scale_mode':'scalar','scale_factor': length}, aux_data=[(zhat,'Z'), (origin,'Origin')])
        plotobj = PlotObject('CS','cs','3D',[xax, yax, zax])
        self.active_group.add_object(plotobj)

    def zoom(self, zoomlevel):
        self.sender.send_data(('zoom', zoomlevel))
        
    def update(self):
        self.send_plotgroup()
        self.sender.send_data(('update',None))

    def reset(self):
        self.sender.send_data(('reset',None))


class RemoteView2D:
    pass

class RemoteViewer:
    def __init__(self):
        self.sender = Sender()
        self.v2d: RemoteView2D = RemoteView2D()
        self.v3d: RemoteView3D = RemoteView3D(self.sender)

    def new2d(self, name) -> RemoteView2D:
        self.v2d.new_group(name)
        return self.v2d
    
    def new3d(self, name) -> RemoteView3D:
        self.v3d.new_group(name)
        return self.v3d
