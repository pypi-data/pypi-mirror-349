"""Vector Store Client implementation.

This module provides the main client class for interacting with the Vector Store API.
"""

import logging
from typing import Dict, List, Optional, Union, Any
from uuid import UUID
import datetime
import json

from .models import (
    SearchResult, 
    ConfigParams,
    CreateRecordParams,
    CreateTextRecordParams,
    DeleteParams,
    FilterRecordsParams,
    GetMetadataParams,
    GetTextParams,
    SearchByVectorParams,
    SearchRecordsParams,
    SearchTextRecordsParams,
    HealthResponse
)
from .exceptions import (
    ValidationError,
    JsonRpcException,
    ResourceNotFoundError,
    AuthenticationError,
    DuplicateError,
    RateLimitError,
    ServerError,
    BadResponseError
)
from .base_client import BaseVectorStoreClient
from .utils import extract_uuid_from_response, clean_metadata
from .validation import (
    validate_session_id, 
    validate_message_id, 
    validate_timestamp,
    validate_create_record_params,
    validate_limit
)

logger = logging.getLogger(__name__)

class VectorStoreClient(BaseVectorStoreClient):
    """Client for interacting with Vector Store API."""

    async def create_record(
        self,
        vector: List[float],
        metadata: Dict,
        session_id: Optional[str] = None,
        message_id: Optional[str] = None,
        timestamp: Optional[str] = None,
    ) -> str:
        """Creates a new record with vector and metadata.
        
        Args:
            vector: Vector data as list of floats
            metadata: Metadata dictionary
            session_id: Optional session ID (UUID)
            message_id: Optional message ID (UUID)
            timestamp: Optional timestamp (ISO 8601 format)
            
        Returns:
            Record ID as string
            
        Raises:
            ValidationError: If parameters are invalid
            ConnectionError: If API is unreachable
            JsonRpcException: If API returns an error
        """
        # Clone metadata to avoid modifying the original
        metadata_copy = clean_metadata(metadata.copy() if metadata else {})
        
        # Add required 'body' field if missing - это обязательное поле для API сервера
        if 'body' not in metadata_copy:
            # Try to use 'text' field if available
            if 'text' in metadata_copy:
                metadata_copy['body'] = metadata_copy['text']
            else:
                # Use a placeholder value if no text is available
                metadata_copy['body'] = "Vector record created with no text content"
        
        # Проверка, что поле body не пустое
        if not metadata_copy.get('body'):
            metadata_copy['body'] = "Vector record created with no text content"
            
        params = CreateRecordParams(
            vector=vector,
            metadata=metadata_copy,
        ).model_dump(exclude_none=True)
        
        validate_session_id(session_id, params)
        validate_message_id(message_id, params)
        validate_timestamp(timestamp, params)
        
        try:
            response = await self._make_request(
                "create_record",
                params
            )
            
            # Log the response for debugging
            logger.debug(f"Raw create_record response: {response!r}")
            
            # Process nested response if needed
            result = response["result"]
            if isinstance(result, dict) and "success" in result and result.get("success") and "data" in result:
                result = result["data"]
                
            # Extract UUID from response
            return extract_uuid_from_response(result)
        except JsonRpcException as e:
            if e.code == 409:
                raise DuplicateError(f"Record with these parameters already exists: {e.message}")
            if e.code in (-32602, -32600):
                raise ValidationError(f"Invalid parameters: {e.message}")
            raise

    async def create_text_record(
        self,
        text: str,
        metadata: Optional[Dict] = None,
        model: Optional[str] = None,
        session_id: Optional[str] = None,
        message_id: Optional[str] = None,
        timestamp: Optional[str] = None,
    ) -> str:
        """Creates a new record from text with automatic vectorization.
        
        Args:
            text: Text to vectorize
            metadata: Optional metadata dictionary
            model: Optional model name for vectorization
            session_id: Optional session ID (UUID)
            message_id: Optional message ID (UUID)
            timestamp: Optional timestamp (ISO 8601 format)
            
        Returns:
            Record ID as string
            
        Raises:
            ValidationError: If parameters are invalid
            ConnectionError: If API is unreachable
            JsonRpcException: If API returns an error
        """
        # Ensure metadata has required fields for server compatibility
        metadata_copy = clean_metadata(metadata or {})
        
        # Обязательно добавляем текст в поле body для совместимости с сервером
        if "body" not in metadata_copy or not metadata_copy["body"]:
            metadata_copy["body"] = text
            
        params = CreateTextRecordParams(
            text=text,
            metadata=metadata_copy,
        ).model_dump(exclude_none=True)
        
        if model:
            params["model"] = model
            
        validate_session_id(session_id, params)
        validate_message_id(message_id, params)
        validate_timestamp(timestamp, params)
        
        try:
            response = await self._make_request(
                "create_text_record",
                params
            )
            
            # Log the response for debugging
            logger.debug(f"Raw create_text_record response: {response!r}")
            
            # Process nested response if needed
            result = response["result"]
            if isinstance(result, dict) and "success" in result and result.get("success") and "data" in result:
                result = result["data"]
                
            # Extract UUID from response
            return extract_uuid_from_response(result)
        except JsonRpcException as e:
            if e.code == 409:
                raise DuplicateError(f"Record with this text already exists: {e.message}")
            if e.code in (-32602, -32600):
                raise ValidationError(f"Invalid parameters: {e.message}")
            raise

    async def search_by_vector(
        self,
        vector: List[float],
        limit: int = 10,
        include_vectors: bool = False,
        include_metadata: bool = True,
    ) -> List[SearchResult]:
        """Search for records by vector similarity.
        
        Args:
            vector: Vector to search with
            limit: Maximum number of results to return
            include_vectors: Whether to include vectors in results
            include_metadata: Whether to include metadata in results
            
        Returns:
            List of search results
            
        Raises:
            ValidationError: If parameters are invalid
            ConnectionError: If API is unreachable
            JsonRpcException: If API returns an error
        """
        # Проверка размерности вектора
        # Для Vector Store обычно требуется 384 измерения
        expected_dimensions = 384
        if len(vector) != expected_dimensions:
            raise ValidationError(
                f"Vector dimension mismatch: got {len(vector)}, expected {expected_dimensions}",
                dimensions=len(vector),
                expected_dimensions=expected_dimensions
            )
        
        params = SearchByVectorParams(
            vector=vector,
            limit=limit,
            include_vectors=include_vectors,
            include_metadata=include_metadata,
        ).model_dump(exclude_none=True)
        
        try:
            response = await self._make_request(
                "search_by_vector",
                params
            )
            
            return self._process_search_results(response)
            
        except JsonRpcException as e:
            if "dimension mismatch" in e.message.lower():
                raise ValidationError(f"Vector dimension mismatch: {e.message}")
            raise

    async def search_text_records(
        self,
        text: str,
        limit: int = 10,
        model: Optional[str] = None,
        include_vectors: bool = False,
        include_metadata: bool = True,
        metadata_filter: Optional[Dict] = None
    ) -> List[SearchResult]:
        """Search for records by text similarity.
        
        Args:
            text: Query text
            limit: Maximum number of results (1-100)
            model: Optional model name for vectorization
            include_vectors: Whether to include vectors in results
            include_metadata: Whether to include metadata in results
            metadata_filter: Optional metadata criteria to filter results
            
        Returns:
            List of search results
            
        Raises:
            ValidationError: If parameters are invalid
            ConnectionError: If API is unreachable
            JsonRpcException: If API returns an error
        """
        params = SearchTextRecordsParams(
            text=text,
            limit=validate_limit(limit),
            include_vectors=include_vectors,
            include_metadata=include_metadata
        ).model_dump(exclude_none=True)
        
        if model:
            params["model"] = model
            
        if metadata_filter:
            params["metadata_filter"] = metadata_filter
        
        try:
            response = await self._make_request(
                "search_text_records",
                params
            )
            
            return self._process_search_results(response)
        except JsonRpcException as e:
            if e.code in (-32602, -32600):
                raise ValidationError(f"Invalid parameters: {e.message}")
            raise

    async def filter_records(
        self,
        metadata_filter: Dict,
        limit: int = 100,
        include_vectors: bool = False,
        include_metadata: bool = True
    ) -> List[SearchResult]:
        """Filter records by metadata criteria.
        
        Args:
            metadata_filter: Filter criteria for metadata
            limit: Maximum number of results (1-1000)
            include_vectors: Whether to include vectors in results
            include_metadata: Whether to include metadata in results
            
        Returns:
            List of filtered results
            
        Raises:
            ValidationError: If parameters are invalid
            ConnectionError: If API is unreachable
            JsonRpcException: If API returns an error
        """
        params = FilterRecordsParams(
            metadata_filter=metadata_filter,
            limit=validate_limit(limit, max_value=1000),
            include_vectors=include_vectors,
            include_metadata=include_metadata
        ).model_dump(exclude_none=True)
        
        # Log request parameters
        logger.debug(f"filter_records request params: {params}")
        
        try:
            response = await self._make_request(
                "filter_records",
                params
            )
            
            return self._process_search_results(response)
        except JsonRpcException as e:
            if e.code in (-32602, -32600):
                raise ValidationError(f"Invalid parameters: {e.message}")
            raise

    async def get_metadata(self, record_id: str) -> Dict:
        """Get metadata for a record by ID.
        
        Args:
            record_id: Record ID
            
        Returns:
            Metadata dictionary
            
        Raises:
            ValidationError: If parameters are invalid
            ResourceNotFoundError: If record does not exist
            ConnectionError: If API is unreachable
            JsonRpcException: If API returns an error
        """
        try:
            # Validate record ID format
            if not record_id:
                raise ValidationError("Record ID is required")
                
            # Create request
            params = GetMetadataParams(
                record_id=record_id
            ).model_dump(exclude_none=True)
            
            # Make the request
            response = await self._make_request(
                "get_metadata",
                params
            )
            
            # Process response
            result = response["result"]
            
            # Check for error in response
            if isinstance(result, dict):
                if "success" in result and result.get("success") is False:
                    if "error" in result and isinstance(result["error"], dict):
                        error = result["error"]
                        if "code" in error and error.get("code") == 404:
                            raise ResourceNotFoundError(f"Record with ID {record_id} not found")
                        raise JsonRpcException(
                            message=error.get("message", "Error in response"), 
                            code=error.get("code", -1)
                        )
            
            # Handle nested data format
            if isinstance(result, dict):
                if "success" in result and result.get("success") and "data" in result:
                    result = result["data"]
                elif "result" in result and isinstance(result["result"], dict) and "metadata" in result["result"]:
                    return result["result"]["metadata"]
                elif "metadata" in result:
                    return result["metadata"]
            
            # Must be a dictionary
            if not isinstance(result, dict):
                logger.warning(f"Unexpected metadata format: {result}")
                if isinstance(result, str):
                    try:
                        # Try to parse as JSON
                        return json.loads(result)
                    except:
                        pass
                        
                # Return as is, wrapped in a dict
                return {"metadata": result}
                
            return result
        except JsonRpcException as e:
            if e.code == 404:
                raise ResourceNotFoundError(f"Record with ID {record_id} not found")
            if e.code in (-32602, -32600):
                raise ValidationError(f"Invalid parameters: {e.message}")
            raise

    async def get_text(self, record_id: str) -> str:
        """Get text for a record by ID.
        
        Args:
            record_id: Record ID
            
        Returns:
            The text content
            
        Raises:
            ValidationError: If parameters are invalid
            ResourceNotFoundError: If record does not exist
            ConnectionError: If API is unreachable
            JsonRpcException: If API returns an error
        """
        try:
            # Validate record ID format
            if not record_id:
                raise ValidationError("Record ID is required")
                
            # Create request
            params = GetTextParams(
                record_id=record_id
            ).model_dump(exclude_none=True)
            
            # Make the request
            response = await self._make_request(
                "get_text",
                params
            )
            
            # Process response
            result = response["result"]
            
            # Check for error in response
            if isinstance(result, dict):
                if "success" in result and result.get("success") is False:
                    if "error" in result and isinstance(result["error"], dict):
                        error = result["error"]
                        if "code" in error and error.get("code") == 404:
                            raise ResourceNotFoundError(f"Record with ID {record_id} not found")
                        raise JsonRpcException(
                            message=error.get("message", "Error in response"), 
                            code=error.get("code", -1)
                        )
            
            # Handle different response formats based on potential server implementations
            text = result
            
            # Handle nested data format - основные возможные форматы ответа
            if isinstance(result, dict):
                # Формат: {"result": {"text": "content"}}
                if "text" in result:
                    return result["text"]
                
                # Формат: {"success": true, "result": {"text": "content"}}
                if "success" in result and result.get("success") and "result" in result:
                    if isinstance(result["result"], dict):
                        if "text" in result["result"]:
                            return result["result"]["text"]
                
                # Формат: {"success": true, "data": {"text": "content"}}
                if "success" in result and result.get("success") and "data" in result:
                    if isinstance(result["data"], dict) and "text" in result["data"]:
                        return result["data"]["text"]
                    elif isinstance(result["data"], str):
                        return result["data"]
                
                # Формат: {"data": "content"}
                if "data" in result and isinstance(result["data"], str):
                    return result["data"]
                    
                # Если есть поле body - часто текст хранится там
                if "body" in result:
                    return result["body"]
                
                # Если это вложенный формат с result
                if "result" in result:
                    nested = result["result"]
                    if isinstance(nested, dict):
                        if "text" in nested:
                            return nested["text"]
                
                # Если это JSON, возвращаем его в виде строки
                try:
                    return json.dumps(result)
                except:
                    logger.warning(f"Failed to convert dict to JSON string: {result}")

            # For text content, it should be a string now
            if not isinstance(text, str):
                logger.warning(f"Unexpected get_text format: {text}")
                # Convert to string as a fallback
                return str(text)
                
            return text
            
        except JsonRpcException as e:
            if e.code == 404:
                raise ResourceNotFoundError(f"Record with ID {record_id} not found")
            if e.code in (-32602, -32600):
                raise ValidationError(f"Invalid parameters: {e.message}")
            raise

    async def delete(
        self,
        record_id: Optional[str] = None,
        record_ids: Optional[List[str]] = None,
        filter: Optional[Dict] = None,
        max_records: int = 100,
        confirm: bool = False
    ) -> bool:
        """Delete one or more records.
        
        Must specify exactly one of: record_id, record_ids, or filter.
        
        Args:
            record_id: Single record ID to delete
            record_ids: List of record IDs to delete
            filter: Metadata filter to delete matching records
            max_records: Maximum records to delete when using filter
            confirm: Must be True when deleting multiple records
            
        Returns:
            True if deletion was successful
            
        Raises:
            ValidationError: If parameters are invalid
            ResourceNotFoundError: If record does not exist
            ConnectionError: If API is unreachable
            JsonRpcException: If API returns an error
        """
        # Check that only one parameter is specified
        specified_params = sum(1 for p in [record_id, record_ids, filter] if p is not None)
        if specified_params != 1:
            raise ValidationError("Must specify exactly one of: record_id, record_ids, or filter")
            
        # Create the request parameters
        params = DeleteParams().model_dump(exclude_none=True)
        
        if record_id:
            params["record_id"] = record_id
        elif record_ids:
            if not confirm and len(record_ids) > 1:
                raise ValidationError("Must set confirm=True when deleting multiple records")
            params["record_ids"] = record_ids
            params["confirm"] = confirm
        elif filter:
            if not confirm:
                raise ValidationError("Must set confirm=True when deleting by filter")
            params["filter"] = filter
            params["max_records"] = max_records
            params["confirm"] = confirm
            
        try:
            # Send the request
            response = await self._make_request(
                "delete",
                params
            )
            
            return True
        except JsonRpcException as e:
            if e.code == 404:
                raise ResourceNotFoundError(f"Record not found")
            if e.code in (-32602, -32600):
                raise ValidationError(f"Invalid parameters: {e.message}")
            raise

    async def search_records(
        self,
        vector: List[float],
        limit: int = 10,
        include_vectors: bool = False,
        include_metadata: bool = True,
        filter_criteria: Optional[Dict] = None
    ) -> List[SearchResult]:
        """Search for records by vector similarity with optional filtering.
        
        Args:
            vector: Query vector
            limit: Maximum number of results
            include_vectors: Whether to include vectors in results
            include_metadata: Whether to include metadata in results
            filter_criteria: Optional metadata criteria to filter results
            
        Returns:
            List of search results
            
        Raises:
            ValidationError: If parameters are invalid
            ConnectionError: If API is unreachable
            JsonRpcException: If API returns an error
        """
        params = SearchRecordsParams(
            vector=vector,
            limit=validate_limit(limit),
            include_vectors=include_vectors,
            include_metadata=include_metadata
        ).model_dump(exclude_none=True)
        
        if filter_criteria:
            params["filter_criteria"] = filter_criteria
        
        try:
            response = await self._make_request(
                "search_records",
                params
            )
            
            return self._process_search_results(response)
        except JsonRpcException as e:
            if e.code in (-32602, -32600):
                raise ValidationError(f"Invalid parameters: {e.message}")
            raise

    async def health(self) -> Dict:
        """Get service health status.
        
        Returns:
            Health status information as a dictionary with keys:
            - status: Service status (ok/error)
            - model: Current active model
            - version: Service version
            
        Raises:
            ConnectionError: If API is unreachable
            JsonRpcException: If API returns an error
        """
        try:
            response = await self._make_request("health", {})
            result = response["result"]
            
            # For backwards compatibility - older format had status directly in result
            # but newer format may have it nested in data
            if isinstance(result, dict) and "data" in result and "success" in result:
                if result["success"]:
                    result = result["data"]
                    
            # Ensure we return a dict with 'status' for compatibility
            if isinstance(result, dict) and "status" not in result and result.get("success", False):
                # Extract status from nested data if available
                data = result.get("data", {})
                if isinstance(data, dict) and "status" in data:
                    result["status"] = data["status"]
            
            return result
        except JsonRpcException as e:
            raise ServerError(f"Health check failed: {e.message}")

    async def config(
        self,
        operation: str = "get",
        path: Optional[str] = None,
        value: Optional[Any] = None
    ) -> Any:
        """Access or modify service configuration.
        
        Args:
            operation: Operation type (get/set)
            path: Configuration path (dot-separated)
            value: Optional value to set
            
        Returns:
            Configuration value or status
            
        Raises:
            ValidationError: If parameters are invalid
            ConnectionError: If API is unreachable
            JsonRpcException: If API returns an error
        """
        params = ConfigParams(
            operation=operation
        ).model_dump(exclude_none=True)
        
        if path:
            params["path"] = path
            
        if value is not None:
            params["value"] = value
        
        try:
            response = await self._make_request("config", params)
            return response["result"]
        except JsonRpcException as e:
            if e.code in (-32602, -32600):
                raise ValidationError(f"Invalid configuration parameters: {e.message}")
            if e.code == 403:
                raise AuthenticationError("Not authorized to access configuration")
            raise

    async def help(self, cmdname: Optional[str] = None) -> Dict:
        """Get help information about available commands.
        
        Args:
            cmdname: Optional specific command name to get help for
            
        Returns:
            Help information
            
        Raises:
            ConnectionError: If API is unreachable
            JsonRpcException: If API returns an error
        """
        params = {}
        if cmdname:
            params["command"] = cmdname
        
        try:
            response = await self._make_request("help", params)
            result = response["result"]
            
            # Проверка и обработка нестандартных форматов ответа
            if isinstance(result, dict):
                # Обработка вложенного формата с data
                if "success" in result and "data" in result and result.get("success", False):
                    result = result["data"]
                
                # Если запрашиваем информацию о конкретной команде, но получаем общий список команд
                if cmdname and "commands" in result and cmdname in result["commands"]:
                    # Вытащить информацию о конкретной команде
                    command_info = result["commands"][cmdname]
                    # Добавить общую информацию для контекста
                    if "tool_info" in result:
                        command_info["tool_info"] = result["tool_info"]
                    return command_info
            
            return result
        except JsonRpcException as e:
            if e.code == 404 and cmdname:
                raise ResourceNotFoundError(f"Command '{cmdname}' not found")
            raise JsonRpcException(f"Error getting help: {e.message}", code=e.code) 