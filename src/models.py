from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, EmailStr, model_validator


class Location(BaseModel):
    address:str
    postal_code:str
    city:str
    country_code:str
    region:str

class Profile(BaseModel):
    network:str
    username:str
    url:str

class Basics(BaseModel):
    name:str
    label:str
    image:str
    email:EmailStr
    phone:str
    url:Optional[str]
    summary:str
    location:Location
    profiles:List[Profile]

class Work(BaseModel):
    name:str
    position:str
    url:Optional[str]
    start_date:str
    end_date:str
    summary:str
    highlights:Optional[List[str]]

class Volunteer(BaseModel):
    organization:str
    position:str
    url:Optional[str]
    start_date:str
    end_date:str
    summary:str
    highlights:Optional[List[str]]

class StudyType(str, Enum):
    ASSOCIATE="Associate"
    BACHELOR="Bachelor"
    MASTER="Master"
    DOCTORAL="Doctoral"
    TECHNICAL="Technical"
    DIPLOMA="Diploma"
    ONLINE_COURSE="OnlineCourse"

class Education(BaseModel):
    institution:str
    url:str
    area:str
    study_type:StudyType
    start_date:str
    end_date:str
    score:str
    courses:List[str]

class Awards(BaseModel):
    title:str
    date:str
    awarder:str
    summary:str

class Certificate(BaseModel):
    name:str
    date:str
    issuer:str
    url:str

class Publication(BaseModel):
    name:str
    publisher:str
    release_date:str
    url:str
    summary:str


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
    name: str
    level: SkillLevel
    keywords: List[str]
    color: str = "#0070c0"
    level_percent: int = 0

    @model_validator(mode="after")
    def set_level_percent(cls, data):
        data.level_percent = data.level.to_percentage()
        return data


class Fluency(Enum):
    # ACTFL
    NOVICE="Novice"
    INTERMEDIATE="Intermediate"
    ADVANCED="Advanced"
    SUPERIOR="Superior"
    DISTINGUISHED="Distinguished"
    NATIVE="Native"
    # CEFR
    A1="Beginner"
    A2="Elementary"
    B1="Intermediate"
    B2="Upper Intermediate"
    C1="Advanced"
    C2="Proficient"

class Language(BaseModel):
    language:str
    fluency:Fluency

class Interest(BaseModel):
    name:str
    keywords:List[str]

class Reference(BaseModel):
    name:str
    reference:str
    email:Optional[EmailStr]
    phone:Optional[str]

class Project(BaseModel):
    name:str
    start_date:str
    end_date:str
    description:str
    highlights:List[str]
    url:str

class Resume(BaseModel):
    basics:Basics
    work:List[Work]
    volunteer:Optional[List[Volunteer]]
    education:List[Education]
    awards:Optional[List[Awards]]
    certificates:Optional[List[Certificate]]
    publications:Optional[List[Publication]]
    skills:List[Skill]
    languages:List[Language]
    interests:Optional[List[Interest]]
    references:Optional[List[Reference]]
    projects:Optional[List[Project]]



