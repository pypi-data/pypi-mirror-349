from pydantic import BaseModel, Field
from typing import Optional, Any, Literal, Union, List
from uuid import UUID
from enum import Enum


class CollectionStatus(str, Enum):
  UNDEFINED: str = 'undefined'  # undefined
  CREATED: str = 'created'  # created
  READY: str = 'ready'  # ready
  DELETED: str = 'deleted'  # deleted
  ERROR: str = 'error'  # error
  PENDING: str = 'pending'  # pending


class CollectionType(str, Enum):
  QDRANT: str = 'qdrant'  # qdrant
  UNKNOWN: str = 'unknown'  # unknown


class DistanceMethod(str, Enum):
  COSINE: str = 'Cosine'  # Cosine
  EUCLIDEAN: str = 'Euclidean'  # Euclidean
  DOT: str = 'Dot'  # Dot
  MANHATTAN: str = 'Manhattan'  # Manhattan


class CollectionEntity(BaseModel):
  input: str = ...  # Input
  payload: dict = ...  # Payload
  id: Union[str, UUID, int] = ...  # Id
  variants: Union[List[str], Any] = None  # Variants


class CollectionEntityAlreadyExistsResponse(BaseModel):
  detail: str = 'Collection entity with this id already exists'  # Detail


class CollectionEntityListResponse(BaseModel):
  results: List['CollectionEntityResponse'] = ...  # Results
  count: int = ...  # Count


class CollectionEntityResponse(BaseModel):
  id: Union[str, UUID, int] = ...  # Id
  payload: dict = ...  # Payload


class CollectionInfo(BaseModel):
  id: Union[Any, str, UUID, int] = None  # Id
  name: str = ...  # Name
  embedding_model: 'EmbeddingModel' = ...
  internal_name: str = 'None'  # Internal Name
  collection_id: Union[Any, UUID] = None  # Collection Id
  metadata: Union['QdrantCollectionMetadata', dict] = None  # Metadata
  owner: Union[Any, str] = None  # Owner
  collection_type: CollectionType = CollectionType.QDRANT  # CollectionType
  status: CollectionStatus = CollectionStatus.UNDEFINED  # CollectionStatus


class CollectionNotFoundResponse(BaseModel):
  detail: str = 'Collection not found'  # Detail


class DataPoint(BaseModel):
  input: str = ...  # Input
  payload: dict = ...  # Payload
  id: Union[str, UUID, int] = None  # Id


class EmbeddingModel(BaseModel):
  id: Union[str, UUID, int] = None  # Id
  name: str = ...  # Name
  version: str = '0.0.1'  # Version
  library: str = 'transformers'  # Library
  loaded: bool = False  # Loaded
  eb_model: Any = None  # Eb Model
  tokenizer: Any = None  # Tokenizer


class EmbeddingRequest(BaseModel):
  text: Union[List[str], str] = ...  # Text
  eb_model_name: str = ...  # Eb Model Name
  eb_model_version: Union[Any, str] = None  # Eb Model Version


class EmbeddingResponse(BaseModel):
  embeddings: 'Embeddings' = ...  # Embeddings
  eb_model_name: str = ...  # Eb Model Name
  eb_model_version: Union[Any, str] = None  # Eb Model Version


class ErrorResponse(BaseModel):
  detail: str = ...  # Detail


class HTTPValidationError(BaseModel):
  detail: List['ValidationError'] = None  # Detail


class HealthCheckResponse(BaseModel):
  status: str = 'ok'  # Status


class ModelNotFoundResponse(BaseModel):
  detail: str = 'Model not found'  # Detail


class PartialCollectionEntity(BaseModel):
  input: Union[Any, str] = None  # Input
  payload: Union[Any, dict] = None  # Payload
  id: Union[Any, str, UUID, int] = None  # Id
  variants: Union[List[str], Any] = None  # Variants


class PartialCollectionInfo(BaseModel):
  id: Union[Any, str, UUID, int] = None  # Id
  name: Union[Any, str] = None  # Name
  embedding_model: Union[Any, 'PartialEmbeddingModel'] = None
  internal_name: Union[Any, str] = None  # Internal Name
  collection_id: Union[Any, UUID] = None  # Collection Id
  metadata: Union['QdrantCollectionMetadata', Any, dict] = None  # Metadata
  owner: Union[Any, str] = None  # Owner
  collection_type: Union[Any, 'CollectionType'] = None
  status: Union['CollectionStatus', Any] = None


class PartialEmbeddingModel(BaseModel):
  id: Union[Any, str, UUID, int] = None  # Id
  name: Union[Any, str] = None  # Name
  version: Union[Any, str] = None  # Version
  library: Union[Any, str] = None  # Library
  loaded: Union[Any, bool] = None  # Loaded
  eb_model: Any = None  # Eb Model
  tokenizer: Any = None  # Tokenizer


class QdrantCollectionInfo(BaseModel):
  id: Union[Any, str, UUID, int] = None  # Id
  name: str = ...  # Name
  embedding_model: 'EmbeddingModel' = ...
  internal_name: str = 'None'  # Internal Name
  collection_id: Union[Any, UUID] = None  # Collection Id
  metadata: 'QdrantCollectionMetadata' = ...
  owner: Union[Any, str] = None  # Owner
  collection_type: CollectionType = CollectionType.QDRANT  # CollectionType
  status: CollectionStatus = CollectionStatus.UNDEFINED  # CollectionStatus


class QdrantCollectionMetadata(BaseModel):
  host: str = ...  # Host
  token: str = ...  # Token
  distance_method: DistanceMethod = DistanceMethod.DOT  # DistanceMethod
  dimension: Union[Any, int] = None  # Dimension


class QueryRequest(BaseModel):
  query: str = ...  # Query
  top_k: Union[Any, int] = 10  # Top K


class ReadRootResponse(BaseModel):
  status: str = 'ok'  # Status


class UnauthorizedResponse(BaseModel):
  detail: str = 'Unauthorized'  # Detail


class UnsupportedCollectionTypeResponse(BaseModel):
  detail: str = 'Unsupported collection type'  # Detail


class ValidationError(BaseModel):
  loc: List[Union[str, int]] = ...  # Location
  msg: str = ...  # Message
  type: str = ...  # Error Type

