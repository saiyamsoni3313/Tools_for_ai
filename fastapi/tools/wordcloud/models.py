from pydantic import BaseModel, constr
from typing import List, Optional
from enum import Enum


class ScaleType(str, Enum):
    linear = "linear"
    sqrt = "sqrt"
    log = "log"


class Case(str, Enum):
    upper = "upper"
    lower = "lower"
    none = "none"


class LanguageCode(str, Enum):
    English = "en"
    Afrikaans = "af"
    Arabic = "ar"
    Armenian = "hy"
    Basque = "eu"
    Bengali = "be"
    Breton = "br"
    Bulgarian = "bu"
    Catalan = "ca"
    Chinese = "zh"
    Croatian = "hr"
    Czech = "ce"
    Danish = "da"
    Dutch = "nl"
    Esperanto = "ep"
    Estonian = "es"
    Finnish = "fi"
    French = "fr"
    Galician = "gl"
    German = "de"
    Greek = "el"
    Gujarati = "gu"
    Hausa = "ha"
    Hebrew = "he"
    Hindi = "hi"
    Hungarian = "hu"
    Indonesian = "in"
    Irish = "ir"
    Italian = "it"
    Japanese = "ja"
    Korean = "ko"
    Kurdish = "ku"
    Latin = "la"
    Latvian = "lv"
    Lithuanian = "li"
    Lugbara = "lg"
    Malay = "ms"
    Marathi = "ma"
    Burmese = "my"
    Norwegian = "no"
    Persian = "fa"
    Polish = "po"
    Portuguese = "pt"
    Punjabi = "pa"
    Romanian = "ro"
    Russian = "ru"
    Slovak = "sk"
    Slovenian = "sl"
    Somali = "so"
    Sotho = "st"
    Spanish = "sp"
    Swahili = "sw"
    Swedish = "sv"
    Tagalog = "ta"
    Thai = "th"
    Turkish = "tu"
    Ukrainian = "uk"
    Urdu = "ur"
    Vietnamese = "vi"
    Yoruba = "yo"
    Zulu = "zu"


class WordCloud(BaseModel):
    text: str
    format: str = "png"
    width: int = 1000
    height: int = 1000
    backgroundColor: str = "transparent"
    fontFamily: str = "serif"
    fontWeight: str = "normal"
    fontScale: int = 15
    scale: ScaleType = ScaleType.linear
    padding: int = 1
    rotation: int = 20
    maxNumWords: int = 200
    minWordLength: int = 4
    case: Case = Case.none
    colors: Optional[List[str]] = None
    removeStopwords: bool = True
    cleanWords: bool = True
    language: LanguageCode = LanguageCode.English
    useWordList: bool = True


class WordCloudRequest(BaseModel):
    text: str
    width: Optional[int] = None
    height: Optional[int] = None
    backgroundColor: Optional[str] = None
    fontFamily: Optional[str] = None
    fontWeight: Optional[str] = None
    fontScale: Optional[int] = None
    padding: Optional[int] = None
    rotation: Optional[int] = None
    maxNumWords: Optional[int] = None
    minWordLength: Optional[int] = None
    scale: Optional[ScaleType] = None
    case: Optional[Case] = None
    colors: Optional[List[str]] = None
    removeStopwords: Optional[bool] = None
    cleanWords: Optional[bool] = None
    language: Optional[LanguageCode] = None

    class Config:
        json_schema_extra = {
            "example": {
                "text": "hello:10,world:5,testing:5,123",
                "width": 800,
                "height": 600,
                "backgroundColor": "#ffffff",
                "fontFamily": "Arial",
                "fontWeight": "bold",
                "fontScale": 10,
                "padding": 2,
                "rotation": 45,
                "maxNumWords": 150,
                "minWordLength": 3,
                "scale": ScaleType.linear,
                "case": Case.upper,
                "colors": ["#FF5733", "#33FF57", "#3357FF"],
                "removeStopwords": False,
                "cleanWords": True,
                "language": LanguageCode.English,
            }
        }


def create_word_cloud(request: WordCloudRequest) -> WordCloud:
    # Create a default instance of WordCloud to use for default values
    default_word_cloud = WordCloud(text=request.text)

    # Create a WordCloud object using the data from WordCloudRequest
    return WordCloud(
        text=request.text,
        format="png",
        width=request.width or default_word_cloud.width,
        height=request.height or default_word_cloud.height,
        backgroundColor=request.backgroundColor or default_word_cloud.backgroundColor,
        fontFamily=request.fontFamily or default_word_cloud.fontFamily,
        fontWeight=request.fontWeight or default_word_cloud.fontWeight,
        fontScale=request.fontScale or default_word_cloud.fontScale,
        scale=request.scale or default_word_cloud.scale,
        padding=request.padding or default_word_cloud.padding,
        rotation=request.rotation or default_word_cloud.rotation,
        maxNumWords=request.maxNumWords or default_word_cloud.maxNumWords,
        minWordLength=request.minWordLength or default_word_cloud.minWordLength,
        case=request.case or default_word_cloud.case,
        colors=request.colors,
        removeStopwords=(
            request.removeStopwords
            if request.removeStopwords is not None
            else default_word_cloud.removeStopwords
        ),
        cleanWords=(
            request.cleanWords
            if request.cleanWords is not None
            else default_word_cloud.cleanWords
        ),
        language=request.language or default_word_cloud.language,
        useWordList=True,
    )
