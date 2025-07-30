from django.urls import path

from . import views

urlpatterns = [
    path(
        "timetable/<int:time_grid>/<str:type_>/<int:pk>/print/",
        views.print_timetable,
        name="timetable_print",
    ),
]
