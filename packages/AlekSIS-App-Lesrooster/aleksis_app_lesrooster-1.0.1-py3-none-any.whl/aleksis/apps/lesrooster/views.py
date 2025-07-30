from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404

from rules.contrib.views import permission_required

from aleksis.apps.chronos.managers import TimetableType
from aleksis.apps.chronos.util.chronos_helpers import get_el_by_pk
from aleksis.apps.lesrooster.models import Slot, TimeGrid
from aleksis.apps.lesrooster.util.build import build_timetable
from aleksis.core.util.pdf import render_pdf


@permission_required("chronos.view_timetable_rule", fn=get_el_by_pk)
def print_timetable(
    request: HttpRequest,
    time_grid: int,
    type_: str,
    pk: int,
) -> HttpResponse:
    """View a selected timetable for a person, group or room."""
    context = {}

    time_grid = get_object_or_404(TimeGrid, pk=time_grid)
    el = get_el_by_pk(request, type_, pk, prefetch=True)

    if isinstance(el, HttpResponseNotFound):
        return HttpResponseNotFound()

    type_ = TimetableType.from_string(type_)

    timetable = build_timetable(time_grid, type_, el)
    context["timetable"] = timetable

    context["weekdays"] = Slot.WEEKDAY_CHOICES[time_grid.weekday_min : time_grid.weekday_max + 1]

    context["time_grid"] = time_grid
    context["type"] = type_
    context["pk"] = pk
    context["el"] = el

    return render_pdf(request, "lesrooster/timetable_print.html", context)
