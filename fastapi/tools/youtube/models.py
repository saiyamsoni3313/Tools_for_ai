from pydantic import BaseModel
from typing import List
from enum import Enum


class Language(Enum):
    Afrikaans = "af"
    Akan = "ak"
    Albanian = "sq"
    Amharic = "am"
    Arabic = "ar"
    Armenian = "hy"
    Assamese = "as"
    Aymara = "ay"
    Azerbaijani = "az"
    Bangla = "bn"
    Basque = "eu"
    Belarusian = "be"
    Bhojpuri = "bho"
    Bosnian = "bs"
    Bulgarian = "bg"
    Burmese = "my"
    Catalan = "ca"
    Cebuano = "ceb"
    Chinese_Simplified = "zh-Hans"
    Chinese_Traditional = "zh-Hant"
    Corsican = "co"
    Croatian = "hr"
    Czech = "cs"
    Danish = "da"
    Divehi = "dv"
    Dutch = "nl"
    English = "en"
    English_US = "en-US"
    Esperanto = "eo"
    Estonian = "et"
    Ewe = "ee"
    Filipino = "fil"
    Finnish = "fi"
    French = "fr"
    Galician = "gl"
    Ganda = "lg"
    Georgian = "ka"
    German = "de"
    Greek = "el"
    Guarani = "gn"
    Gujarati = "gu"
    Haitian_Creole = "ht"
    Hausa = "ha"
    Hawaiian = "haw"
    Hebrew = "iw"
    Hindi = "hi"
    Hmong = "hmn"
    Hungarian = "hu"
    Icelandic = "is"
    Igbo = "ig"
    Indonesian = "id"
    Irish = "ga"
    Italian = "it"
    Japanese = "ja"
    Javanese = "jv"
    Kannada = "kn"
    Kazakh = "kk"
    Khmer = "km"
    Kinyarwanda = "rw"
    Korean = "ko"
    Krio = "kri"
    Kurdish = "ku"
    Kyrgyz = "ky"
    Lao = "lo"
    Latin = "la"
    Latvian = "lv"
    Lingala = "ln"
    Lithuanian = "lt"
    Luxembourgish = "lb"
    Macedonian = "mk"
    Malagasy = "mg"
    Malay = "ms"
    Malayalam = "ml"
    Maltese = "mt"
    Maori = "mi"
    Marathi = "mr"
    Mongolian = "mn"
    Nepali = "ne"
    Northern_Sotho = "nso"
    Norwegian = "no"
    Nyanja = "ny"
    Odia = "or"
    Oromo = "om"
    Pashto = "ps"
    Persian = "fa"
    Polish = "pl"
    Portuguese = "pt"
    Punjabi = "pa"
    Quechua = "qu"
    Romanian = "ro"
    Russian = "ru"
    Samoan = "sm"
    Sanskrit = "sa"
    Scottish_Gaelic = "gd"
    Serbian = "sr"
    Shona = "sn"
    Sindhi = "sd"
    Sinhala = "si"
    Slovak = "sk"
    Slovenian = "sl"
    Somali = "so"
    Southern_Sotho = "st"
    Spanish = "es"
    Sundanese = "su"
    Swahili = "sw"
    Swedish = "sv"
    Tajik = "tg"
    Tamil = "ta"
    Tatar = "tt"
    Telugu = "te"
    Thai = "th"
    Tigrinya = "ti"
    Tsonga = "ts"
    Turkish = "tr"
    Turkmen = "tk"
    Ukrainian = "uk"
    Urdu = "ur"
    Uyghur = "ug"
    Uzbek = "uz"
    Vietnamese = "vi"
    Welsh = "cy"
    Western_Frisian = "fy"
    Xhosa = "xh"
    Yiddish = "yi"
    Yoruba = "yo"
    Zulu = "zu"


class Transcription(BaseModel):
    language: Language = Language.English
    urls: List[str]
    summarize: bool = False
    entities: str = None

    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://www.youtube.com/watch?v=Uk5f3ajkfSs&ab_channel=LiamOttley",
                "language": "en",
            }
        }


class TranscriptionObject(BaseModel):
    text: str
    start: float
    duration: float

    class Config:
        json_schema_extra = {
            "example": {"text": "hey", "start": 0.00, "duration": 3.00}
        }


class TranscriptionResponseVideo(BaseModel):
    transcript: List[TranscriptionObject]

    class Config:
        json_schema_extra = {
            "example": {
                "transcript": [{"text": "hey", "start": 0.00, "duration": 3.00}]
            }
        }


class TranscriptionResponse(BaseModel):
    urls: List[str]
    transcripts: List[TranscriptionResponseVideo]
