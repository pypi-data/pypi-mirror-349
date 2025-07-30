from aleksis.core.util.apps import AppConfig


class DefaultConfig(AppConfig):
    name = "aleksis.apps.cursus"
    verbose_name = "AlekSIS — Cursus (Subjects and Courses)"
    dist_name = "AlekSIS-App-Cursus"

    urls = {
        "Repository": "https://edugit.org/AlekSIS/official/AlekSIS-App-Cursus",
    }
    licence = "EUPL-1.2+"
    copyright_info = (
        ([2023, 2024], "Michael Bauer", "michael-bauer@posteo.de"),
        ([2023, 2024], "Julian Leucker", "julian.leucker@teckids.org"),
        ([2023, 2024], "Jonathan Weth", "jonathan.weth@teckids.org"),
        ([2023, 2024], "Hangzhi Yu", "hangzhi.yu@teckids.org"),
    )
