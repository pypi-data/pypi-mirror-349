from aleksis.core.util.apps import AppConfig


class DefaultConfig(AppConfig):
    name = "aleksis.apps.lesrooster"
    verbose_name = "AlekSIS — Lesrooster (Timetable Management Using Time Grids)"
    dist_name = "AlekSIS-App-Lesrooster"

    urls = {
        "Repository": "https://edugit.org/AlekSIS/official/AlekSIS-App-Lesrooster",
    }
    licence = "EUPL-1.2+"

    copyright_info = (
        ([2023, 2024], "Julian Leucker", "julian.leucker@teckids.org"),
        ([2023, 2024], "Jonathan Weth", "jonathan.weth@teckids.org"),
        ([2023, 2024], "Hangzhi Yu", "hangzhi.yu@teckids.org"),
        ([2024], "magicfelix", "felix@felix-zauberer.de"),
        ([2024], "Michael Bauer", "michael-bauer@posteo.de"),
    )
