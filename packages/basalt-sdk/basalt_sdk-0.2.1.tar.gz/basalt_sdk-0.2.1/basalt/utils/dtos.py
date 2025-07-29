from dataclasses import dataclass
from typing import Optional, Dict, Any, List, Tuple

from ..ressources.monitor.generation_types import Generation

from .utils import pick_typed, pick_number

# ------------------------------ Get Prompt ----------------------------- #
@dataclass
class PromptModelParameters:
    temperature: float
    top_k: float
    top_p: Optional[float]

    frequency_penalty: Optional[float]
    presence_penalty: Optional[float]

    max_length: int
    response_format: str
    json_object: Optional[dict]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            temperature=pick_number(data, "temperature"),
            frequency_penalty=pick_number(data, 'frequencyPenalty') if data.get("frequencyPenalty") else None,
            presence_penalty=pick_number(data, "presencePenalty") if data.get("presencePenalty") else None,
            top_p=pick_number(data, "topP"),
            top_k=pick_number(data, "topK") if data.get("topK") else None,
            max_length=data["maxLength"],
            response_format=pick_typed(data, "responseFormat", str),
            json_object=data.get("jsonObject"),
        )

@dataclass(frozen=True)
class PromptModel:
    provider: str
    model: str
    version: str
    parameters: PromptModelParameters

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            provider=pick_typed(data, "provider", str),
            model=pick_typed(data, "model", str),
            version=pick_typed(data, "version", str),
            parameters=PromptModelParameters.from_dict(data.get("parameters")),
        )

@dataclass(frozen=True)
class PromptResponse:
    text: str
    model: PromptModel
    systemText: str
    version: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            text=pick_typed(data, "text", str),
            model=PromptModel.from_dict(data.get("model")),
            systemText=pick_typed(data, "systemText", str),
            version=pick_typed(data, "version", str),
        )

@dataclass(frozen=True)
class GetPromptDTO:
    slug: str
    tag: Optional[str] = None
    version: Optional[str] = None

GetResult = Tuple[Optional[Exception], Optional[PromptResponse], Optional[Generation]]

# ------------------------------ Describe Prompt ----------------------------- #
@dataclass(frozen=True)
class DescribePromptResponse:
	slug: str
	status: str
	name: str
	description: str
	available_versions: List[str]
	available_tags: List[str]
	variables: List[Dict[str, str]]

	@classmethod
	def from_dict(cls, data: Dict[str, Any]):
		return cls(
			slug=pick_typed(data, "slug", str) if data.get("slug") else None,
			status=pick_typed(data, "status", str),
			name=pick_typed(data, "name", str),
			description=pick_typed(data, "description", str) if data.get("description") else None,
			available_versions=pick_typed(data, "availableVersions", list),
			available_tags=pick_typed(data, "availableTags", list),
			variables=pick_typed(data, "variables", list),
		)

@dataclass(frozen=True)
class DescribePromptDTO:
    slug: str
    tag: Optional[str] = None
    version: Optional[str] = None

DescribeResult = Tuple[Optional[Exception], Optional[DescribePromptResponse]]

# ------------------------------ List Prompts ----------------------------- #
@dataclass(frozen=True)
class PromptListResponse:
    slug: str
    status: str
    name: str
    description: str
    available_versions: List[str]
    available_tags: List[str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            slug=pick_typed(data, "slug", str) if data.get("slug") else None,
            status=pick_typed(data, "status", str),
            name=pick_typed(data, "name", str),
            description=pick_typed(data, "description", str) if data.get("description") else None,
            available_versions=pick_typed(data, "availableVersions", list),
            available_tags=pick_typed(data, "availableTags", list),
        )

@dataclass(frozen=True)
class PromptListDTO:
    featureSlug: Optional[str] = None



ListResult = Tuple[Optional[Exception], Optional[List[PromptListResponse]]]