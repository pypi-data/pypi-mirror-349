from __future__ import annotations
import datetime
import random
import core.solar
import core.weather
import ecommunity.irise
import ecommunity.simulator


class CommunityMember(ecommunity.simulator.SynchronizedMember):

    def __init__(self, member: ecommunity.irise.House, datetimes: list[datetime.datetime], group_name: str, randomize_ratio: float = .2, averager_depth_in_hours: int = 3):
        super().__init__(member, datetimes, group_name, randomize_ratio, averager_depth_in_hours)

    def day_interactions(self, the_date: datetime.date, day_hour_indices: list[int], interaction: int, init: bool):
        pass

    def hour_interactions(self, the_datetime: datetime.datetime, hour_index: int,  interaction: int, init: bool):
        pass


class AdaptiveCommunityManager(ecommunity.simulator.Manager):

    def __init__(self, pv_system: core.solar.PVsystem, no_alert_threshold, randomize_ratio: int = .2, averager_depth_in_hours: int = 3) -> None:
        super().__init__(pv_system, 1, 1, no_alert_threshold=no_alert_threshold, randomize_ratio=randomize_ratio, averager_depth_in_hours=averager_depth_in_hours)

        for member in ecommunity.irise.IRISE(pv_system.datetimes, zipcode_pattern='381%').get_houses():
            member_agent = CommunityMember(member, self.datetimes, 'ecom')
            self.register_synchronized_member(member_agent)
        self.color_delta_power_dict = None
        self.predicted_consumptions_kWh = self.get_predicted_consumptions_kWh(group_name='ecom')

    def day_interactions(self, the_date: datetime.date, day_hour_indices: list[int], interaction: int, init: bool) -> None:
        if day_hour_indices[0] >= 24 * 7:
            predicted_consumptions: list[float] = [sum([member._predicted_consumptions_kWh[i] for member in self.members]) for i in range(0, day_hour_indices[0])]
            actual_consumptions: list[float] = [sum([member._actual_consumptions_kWh[i] for member in self.members]) for i in range(0, day_hour_indices[0])]
            colors: list[ecommunity.simulator.COLOR] = [self.get_hour_colors(i) for i in range(0, day_hour_indices[0])]
            # compute the average consumption variations of the distribution per color
            _, color_level_average_values = ecommunity.indicators.color_statistics(actual_consumptions, predicted_consumptions, colors)
            self.color_delta_power_dict = {color: color_level_average_values[color] for color in color_level_average_values}

    def hour_interactions(self, the_datetime: datetime.datetime, hour_index: int,  interaction: int, init: bool) -> None:
        productions_kWh: float = self.predicted_productions_kWh[hour_index]
        consumptions_kWh: float = self.predicted_consumptions_kWh[hour_index]

        hour_color: ecommunity.simulator.COLOR = self.get_hour_colors(hour_index)
        if hour_index < 24 * 7 or random.uniform(0, 1) <= .05:
            productions_kWh: float = self.predicted_productions_kWh[hour_index]
            consumptions_kWh: float = self.get_predicted_consumption_kWh(hour_index)
            hour_color = ecommunity.simulator.COLOR.WHITE
            if self.datetimes[hour_index].hour > 7 and self.datetimes[hour_index].hour < 23:
                if productions_kWh > consumptions_kWh + self.no_alert_threshold:
                    hour_color = ecommunity.simulator.COLOR.GREEN
                elif consumptions_kWh > productions_kWh + self.no_alert_threshold:
                    hour_color = ecommunity.simulator.COLOR.RED
        else:

            if self.color_delta_power_dict is not None:
                color_match = None
                for color in self.color_delta_power_dict:  # search for the color that best match the need in term of historical consumption variations
                    match = abs(consumptions_kWh - productions_kWh + self.color_delta_power_dict[color])
                    if color_match is None or match < color_match[1]:
                        color_match = (color, match)
                if match > self.no_alert_threshold:
                    hour_color = color_match[0]
            else:  # if less than one week of history, apply reactive strategy
                if productions_kWh > consumptions_kWh + self.no_alert_threshold:
                    hour_color = ecommunity.simulator.COLOR.GREEN
                elif consumptions_kWh > productions_kWh + self.no_alert_threshold:
                    hour_color = ecommunity.simulator.COLOR.RED
        self.set_hour_colors(hour_index, hour_color)

    def finalize(self) -> None:
        pass


if __name__ == '__main__':
    site_weather_data: core.weather.SiteWeatherData = core.weather.WeatherJsonReader('grenoble1979-2022.json', from_requested_stringdate='1/01/2021', to_requested_stringdate='1/01/2022', altitude=330, albedo=0.1, pollution=0.1, location="Grenoble").site_weather_data

    pv_plant_properties = core.solar.PVplantProperties()
    pv_plant_properties.skyline_azimuths_altitudes_in_deg: list[tuple[float, float]] = ([(-180.0,13.8), (-170.0,18.9), (-145.1,9.8), (-120.0,18.3), (-96.1,17.3), (-60.8,6.2), (-14.0,2.6), (-8.4,5.6), (0.8,2.6), (21.6,5.5), (38.1,14.6), (49.4,8.9), (60.1,11.3), (87.4,10.4), (99.3,12.0), (142.1,2.6), (157.8,4.0), (175.1,17.1), (180.0,15.9)])
    pv_plant_properties.surfacePV_in_m2: float = 16
    pv_plant_properties.panel_height_in_m: float = 1.2
    pv_plant_properties.efficiency = 0.2 * 0.95 
    pv_plant_properties.temperature_coefficient: float = 0.0035
    pv_plant_properties.array_width: float = 4  # in m
    pv_plant_properties.exposure_in_deg=0  # TO BE ADJUSTED IF NEEDED
    pv_plant_properties.slope_in_deg=0  # TO BE ADJUSTED IF NEEDED
    pv_plant_properties.distance_between_arrays_in_m = 1.2  # TO BE ADJUSTED IF NEEDED
    pv_plant_properties.mount_type: core.solar.MOUNT_TYPE = core.solar.MOUNT_TYPE.FLAT  # TO BE ADJUSTED IF NEEDED
    
    pv_plant: core.solar.PVplant = core.solar.PVplant(core.solar.SolarModel(site_weather_data), pv_plant_properties)
    
    manager = AdaptiveCommunityManager(pv_plant, no_alert_threshold=2)
    manager.run()
