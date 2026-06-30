from __future__ import annotations

import re

from app.domain.contracts import Ontology, OntologyEntity, SeedDocument

_WORD_RE = re.compile(r"[A-Za-z가-힣一-龥0-9]{2,}")


def extract_ontology(seed: SeedDocument) -> Ontology:
    words: list[str] = []
    for match in _WORD_RE.findall(seed.body):
        if match not in words and len(match) >= 2:
            words.append(match)
        if len(words) >= 5:
            break
    while len(words) < 3:
        words.append(f"Signal{len(words)+1}")
    entities = [OntologyEntity(name=word, type="Signal", rationale="seed document recurring term") for word in words[:5]]
    relations = [
        {"source": entities[i].name, "target": entities[(i + 1) % len(entities)].name, "type": "influences"}
        for i in range(min(3, len(entities)))
    ]
    return Ontology(entities=entities, relations=relations)
