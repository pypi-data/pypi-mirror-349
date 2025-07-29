"""
Sarmat.
Ядро пакета.
Описание бизнес логики.
Вспомогательные инструменты.
Вычисления с участием Sarmat объектов.
"""
from datetime import (
    date,
    timedelta,
)
from typing import Union

from sarmat.core.constants import (
    DurationMonthCalcStrategy,
    DurationType,
    RouteType,
    month_len,
)
from sarmat.core.context.models import (
    DurationItemModel,
    DurationModel,
    JourneyModel,
    RouteMetrics,
    RouteModel,
)

max_month_len = 31
months_in_year = 12

MetricsSource = Union[JourneyModel, RouteModel]


def get_timedelta_from_duration(
    duration: DurationModel,
    calculation_date: date,
    calc_strategy: DurationMonthCalcStrategy,
    only_active: bool = False,
) -> timedelta:
    """Вычисление приращения по времени на основе объекта продолжительности.

    Args:
        duration: объект продолжительности
        calculation_date: дата на момент вычисления
        calc_strategy: стратегия обработки продолжительности в месяц
        only_active: признак учёта только времени активности

    Returns: приращение по времени

    """
    time_delta = timedelta(minutes=0)
    start_date = calculation_date + time_delta

    if duration.values:
        for val in duration.values:
            if only_active and not val.in_activity:
                continue
            time_delta += get_timedelta_from_duration_item(val, start_date, calc_strategy)
            start_date = calculation_date + time_delta

    return time_delta


def get_timedelta_from_duration_item(
    duration_item: DurationItemModel,
    calculation_date: date,
    calc_strategy: DurationMonthCalcStrategy,
) -> timedelta:
    """Преобразование элемента продолжительности в приращение по времени."""

    if duration_item.duration_type == DurationType.MONTH:
        args = {
            DurationType.DAY.as_cypher: get_month_increase(duration_item.value, calculation_date, calc_strategy),
        }
    elif duration_item.duration_type == DurationType.YEAR:
        args = {
            DurationType.DAY.as_cypher: get_month_increase(duration_item.value*12, calculation_date, calc_strategy),
        }
    else:
        args = {duration_item.duration_type.as_cypher: duration_item.value}
    return timedelta(**args)


def get_month_increase(
    value: int,
    calculation_date: date,
    calc_strategy: DurationMonthCalcStrategy,
) -> int:
    """Вычисление приращения по дням для месяцев."""
    current_month = calculation_date.month
    current_day = calculation_date.day
    current_year = calculation_date.year
    current_month_len, target_month_len = 0, 0

    # составление годовых кругов по количеству затронутых месяцев
    month_cycle = []
    months_count = current_month + value
    years_count, mod = divmod(months_count, months_in_year)
    if mod:
        years_count += 1

    # учитываем количество дней в високосных годах
    feb_pos = 1
    for i in range(years_count):
        month_cycle.extend(month_len)
        year = current_year + i
        if not year % 4:
            month_cycle[feb_pos] += 1
        feb_pos += months_in_year
    month_cycle_gen = (m for m in month_cycle)

    for _ in range(current_month):
        current_month_len = next(month_cycle_gen)
    # количество дней до конца текущего месяца
    days_increase = current_month_len - current_day

    if value > 1:
        if calc_strategy == DurationMonthCalcStrategy.FULL:
            for _ in range(value - 1):
                days_increase += max_month_len
                next(month_cycle_gen)
        else:
            for _ in range(value - 1):
                days_increase += next(month_cycle_gen)

    target_month_len = next(month_cycle_gen)
    # если текущая дата не превышает максимальную дату месяца,
    # то вычисляем количество дней как число дней до текущего месяца + текущая дата
    if current_day <= target_month_len:
        days_increase += current_day
    else:
        # в противном случае применяем стратегию вычисления дней для конца месяца
        # Откат к наименьшему дню месяца
        if calc_strategy == DurationMonthCalcStrategy.DOWN:
            days_increase += target_month_len
        elif calc_strategy == DurationMonthCalcStrategy.MOVE:
            days_increase += target_month_len + (current_day - target_month_len)
        elif calc_strategy == DurationMonthCalcStrategy.FULL:
            days_increase += max_month_len

    return days_increase


def calculate_route_metrics(source: MetricsSource) -> RouteMetrics:
    """Вычисление метрики для маршрута или рейса.

    Args:
        source: JourneyModel | RouteModel - маршрут или рейс

    Returns: метрика
    """
    last_item = source.structure[-1]

    # Для кольцевых маршрутов последний пункт совпадает с начальным,
    #    поэтому вычислять фактическое имя маршрута не имеет смысла
    if source.route_type == RouteType.CIRCLE:
        route_name = source.name
    else:
        route_name = f"{source.start_point.name} - {last_item.point.name}"

    metrics = RouteMetrics(
        fact_route_name=route_name,
        points_count=len(source.structure),
        total_length=last_item.length_from_last_km,
        spent_time=last_item.travel_time_min,
        move_time=last_item.travel_time_min,
        stop_time=0,
    )

    for item in source.structure[:-1]:
        metrics.total_length += item.length_from_last_km
        metrics.spent_time += (item.travel_time_min + (item.stop_time_min or 0))
        metrics.move_time += item.travel_time_min
        metrics.stop_time += item.stop_time_min or 0

    return metrics
