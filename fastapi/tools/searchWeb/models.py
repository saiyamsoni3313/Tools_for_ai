from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict
from enum import Enum


class SearchEngines(str, Enum):
    google = "google"  # General web search
    brave = "brave"  # General web search
    wikipedia = "wikipedia"  # Encyclopedic search
    duckduckgo = "duckduckgo"  # Privacy-focused web search
    github = "github"  # Code repository search
    arxiv = "arxiv"  # Scientific publications
    pubmed = "pubmed"  # Medical publications
    youtube = "youtube"  # Video search
    bing = "bing"  # General web search
    startpage = "startpage"  # Privacy-focused web search
    qwant = "qwant"  # Privacy-focused web search
    google_scholar = "google_scholar"  # Academic publications
    semantic_scholar = "semantic_scholar"  # Academic publications
    stackoverflow = "stackoverflow"  # Programming Q&A
    reddit = "reddit"  # Social media search
    presearch = "presearch"  # Decentralized search engine
    yahoo = "yahoo"  # General web search


class SafeSearch(str, Enum):
    off = "0"
    moderate = "1"
    strict = "2"


class EngineRef(BaseModel):
    name: str
    category: str

    def __repr__(self):
        return f"EngineRef({self.name!r}, {self.category!r})"

    def __eq__(self, other):
        return self.name == other.name and self.category == other.category

    def __hash__(self):
        return hash((self.name, self.category))


class SearchParams(BaseModel):
    query: str = Field(..., description="The search query.")
    format: str = Field(
        "json",
        description="The format in which the search results are returned.",
        pattern="^(json|xml|rss|html)$",
    )
    categories: Optional[str] = Field(
        None,
        description="The category to search within.",
        pattern="^(general|images|news|videos|map|science|music|files|it|social media|economy)$",
    )
    crawl: Optional[bool] = Field(False, description="Crawl the webpage for content")
    summarize: Optional[bool] = Field(
        False, description="Summarize the webpage content"
    )
    entities: Optional[str] = Field(
        None, description="Stringified JSON of response format"
    )
    language: Optional[str] = Field(
        None, description="The language for the search results. E.g., 'en', 'fr', etc."
    )
    safesearch: Optional[SafeSearch] = Field(
        SafeSearch.strict, description="Filter explicit content"
    )
    time_range: Optional[str] = Field(
        None,
        description="Limit search results to a specific time range.",
        pattern="^(day|week|month|year)$",
    )
    engines: Optional[List[SearchEngines]] = Field(
        [SearchEngines.google, SearchEngines.duckduckgo],
        description="Specify the search engines to use as a list.",
    )
    pageno: Optional[int] = Field(
        1, description="The page number of search results.", ge=1
    )
    limit: Optional[int] = Field(
        10, description="Limit the number of results returned."
    )
    timeout_limit: Optional[float] = Field(
        None, description="Limit the search query timeout."
    )
    external_bang: Optional[str] = Field(
        None, description="External bang for search redirection."
    )
    redirect_to_first_result: Optional[bool] = Field(
        None, description="Redirect to the first search result if available."
    )

    @field_validator("summarize")
    @classmethod
    def check_summarize_condition(cls, value, values):
        if value and not values.data.get("crawl", False):
            raise ValueError("summarize can only be true if crawl is true")
        return value

    @field_validator("entities")
    @classmethod
    def validate_entities(cls, value, values):
        if value and not values.data.get("summarize", False):
            raise ValueError("entities can only be true if summarize is true")
        return value

    class Config:
        json_schema_extra = {
            "example": {
                "query": "quantum computing",
                "categories": "general",
                "engines": ["google", "duckduckgo", "github", "arxiv", "pubmed"],
                "limit": 10,
                "external_bang": None,
            }
        }

    def to_search_query(self) -> "SearchQuery":
        engineref_list = [
            EngineRef(name=engine.value, category=self.categories or "general")
            for engine in self.engines
        ]
        return SearchQuery(
            query=self.query,
            engineref_list=engineref_list,
            lang=self.language or "all",
            safesearch=int(self.safesearch.value),
            pageno=self.pageno,
            time_range=self.time_range,
            timeout_limit=self.timeout_limit,
            external_bang=self.external_bang,
            redirect_to_first_result=self.redirect_to_first_result,
        )


class SearchQuery:
    """Container for all the search parameters (query, language, etc...)"""

    def __init__(
        self,
        query: str,
        engineref_list: List[EngineRef],
        lang: str = "all",
        safesearch: int = 0,
        pageno: int = 1,
        time_range: Optional[str] = None,
        timeout_limit: Optional[float] = None,
        external_bang: Optional[str] = None,
        engine_data: Optional[Dict[str, str]] = None,
        redirect_to_first_result: Optional[bool] = None,
    ):
        self.query = query
        self.engineref_list = engineref_list
        self.lang = lang
        self.safesearch = safesearch
        self.pageno = pageno
        self.time_range = time_range
        self.timeout_limit = timeout_limit
        self.external_bang = external_bang
        self.engine_data = engine_data or {}
        self.redirect_to_first_result = redirect_to_first_result

        self.locale = None
        if self.lang:
            self.locale = self.lang.replace("_", "-")

    @property
    def categories(self):
        return list(set(map(lambda engineref: engineref.category, self.engineref_list)))

    def __repr__(self):
        return (
            f"SearchQuery({self.query!r}, {self.engineref_list!r}, {self.lang!r}, {self.safesearch!r}, "
            f"{self.pageno!r}, {self.time_range!r}, {self.timeout_limit!r}, {self.external_bang!r}, "
            f"{self.redirect_to_first_result!r})"
        )

    def __eq__(self, other):
        return (
            self.query == other.query
            and self.engineref_list == other.engineref_list
            and self.lang == other.lang
            and self.safesearch == other.safesearch
            and self.pageno == other.pageno
            and self.time_range == other.time_range
            and self.timeout_limit == other.timeout_limit
            and self.external_bang == other.external_bang
            and self.redirect_to_first_result == other.redirect_to_first_result
        )

    def __hash__(self):
        return hash(
            (
                self.query,
                tuple(self.engineref_list),
                self.lang,
                self.safesearch,
                self.pageno,
                self.time_range,
                self.timeout_limit,
                self.external_bang,
                self.redirect_to_first_result,
            )
        )

    def __copy__(self):
        return SearchQuery(
            self.query,
            self.engineref_list,
            self.lang,
            self.safesearch,
            self.pageno,
            self.time_range,
            self.timeout_limit,
            self.external_bang,
            self.engine_data,
            self.redirect_to_first_result,
        )


class SearchResult(BaseModel):
    url: str
    title: str
    description: str
    score: Optional[float] = None
    category: Optional[str] = None
    content: Optional[str] = None


class SearchResponse(BaseModel):
    query: str
    answers: Optional[List[str]] = None
    results: Optional[List[SearchResult]] = None
