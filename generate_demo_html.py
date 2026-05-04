#!/usr/bin/env python3
from dataclasses import dataclass
from html import escape
from pathlib import Path

from scout4u_score import (
    RECOMMENDATION_SECTION_ORDER,
    display_label,
    display_labels,
    evaluate_pois,
    format_bool_de,
    format_category,
    format_number,
    format_price,
    group_recommendations,
    is_service_poi,
    parse_pois,
    parse_profiles,
    select_profile,
    weather_sentence,
)


@dataclass(frozen=True)
class DemoScenario:
    output_path: Path
    pois_path: Path
    profiles_path: Path
    profile_id: str
    weather: str
    top: int
    document_title: str
    subtitle: str
    section_order: tuple[str, ...]
    section_labels: dict[str, str]
    summary_labels: dict[str, str]
    default_active_section: str
    show_empty_sections: bool = True
    show_interest_weights: bool = True
    intro_template: str = ""


CAMPER_SECTION_ORDER = tuple(key for key, _label in RECOMMENDATION_SECTION_ORDER)
EXPERIENCE_POIS_PATH = Path("pois_bern_test_sample.csv")
EXPERIENCE_PROFILES_PATH = Path("profiles_test_sample.csv")
EXPERIENCE_PROFILE_ID = "A"
EXPERIENCE_WEATHER = "sunny"
EXPERIENCE_TOP = 4

CAMPER_SCENARIO = DemoScenario(
    output_path=Path("demo.html"),
    pois_path=Path("pois_camper_test_sample.csv"),
    profiles_path=Path("profiles_camper_test_sample.csv"),
    profile_id="V",
    weather="rainy",
    top=10,
    document_title="Scout4U Camping-Reisebegleiter",
    subtitle="Camping-Reisebegleiter rund um Bern",
    section_order=CAMPER_SECTION_ORDER,
    section_labels={
        "stays": "Übernachten / Stellplätze",
        "camper_services": "Services",
        "experiences": "Erleben",
    },
    summary_labels={
        "stays": "Übernachten",
        "camper_services": "Services",
        "experiences": "Erleben",
    },
    default_active_section="stays",
    intro_template="Scout4U zeigt dir passende Stopps zum Übernachten, Versorgen und Erleben.",
)

SCENARIOS = (
    CAMPER_SCENARIO,
)


def h(value) -> str:
    return escape(str(value), quote=True)


def weather_label(weather: str) -> str:
    labels = {
        "rainy": "Regen",
        "sunny": "Sonne",
    }
    return labels.get(weather, weather)


def count_word_de(count: int) -> str:
    words = {
        0: "Keine",
        1: "Ein",
        2: "Zwei",
        3: "Drei",
        4: "Vier",
        5: "Fünf",
        6: "Sechs",
        7: "Sieben",
        8: "Acht",
        9: "Neun",
        10: "Zehn",
    }
    return words.get(count, format_number(count))


def matched_interests_text(result, show_weights: bool) -> str:
    if not result.score.matched_interests:
        return "Schöner Ort in deinem Radius"
    if show_weights:
        interests = ", ".join(
            f"{display_label(tag)} ({weight})"
            for tag, weight in result.score.matched_interests
        )
    else:
        interests = ", ".join(
            display_label(tag)
            for tag, _weight in result.score.matched_interests
        )
    return f"Trifft deine Interessen: {interests}"


def why_text(result, show_interest_weights: bool) -> str:
    if is_service_poi(result.poi):
        if result.score.matched_services:
            return "Passt zu deinen Bedürfnissen: " + display_labels(result.score.matched_services)
        return "Service-Ort in deiner Nähe"
    return matched_interests_text(result, show_interest_weights)


def details_items(result) -> list[str]:
    if is_service_poi(result.poi):
        if result.poi.services:
            return [display_label(tag) for tag in sorted(result.poi.services)]
        return ["Keine Services angegeben"]
    if result.experience_tags:
        return [display_label(tag) for tag in result.experience_tags]
    return ["Kein Erlebnis-Schwerpunkt angegeben"]


def notes_for(result) -> list[str]:
    notes = []
    if result.poi.oeffnungszeiten_relevant:
        notes.append("Öffnungszeiten prüfen")
    if result.poi.notes:
        notes.append(result.poi.notes)
    return notes


def render_summary_card(key: str, label: str, count: int, is_active: bool) -> str:
    active_class = " active" if is_active else ""
    aria_pressed = "true" if is_active else "false"
    return f"""
      <button class="summary-card summary-{h(key)}{active_class}" type="button" data-filter="{h(key)}" aria-pressed="{aria_pressed}" aria-label="{h(label)} anzeigen, {h(count)} Treffer">
        <div class="summary-number">{h(count)}</div>
        <div class="summary-label">{h(label)}</div>
      </button>
    """


def fit_label(score: float) -> str:
    if score >= 12:
        return "Passt sehr gut"
    if score >= 8:
        return "Passt gut"
    return "Kann passen"


def render_page_script() -> str:
    return """  <script>
    (() => {
      const filterButtons = Array.from(document.querySelectorAll("[data-filter]"));
      const sections = Array.from(document.querySelectorAll("[data-section]"));
      let activeFilter = filterButtons.find((button) => button.getAttribute("aria-pressed") === "true")?.dataset.filter || "";

      const setFilter = (key) => {
        activeFilter = key || "";

        filterButtons.forEach((button) => {
          const isActive = activeFilter !== "" && button.dataset.filter === activeFilter;
          button.classList.toggle("active", isActive);
          button.setAttribute("aria-pressed", isActive ? "true" : "false");
        });

        sections.forEach((section) => {
          section.hidden = activeFilter !== "" && section.dataset.section !== activeFilter;
        });
      };

      filterButtons.forEach((button) => {
        button.addEventListener("click", () => {
          const nextFilter = activeFilter === button.dataset.filter ? "" : button.dataset.filter;
          setFilter(nextFilter);
        });
      });

      const savedPlaces = new Map();
      const saveButtons = Array.from(document.querySelectorAll("[data-save-place]"));
      const favoritesToggle = document.querySelector("[data-favorites-toggle]");
      const favoritesBody = document.querySelector("[data-favorites-body]");
      const favoritesList = document.querySelector("[data-favorites-list]");
      const favoritesEmpty = document.querySelector("[data-favorites-empty]");
      const categoryLabels = {
        stays: "Übernachten",
        camper_services: "Services",
        experiences: "Erleben",
      };
      const categoryOrder = ["Übernachten", "Services", "Erleben"];

      const setButtonState = (button, isSaved) => {
        const name = button.dataset.placeName;
        button.classList.toggle("saved", isSaved);
        button.setAttribute("aria-pressed", isSaved ? "true" : "false");
        button.setAttribute(
          "aria-label",
          isSaved ? `${name} aus Merkliste entfernen` : `${name} merken`
        );
        button.textContent = isSaved ? "Gemerkt" : "Merken";
      };

      const jumpToPlace = (button) => {
        const section = button.closest("[data-section]");
        const card = button.closest("[data-place-card]");

        if (section?.dataset.section) {
          setFilter(section.dataset.section);
        }

        if (!card) {
          return;
        }

        card.scrollIntoView({ behavior: "smooth", block: "center" });
        card.classList.add("favorite-highlight");
        window.setTimeout(() => {
          card.classList.remove("favorite-highlight");
        }, 1400);
      };

      const renderFavorites = () => {
        if (!favoritesList || !favoritesEmpty) {
          return;
        }

        favoritesList.textContent = "";
        favoritesEmpty.hidden = savedPlaces.size > 0;

        categoryOrder.forEach((categoryName) => {
          const groupItems = saveButtons.filter((button) => {
            const place = savedPlaces.get(button.dataset.placeId);
            return place?.category === categoryName;
          });

          if (groupItems.length === 0) {
            return;
          }

          const heading = document.createElement("li");
          heading.className = "favorite-group-heading";
          heading.textContent = categoryName;
          favoritesList.appendChild(heading);

          groupItems.forEach((button) => {
            const id = button.dataset.placeId;
            const place = savedPlaces.get(id);
            const item = document.createElement("li");
            item.className = "favorite-item";

            const jumpButton = document.createElement("button");
            jumpButton.className = "favorite-jump";
            jumpButton.type = "button";
            jumpButton.textContent = place.name;
            jumpButton.addEventListener("click", () => {
              jumpToPlace(button);
            });

            const removeButton = document.createElement("button");
            removeButton.className = "favorite-remove";
            removeButton.type = "button";
            removeButton.textContent = "Entfernen";
            removeButton.setAttribute("aria-label", `${place.name} aus Merkliste entfernen`);
            removeButton.addEventListener("click", () => {
              savedPlaces.delete(id);
              setButtonState(button, false);
              renderFavorites();
            });

            item.append(jumpButton, removeButton);
            favoritesList.appendChild(item);
          });
        });
      };

      saveButtons.forEach((button) => {
        button.addEventListener("click", () => {
          const id = button.dataset.placeId;
          const name = button.dataset.placeName;

          if (savedPlaces.has(id)) {
            savedPlaces.delete(id);
          } else {
            const section = button.closest("[data-section]");
            const category = categoryLabels[section?.dataset.section] || "";
            savedPlaces.set(id, { name, category });
          }

          setButtonState(button, savedPlaces.has(id));
          renderFavorites();
        });
      });

      if (favoritesToggle && favoritesBody) {
        favoritesToggle.addEventListener("click", () => {
          const isExpanded = favoritesToggle.getAttribute("aria-expanded") === "true";
          favoritesToggle.setAttribute("aria-expanded", isExpanded ? "false" : "true");
          favoritesBody.hidden = isExpanded;
        });
      }

      renderFavorites();

    })();
  </script>"""


def render_fact_chip(label: str, value: str, class_name: str = "") -> str:
    classes = "chip fact-chip"
    if class_name:
        classes += f" {class_name}"
    return f'<span class="{classes}"><span>{h(label)}</span>{h(value)}</span>'


def render_detail_chip(value: str) -> str:
    return f'<span class="chip detail-chip">{h(value)}</span>'


def join_today_reasons(reasons: list[str]) -> str:
    if len(reasons) == 1:
        return reasons[0]
    return " und ".join(reasons)


def today_sentence(text: str) -> str:
    if text:
        text = text[0].upper() + text[1:]
    return f"Heute passend: {text}."


def focus_pair_text(tags: set[str]) -> str:
    if "aussicht" in tags and "natur" in tags:
        return "Aussicht und Natur"
    if "natur" in tags and "wasser" in tags:
        return "Natur und Wasser"
    if "aussicht" in tags:
        return "Aussicht"
    if "natur" in tags:
        return "Natur"
    return "diesen Ausflug"


def dry_window_experience_reason(tags: set[str]) -> str:
    focus = focus_pair_text(tags)
    if focus == "diesen Ausflug":
        return "passt gut, wenn das Wetter kurz aufmacht"
    verb = "passen" if " und " in focus else "passt"
    return f"{focus} {verb} gut, wenn das Wetter kurz aufmacht"


def weather_today_reason(poi, weather: str) -> str:
    if weather == "rainy":
        if poi.indoor_anteil == 1.0:
            return "regenfreundlich"
        if poi.indoor_anteil == 0.5:
            return "teilweise wettergeschützt"
        return ""
    if weather == "sunny":
        if poi.indoor_anteil == 0.0:
            return dry_window_experience_reason(poi.tags)
        if poi.indoor_anteil == 0.5:
            return "teils wettergeschützt für ein trockenes oder sonniges Zeitfenster"
    return ""


def weather_chip_text(poi, weather: str) -> str:
    if weather == "sunny":
        if poi.indoor_anteil == 1.0:
            return "Bei trockenem Zeitfenster weniger passend: indoor"
        if poi.indoor_anteil == 0.5:
            return "Bei trockenem Zeitfenster neutral: teils wettergeschützt"
        return "Bei trockenem Zeitfenster ideal: draußen"
    return weather_sentence(poi, weather)


def distance_today_reason(distance_km: float) -> str:
    if distance_km <= 5:
        return f"nur {format_number(distance_km)} km entfernt"
    if distance_km <= 10:
        return "kurzer Weg"
    return ""


def interest_today_reason(result) -> str:
    if not result.score.matched_interests:
        return ""
    labels = [display_label(tag) for tag, _weight in result.score.matched_interests[:2]]
    verb = "passt" if len(labels) == 1 else "passen"
    return join_today_reasons(labels) + f" {verb} zu deinen Vorlieben"


def today_hint_text(result, weather: str) -> str:
    poi = result.poi
    score = result.score
    reasons = []
    weather_reason = weather_today_reason(poi, weather)
    distance_reason = distance_today_reason(poi.distance_km)
    service_reason = "Versorgung vor Ort" if is_service_poi(poi) and score.matched_services else ""

    if poi.overnight_allowed is True:
        reasons.append("Übernachten möglich")
        if service_reason:
            reasons.append(service_reason)
        elif distance_reason:
            reasons.append(distance_reason)

    elif is_service_poi(poi):
        if weather == "rainy" and poi.indoor_anteil == 1.0:
            reasons.append("regenfreundlich")
        if distance_reason:
            reasons.append(distance_reason)
        if service_reason:
            reasons.append("gute Versorgung")
        if not reasons and weather_reason:
            reasons.append(weather_reason)

    else:
        if weather == "sunny" and poi.indoor_anteil == 0.0:
            if poi.distance_km <= 5:
                return today_sentence(
                    f"nur {format_number(poi.distance_km)} km entfernt und gut für ein trockenes Zeitfenster"
                )
            return today_sentence(weather_reason)
        if weather_reason:
            reasons.append(weather_reason)
        if distance_reason:
            reasons.append(distance_reason)
        if not weather_reason and len(reasons) < 2:
            interest_reason = interest_today_reason(result)
            if interest_reason:
                reasons.append(interest_reason)

    if weather_reason and not reasons:
        reasons.append(weather_reason)

    if not reasons:
        reasons.append("gute Passung zu deinem Reiseszenario")

    return today_sentence(join_today_reasons(reasons[:2]))


def render_recommendation_card(result, weather: str, show_interest_weights: bool) -> str:
    fit_text = fit_label(result.score.total)
    today_hint = today_hint_text(result, weather)
    notes = notes_for(result)
    notes_html = ""
    if notes:
        notes_html = '<p class="note-text">Hinweis: ' + h(" · ".join(notes)) + "</p>"

    fact_chips = [
        render_fact_chip("Entfernung", f"{format_number(result.poi.distance_km)} km"),
    ]

    if is_service_poi(result.poi) or result.poi.price_chf is not None:
        fact_chips.append(render_fact_chip("Preis", format_price(result.poi.price_chf)))

    if result.poi.overnight_allowed is not None:
        fact_chips.append(
            render_fact_chip("Übernachten", format_bool_de(result.poi.overnight_allowed))
        )

    fact_chips.append(
        render_fact_chip("Wetter", weather_chip_text(result.poi, weather), "weather-chip")
    )

    details_html = "\n".join(render_detail_chip(item) for item in details_items(result))
    service_summary_html = ""
    if is_service_poi(result.poi):
        service_summary_html = f"""
        <div class="service-summary">
          <div class="detail-label">Vor Ort</div>
          <div class="chip-row detail-row">{details_html}</div>
        </div>"""
    why = why_text(result, show_interest_weights)

    return f"""
      <article class="place-card" data-place-card>
        <div class="card-topline">
          <span class="category-pill">{h(format_category(result.poi.poi_type))}</span>
          <span class="fit-pill">{h(fit_text)}</span>
        </div>
        <div class="place-title-row">
          <h3>{h(result.poi.name)}</h3>
          <button class="save-button" type="button" data-save-place data-place-id="{h(result.poi.id)}" data-place-name="{h(result.poi.name)}" aria-pressed="false" aria-label="{h(result.poi.name)} merken">Merken</button>
        </div>
        <p class="today-hint">{h(today_hint)}</p>
        <p class="why">{h(why)}</p>{service_summary_html}
        <div class="chip-row fact-row">
          {"".join(fact_chips)}
        </div>
{notes_html}
      </article>
"""


def render_section(
    key: str,
    results: list,
    scenario: DemoScenario,
    active_key: str,
    weather: str,
    show_interest_weights: bool,
) -> str:
    title = scenario.section_labels[key]
    hidden_attr = "" if key == active_key else " hidden"
    count_label = f"{len(results)} Treffer" if results else "Keine Treffer"
    if not results:
        content_html = (
            '      <p class="empty-state">Für diesen Bereich gibt es gerade keine passenden Treffer.</p>'
        )
    else:
        cards = "\n".join(
            render_recommendation_card(result, weather, show_interest_weights)
            for result in results
        )
        content_html = f"""      <div class="cards">
        {cards}
      </div>"""

    return f"""
    <section class="section" data-section="{h(key)}"{hidden_attr}>
      <div class="section-heading">
        <h2>{h(title)}</h2>
        <span>{h(count_label)}</span>
      </div>
{content_html}
    </section>
    """


def visible_section_keys(grouped: dict, scenario: DemoScenario) -> list[str]:
    keys = [
        key
        for key in scenario.section_order
        if scenario.show_empty_sections or grouped[key]
    ]
    if keys:
        return keys
    return [scenario.default_active_section]


def active_section_key(grouped: dict, scenario: DemoScenario, section_keys: list[str]) -> str:
    if scenario.default_active_section in section_keys:
        return scenario.default_active_section
    for key in section_keys:
        if grouped[key]:
            return key
    return section_keys[0]


def render_intro(scenario: DemoScenario, grouped: dict, section_keys: list[str]) -> str:
    if not scenario.intro_template:
        return ""
    count = sum(len(grouped[key]) for key in section_keys)
    proposal_word = "Vorschlag" if count == 1 else "Vorschläge"
    text = scenario.intro_template.format(
        count=count,
        count_word=count_word_de(count),
        proposal_word=proposal_word,
    )
    return f'      <p class="intro-text">{h(text)}</p>'


def render_favorites_panel() -> str:
    return """      <section class="favorites-panel" aria-label="Gemerkte Orte">
        <button class="favorites-heading" type="button" data-favorites-toggle aria-expanded="true">Gemerkte Orte</button>
        <div data-favorites-body>
          <p class="favorites-empty" data-favorites-empty>Noch keine Orte gemerkt.</p>
          <ul class="favorites-list" data-favorites-list></ul>
        </div>
      </section>"""


def render_html(
    scenario: DemoScenario,
    profile,
    recommendations: list,
    experience_recommendations=None,
) -> str:
    visible_recommendations = recommendations[: scenario.top]
    grouped = group_recommendations(visible_recommendations)
    section_weather = {key: scenario.weather for key in scenario.section_order}
    section_interest_weights = {
        key: scenario.show_interest_weights for key in scenario.section_order
    }
    if experience_recommendations is not None:
        grouped["experiences"] = experience_recommendations[:EXPERIENCE_TOP]
        section_weather["experiences"] = EXPERIENCE_WEATHER
        section_interest_weights["experiences"] = False

    section_keys = visible_section_keys(grouped, scenario)
    active_key = active_section_key(grouped, scenario, section_keys)

    summary_html = "\n".join(
        render_summary_card(
            key,
            scenario.summary_labels[key],
            len(grouped[key]),
            key == active_key,
        )
        for key in section_keys
    )
    sections_html = "\n".join(
        render_section(
            key,
            grouped[key],
            scenario,
            active_key,
            section_weather[key],
            section_interest_weights[key],
        )
        for key in section_keys
    )
    intro_html = render_intro(scenario, grouped, section_keys)
    favorites_html = render_favorites_panel()

    section_count = len(section_keys)
    page_script_html = render_page_script()

    context = (
        f"{profile.profile_name} · {weather_label(scenario.weather)} · "
        f"{format_number(profile.radius_km)} km"
    )

    return f"""<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{h(scenario.document_title)}</title>
  <style>
    :root {{
      --blue-950: #08233f;
      --blue-900: #0b3158;
      --blue-700: #1769aa;
      --blue-500: #2f96d4;
      --blue-100: #e8f4ff;
      --blue-50: #f4faff;
      --aqua-100: #dcfbf5;
      --aqua-700: #0f7c73;
      --mint-100: #e7f8ec;
      --mint-700: #217346;
      --warm-100: #fff3d6;
      --warm-700: #a85d00;
      --ink: #14324a;
      --muted: #5d7386;
      --card: #ffffff;
      --line: #d7e8f6;
      --shadow: 0 18px 45px rgba(13, 67, 110, 0.14);
    }}

    * {{
      box-sizing: border-box;
    }}

    body {{
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: var(--ink);
      background:
        radial-gradient(circle at top left, rgba(47, 150, 212, 0.18), transparent 28rem),
        radial-gradient(circle at bottom right, rgba(15, 124, 115, 0.14), transparent 26rem),
        linear-gradient(180deg, #f7fcff 0%, #eaf5ff 100%);
      min-height: 100vh;
    }}

    .stage {{
      min-height: 100vh;
      display: flex;
      align-items: flex-start;
      justify-content: center;
      padding: 28px 14px 40px;
    }}

    .phone-shell {{
      width: min(600px, 100%);
      margin: 0 auto;
      background: #f7fbff;
      border: 1px solid rgba(186, 218, 242, 0.9);
      border-radius: 34px;
      box-shadow:
        0 32px 80px rgba(8, 35, 63, 0.24),
        0 0 0 8px rgba(255, 255, 255, 0.44);
      overflow: hidden;
    }}

    .hero {{
      color: white;
      background: linear-gradient(135deg, var(--blue-950), var(--blue-700));
      padding: 24px 20px 22px;
      overflow: hidden;
      position: relative;
    }}

    .hero::after {{
      content: "";
      position: absolute;
      inset: auto -60px -72px auto;
      width: 180px;
      height: 180px;
      background: rgba(255, 255, 255, 0.12);
      border-radius: 999px;
    }}

    .eyebrow {{
      margin: 0 0 10px;
      font-size: 0.78rem;
      color: #bfe3ff;
      font-weight: 700;
      letter-spacing: 0.02em;
    }}

    h1 {{
      margin: 0;
      font-size: 2.55rem;
      line-height: 0.95;
      letter-spacing: 0;
    }}

    .subtitle {{
      margin: 12px 0 0;
      font-size: 1rem;
      color: #e2f3ff;
      max-width: 310px;
    }}

    .context {{
      display: inline-flex;
      margin-top: 16px;
      padding: 8px 11px;
      border: 1px solid rgba(255, 255, 255, 0.28);
      border-radius: 999px;
      background: rgba(255, 255, 255, 0.12);
      color: #f5fbff;
      font-size: 0.88rem;
      font-weight: 650;
    }}

    .summary {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(110px, 1fr));
      gap: 8px;
      margin: 14px 14px 12px;
    }}

    .summary-card {{
      appearance: none;
      width: 100%;
      background: rgba(255, 255, 255, 0.78);
      border: 1px solid var(--line);
      border-radius: 17px;
      padding: 12px 10px;
      box-shadow: 0 8px 22px rgba(13, 67, 110, 0.08);
      color: inherit;
      cursor: pointer;
      font: inherit;
      text-align: left;
      transition: border-color 160ms ease, box-shadow 160ms ease, transform 160ms ease;
    }}

    .summary-card.active {{
      border-color: var(--blue-700);
      box-shadow:
        0 0 0 2px rgba(23, 105, 170, 0.16),
        0 10px 26px rgba(13, 67, 110, 0.13);
    }}

    .summary-card:hover {{
      transform: translateY(-1px);
    }}

    .summary-card:focus-visible {{
      outline: 2px solid var(--blue-500);
      outline-offset: 3px;
    }}

    .summary-stays {{
      background: linear-gradient(135deg, #ffffff, #e8f4ff);
      border-color: #b9def8;
    }}

    .summary-camper_services {{
      background: linear-gradient(135deg, #ffffff, #e5fbf5);
      border-color: #aee8d6;
    }}

    .summary-experiences {{
      background: linear-gradient(135deg, #ffffff, #eef5ff);
      border-color: #c7dcff;
    }}

    .summary-number {{
      color: var(--blue-900);
      font-size: 1.55rem;
      font-weight: 800;
      line-height: 1;
    }}

    .summary-label {{
      margin-top: 5px;
      color: var(--muted);
      font-size: 0.78rem;
      font-weight: 700;
    }}

    .intro-text {{
      margin: 0 18px 18px;
      color: var(--blue-900);
      font-size: 0.95rem;
      font-weight: 700;
      line-height: 1.45;
    }}

    .favorites-panel {{
      margin: 0 18px 18px;
      padding: 12px;
      border: 1px solid #cfe4f5;
      border-radius: 18px;
      background: rgba(244, 250, 255, 0.82);
    }}

    .favorites-heading {{
      display: inline-flex;
      align-items: center;
      padding: 0;
      border: 0;
      background: transparent;
      color: var(--blue-900);
      cursor: pointer;
      font-family: inherit;
      font-size: 0.86rem;
      font-weight: 850;
      margin-bottom: 6px;
    }}

    .favorites-heading:focus-visible {{
      outline: 2px solid var(--blue-500);
      outline-offset: 3px;
    }}

    .favorites-empty {{
      margin: 0;
      color: var(--muted);
      font-size: 0.84rem;
      line-height: 1.35;
    }}

    .favorites-list {{
      margin: 0;
      padding-left: 0;
      color: var(--ink);
      font-size: 0.86rem;
      font-weight: 700;
      line-height: 1.45;
      list-style: none;
    }}

    .favorites-list:empty {{
      display: none;
    }}

    .favorite-item {{
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 3px 0 4px;
    }}

    .favorite-jump {{
      flex: 0 1 auto;
      padding: 0;
      border: 0;
      background: transparent;
      color: var(--ink);
      cursor: pointer;
      font-family: inherit;
      font-size: inherit;
      font-weight: 800;
      text-align: left;
    }}

    .favorite-group-heading {{
      margin: 9px 0 2px;
      color: var(--blue-700);
      font-size: 0.72rem;
      font-weight: 850;
      text-transform: uppercase;
    }}

    .favorite-remove {{
      min-height: 24px;
      padding: 3px 7px;
      border: 1px solid transparent;
      border-radius: 999px;
      background: transparent;
      color: var(--muted);
      cursor: pointer;
      font-family: inherit;
      font-size: 0.72rem;
      font-weight: 850;
    }}

    .section {{
      margin: 22px 14px 0;
    }}

    .section[hidden] {{
      display: none;
    }}

    .section-heading {{
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 10px;
    }}

    h2 {{
      margin: 0;
      font-size: 1.3rem;
      color: var(--blue-950);
      letter-spacing: 0;
    }}

    .section-heading span {{
      color: var(--blue-700);
      font-weight: 750;
      white-space: nowrap;
    }}

    .cards {{
      display: grid;
      grid-template-columns: 1fr;
      gap: 13px;
    }}

    .place-card {{
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 24px;
      padding: 16px;
      box-shadow: 0 12px 28px rgba(13, 67, 110, 0.12);
      transition: border-color 180ms ease, box-shadow 180ms ease;
    }}

    .place-card.favorite-highlight {{
      border-color: var(--blue-500);
      box-shadow: 0 0 0 3px rgba(42, 139, 217, 0.18), 0 12px 28px rgba(13, 67, 110, 0.12);
    }}

    .card-topline {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 10px;
      margin-bottom: 12px;
      flex-wrap: wrap;
    }}

    .category-pill,
    .fit-pill {{
      display: inline-flex;
      align-items: center;
      min-height: 29px;
      padding: 6px 10px;
      border-radius: 999px;
      font-size: 0.8rem;
      font-weight: 800;
    }}

    .category-pill {{
      background: var(--blue-100);
      color: var(--blue-900);
    }}

    .fit-pill {{
      background: var(--mint-100);
      color: var(--mint-700);
      border: 1px solid #bde8c8;
      white-space: nowrap;
    }}

    .place-title-row {{
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 10px;
    }}

    .place-title-row h3 {{
      flex: 1;
      min-width: 0;
    }}

    h3 {{
      margin: 0;
      color: var(--blue-950);
      font-size: 1.13rem;
      letter-spacing: 0;
    }}

    .save-button {{
      min-height: 32px;
      padding: 6px 10px;
      border: 1px solid #b9def8;
      border-radius: 999px;
      background: var(--blue-50);
      color: var(--blue-900);
      cursor: pointer;
      font-family: inherit;
      font-size: 0.78rem;
      font-weight: 850;
      white-space: nowrap;
      transition: background 160ms ease, border-color 160ms ease, color 160ms ease;
    }}

    .save-button.saved {{
      background: var(--blue-700);
      border-color: var(--blue-700);
      color: #ffffff;
    }}

    .save-button:focus-visible {{
      outline: 2px solid var(--blue-500);
      outline-offset: 2px;
    }}

    .today-hint {{
      margin: 10px 0 8px;
      padding: 9px 10px;
      border: 1px solid #c4ead5;
      border-radius: 15px;
      background: #f1fbf5;
      color: #1d6845;
      line-height: 1.38;
      font-size: 0.88rem;
      font-weight: 800;
    }}

    .why {{
      margin: 0 0 14px;
      color: var(--muted);
      line-height: 1.45;
      font-size: 0.95rem;
    }}

    .chip-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }}

    .fact-row {{
      margin: 0 0 13px;
    }}

    .service-summary {{
      margin: 0 0 13px;
    }}

    .chip {{
      display: inline-flex;
      align-items: center;
      min-height: 35px;
      border-radius: 999px;
      font-size: 0.82rem;
      line-height: 1.2;
      font-weight: 750;
      padding: 8px 10px;
      max-width: 100%;
    }}

    .fact-chip {{
      flex: 1 1 140px;
      background: var(--blue-100);
      color: var(--blue-900);
      border: 1px solid #cae7fb;
      gap: 6px;
    }}

    .fact-chip span {{
      color: var(--muted);
      font-weight: 750;
    }}

    .weather-chip {{
      flex-basis: 100%;
      background: #edf7ff;
    }}

    .detail-label {{
      color: var(--muted);
      font-size: 0.8rem;
      font-weight: 850;
      margin-bottom: 8px;
    }}

    .detail-chip {{
      background: var(--aqua-100);
      color: var(--aqua-700);
      border: 1px solid #b9eee2;
    }}

    .note-text {{
      margin: 14px 0 0;
      padding: 10px 11px;
      border-radius: 16px;
      background: #fff9ea;
      color: #795000;
      line-height: 1.45;
      font-size: 0.88rem;
    }}

    .footnote {{
      margin: 24px 18px 24px;
      color: var(--muted);
      text-align: center;
      font-size: 0.78rem;
      line-height: 1.4;
    }}

    .empty {{
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 18px;
      padding: 20px;
      color: var(--muted);
    }}

    .empty-state {{
      margin: 0;
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 18px;
      padding: 18px;
      color: var(--muted);
      line-height: 1.45;
    }}

    @media (max-width: 760px) {{
      .stage {{
        padding: 0;
      }}

      .phone-shell {{
        width: 100%;
        min-height: 100vh;
        border-radius: 0;
        border: 0;
        box-shadow: none;
      }}

      .hero {{
        padding: 22px 18px 20px;
      }}

      .section-heading {{
        gap: 8px;
      }}

      .chip {{
        min-height: 38px;
      }}
    }}

    @media (max-width: 440px) {{
      .summary {{
        grid-template-columns: repeat(auto-fit, minmax(96px, 1fr));
      }}

      .place-title-row {{
        flex-direction: column;
        align-items: stretch;
      }}

      .save-button {{
        align-self: flex-start;
      }}

      .fact-chip {{
        flex-basis: 100%;
      }}
    }}
  </style>
</head>
<body>
  <main class="stage">
    <div class="phone-shell">
      <header class="hero">
        <p class="eyebrow">Lokale Demo mit Beispiel-Daten</p>
        <h1>Scout4U</h1>
        <p class="subtitle">{h(scenario.subtitle)}</p>
        <div class="context">{h(context)}</div>
      </header>

      <section class="summary" style="--summary-count: {h(section_count)}" aria-label="Zusammenfassung">
        {summary_html}
      </section>

{intro_html}
{favorites_html}

      {sections_html}

      <p class="footnote">Diese HTML-Seite wird lokal aus CSV-Testdaten erzeugt. Keine Live-Daten, keine Karte, keine API.</p>
    </div>
  </main>
{page_script_html}
</body>
</html>
"""


def load_recommendations(pois_path: Path, profiles_path: Path, profile_id: str, weather: str):
    pois = parse_pois(pois_path)
    profiles = parse_profiles(profiles_path)
    profile = select_profile(profiles, profile_id)
    recommendations, _filtered = evaluate_pois(pois, profile, weather)
    return profile, recommendations


def build_experience_recommendations() -> list:
    _profile, recommendations = load_recommendations(
        EXPERIENCE_POIS_PATH,
        EXPERIENCE_PROFILES_PATH,
        EXPERIENCE_PROFILE_ID,
        EXPERIENCE_WEATHER,
    )
    return recommendations[:EXPERIENCE_TOP]


def build_demo(scenario: DemoScenario) -> None:
    profile, recommendations = load_recommendations(
        scenario.pois_path,
        scenario.profiles_path,
        scenario.profile_id,
        scenario.weather,
    )
    experience_recommendations = build_experience_recommendations()
    html = render_html(scenario, profile, recommendations, experience_recommendations)
    scenario.output_path.write_text(html, encoding="utf-8")
    print(f"HTML-Demo erzeugt: {scenario.output_path}")


def main() -> int:
    for scenario in SCENARIOS:
        build_demo(scenario)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
