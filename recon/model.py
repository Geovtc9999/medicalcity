"""Modèle de données minimal du prototype de réconciliation e-comms.

Dix entités suffisent pour porter les trois niveaux de réconciliation
(populations, volumétrie, fidélité). Deux invariants dictent la forme :

- toute appartenance est **datée** : une personne change de rôle, de terminal,
  d'entité, et le périmètre attendu d'hier doit rester reconstituable ;
- un message conserve **sa preuve de distribution** (destinataires) même après
  dédoublonnage, parce que c'est l'information la plus utile en enquête.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum


class Channel(str, Enum):
    EMAIL = "email"          # Exchange / Exchange Online
    TEAMS = "teams"          # Microsoft Teams
    BLOOMBERG = "bloomberg"  # Bloomberg IB / MSG

    @property
    def label(self) -> str:
        return {"email": "Exchange/O365", "teams": "Teams", "bloomberg": "Bloomberg IB/MSG"}[self.value]


class Severity(str, Enum):
    CRITIQUE = "critique"
    MAJEURE = "majeure"
    MINEURE = "mineure"


class Status(str, Enum):
    OUVERTE = "ouverte"
    EXPLIQUEE = "expliquée"
    RESOLUE = "résolue"


@dataclass(frozen=True)
class Party:
    """Personne physique, indépendamment de ses comptes."""

    party_id: str
    nom: str
    entite: str
    hired_on: date
    terminated_on: date | None = None

    def active_on(self, day: date) -> bool:
        if day < self.hired_on:
            return False
        return self.terminated_on is None or day <= self.terminated_on


@dataclass(frozen=True)
class Identity:
    """Un compte, une adresse, un terminal : ce que voit une source."""

    identity_id: str
    channel: Channel
    handle: str
    valid_from: date
    valid_to: date | None = None
    source_ref: str = "directory"

    def active_on(self, day: date) -> bool:
        if day < self.valid_from:
            return False
        return self.valid_to is None or day <= self.valid_to


@dataclass(frozen=True)
class PartyIdentity:
    """Rattachement daté d'une identité à une personne."""

    party_id: str
    identity_id: str
    valid_from: date
    valid_to: date | None = None

    def active_on(self, day: date) -> bool:
        if day < self.valid_from:
            return False
        return self.valid_to is None or day <= self.valid_to


@dataclass(frozen=True)
class SupervisionScope:
    """Qui est supervisé, sur quel canal, du … au … — la liste tenue par Compliance."""

    party_id: str
    channel: Channel
    valid_from: date
    valid_to: date | None = None

    def active_on(self, day: date) -> bool:
        if day < self.valid_from:
            return False
        return self.valid_to is None or day <= self.valid_to


@dataclass(frozen=True)
class CaptureConfig:
    """Journalisation effectivement active sur une identité (ce que l'IT a paramétré).

    L'écart entre `SupervisionScope` (ce qui devait être capté) et `CaptureConfig`
    (ce qui l'est) est le niveau 1 de la réconciliation.
    """

    identity_id: str
    channel: Channel
    valid_from: date
    valid_to: date | None = None
    mechanism: str = "journal"

    def active_on(self, day: date) -> bool:
        if day < self.valid_from:
            return False
        return self.valid_to is None or day <= self.valid_to


@dataclass(frozen=True)
class Attachment:
    name: str
    size: int
    sha256: str


@dataclass
class Message:
    """Enregistrement canonique. `source_id` est la clé de la source, `content_hash`
    la clé de dédoublonnage ; les deux sont nécessaires."""

    source_id: str
    content_hash: str
    channel: Channel
    sender_identity: str
    recipients: tuple[str, ...]
    sent_at: datetime
    day: date
    thread_id: str
    subject: str
    body: str
    attachments: tuple[Attachment, ...] = ()
    version: int = 1
    edited_from: str | None = None
    encrypted: bool = False
    readable: bool = True
    is_canary: bool = False
    ingested_at: datetime | None = None

    @property
    def key(self) -> str:
        return f"{self.source_id}#v{self.version}"


@dataclass
class SourceBatch:
    """Lot livré par une source, avec son décompte **déclaré**.

    Le décompte déclaré est une déclaration de la source : il peut différer du
    contenu livré. C'est exactement ce que mesure le contrôle C06.
    """

    batch_id: str
    channel: Channel
    day: date
    declared_count: int
    messages: list[Message] = field(default_factory=list)
    received_at: datetime | None = None


@dataclass(frozen=True)
class ArchiveReceipt:
    """Accusé de prise en compte par l'archive : sans lui, le niveau 2 est bancal."""

    message_key: str
    archive: str
    acknowledged_at: datetime
    stored_hash: str
    attachment_count: int


@dataclass
class ControlResult:
    control_id: str
    libelle: str
    scope: str
    period: str
    expected: float | int | None
    observed: float | int | None
    verdict: str  # "ok" | "ko" | "non exécuté"
    detail: str = ""

    @property
    def ok(self) -> bool:
        return self.verdict == "ok"


@dataclass
class Exception_:
    """Écart qualifié. L'aging compte plus que le nombre : c'est l'ancienneté du
    plus vieil écart inexpliqué qu'un auditeur retient."""

    exception_id: str
    control_id: str
    severity: Severity
    scope: str
    cause: str
    owner: str
    opened_on: date
    status: Status = Status.OUVERTE
    due_in_days: int = 5

    def age_days(self, as_of: date) -> int:
        return max((as_of - self.opened_on).days, 0)

    def overdue(self, as_of: date) -> bool:
        return self.status is Status.OUVERTE and self.age_days(as_of) > self.due_in_days


@dataclass(frozen=True)
class Defect:
    """Défaut injecté par le générateur : la vérité terrain des tests."""

    code: str
    control_id: str
    scope: str
    description: str
