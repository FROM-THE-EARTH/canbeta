
from pisat.calc import Navigator, Position
from pisat.model import (
    cached_loggable, LinkedDataModelBase, linked_loggable, loggable
)
from pisat.sensor import SamM8Q, Bno055
from pisat.util.deco import cached_property

import can09.parent.setting as setting


class RunningModel(LinkedDataModelBase):
    
    longitude = linked_loggable(SamM8Q.DataModel.longitude, setting.NAME_GPS)
    latitude = linked_loggable(SamM8Q.DataModel.latitude, setting.NAME_GPS)
    mag = linked_loggable(Bno055.DataModel.mag, setting.NAME_BNO055)
    euler = linked_loggable(Bno055.DataModel.euler, setting.NAME_BNO055)
    
    def setup(self):
        self._navi_goal = Navigator(Position(*setting.POSITION_GOAL))
        self._navi_child = Navigator(Position(*setting.POSITION_CHILD))
        
    @loggable
    def heading(self):
        return self.euler[0]
        
    @cached_property
    def position(self):
        return Position(self.longitude, self.latitude, degree=True)
        
    @cached_loggable
    def distance2goal(self):
        return self._navi_goal.delta_distance(self.postition)
    
    @cached_loggable
    def offset_angle2goal(self):
        heading = self.calc_heading(self.mag)
        return self._navi_goal.delta_angle(self.position, self.heading)
    
    @cached_loggable
    def distance2child(self):
        postition = Position(self.longitude, self.latitude, degree=True)
        return self._navi_child.delta_distance(postition)
    
    @cached_loggable
    def offset_angle2child(self):
        heading = self.calc_heading(self.mag)
        return self._navi_child.delta_angle(self.position, self.heading)
