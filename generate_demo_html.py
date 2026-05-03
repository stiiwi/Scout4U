#!/usr/bin/env python3
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
    format_score,
    group_recommendations,
    is_service_poi,
    parse_pois,
    parse_profiles,
    select_profile,
    weather_sentence,
)


POIS_PATH = Path("pois_camper_test_sample.csv")
PROFILES_PATH = Path("profiles_camper_test_sample.csv")
PROFILE_ID = "V"
WEATHER = "rainy"
TOP = 10
OUTPUT_PATH = Path("demo.html")

SECTION_LABELS = {
    "stays": "Stellplätze",
    "camper_services": "Camper-Services",
    "experiences": "Ausflüge / schöne Orte",
}

SUMMARY_LABELS = {
    "stays": "Stellplätze",
    "camper_services": "Services",
    "experiences": "Ausflug",
}

TAB_LABELS = {
    "stays": "Stellplätze",
    "camper_services": "Services",
    "experiences": "Ausflüge",
}


def h(value) -> str:
    return escape(str(value), quote=True)


def weather_label(weather: str) -> str:
    labels = {
        "rainy": "Regen",
        "sunny": "Sonne",
    }
    return labels.get(weather, weather)


def matched_interests_text(result) -> str:
    if not result.score.matched_interests:
        return "Schöner Ort in deinem Radius"
    interests = ", ".join(
        f"{display_label(tag)} ({weight})"
        for tag, weight in result.score.matched_interests
    )
    return f"Trifft deine Interessen: {interests}"


def why_text(result) -> str:
    if is_service_poi(result.poi):
        if result.score.matched_services:
            return "Passt zu deinen Bedürfnissen: " + display_labels(result.score.matched_services)
        return "Service-Ort in deiner Nähe"
    return matched_interests_text(result)


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


def render_summary_card(key: str, label: str, count: int) -> str:
    return f"""
      <div class="summary-card summary-{h(key)}">
        <div class="summary-number">{h(count)}</div>
        <div class="summary-label">{h(label)}</div>
      </div>
    """


def render_tabs(grouped: dict) -> str:
    tabs = []
    for key, _ in RECOMMENDATION_SECTION_ORDER:
        active_class = " active" if grouped[key] else ""
        tabs.append(
            f'<span class="tab{active_class}">{h(TAB_LABELS[key])}</span>'
        )
    return "\n".join(tabs)


def render_fact_chip(label: str, value: str, class_name: str = "") -> str:
    classes = "chip fact-chip"
    if class_name:
        classes += f" {class_name}"
    return f'<span class="{classes}"><span>{h(label)}</span>{h(value)}</span>'


def render_detail_chip(value: str) -> str:
    return f'<span class="chip detail-chip">{h(value)}</span>'


def render_recommendation_card(result) -> str:
    detail_label = "Vor Ort" if is_service_poi(result.poi) else "Erlebnis"
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
        render_fact_chip("Wetter", weather_sentence(result.poi, WEATHER), "weather-chip")
    )

    details_html = "\n".join(render_detail_chip(item) for item in details_items(result))

    return f"""
      <article class="place-card">
        <div class="card-topline">
          <span class="category-pill">{h(format_category(result.poi.poi_type))}</span>
          <span class="fit-pill">Passung {h(format_score(result.score.total))}</span>
        </div>
        <h3>{h(result.poi.name)}</h3>
        <p class="why">{h(why_text(result))}</p>
        <div class="chip-row fact-row">
          {"".join(fact_chips)}
        </div>
        <div class="detail-block">
          <div class="detail-label">{h(detail_label)}</div>
          <div class="chip-row detail-row">{details_html}</div>
        </div>
        {notes_html}
      </article>
    """


def render_section(key: str, results: list) -> str:
    title = SECTION_LABELS[key]
    if not results:
        return ""

    cards = "\n".join(render_recommendation_card(result) for result in results)
    return f"""
    <section class="section">
      <div class="section-heading">
        <h2>{h(title)}</h2>
        <span>{h(len(results))} Treffer</span>
      </div>
      <div class="cards">
        {cards}
      </div>
    </section>
    """


def render_html(profile, weather: str, recommendations: list) -> str:
    visible_recommendations = recommendations[:TOP]
    grouped = group_recommendations(visible_recommendations)

    summary_html = "\n".join(
        render_summary_card(key, SUMMARY_LABELS[key], len(grouped[key]))
        for key, _ in RECOMMENDATION_SECTION_ORDER
    )
    tabs_html = render_tabs(grouped)
    sections_html = "\n".join(
        render_section(key, grouped[key])
        for key, _ in RECOMMENDATION_SECTION_ORDER
        if grouped[key]
    )
    if not sections_html:
        sections_html = '<p class="empty">Für diese Demo wurden keine passenden Orte gefunden.</p>'

    context = f"{profile.profile_name} · {weather_label(weather)} · {format_number(profile.radius_km)} km"

    return f"""<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Scout4U Demo</title>
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
      width: min(420px, 100%);
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
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 8px;
      margin: 14px 14px 12px;
    }}

    .summary-card {{
      background: rgba(255, 255, 255, 0.78);
      border: 1px solid var(--line);
      border-radius: 17px;
      padding: 12px 10px;
      box-shadow: 0 8px 22px rgba(13, 67, 110, 0.08);
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

    .tabs {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 6px;
      margin: 0 14px 18px;
      padding: 5px;
      border-radius: 999px;
      background: #e6f2fb;
      border: 1px solid #d2e7f6;
    }}

    .tab {{
      display: inline-flex;
      justify-content: center;
      align-items: center;
      min-height: 36px;
      padding: 7px 6px;
      border-radius: 999px;
      color: var(--muted);
      font-size: 0.8rem;
      font-weight: 800;
    }}

    .tab.active {{
      background: #ffffff;
      color: var(--blue-900);
      box-shadow: 0 5px 14px rgba(13, 67, 110, 0.11);
    }}

    .section {{
      margin: 22px 14px 0;
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
      background: var(--warm-100);
      color: var(--warm-700);
      border: 1px solid #ffd88e;
      white-space: nowrap;
    }}

    h3 {{
      margin: 0;
      color: var(--blue-950);
      font-size: 1.13rem;
      letter-spacing: 0;
    }}

    .why {{
      margin: 9px 0 14px;
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
      background: #edf7ff;
    }}

    .detail-block {{
      margin-top: 11px;
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
  </style>
</head>
<body>
  <main class="stage">
    <div class="phone-shell">
      <header class="hero">
        <p class="eyebrow">Lokale Demo mit Beispiel-Daten</p>
        <h1>Scout4U</h1>
        <p class="subtitle">Camper-Vorschläge rund um Bern</p>
        <div class="context">{h(context)}</div>
      </header>

      <section class="summary" aria-label="Zusammenfassung">
        {summary_html}
      </section>

      <nav class="tabs" aria-label="Demo-Bereiche">
        {tabs_html}
      </nav>

      {sections_html}

      <p class="footnote">Diese HTML-Seite wird lokal aus CSV-Testdaten erzeugt. Keine Live-Daten, keine Karte, keine API.</p>
    </div>
  </main>
</body>
</html>
"""


def main() -> int:
    pois = parse_pois(POIS_PATH)
    profiles = parse_profiles(PROFILES_PATH)
    profile = select_profile(profiles, PROFILE_ID)
    recommendations, _filtered = evaluate_pois(pois, profile, WEATHER)
    html = render_html(profile, WEATHER, recommendations)
    OUTPUT_PATH.write_text(html, encoding="utf-8")
    print(f"HTML-Demo erzeugt: {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
