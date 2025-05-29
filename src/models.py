from datetime import date
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, EmailStr


class Location(BaseModel):
    adress:str
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
    start_date:date
    end_date:date
    summary:str
    highlights:Optional[List[str]]

class Volunteer(BaseModel):
    organization:str
    position:str
    url:Optional[str]
    start_date:date
    end_date:date
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
    start_date:date
    end_date:date
    score:str
    courses:List[str]

class Awards(BaseModel):
    title:str
    date:date
    awarder:str
    summary:str

class Certificate(BaseModel):
    name:str
    date:date
    issuer:str
    url:str

class Publication(BaseModel):
    name:str
    publisher:str
    releaseDate:str
    url:str
    summary:str

class Skill(BaseModel):
    name:str
    level:str
    keywords:List[str]

class Fluency(Enum):
    # ACTFL
    NOVICE="Novice"	
    INTERMEDIATE="Intermediate"	
    ADVANCED="Advanced"	
    SUPERIOR="Superior"
    DISTINGUISHED="Distinguished"
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
    start_date:date
    end_date:date
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
    model_config = {
        "json_schema_extra" : {
            "examples" : [
                {
                    "basics": {
                        "name": "John Doe",
                        "label": "Programmer",
                        "image": "",
                        "email": "john@gmail.com",
                        "phone": "(912) 555-4321",
                        "url": "https://johndoe.com",
                        "summary": "A summary of John Doe…",
                        "location": {
                        "address": "2712 Broadway St",
                        "postalCode": "CA 94115",
                        "city": "San Francisco",
                        "countryCode": "US",
                        "region": "California"
                        },
                        "profiles": [{
                        "network": "Twitter",
                        "username": "john",
                        "url": "https://twitter.com/john"
                        }]
                    },
                    "work": [{
                        "name": "Company",
                        "position": "President",
                        "url": "https://company.com",
                        "startDate": "2013-01-01",
                        "endDate": "2014-01-01",
                        "summary": "Description…",
                        "highlights": [
                        "Started the company"
                        ]
                    }],
                    "volunteer": [{
                        "organization": "Organization",
                        "position": "Volunteer",
                        "url": "https://organization.com/",
                        "startDate": "2012-01-01",
                        "endDate": "2013-01-01",
                        "summary": "Description…",
                        "highlights": [
                        "Awarded 'Volunteer of the Month'"
                        ]
                    }],
                    "education": [{
                        "institution": "University",
                        "url": "https://institution.com/",
                        "area": "Software Development",
                        "studyType": "Bachelor",
                        "startDate": "2011-01-01",
                        "endDate": "2013-01-01",
                        "score": "4.0",
                        "courses": [
                        "DB1101 - Basic SQL"
                        ]
                    }],
                    "awards": [{
                        "title": "Award",
                        "date": "2014-11-01",
                        "awarder": "Company",
                        "summary": "There is no spoon."
                    }],
                    "certificates": [{
                        "name": "Certificate",
                        "date": "2021-11-07",
                        "issuer": "Company",
                        "url": "https://certificate.com"
                    }],
                    "publications": [{
                        "name": "Publication",
                        "publisher": "Company",
                        "releaseDate": "2014-10-01",
                        "url": "https://publication.com",
                        "summary": "Description…"
                    }],
                    "skills": [{
                        "name": "Web Development",
                        "level": "Master",
                        "keywords": [
                        "HTML",
                        "CSS",
                        "JavaScript"
                        ]
                    }],
                    "languages": [{
                        "language": "English",
                        "fluency": "Native speaker"
                    }],
                    "interests": [{
                        "name": "Wildlife",
                        "keywords": [
                        "Ferrets",
                        "Unicorns"
                        ]
                    }],
                    "references": [{
                        "name": "Jane Doe",
                        "reference": "Reference…"
                    }],
                    "projects": [{
                        "name": "Project",
                        "startDate": "2019-01-01",
                        "endDate": "2021-01-01",
                        "description": "Description...",
                        "highlights": [
                        "Won award at AIHacks 2016"
                        ],
                        "url": "https://project.com/"
                    }]
                }
            ]
            
            }
        }



