from pydantic import BaseModel
from pydantic import Field
from typing import List
from typing import Optional
from typing import Union
from typing import Literal
from datetime import datetime
from datetime import date
from pydantic import constr


class ChannelModel(BaseModel):
    channel_id: str = Field(max_length=8, default='A0001')
    # channel_group_id: str = 'chgrp01'
    distance_along_fiber: float
    x_coordinate: float
    y_coordinate: float
    elevation_above_sea_level: Optional[float] = None
    depth_below_surface: Optional[float] = None
    strike: Optional[float] = None
    dip: Optional[float] = None


class ChannelGroupModel(BaseModel):
    channel_group_id: str = Field(max_length=8, default='chgrp01')
    # interrogator_id: str = 'inter01'
    # acquisition_id: str = 'acqui01'
    cable_id: str = Field(max_length=8, default='cable01')
    fiber_id: str = Field(max_length=8, default='fiber01')
    coordinate_generation_date: Union[datetime, date] = datetime.utcnow()
    coordinate_system: Literal['geographic', 'UTM', 'local'] = 'geographic'
    reference_frame: str = 'WGS84'
    location_method: Optional[str] = ''
    distance_along_fiber_unit: str = 'meter'
    x_coordinate_unit: Literal['decimal degree', 'meter'] = 'meter'
    uncertainty_in_x_coordinate: Optional[float] = None
    uncertainty_in_x_coordinate_unit: Optional[str] = ''
    y_coordinate_unit: Literal['decimal degree', 'meter'] = 'meter'
    uncertainty_in_y_coordinate: Optional[float] = None
    uncertainty_in_y_coordinate_unit: Optional[str] = ''
    elevation_above_sea_level_unit: Optional[str] = ''
    uncertainty_in_elevation: Optional[float] = None
    uncertainty_in_elevation_unit: Optional[str] = ''
    depth_below_surface_unit: Optional[str] = ''
    uncertainty_in_depth: Optional[float] = None
    uncertainty_in_depth_unit: Optional[str] = ''
    strike_unit: Optional[str] = ''
    uncertainty_in_strike: Optional[float] = None
    uncertainty_in_strike_unit: Optional[str] = ''
    dip_unit: Optional[str] = ''
    uncertainty_in_dip: Optional[float] = None
    uncertainty_in_dip_unit: Optional[str] = ''
    first_usable_channel_id: Optional[str] = ''
    last_usable_channel_id: Optional[str] = ''
    comment: Optional[str] = ''
    channels: Optional[List[ChannelModel]] = Field(default=list())


class AcquisitionModel(BaseModel):
    acquisition_id: str = Field(max_length=8, default='acqui01')
    acquisition_start_time: Union[datetime, date] = datetime(1980, 1, 1)
    acquisition_end_time: Union[datetime, date] = datetime(2999, 12, 31)
    acquisition_sample_rate: float = Field(gt=0, default=None)
    acquisition_sample_rate_unit: str = Field(default='Hertz')
    gauge_length: float = Field(gt=0, default=None)
    gauge_length_unit: str = 'meter'
    unit_of_measure: Literal['count', 'strain', 'strain-rate', 'velocity'] = ''
    number_of_channels: int = Field(gt=0, default=None)
    spatial_sampling_interval: float = Field(gt=0, default=None)
    spatial_sampling_interval_unit: str = 'meter'
    pulse_rate: Optional[float] = Field(ge=0, default=None)
    pulse_rate_unit: Optional[str] = ''
    pulse_width: Optional[float] = None
    pulse_width_unit: Optional[str] = ''
    comment: Optional[str] = ''
    channel_groups: List[ChannelGroupModel] = Field(default=list())


class InterrogatorModel(BaseModel):
    interrogator_id: str = Field(max_length=8, default='inter01')
    manufacturer: str = 'COMPLETE!'
    model: str = 'COMPLETE!'
    serial_number: Optional[str] = ''
    firmware_version: Optional[str] = ''
    comment: Optional[str] = ''
    acquisitions: List[AcquisitionModel] = Field(default=[AcquisitionModel()])


class FiberModel(BaseModel):
    fiber_id: str = Field(max_length=8, default='fiber01')
    # cable_id: str = 'cable01'
    fiber_geometry: str = 'COMPLETE!'
    fiber_mode: Literal['single-mode', 'multi-mode', 'other'] = Field(default='single-mode')
    fiber_refraction_index: float = Field(default=1.4681)
    fiber_winding_angle: Optional[float] = None
    fiber_start_location: Optional[float] = Field(ge=0, default=None)
    fiber_start_location_unit: Optional[str] = ''
    fiber_end_location: Optional[float] = Field(ge=0, default=None)
    fiber_end_location_unit: Optional[str] = ''
    fiber_optical_length: Optional[float] = Field(ge=0, default=None)
    fiber_optical_length_unit: Optional[str] = ''
    fiber_one_way_attenuation: Optional[float] = Field(ge=0, default=None)
    fiber_one_way_attenuation_unit: Optional[str] = ''
    comment: Optional[str] = ''


class CableModel(BaseModel):
    cable_id: str = Field(max_length=8, default='cable01')
    cable_bounding_box: List[float] = Field(default=[0, 0, 0, 0])
    cable_owner: Optional[str] = ''
    cable_installation_date: Optional[Union[datetime, date]] = None
    cable_removal_date: Optional[Union[datetime, date]] = None
    cable_characteristics: Optional[str] = ''
    cable_environment: Optional[str] = ''
    cable_installation_environment: Optional[str] = ''
    cable_model: Optional[str] = ''
    cable_outside_diameter: Optional[float] = None
    cable_outside_diameter_unit: Optional[str] = ''
    comment: Optional[str] = ''
    fibers: List[FiberModel] = Field(default=[FiberModel()])


class DASMetadata(BaseModel):
    network_code: constr(max_length=8, strip_whitespace=True) = 'COMPLETE!'
    location: str = Field(default='COMPLETE: Geographic location of the installation')
    country: constr(min_length=3, max_length=3, to_upper=True, strip_whitespace=True) = '3-letter-code'
    principal_investigator_name: str = Field(default='COMPLETE!')
    principal_investigator_email: str = Field(default='COMPLETE!')
    principal_investigator_address: str = Field(default='COMPLETE: Physical address and institution')
    point_of_contact: str = Field(default='COMPLETE!')
    point_of_contact_email: str = Field(default='COMPLETE!')
    point_of_contact_address: str = Field(default='COMPLETE: Physical address and institution')
    start_date: Union[datetime, date] = date(1980, 1, 1)
    end_date: Union[datetime, date] = date(2999, 12, 31)
    funding_agency: Optional[str] = ''
    project_number: Optional[str] = ''
    digital_object_identifier: Optional[str] = ''
    purpose_of_data_collection: Optional[str] = ''
    comment: str = Field(default='Automatically generated by dasmetadata (dastools).')
    interrogators: List[InterrogatorModel] = Field(default=[InterrogatorModel()])
    cables: List[CableModel] = Field(default=[CableModel()])
