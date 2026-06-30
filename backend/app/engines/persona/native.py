from __future__ import annotations

from app.domain.contracts import Locale, Ontology, Persona


def build_personas(ontology: Ontology, locale: Locale) -> list[Persona]:
    labels = {
        Locale.KO: [("관찰자", "근거를 조심스럽게 검토"), ("확산자", "새로운 신호에 빠르게 반응"), ("회의론자", "데이터 부족을 강조")],
        Locale.ZH: [("观察者", "谨慎审查证据"), ("扩散者", "快速响应新信号"), ("怀疑者", "强调数据不足")],
        Locale.EN: [("Observer", "reviews evidence cautiously"), ("Amplifier", "reacts quickly to new signals"), ("Skeptic", "highlights data gaps")],
    }[locale]
    anchor = ontology.entities[0].name if ontology.entities else "seed"
    return [Persona(name=name, role=f"{anchor} persona", stance=stance) for name, stance in labels]
