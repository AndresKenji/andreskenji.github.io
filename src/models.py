from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, EmailStr, model_validator

LANGUAGES = ("en", "es")


class I18nStr(BaseModel):
    """Un texto con una versión por idioma.

    Acepta también un string plano, que se replica en todos los idiomas. Eso
    mantiene tolerante tanto la migración como la edición a mano del JSON.
    """
    en: str
    es: str

    @model_validator(mode="before")
    @classmethod
    def _coerce_plain_string(cls, value):
        if isinstance(value, str):
            return {lang: value for lang in LANGUAGES}
        return value

    def get(self, lang: str) -> str:
        return getattr(self, lang, self.en)

    def __str__(self) -> str:
        return self.en


class Location(BaseModel):
    address: str
    postal_code: str
    city: str
    country_code: str
    region: str


class Profile(BaseModel):
    network: str
    username: str
    url: str


class Basics(BaseModel):
    name: str
    label: I18nStr
    image: str
    email: EmailStr
    phone: str
    url: Optional[str]
    summary: I18nStr
    location: Location
    profiles: List[Profile]


class Work(BaseModel):
    name: str
    position: I18nStr
    url: Optional[str]
    start_date: str
    end_date: Optional[str] = None
    summary: I18nStr
    highlights: Optional[List[I18nStr]] = None


class Volunteer(BaseModel):
    organization: str
    position: I18nStr
    url: Optional[str]
    start_date: str
    end_date: Optional[str] = None
    summary: I18nStr
    highlights: Optional[List[I18nStr]] = None


class StudyType(str, Enum):
    ASSOCIATE = "Associate"
    BACHELOR = "Bachelor"
    MASTER = "Master"
    DOCTORAL = "Doctoral"
    TECHNICAL = "Technical"
    DIPLOMA = "Diploma"
    ONLINE_COURSE = "OnlineCourse"


class Education(BaseModel):
    institution: str
    url: str
    area: I18nStr
    study_type: StudyType
    start_date: str
    end_date: Optional[str] = None
    score: str
    courses: List[I18nStr] = []


class Awards(BaseModel):
    title: I18nStr
    date: str
    awarder: str
    summary: I18nStr


class Certificate(BaseModel):
    name: I18nStr
    date: str
    issuer: str
    url: str


class Publication(BaseModel):
    name: str
    publisher: str
    release_date: str
    url: str
    summary: I18nStr


class SkillLevel(str, Enum):
    NOVICE = "Novice"
    COMPETENT = "Competent"
    PROFICIENT = "Proficient"
    MASTER = "Master"

    def to_percentage(self) -> int:
        return {
            "Novice": 25,
            "Competent": 50,
            "Proficient": 75,
            "Master": 100
        }[self.value]


class Skill(BaseModel):
    name: I18nStr
    level: SkillLevel
    keywords: List[I18nStr] = []
    color: str = "#0070c0"
    level_percent: int = 0

    @model_validator(mode="after")
    def set_level_percent(cls, data):
        data.level_percent = data.level.to_percentage()
        return data


class Fluency(str, Enum):
    # ACTFL
    NOVICE = "Novice"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"
    SUPERIOR = "Superior"
    DISTINGUISHED = "Distinguished"
    NATIVE = "Native"
    # CEFR (los valores que se repiten quedan como alias del miembro anterior)
    A1 = "Beginner"
    A2 = "Elementary"
    B2 = "Upper Intermediate"
    C2 = "Proficient"


class Language(BaseModel):
    language: I18nStr
    fluency: Fluency


class Interest(BaseModel):
    name: I18nStr
    keywords: List[I18nStr] = []


class Reference(BaseModel):
    name: str
    reference: I18nStr
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


class Project(BaseModel):
    name: str
    start_date: str
    end_date: Optional[str] = None
    description: I18nStr
    highlights: List[I18nStr] = []
    url: str


class Resume(BaseModel):
    basics: Basics
    work: List[Work] = []
    volunteer: List[Volunteer] = []
    education: List[Education] = []
    awards: List[Awards] = []
    certificates: List[Certificate] = []
    publications: List[Publication] = []
    skills: List[Skill] = []
    languages: List[Language] = []
    interests: List[Interest] = []
    references: List[Reference] = []
    projects: List[Project] = []
