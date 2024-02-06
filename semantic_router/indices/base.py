from pydantic.v1 import BaseModel
from typing import Any, List, Tuple, Optional
import numpy as np


class BaseIndex(BaseModel):
    """
    Base class for indices using Pydantic's BaseModel.
    This class outlines the expected interface for index classes.
    Actual method implementations should be provided in subclasses.
    """

    # You can define common attributes here if there are any.
    # For example, a placeholder for the index attribute:
    index: Optional[Any] = None

    def add(self, embeds: List[Any]):
        """
        Add embeddings to the index.
        This method should be implemented by subclasses.
        """
        raise NotImplementedError("This method should be implemented by subclasses.")

    def remove(self, indices_to_remove: List[int]):
        """
        Remove items from the index by their indices.
        This method should be implemented by subclasses.
        """
        raise NotImplementedError("This method should be implemented by subclasses.")

    def is_index_populated(self) -> bool:
        """
        Check if the index is populated.
        This method should be implemented by subclasses.
        """
        raise NotImplementedError("This method should be implemented by subclasses.")

    def query(self, query_vector: Any, top_k: int = 5) -> Tuple[np.ndarray, np.ndarray]:
        """
        Search the index for the query_vector and return top_k results.
        This method should be implemented by subclasses.
        """
        raise NotImplementedError("This method should be implemented by subclasses.")

    class Config:
        arbitrary_types_allowed = True