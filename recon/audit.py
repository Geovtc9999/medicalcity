"""Piste d'audit append-only hash-chaînée.

Chaque entrée chaîne le hash de la précédente : réception d'un lot, résultat de
contrôle, ouverture ou clôture d'exception, export. Une modification silencieuse
devient détectable **sans faire confiance à l'exploitant**, ce qui est le seul
sens utile du mot « inaltérable ».

Le stockage réel serait un objet verrouillé (Object Lock / blob immuable) ; ici
un fichier JSONL suffit à démontrer la mécanique et à la tester.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

GENESIS = "0" * 64


def _canonical(payload: dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str, ensure_ascii=False)


@dataclass(frozen=True)
class Entry:
    seq: int
    at: str
    kind: str
    payload: dict[str, Any]
    prev_hash: str
    hash: str

    def recompute(self) -> str:
        return hashlib.sha256(
            f"{self.seq}|{self.at}|{self.kind}|{_canonical(self.payload)}|{self.prev_hash}".encode()
        ).hexdigest()

    def to_json(self) -> str:
        return json.dumps(
            {
                "seq": self.seq,
                "at": self.at,
                "kind": self.kind,
                "payload": self.payload,
                "prev_hash": self.prev_hash,
                "hash": self.hash,
            },
            sort_keys=True,
            default=str,
            ensure_ascii=False,
        )


class AuditJournal:
    """Journal en mémoire, persistable en JSONL. Aucune API de modification :
    `append` est la seule écriture possible."""

    def __init__(self, rules_version: str = "1.0.0") -> None:
        self._entries: list[Entry] = []
        self.rules_version = rules_version

    def append(self, kind: str, **payload: Any) -> Entry:
        payload.setdefault("rules_version", self.rules_version)
        seq = len(self._entries) + 1
        prev = self._entries[-1].hash if self._entries else GENESIS
        at = datetime.now(timezone.utc).isoformat(timespec="milliseconds")
        digest = hashlib.sha256(
            f"{seq}|{at}|{kind}|{_canonical(payload)}|{prev}".encode()
        ).hexdigest()
        entry = Entry(seq=seq, at=at, kind=kind, payload=payload, prev_hash=prev, hash=digest)
        self._entries.append(entry)
        return entry

    def __len__(self) -> int:
        return len(self._entries)

    def __iter__(self) -> Iterator[Entry]:
        return iter(self._entries)

    def verify(self) -> tuple[bool, str]:
        """Vérifie la chaîne. Retourne (intègre, explication)."""
        prev = GENESIS
        for i, entry in enumerate(self._entries, start=1):
            if entry.seq != i:
                return False, f"numérotation rompue à la position {i} (seq={entry.seq})"
            if entry.prev_hash != prev:
                return False, f"chaînage rompu à l'entrée {entry.seq}"
            if entry.recompute() != entry.hash:
                return False, f"contenu modifié à l'entrée {entry.seq}"
            prev = entry.hash
        return True, f"{len(self._entries)} entrées chaînées, chaîne intègre"

    def evidence_pack(self, kinds: tuple[str, ...] | None = None) -> list[dict[str, Any]]:
        """Extrait un pack de preuve : les entrées, avec la version des règles
        appliquées. Sans le versionnage des règles, on ne sait pas rejouer
        l'histoire — et une piste d'audit qu'on ne peut pas rejouer n'est pas une preuve."""
        return [
            {"seq": e.seq, "at": e.at, "kind": e.kind, "hash": e.hash, **e.payload}
            for e in self._entries
            if kinds is None or e.kind in kinds
        ]

    def write(self, path: Path) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(e.to_json() for e in self._entries) + "\n", encoding="utf-8")
        return path

    @staticmethod
    def read(path: Path) -> "AuditJournal":
        journal = AuditJournal()
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            raw = json.loads(line)
            journal._entries.append(
                Entry(
                    seq=raw["seq"],
                    at=raw["at"],
                    kind=raw["kind"],
                    payload=raw["payload"],
                    prev_hash=raw["prev_hash"],
                    hash=raw["hash"],
                )
            )
        return journal
