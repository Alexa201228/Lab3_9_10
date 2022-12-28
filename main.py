"""
Task to explore data manipulation with Pandas
This work uses 'Police Department Incident Reports: 2018 to Present' dataset
Link^ https://catalog.data.gov/dataset/police-department-incident-reports-2018-to-present
"""
import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def prepare_police_report(filename: str):
    df = pd.read_csv(filename, sep=',')
    df = df.loc[df['Report Type Code'] == 'VS']
    incident_date = df[['Incident Date']]
    incident_description = df[['Incident Description']]
    incident_day_of_week = df[['Incident Day of Week']]
    incident_time = df[['Incident Time']]
    report = pd.concat([incident_date, incident_time, incident_description, incident_day_of_week], axis=1)
    report['Incident Date'] = pd.to_datetime(report['Incident Date'])
    report['Incident Time'] = pd.to_datetime(report['Incident Time'], format='%H:%M').apply(lambda x: pd.Timestamp(x))
    return report


def get_crimes_per_year(police_report: pd.DataFrame):
    print(police_report.groupby(police_report['Incident Date'].dt.year).size())


def get_crimes_per_month(police_report: pd.DataFrame):
    print(police_report.groupby(police_report['Incident Date'].dt.month).size())


def get_crimes_per_day_of_week(police_report: pd.DataFrame):
    print(police_report.groupby(police_report['Incident Day of Week']).size())


def get_crimes_by_time_periods(police_report: pd.DataFrame):
    police_report = police_report.rename(columns={'Incident Day of Week': 'Day of Week',
                                                  })
    night_shift = pd.DataFrame(police_report.groupby([police_report['Incident Date'].dt.year,
                                                      police_report['Day of Week'],
                                                      police_report['Incident Time'].dt.hour.between(0, 6)]).size())\
                    .reset_index()

    night_shift = night_shift.loc[night_shift['Incident Time'] == True].drop('Incident Time', axis=1)
    night_shift.rename({0: 'Crimes Count'}, axis=1, inplace=True)

    morning_shift = pd.DataFrame(police_report.groupby([police_report['Incident Date'].dt.year,
                                                        police_report['Day of Week'],
                                                        police_report['Incident Time'].dt.hour.between(6, 12)]).size())\
                      .reset_index()
    morning_shift = morning_shift.loc[morning_shift['Incident Time'] == True].drop('Incident Time', axis=1)
    morning_shift.rename({0: 'Crimes Count'}, axis=1, inplace=True)

    daylight_shift = pd.DataFrame(police_report.groupby([police_report['Incident Date'].dt.year,
                                                         police_report['Day of Week'],
                                                         police_report['Incident Time'].dt.hour.between(12, 18)]).size())\
                       .reset_index()
    daylight_shift = daylight_shift.loc[daylight_shift['Incident Time'] == True].drop('Incident Time', axis=1)
    daylight_shift.rename({0: 'Crimes Count'}, axis=1, inplace=True)

    evening_shift = pd.DataFrame(police_report.groupby([police_report['Incident Date'].dt.year,
                                                        police_report['Day of Week'],
                                                        police_report['Incident Time'].dt.hour.between(18, 24)]).size())\
                      .reset_index()
    evening_shift = evening_shift.loc[evening_shift['Incident Time'] == True].drop('Incident Time', axis=1)
    evening_shift.rename({0: 'Crimes Count'}, axis=1, inplace=True)

    print(f'Crimes between 0 and 6AM:\n{night_shift}\n')
    print(f'Crimes between 6 and 12AM:\n{morning_shift}\n')
    print(f'Crimes between 12AM and 18PM:\n{daylight_shift}\n')
    print(f'Crimes between 18PM and 0AM:\n{evening_shift}')


def draw_crimes_per_time_graphic(police_report: pd.DataFrame):
    night_shift = pd.DataFrame(police_report.groupby([police_report['Incident Time'].dt.hour.between(0, 6)]).size()).reset_index()
    night_shift = night_shift.loc[night_shift['Incident Time'] == True].drop('Incident Time', axis=1)
    night_shift.rename({0: 'Crimes Count'}, axis=1, inplace=True)

    morning_shift = pd.DataFrame(police_report.groupby(police_report['Incident Time'].dt.hour.between(6, 12)).size()).reset_index()
    morning_shift = morning_shift.loc[morning_shift['Incident Time'] == True].drop('Incident Time', axis=1)
    morning_shift.rename({0: 'Crimes Count'}, axis=1, inplace=True)

    daylight_shift = pd.DataFrame(police_report.groupby(police_report['Incident Time'].dt.hour.between(12, 18)).size()).reset_index()
    daylight_shift = daylight_shift.loc[daylight_shift['Incident Time'] == True].drop('Incident Time', axis=1)
    daylight_shift.rename({0: 'Crimes Count'}, axis=1, inplace=True)

    evening_shift = pd.DataFrame(police_report.groupby(police_report['Incident Time'].dt.hour.between(18, 24)).size()).reset_index()
    evening_shift = evening_shift.loc[evening_shift['Incident Time'] == True].drop('Incident Time', axis=1)
    evening_shift.rename({0: 'Crimes Count'}, axis=1, inplace=True)

    plt.plot([6, 12, 18, 24],
             [night_shift['Crimes Count'], morning_shift['Crimes Count'], daylight_shift['Crimes Count'], evening_shift['Crimes Count']])
    plt.show()


def draw_3d_crimes_per_time_graphic(police_report: pd.DataFrame):
    police_report = police_report.loc[police_report['Incident Date'] < datetime.datetime(2022, 1, 1)]
    night_shift = pd.DataFrame(police_report.groupby([police_report['Incident Time'].dt.hour.between(0, 6)]).size()).reset_index()
    night_shift = night_shift.loc[night_shift['Incident Time'] == True].drop('Incident Time', axis=1)
    night_shift.rename({0: 'Crimes Count'}, axis=1, inplace=True)

    morning_shift = pd.DataFrame(police_report.groupby(police_report['Incident Time'].dt.hour.between(6, 12)).size()).reset_index()
    morning_shift = morning_shift.loc[morning_shift['Incident Time'] == True].drop('Incident Time', axis=1)
    morning_shift.rename({0: 'Crimes Count'}, axis=1, inplace=True)

    daylight_shift = pd.DataFrame(police_report.groupby(police_report['Incident Time'].dt.hour.between(12, 18)).size()).reset_index()
    daylight_shift = daylight_shift.loc[daylight_shift['Incident Time'] == True].drop('Incident Time', axis=1)
    daylight_shift.rename({0: 'Crimes Count'}, axis=1, inplace=True)

    evening_shift = pd.DataFrame(police_report.groupby(police_report['Incident Time'].dt.hour.between(18, 24)).size()).reset_index()
    evening_shift = evening_shift.loc[evening_shift['Incident Time'] == True].drop('Incident Time', axis=1)
    evening_shift.rename({0: 'Crimes Count'}, axis=1, inplace=True)

    ax = plt.axes(projection='3d')
    x_axis = np.array([2018, 2019, 2020, 2021])
    y_axis = np.array([6, 12, 18, 24])
    z_axis = np.array([night_shift['Crimes Count'], morning_shift['Crimes Count'], daylight_shift['Crimes Count'], evening_shift['Crimes Count']]).reshape(-1)
    ax.plot3D(x_axis, y_axis, z_axis)
    plt.show()


if __name__ == '__main__':
    police_report = prepare_police_report('Police_Department_Incident_Reports__2018_to_Present.csv')
    get_crimes_per_year(police_report)
    get_crimes_per_month(police_report)
    get_crimes_per_day_of_week(police_report)
    get_crimes_by_time_periods(police_report)
    draw_crimes_per_time_graphic(police_report)
    draw_3d_crimes_per_time_graphic(police_report)
