from __future__ import annotations

from pathlib import Path

from app.core.i18n import msg
from app.domain.contracts import HandoffManifest, Locale, SeedDocument


def key_points(topic: str, locale: Locale) -> list[str]:
    if locale == Locale.EN:
        return [
            f"Local evidence around {topic} is treated as the research seed.",
            "Market, media, and community signals are separated before simulation.",
            "Data gaps are preserved instead of being hidden as confident findings.",
        ]
    if locale == Locale.ZH:
        return [
            f"围绕“{topic}”的本地证据被整理为研究种子。",
            "市场、媒体与社区信号在模拟前被区分。",
            "数据不足会被保留为警告，而不是伪装成确定结论。",
        ]
    return [
        f"‘{topic}’에 대한 로컬 근거를 조사 seed로 정리합니다.",
        "시장·미디어·커뮤니티 신호를 시뮬레이션 전에 분리합니다.",
        "데이터 부족 구간은 확신처럼 숨기지 않고 경고로 보존합니다.",
    ]


def build_research_report(topic: str, locale: Locale) -> str:
    points = key_points(topic, locale)
    heading = msg(locale, "research_heading")
    return "\n\n".join([
        f"{heading}: {topic}",
        "## Key Signals" if locale == Locale.EN else ("## 核心信号" if locale == Locale.ZH else "## 핵심 신호"),
        "\n".join(f"- {point}" for point in points),
        "## Handoff Note" if locale == Locale.EN else ("## 交接说明" if locale == Locale.ZH else "## 핸드오프 메모"),
        msg(locale, "caveat"),
    ])


def seed_from_report(topic: str, locale: Locale, report: str) -> SeedDocument:
    points = [line[2:] for line in report.splitlines() if line.startswith("- ")]
    return SeedDocument(title=topic, locale=locale, body=report, key_points=points[:5])


def build_native_manifest(topic: str, locale: Locale, report_path: Path) -> HandoffManifest:
    return HandoffManifest(
        source_product="aquarium-native-research",
        target_product="aquarium",
        topic=topic,
        locale=locale,
        final_report_path=str(report_path),
        intermediate_outputs={"query": str(report_path), "media": str(report_path), "insight": str(report_path)},
        sources=[{"title": "Aquarium native evidence seed", "url": "aquarium://native/research", "snippet": topic}],
        provider="aquarium_native",
        data_gaps=["Native seed is deterministic/local until live source adapters are configured"],
    )
