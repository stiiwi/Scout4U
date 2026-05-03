#!/usr/bin/env python3
import argparse
import csv
from dataclasses import dataclass, field
import math
from pathlib import Path
import sys


EXPERIENCE_TAGS = {
    "natur",
    "aussicht",
    "wasser",
    "berg",
    "kultur",
    "altstadt",
    "burg_schloss",
    "museum",
    "genuss",
    "markt",
    "wanderung_leicht",
    "wanderung_mittel",
    "familienfreundlich",
    "fotogen",
    "geheimtipp",
}

STRONG_THEMES = {
    "natur",
    "aussicht",
    "wasser",
    "berg",
    "kultur",
    "altstadt",
    "burg_schloss",
    "museum",
    "genuss",
    "markt",
    "familienfreundlich",
    "fotogen",
    "geheimtipp",
}

EXPERIENCE_TAG_ORDER = (
    "natur",
    "aussicht",
    "wasser",
    "berg",
    "kultur",
    "altstadt",
    "burg_schloss",
    "museum",
    "genuss",
    "markt",
    "wanderung_leicht",
    "wanderung_mittel",
    "familienfreundlich",
    "fotogen",
    "geheimtipp",
)

POI_COLUMNS = (
    "id",
    "name",
    "lat",
    "lon",
    "distance_km",
    "tags",
    "indoor_anteil",
    "aufwand",
    "oeffnungszeiten_relevant",
    "vermutlich_offen",
    "datenquelle",
    "notes",
)

PROFILE_COLUMNS = (
    "profile_id",
    "profile_name",
    "radius_km",
    "interests",
    "hard_anti_tags",
    "soft_anti_tags",
)

WEATHER_CHOICES = ("sunny", "rainy")
CUTOFF_SCORE = 5.0
TOURIST_TRAP_TAGS = {"touristenfalle", "tourist_trap"}
POI_TYPE_CHOICES = {"experience", "camper_service", "mixed"}
SERVICE_TAGS = {
    "camper_stellplatz",
    "stellplatz",
    "overnight",
    "wc_entsorgung",
    "chemietoilette",
    "oeffentliche_toilette",
    "toilette",
    "frischwasser",
    "wasser",
    "strom",
    "grauwasser",
    "abfall",
    "dusche",
}
AMBIGUOUS_SERVICE_TAGS = {"wasser"}
SERVICE_ALIASES = {
    "camper_stellplatz": {"stellplatz", "overnight"},
    "stellplatz": {"camper_stellplatz"},
    "overnight": {"stellplatz", "camper_stellplatz"},
    "oeffentliche_toilette": {"toilette"},
    "toilette": {"oeffentliche_toilette"},
    "frischwasser": {"wasser"},
    "wasser": {"frischwasser"},
}
STAY_SECTION_TAGS = {"camper_stellplatz", "stellplatz"}
CAMPER_SERVICE_SECTION_TAGS = {
    "wc_entsorgung",
    "chemietoilette",
    "toilette",
    "oeffentliche_toilette",
    "frischwasser",
    "strom",
    "grauwasser",
    "abfall",
    "dusche",
}
RECOMMENDATION_SECTION_ORDER = (
    ("stays", "--- Stellplätze ---"),
    ("camper_services", "--- Camper-Services ---"),
    ("experiences", "--- Ausflüge / schöne Orte ---"),
)
DISPLAY_LABELS = {
    "abfall": "Abfall",
    "altstadt": "Altstadt",
    "aussicht": "Aussicht",
    "berg": "Berg",
    "burg_schloss": "Burg / Schloss",
    "camper_stellplatz": "Camper-Stellplatz",
    "chemietoilette": "Chemietoilette",
    "dusche": "Dusche",
    "familienfreundlich": "familienfreundlich",
    "fotogen": "fotogen",
    "frischwasser": "Frischwasser",
    "geheimtipp": "Geheimtipp",
    "genuss": "Genuss",
    "grauwasser": "Grauwasser",
    "kultur": "Kultur",
    "markt": "Markt",
    "museum": "Museum",
    "natur": "Natur",
    "oeffentliche_toilette": "öffentliche Toilette",
    "stellplatz": "Stellplatz",
    "strom": "Strom",
    "toilette": "Toilette",
    "wanderung_leicht": "leichte Wanderung",
    "wanderung_mittel": "mittlere Wanderung",
    "wasser": "Wasser",
    "wc_entsorgung": "WC-Entsorgung",
}


class ParseError(Exception):
    pass


class SelfTestFailure(Exception):
    pass


@dataclass
class POI:
    id: str
    name: str
    lat: str
    lon: str
    distance_km: float
    tags: set[str]
    indoor_anteil: float
    aufwand: str
    oeffnungszeiten_relevant: bool
    vermutlich_offen: bool
    datenquelle: str
    notes: str
    line_number: int = 0
    validation_error: str = ""
    poi_type: str = "experience"
    poi_type_explicit: bool = False
    services: set[str] = field(default_factory=set)
    price_chf: float = None
    overnight_allowed: bool = None


@dataclass
class Profile:
    profile_id: str
    profile_name: str
    radius_km: float
    interests: list[tuple[str, int]]
    hard_anti_tags: set[str]
    soft_anti_tags: set[str]
    needs: set[str] = field(default_factory=set)


@dataclass
class ScoreBreakdown:
    interest_score: float
    weather_score: float
    distance_score: float
    opening_score: float
    touristic_malus: float
    shopping_malus: float
    soft_anti_malus: float
    total: float
    service_score: float = 0.0
    overnight_bonus: float = 0.0
    price_bonus: float = 0.0
    matched_interests: list[tuple[str, int]] = field(default_factory=list)
    matched_services: list[str] = field(default_factory=list)
    soft_anti_hits: list[str] = field(default_factory=list)


@dataclass
class Result:
    poi: POI
    filtered: bool
    reason: str = ""
    detail: str = ""
    score: ScoreBreakdown = None
    experience_tags: list[str] = field(default_factory=list)


def clean(value: str) -> str:
    if value is None:
        return ""
    return value.strip()


def is_valid_tag(tag: str) -> bool:
    if not tag or not tag.isascii():
        return False
    for char in tag:
        if not (char.islower() or char.isdigit() or char == "_"):
            return False
    return True


def parse_tag_list(value: str, field_name: str, line_number: int, allow_empty: bool) -> list[str]:
    raw = clean(value)
    if not raw:
        if allow_empty:
            return []
        raise ParseError(f"Zeile {line_number}, Feld {field_name}: Wert fehlt")

    tags = []
    for part in raw.split(";"):
        tag = part.strip()
        if not is_valid_tag(tag):
            raise ParseError(
                f"Zeile {line_number}, Feld {field_name}: ungültiger Tag {tag!r}"
            )
        tags.append(tag)
    return tags


def parse_bool(value: str, field_name: str, line_number: int) -> bool:
    raw = clean(value).lower()
    if raw == "" or raw == "nein":
        return False
    if raw == "ja":
        return True
    raise ParseError(
        f"Zeile {line_number}, Feld {field_name}: erwartet ja/nein oder leer, erhalten {value!r}"
    )


def parse_optional_bool(value: str, field_name: str, line_number: int) -> bool:
    raw = clean(value).lower()
    if raw == "":
        return None
    if raw == "nein":
        return False
    if raw == "ja":
        return True
    raise ParseError(
        f"Zeile {line_number}, Feld {field_name}: erwartet ja/nein oder leer, erhalten {value!r}"
    )


def parse_required_float(value: str, field_name: str, line_number: int) -> float:
    raw = clean(value)
    if not raw:
        raise ParseError(f"Zeile {line_number}, Feld {field_name}: Wert fehlt")
    try:
        number = float(raw)
    except ValueError as exc:
        raise ParseError(
            f"Zeile {line_number}, Feld {field_name}: ungültige Zahl {raw!r}"
        ) from exc
    if not math.isfinite(number):
        raise ParseError(
            f"Zeile {line_number}, Feld {field_name}: ungültige Zahl {raw!r}"
        )
    return number


def parse_optional_float(value: str, field_name: str, line_number: int) -> float:
    raw = clean(value)
    if not raw:
        return None
    try:
        number = float(raw)
    except ValueError as exc:
        raise ParseError(
            f"Zeile {line_number}, Feld {field_name}: ungültige Zahl {raw!r}"
        ) from exc
    if not math.isfinite(number) or number < 0:
        raise ParseError(
            f"Zeile {line_number}, Feld {field_name}: ungültige Zahl {raw!r}"
        )
    return number


def parse_poi_type(value: str, line_number: int) -> tuple[str, bool]:
    raw = clean(value)
    if not raw:
        return "experience", False
    if raw not in POI_TYPE_CHOICES:
        raise ParseError(
            f"Zeile {line_number}, Feld poi_type: erwartet experience/camper_service/mixed, erhalten {raw!r}"
        )
    return raw, True


def parse_profile_interests(value: str, line_number: int) -> list[tuple[str, int]]:
    raw = clean(value)
    if not raw:
        raise ParseError(f"Zeile {line_number}, Feld interests: Wert fehlt")

    interests = []
    for part in raw.split(";"):
        item = part.strip()
        if ":" not in item:
            raise ParseError(
                f"Zeile {line_number}, Feld interests: erwartet tag:gewicht, erhalten {item!r}"
            )
        tag, weight_text = item.split(":", 1)
        tag = tag.strip()
        weight_text = weight_text.strip()
        if not is_valid_tag(tag):
            raise ParseError(
                f"Zeile {line_number}, Feld interests: ungültiger Tag {tag!r}"
            )
        try:
            weight = int(weight_text)
        except ValueError as exc:
            raise ParseError(
                f"Zeile {line_number}, Feld interests: ungültiges Gewicht {weight_text!r}"
            ) from exc
        if weight not in (1, 2, 3):
            raise ParseError(
                f"Zeile {line_number}, Feld interests: Gewicht muss 1, 2 oder 3 sein"
            )
        interests.append((tag, weight))
    return interests


def require_columns(fieldnames: list[str], expected_columns: tuple[str, ...], csv_name: str) -> None:
    if fieldnames is None:
        raise ParseError(f"{csv_name}: CSV-Datei hat keine Kopfzeile")

    missing = [column for column in expected_columns if column not in fieldnames]
    if missing:
        raise ParseError(
            f"{csv_name}: fehlende Spalte(n) in Zeile 1: {', '.join(missing)}"
        )


def parse_poi_row(row: dict[str, str], line_number: int) -> POI:
    validation_errors = []

    poi_id = clean(row.get("id"))
    name = clean(row.get("name"))
    if not poi_id:
        validation_errors.append("id")
        poi_id = f"line-{line_number}"
    if not name:
        validation_errors.append("name")
        name = f"<Zeile {line_number}>"

    distance_text = clean(row.get("distance_km"))
    distance_km = math.inf
    if not distance_text:
        validation_errors.append("distance_km")
    else:
        try:
            distance_km = float(distance_text)
            if not math.isfinite(distance_km) or distance_km < 0:
                validation_errors.append("distance_km")
                distance_km = math.inf
        except ValueError:
            validation_errors.append("distance_km")

    tags = set()
    try:
        tags = set(parse_tag_list(row.get("tags"), "tags", line_number, allow_empty=False))
    except ParseError:
        validation_errors.append("tags")

    indoor_text = clean(row.get("indoor_anteil"))
    indoor_anteil = math.nan
    if not indoor_text:
        validation_errors.append("indoor_anteil")
    else:
        try:
            indoor_anteil = float(indoor_text)
            if indoor_anteil not in (0.0, 0.5, 1.0):
                validation_errors.append("indoor_anteil")
                indoor_anteil = math.nan
        except ValueError:
            validation_errors.append("indoor_anteil")

    poi_type, poi_type_explicit = parse_poi_type(row.get("poi_type"), line_number)
    services = set(
        parse_tag_list(row.get("services"), "services", line_number, allow_empty=True)
    )
    price_chf = parse_optional_float(row.get("price_chf"), "price_chf", line_number)
    overnight_allowed = parse_optional_bool(
        row.get("overnight_allowed"), "overnight_allowed", line_number
    )

    return POI(
        id=poi_id,
        name=name,
        lat=clean(row.get("lat")),
        lon=clean(row.get("lon")),
        distance_km=distance_km,
        tags=tags,
        indoor_anteil=indoor_anteil,
        aufwand=clean(row.get("aufwand")),
        oeffnungszeiten_relevant=parse_bool(
            row.get("oeffnungszeiten_relevant"), "oeffnungszeiten_relevant", line_number
        ),
        vermutlich_offen=parse_bool(row.get("vermutlich_offen"), "vermutlich_offen", line_number),
        datenquelle=clean(row.get("datenquelle")),
        notes=clean(row.get("notes")),
        line_number=line_number,
        validation_error=", ".join(validation_errors),
        poi_type=poi_type,
        poi_type_explicit=poi_type_explicit,
        services=services,
        price_chf=price_chf,
        overnight_allowed=overnight_allowed,
    )


def parse_pois(path: Path) -> list[POI]:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            require_columns(reader.fieldnames, POI_COLUMNS, str(path))
            pois = []
            for row in reader:
                line_number = reader.line_num
                if None in row:
                    raise ParseError(f"{path}: Zeile {line_number}: zu viele Spalten")
                pois.append(parse_poi_row(row, line_number))
            return pois
    except OSError as exc:
        raise ParseError(f"{path}: Datei kann nicht gelesen werden: {exc}") from exc


def parse_profile_row(row: dict[str, str], line_number: int) -> Profile:
    profile_id = clean(row.get("profile_id"))
    profile_name = clean(row.get("profile_name"))
    if not profile_id:
        raise ParseError(f"Zeile {line_number}, Feld profile_id: Wert fehlt")
    if not profile_name:
        raise ParseError(f"Zeile {line_number}, Feld profile_name: Wert fehlt")

    radius_km = parse_required_float(row.get("radius_km"), "radius_km", line_number)
    if radius_km < 0:
        raise ParseError(f"Zeile {line_number}, Feld radius_km: muss >= 0 sein")

    interests = parse_profile_interests(row.get("interests"), line_number)
    hard_anti_tags = set(
        parse_tag_list(row.get("hard_anti_tags"), "hard_anti_tags", line_number, allow_empty=True)
    )
    soft_anti_tags = set(
        parse_tag_list(row.get("soft_anti_tags"), "soft_anti_tags", line_number, allow_empty=True)
    )
    needs = set(parse_tag_list(row.get("needs"), "needs", line_number, allow_empty=True))

    return Profile(
        profile_id=profile_id,
        profile_name=profile_name,
        radius_km=radius_km,
        interests=interests,
        hard_anti_tags=hard_anti_tags,
        soft_anti_tags=soft_anti_tags,
        needs=needs,
    )


def parse_profiles(path: Path) -> list[Profile]:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            require_columns(reader.fieldnames, PROFILE_COLUMNS, str(path))
            profiles = []
            for row in reader:
                line_number = reader.line_num
                if None in row:
                    raise ParseError(f"{path}: Zeile {line_number}: zu viele Spalten")
                profiles.append(parse_profile_row(row, line_number))
            return profiles
    except OSError as exc:
        raise ParseError(f"{path}: Datei kann nicht gelesen werden: {exc}") from exc


def select_profile(profiles: list[Profile], profile_id: str) -> Profile:
    for profile in profiles:
        if profile.profile_id == profile_id:
            return profile
    available = ", ".join(profile.profile_id for profile in profiles) or "keine"
    raise ParseError(f"Profil {profile_id!r} nicht gefunden. Verfügbar: {available}")


def experience_tags_for(tags: set[str]) -> list[str]:
    return [tag for tag in EXPERIENCE_TAG_ORDER if tag in tags]


def expand_service_terms(terms: set[str]) -> set[str]:
    expanded = set(terms)
    for term in terms:
        expanded.update(SERVICE_ALIASES.get(term, set()))
    return expanded


def service_terms_for(poi: POI) -> set[str]:
    terms = set(poi.services)
    if poi.poi_type == "camper_service":
        terms.update(poi.tags & SERVICE_TAGS)
    else:
        terms.update(poi.tags & (SERVICE_TAGS - AMBIGUOUS_SERVICE_TAGS))
    return terms


def is_service_poi(poi: POI) -> bool:
    if poi.poi_type == "camper_service":
        return True
    if poi.poi_type == "mixed":
        return bool(service_terms_for(poi))
    if not poi.poi_type_explicit:
        return bool(service_terms_for(poi))
    return False


def match_profile_needs(profile: Profile, poi: POI) -> list[str]:
    if not is_service_poi(poi):
        return []
    poi_terms = expand_service_terms(service_terms_for(poi))
    matches = []
    for need in sorted(profile.needs):
        if expand_service_terms({need}) & poi_terms:
            matches.append(need)
    return matches


def calculate_service_score(poi: POI, profile: Profile) -> tuple[float, float, float, list[str]]:
    if not is_service_poi(poi):
        return 0.0, 0.0, 0.0, []

    matched_services = match_profile_needs(profile, poi)
    service_need_score = 3.0 * len(matched_services)

    expanded_needs = expand_service_terms(profile.needs)
    overnight_bonus = 0.0
    if poi.overnight_allowed is True and ({"stellplatz", "overnight"} & expanded_needs):
        overnight_bonus = 2.0

    price_bonus = 0.0
    if poi.price_chf == 0.0 or "kostenlos" in poi.tags or "kostenlos" in poi.services:
        price_bonus = 1.0

    return service_need_score + overnight_bonus + price_bonus, overnight_bonus, price_bonus, matched_services


def has_service_value(score: ScoreBreakdown) -> bool:
    return bool(score.matched_services) or score.overnight_bonus > 0.0


def calculate_score(poi: POI, profile: Profile, weather: str) -> ScoreBreakdown:
    interest_candidates = []
    for index, (tag, weight) in enumerate(profile.interests):
        if tag in poi.tags:
            interest_candidates.append((index, tag, weight))
    selected = sorted(interest_candidates, key=lambda item: (-item[2], item[0]))[:3]
    selected = sorted(selected, key=lambda item: item[0])
    matched_interests = [(tag, weight) for _, tag, weight in selected]
    interest_score = float(sum(weight for _, _, weight in selected))

    weather_score = 0.0
    if weather == "sunny":
        if poi.indoor_anteil == 1.0:
            weather_score = -2.0
        elif poi.indoor_anteil == 0.5:
            weather_score = 0.0
        elif poi.indoor_anteil == 0.0:
            weather_score = 1.0
    elif weather == "rainy":
        if poi.indoor_anteil == 1.0:
            weather_score = 3.0
        elif poi.indoor_anteil == 0.5:
            weather_score = 0.0
        elif poi.indoor_anteil == 0.0:
            weather_score = -4.0

    if poi.distance_km <= 10:
        distance_score = 1.0
    elif poi.distance_km <= 25:
        distance_score = 0.5
    else:
        distance_score = 0.0

    opening_score = 1.0 if poi.oeffnungszeiten_relevant and poi.vermutlich_offen else 0.0
    touristic_malus = -0.5 if "touristisch" in poi.tags else 0.0
    shopping_malus = -3.0 if "shopping" in poi.tags and not (poi.tags & STRONG_THEMES) else 0.0
    soft_anti_hits = sorted(profile.soft_anti_tags & poi.tags)
    soft_anti_malus = -3.0 * len(soft_anti_hits)
    service_score, overnight_bonus, price_bonus, matched_services = calculate_service_score(
        poi, profile
    )

    total = (
        interest_score
        + weather_score
        + distance_score
        + opening_score
        + touristic_malus
        + shopping_malus
        + soft_anti_malus
        + service_score
    )

    return ScoreBreakdown(
        interest_score=interest_score,
        weather_score=weather_score,
        distance_score=distance_score,
        opening_score=opening_score,
        touristic_malus=touristic_malus,
        shopping_malus=shopping_malus,
        soft_anti_malus=soft_anti_malus,
        total=total,
        service_score=service_score,
        overnight_bonus=overnight_bonus,
        price_bonus=price_bonus,
        matched_interests=matched_interests,
        matched_services=matched_services,
        soft_anti_hits=soft_anti_hits,
    )


def evaluate_poi(poi: POI, profile: Profile, weather: str) -> Result:
    if poi.validation_error:
        return Result(
            poi=poi,
            filtered=True,
            reason="missing_required_data",
            detail=poi.validation_error,
        )

    if poi.distance_km > profile.radius_km:
        detail = f"{format_number(poi.distance_km)} km > {format_number(profile.radius_km)} km"
        return Result(poi=poi, filtered=True, reason="outside_radius", detail=detail)

    if poi.tags & TOURIST_TRAP_TAGS:
        return Result(poi=poi, filtered=True, reason="tourist_trap")

    hard_hits = sorted(profile.hard_anti_tags & poi.tags)
    if hard_hits:
        return Result(
            poi=poi,
            filtered=True,
            reason="hard_anti_tag_match",
            detail=", ".join(hard_hits),
        )

    experience_tags = experience_tags_for(poi.tags)
    score = calculate_score(poi, profile, weather)
    service_poi = is_service_poi(poi)
    has_experience_value = len(experience_tags) >= 2

    if poi.poi_type == "mixed":
        if not has_experience_value and not has_service_value(score):
            return Result(
                poi=poi,
                filtered=True,
                reason="too_few_experience_tags",
                score=score,
                experience_tags=experience_tags,
            )
    elif not service_poi and not has_experience_value:
        return Result(poi=poi, filtered=True, reason="too_few_experience_tags")

    if not passes_score_cutoff(score.total):
        return Result(
            poi=poi,
            filtered=True,
            reason="below_score_cutoff",
            detail=format_score(score.total),
            score=score,
            experience_tags=experience_tags,
        )

    return Result(
        poi=poi,
        filtered=False,
        score=score,
        experience_tags=experience_tags,
    )


def passes_score_cutoff(total: float) -> bool:
    return total >= CUTOFF_SCORE


def sort_recommendations(results: list[Result]) -> list[Result]:
    return sorted(
        results,
        key=lambda result: (
            -result.score.total,
            -len(result.experience_tags),
            result.poi.distance_km,
            result.poi.name.casefold(),
        ),
    )


def evaluate_pois(pois: list[POI], profile: Profile, weather: str) -> tuple[list[Result], list[Result]]:
    results = [evaluate_poi(poi, profile, weather) for poi in pois]
    recommendations = sort_recommendations([result for result in results if not result.filtered])
    filtered = [result for result in results if result.filtered]
    return recommendations, filtered


def format_score(value: float) -> str:
    return f"{value:.1f}"


def format_number(value: float) -> str:
    if math.isfinite(value) and value == int(value):
        return str(int(value))
    return f"{value:.1f}"


def display_label(tag: str) -> str:
    if tag in DISPLAY_LABELS:
        return DISPLAY_LABELS[tag]
    return tag.replace("_", " ").capitalize()


def display_labels(tags) -> str:
    return ", ".join(display_label(tag) for tag in tags)


def weather_sentence(poi: POI, weather: str) -> str:
    if weather == "sunny":
        if poi.indoor_anteil == 1.0:
            return "Bei Sonne weniger passend: indoor"
        if poi.indoor_anteil == 0.5:
            return "Bei Sonne neutral: teils wettergeschützt"
        return "Bei Sonne ideal: draußen"

    if poi.indoor_anteil == 1.0:
        return "Bei Regen ideal: gut wettergeschützt"
    if poi.indoor_anteil == 0.5:
        return "Bei Regen neutral: teilweise wettergeschützt"
    return "Bei Regen schwach: draußen"


def render_score_breakdown(score: ScoreBreakdown, include_service: bool = False) -> str:
    parts = [
        f"interest={format_score(score.interest_score)}",
        f"weather={format_score(score.weather_score)}",
        f"distance={format_score(score.distance_score)}",
        f"opening={format_score(score.opening_score)}",
        f"touristic={format_score(score.touristic_malus)}",
        f"shopping={format_score(score.shopping_malus)}",
        f"soft_anti={format_score(score.soft_anti_malus)}",
    ]
    if include_service or score.service_score != 0.0:
        parts.append(f"service={format_score(score.service_score)}")
    parts.append(f"total={format_score(score.total)}")
    return "Testdetails (Score): " + ", ".join(parts)


def format_bool_de(value: bool) -> str:
    if value is True:
        return "ja"
    if value is False:
        return "nein"
    return "unbekannt"


def format_price(price_chf: float) -> str:
    if price_chf is None:
        return "unbekannt"
    if price_chf == 0.0:
        return "kostenlos"
    return f"CHF {format_number(price_chf)}"


def format_category(poi_type: str) -> str:
    labels = {
        "experience": "Ausflug / schöner Ort",
        "camper_service": "Camper-Service",
        "mixed": "Gemischt",
    }
    return labels.get(poi_type, poi_type)


def render_result(result: Result, index: int, weather: str, debug_score: bool = False) -> list[str]:
    score = result.score
    service_poi = is_service_poi(result.poi)
    lines = [
        f"{index}. {result.poi.name} — Passung: {format_score(score.total)}",
    ]

    if service_poi:
        if score.matched_services:
            services_reason = display_labels(score.matched_services)
            lines.append(f"   Warum passt das? Passt zu deinen Bedürfnissen: {services_reason}")
        else:
            lines.append("   Warum passt das? Service-Ort in deiner Nähe")
        lines.append(f"   Entfernung: {format_number(result.poi.distance_km)} km")
        if result.poi.services:
            lines.append(f"   Vor Ort: {display_labels(sorted(result.poi.services))}")
        else:
            lines.append("   Vor Ort: keine Services angegeben")
        lines.append(f"   Preis: {format_price(result.poi.price_chf)}")
        if result.poi.overnight_allowed is not None:
            lines.append(
               f"   Übernachten erlaubt: {format_bool_de(result.poi.overnight_allowed)}"
            )
        lines.append(f"   Wetter: {weather_sentence(result.poi, weather)}")
        lines.append(f"   Kategorie: {format_category(result.poi.poi_type)}")
    else:
        if score.matched_interests:
            interests = ", ".join(
                f"{display_label(tag)} ({weight})" for tag, weight in score.matched_interests
            )
            lines.append(f"   Warum passt das? Trifft deine Interessen: {interests}")
        else:
            lines.append("   Warum passt das? Schöner Ort in deinem Radius")
        lines.append(f"   Wetter: {weather_sentence(result.poi, weather)}")
        lines.append(f"   Entfernung: {format_number(result.poi.distance_km)} km")
        if result.experience_tags:
            lines.append(f"   Erlebnis: {display_labels(result.experience_tags)}")
        else:
            lines.append("   Erlebnis: keine")
    if result.poi.oeffnungszeiten_relevant:
        lines.append("   Hinweis: Öffnungszeiten prüfen")
    if result.poi.notes:
        lines.append(f"   Hinweis: {result.poi.notes}")
    if debug_score:
        lines.append(f"   {render_score_breakdown(score, service_poi)}")
    return lines


def recommendation_section(result: Result) -> str:
    service_terms = service_terms_for(result.poi)
    if service_terms & STAY_SECTION_TAGS or result.poi.overnight_allowed is True:
        return "stays"
    if service_terms & CAMPER_SERVICE_SECTION_TAGS:
        return "camper_services"
    return "experiences"


def group_recommendations(results: list[Result]) -> dict[str, list[Result]]:
    grouped = {key: [] for key, _ in RECOMMENDATION_SECTION_ORDER}
    for result in results:
        grouped[recommendation_section(result)].append(result)
    return grouped


def render_recommendation_sections(
    results: list[Result],
    weather: str,
    debug_score: bool = False,
) -> list[str]:
    grouped = group_recommendations(results)
    lines = []
    for key, title in RECOMMENDATION_SECTION_ORDER:
        section_results = grouped[key]
        if not section_results:
            continue
        lines.append(title)
        for index, result in enumerate(section_results, start=1):
            lines.extend(render_result(result, index, weather, debug_score))
            lines.append("")
    if lines and lines[-1] == "":
        lines.pop()
    return lines


def render_filtered(result: Result) -> str:
    name = result.poi.name
    if result.detail:
        return f"{name:<24} [{result.reason}: {result.detail}]"
    return f"{name:<24} [{result.reason}]"


def render(
    profile: Profile,
    weather: str,
    recommendations: list[Result],
    filtered: list[Result],
    top: int,
    show_filtered: bool,
    debug_score: bool = False,
) -> str:
    lines = [
        f"Profil: {profile.profile_id} — {profile.profile_name} | Wetter: {weather} | Radius: {format_number(profile.radius_km)} km",
        "",
    ]

    visible_recommendations = recommendations[:top]
    if visible_recommendations:
        lines.extend(
            render_recommendation_sections(visible_recommendations, weather, debug_score)
        )
    else:
        lines.append("Keine Empfehlungen gefunden.")

    if len(recommendations) < 5:
        lines.extend([
            "",
            f"Hinweis: Für diese kleine Demo wurden {len(recommendations)} passende Treffer gefunden.",
        ])

    if show_filtered:
        lines.extend(["", "--- Gefilterte Orte ---"])
        if filtered:
            for result in filtered:
                lines.append(render_filtered(result))
        else:
            lines.append("Keine gefilterten Orte.")

    return "\n".join(lines)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="scout4u-score")
    parser.add_argument("--pois", type=Path, help="Pfad zur POI-CSV")
    parser.add_argument("--profiles", type=Path, help="Pfad zur Profile-CSV")
    parser.add_argument("--profile", help="Profil-ID")
    parser.add_argument("--weather", choices=WEATHER_CHOICES, help="Wetterlage")
    parser.add_argument("--top", type=int, default=10, help="Anzahl Empfehlungen, default 10")
    parser.add_argument("--show-filtered", action="store_true", help="Gefilterte Orte anzeigen")
    parser.add_argument("--debug-score", action="store_true", help="Score-Details anzeigen")
    parser.add_argument("--self-test", action="store_true", help="Eingebaute Smoke-Tests ausführen")
    return parser


def make_self_test_poi(
    poi_id: str,
    name: str,
    distance_km: float,
    tags: set[str],
    indoor_anteil: float,
    oeffnungszeiten_relevant: bool = False,
    vermutlich_offen: bool = False,
    notes: str = "",
    poi_type: str = "experience",
    services: set[str] = None,
    price_chf: float = None,
    overnight_allowed: bool = None,
    poi_type_explicit: bool = True,
) -> POI:
    return POI(
        id=poi_id,
        name=name,
        lat="",
        lon="",
        distance_km=distance_km,
        tags=tags,
        indoor_anteil=indoor_anteil,
        aufwand="",
        oeffnungszeiten_relevant=oeffnungszeiten_relevant,
        vermutlich_offen=vermutlich_offen,
        datenquelle="self-test",
        notes=notes,
        poi_type=poi_type,
        poi_type_explicit=poi_type_explicit,
        services=services or set(),
        price_chf=price_chf,
        overnight_allowed=overnight_allowed,
    )


def build_self_test_data() -> tuple[list[POI], list[Profile]]:
    profile_a = Profile(
        profile_id="A",
        profile_name="Self-Test Natur",
        radius_km=50.0,
        interests=[
            ("natur", 3),
            ("wasser", 2),
            ("fotogen", 2),
            ("kultur", 3),
            ("museum", 2),
            ("altstadt", 2),
        ],
        hard_anti_tags={"wanderung_schwer"},
        soft_anti_tags={"teuer"},
    )
    profile_b = Profile(
        profile_id="B",
        profile_name="Self-Test Kultur",
        radius_km=20.0,
        interests=[("kultur", 3), ("museum", 3), ("altstadt", 2)],
        hard_anti_tags=set(),
        soft_anti_tags=set(),
    )

    pois = [
        make_self_test_poi(
            "outside",
            "Outside Lake",
            55.0,
            {"natur", "wasser", "fotogen"},
            0.0,
        ),
        make_self_test_poi(
            "trap",
            "Trap Shop",
            2.0,
            {"altstadt", "markt", "touristenfalle"},
            0.5,
        ),
        make_self_test_poi(
            "trap_alias",
            "Trap Alias Shop",
            2.0,
            {"altstadt", "markt", "tourist_trap"},
            0.5,
        ),
        make_self_test_poi(
            "hard",
            "Hard Hike",
            10.0,
            {"natur", "berg", "wanderung_schwer"},
            0.0,
        ),
        make_self_test_poi(
            "soft",
            "Soft Museum",
            5.0,
            {"museum", "kultur", "teuer"},
            1.0,
            oeffnungszeiten_relevant=True,
            vermutlich_offen=True,
        ),
        make_self_test_poi(
            "single",
            "Single View",
            5.0,
            {"aussicht"},
            0.0,
        ),
        make_self_test_poi(
            "low",
            "Low Oldtown",
            5.0,
            {"altstadt", "markt"},
            0.0,
        ),
        make_self_test_poi(
            "cutoff_exact",
            "Cutoff Exact",
            30.0,
            {"natur", "wasser"},
            0.5,
        ),
        make_self_test_poi(
            "tie_more",
            "Tie More",
            12.0,
            {"natur", "wasser", "fotogen", "familienfreundlich"},
            0.5,
        ),
        make_self_test_poi(
            "tie_less",
            "Tie Less",
            12.0,
            {"natur", "wasser"},
            0.5,
        ),
    ]
    return pois, [profile_a, profile_b]


def require_self_test(condition: bool, reason: str) -> None:
    if not condition:
        raise SelfTestFailure(reason)


def require_parse_error(action, expected_text: str, reason: str) -> None:
    try:
        action()
    except ParseError as exc:
        require_self_test(expected_text in str(exc), reason)
        return
    raise SelfTestFailure(reason)


def run_self_test() -> int:
    try:
        pois, profiles = build_self_test_data()
        profile = profiles[0]
        recommendations, filtered = evaluate_pois(pois, profile, "rainy")
        all_results = recommendations + filtered
        by_id = {result.poi.id: result for result in all_results}

        require_self_test(
            by_id["outside"].reason == "outside_radius",
            "distance_km > radius_km wurde nicht als outside_radius gefiltert",
        )
        require_self_test(
            by_id["trap"].reason == "tourist_trap",
            "touristenfalle wurde nicht als tourist_trap gefiltert",
        )
        require_self_test(
            by_id["trap_alias"].reason == "tourist_trap",
            "tourist_trap wurde nicht als tourist_trap gefiltert",
        )
        require_self_test(
            by_id["hard"].reason == "hard_anti_tag_match",
            "hard_anti_tag wurde nicht als hard_anti_tag_match gefiltert",
        )
        require_self_test(
            not by_id["soft"].filtered
            and by_id["soft"].score is not None
            and by_id["soft"].score.soft_anti_malus == -3.0,
            "soft_anti_tag wurde nicht als Score-Malus behandelt",
        )
        require_self_test(
            by_id["single"].reason == "too_few_experience_tags",
            "POI mit nur 1 Erlebnis-Tag wurde nicht gefiltert",
        )
        require_self_test(
            by_id["low"].reason == "below_score_cutoff",
            "POI mit Score < 5.0 wurde nicht als below_score_cutoff gefiltert",
        )
        require_self_test(
            not by_id["cutoff_exact"].filtered
            and by_id["cutoff_exact"].score is not None
            and by_id["cutoff_exact"].score.total == 5.0,
            "POI mit Score 5.0 wurde nicht empfohlen",
        )
        require_self_test(
            passes_score_cutoff(5.0) and not passes_score_cutoff(4.9),
            "Cutoff-Grenze 5.0/4.9 wird nicht korrekt behandelt",
        )

        soft_poi = by_id["soft"].poi
        sunny_score = calculate_score(soft_poi, profile, "sunny")
        rainy_score = calculate_score(soft_poi, profile, "rainy")
        require_self_test(
            sunny_score.total != rainy_score.total,
            "identischer POI wurde bei sunny und rainy gleich bewertet",
        )

        recommendation_ids = [result.poi.id for result in recommendations]
        require_self_test(
            recommendation_ids.index("tie_more") < recommendation_ids.index("tie_less"),
            "Tie-Breaker nach Anzahl Erlebnis-Tags wurde nicht respektiert",
        )

        high_score_poi = make_self_test_poi(
            "high",
            "High Score Museum",
            5.0,
            {"kultur", "museum", "altstadt"},
            1.0,
            oeffnungszeiten_relevant=True,
            vermutlich_offen=True,
        )
        high_score_result = evaluate_poi(high_score_poi, profiles[1], "rainy")
        require_self_test(
            not high_score_result.filtered
            and high_score_result.score is not None
            and high_score_result.score.total > 10.0,
            "hohe Scores wurden nicht über 10 zugelassen",
        )

        legacy_poi = parse_poi_row(
            {
                "id": "legacy",
                "name": "Legacy POI",
                "lat": "",
                "lon": "",
                "distance_km": "5",
                "tags": "natur;fotogen",
                "indoor_anteil": "0.5",
                "aufwand": "",
                "oeffnungszeiten_relevant": "",
                "vermutlich_offen": "",
                "datenquelle": "",
                "notes": "",
            },
            2,
        )
        legacy_profile = parse_profile_row(
            {
                "profile_id": "L",
                "profile_name": "Legacy Profile",
                "radius_km": "20",
                "interests": "natur:3;fotogen:2",
                "hard_anti_tags": "",
                "soft_anti_tags": "",
            },
            2,
        )
        require_self_test(
            legacy_poi.poi_type == "experience"
            and not legacy_poi.poi_type_explicit
            and legacy_poi.services == set()
            and legacy_poi.price_chf is None
            and legacy_poi.overnight_allowed is None
            and legacy_profile.needs == set(),
            "CSV-Zeilen ohne neue Camper-Spalten bleiben nicht kompatibel",
        )

        camper_profile = Profile(
            profile_id="CAMP",
            profile_name="Self-Test Camper",
            radius_km=20.0,
            interests=[("natur", 1)],
            hard_anti_tags=set(),
            soft_anti_tags=set(),
            needs={"wc_entsorgung", "strom", "stellplatz", "overnight"},
        )
        wc_service = make_self_test_poi(
            "wc_service",
            "WC Entsorgung",
            3.0,
            {"wc_entsorgung", "kostenlos"},
            0.5,
            poi_type="camper_service",
            services={"wc_entsorgung"},
            price_chf=0.0,
            overnight_allowed=False,
        )
        wc_result = evaluate_poi(wc_service, camper_profile, "rainy")
        require_self_test(
            not wc_result.filtered
            and wc_result.score is not None
            and "wc_entsorgung" in wc_result.score.matched_services
            and len(wc_result.experience_tags) == 0,
            "WC-Entsorgung ohne Erlebnis-Tags scheitert am Erlebnis-Gate",
        )

        mixed_service = make_self_test_poi(
            "mixed_service",
            "Mixed Strompunkt",
            3.0,
            {"strom"},
            0.5,
            poi_type="mixed",
            services={"strom"},
            price_chf=0.0,
        )
        mixed_result = evaluate_poi(mixed_service, camper_profile, "rainy")
        require_self_test(
            not mixed_result.filtered
            and mixed_result.score is not None
            and "strom" in mixed_result.score.matched_services,
            "Mixed-POI mit Service-Nutzen scheitert am Erlebnis-Gate",
        )

        no_need_service = make_self_test_poi(
            "no_need_service",
            "Service ohne Need",
            3.0,
            {"wc_entsorgung"},
            0.5,
            poi_type="camper_service",
            services={"wc_entsorgung"},
        )
        no_need_result = evaluate_poi(no_need_service, legacy_profile, "rainy")
        require_self_test(
            no_need_result.filtered and no_need_result.reason == "below_score_cutoff",
            "Service-Ort ohne passenden Need wird unerwartet empfohlen",
        )

        stay_poi = make_self_test_poi(
            "stay",
            "Self-Test Stellplatz",
            3.0,
            {"camper_stellplatz"},
            0.5,
            poi_type="camper_service",
            services={"camper_stellplatz", "strom"},
            price_chf=0.0,
            overnight_allowed=True,
        )
        stay_result = evaluate_poi(stay_poi, camper_profile, "rainy")
        experience_result = evaluate_poi(legacy_poi, legacy_profile, "rainy")
        require_self_test(
            recommendation_section(stay_result) == "stays",
            "Stellplatz landet nicht im Abschnitt Stellplätze",
        )
        require_self_test(
            recommendation_section(wc_result) == "camper_services",
            "WC-Entsorgung landet nicht im Abschnitt Camper-Services",
        )
        require_self_test(
            recommendation_section(experience_result) == "experiences",
            "Experience-POI landet nicht im Abschnitt Ausflüge / schöne Orte",
        )
        grouped_output = render(
            camper_profile,
            "rainy",
            [wc_result, experience_result, stay_result],
            [],
            10,
            False,
        )
        require_self_test(
            grouped_output.index("--- Stellplätze ---")
            < grouped_output.index("Self-Test Stellplatz")
            < grouped_output.index("--- Camper-Services ---")
            < grouped_output.index("WC Entsorgung")
            < grouped_output.index("--- Ausflüge / schöne Orte ---")
            < grouped_output.index("Legacy POI"),
            "Gruppierte Ausgabe rendert Stellplatz, Service und Ausflug nicht in Abschnittsreihenfolge",
        )
        require_self_test(
            "Testdetails (Score)" not in grouped_output,
            "Score-Details werden ohne --debug-score gerendert",
        )
        debug_output = render(
            camper_profile,
            "rainy",
            [wc_result],
            [],
            10,
            False,
            debug_score=True,
        )
        require_self_test(
            "Testdetails (Score)" in debug_output,
            "Score-Details werden mit --debug-score nicht gerendert",
        )

        require_parse_error(
            lambda: select_profile(profiles, "UNKNOWN"),
            "Profil 'UNKNOWN' nicht gefunden",
            "unbekannte Profil-ID schlägt nicht verständlich fehl",
        )
        require_parse_error(
            lambda: parse_pois(Path("__scout4u_missing_pois_for_self_test__.csv")),
            "Datei kann nicht gelesen werden",
            "fehlende POI-CSV schlägt nicht verständlich fehl",
        )
        require_parse_error(
            lambda: parse_profiles(Path("__scout4u_missing_profiles_for_self_test__.csv")),
            "Datei kann nicht gelesen werden",
            "fehlende Profile-CSV schlägt nicht verständlich fehl",
        )

        weather_action = None
        for action in build_arg_parser()._actions:
            if "--weather" in action.option_strings:
                weather_action = action
        require_self_test(
            weather_action is not None and tuple(weather_action.choices) == WEATHER_CHOICES,
            "argparse begrenzt --weather nicht auf sunny/rainy",
        )

        print("Self-Test OK")
        return 0
    except SelfTestFailure as exc:
        print(f"Self-Test FAILED: {exc}")
        return 1


def validate_normal_args(parser: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    missing = []
    if args.pois is None:
        missing.append("--pois")
    if args.profiles is None:
        missing.append("--profiles")
    if args.profile is None:
        missing.append("--profile")
    if args.weather is None:
        missing.append("--weather")
    if missing:
        parser.error("erforderlich ohne --self-test: " + ", ".join(missing))
    if args.top <= 0:
        parser.error("--top muss größer als 0 sein")


def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()

    if args.self_test:
        return run_self_test()

    validate_normal_args(parser, args)

    try:
        pois = parse_pois(args.pois)
        profiles = parse_profiles(args.profiles)
        profile = select_profile(profiles, args.profile)
        recommendations, filtered = evaluate_pois(pois, profile, args.weather)
    except ParseError as exc:
        print(f"CSV-/Parse-Fehler: {exc}", file=sys.stderr)
        return 2

    print(
        render(
            profile,
            args.weather,
            recommendations,
            filtered,
            args.top,
            args.show_filtered,
            args.debug_score,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
