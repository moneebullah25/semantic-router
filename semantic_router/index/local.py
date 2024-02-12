import numpy as np
from typing import List, Tuple, Optional
from semantic_router.linear import similarity_matrix, top_scores
from semantic_router.index.base import BaseIndex
from semantic_router.route import Route

class LocalIndex(BaseIndex):
    def __init__(self):
        super().__init__()
        self.type = "local"
        self.index: Optional[np.ndarray] = None
        self.routes: Optional[List[Route]] = None
        self.route_names: Optional[List[str]] = None
        self.utterances: Optional[np.ndarray] = None

    class Config:  # Stop pydantic from complaining about  Optional[np.ndarray] type hints.
        arbitrary_types_allowed = True

    def add(
        self, embeddings: List[List[float]], route: Route, utterances: List[str]
    ):
        embeds = np.array(embeddings)  # type: ignore
        route_names_arr = np.array([route.name] * len(utterances))
        utterances_arr = np.array(utterances)
        if self.index is None:
            self.index = embeds  # type: ignore
            self.routes = [route]
            self.route_names = route_names_arr
            self.utterances = utterances_arr
        else:
            self.index = np.concatenate([self.index, embeds])
            self.routes.append(route)
            self.route_names = np.concatenate([self.route_names, route_names_arr])
            self.utterances = np.concatenate([self.utterances, utterances_arr])

    def _get_indices_for_route(self, route_name: str):
        """Gets an array of indices for a specific route."""
        if self.route_names is None:
            raise ValueError("Routes are not populated.")
        idx = [i for i, _route_name in enumerate(self.route_names) if _route_name == route_name]
        return idx
    
    def get_routes(self) -> List[Route]:
        """
        Gets a list of Route objects currently stored in the index.

        Returns:
            List[Route]: A list of Route objects.
        """
        if self.routes is None:
            raise ValueError("No routes have been added to the index.")
        return self.routes

    def delete(self, route_name: str):
        """
        Delete all records of a specific route from the index.
        """
        if (
            self.index is not None
            and self.route_names is not None
            and self.utterances is not None
        ):
            delete_idx = self._get_indices_for_route(route_name=route_name)
            self.index = np.delete(self.index, delete_idx, axis=0)
            self.routes = [route for route in self.routes if route.name != route_name] if self.routes else None
            self.route_names = np.delete(self.route_names, delete_idx, axis=0)
            self.utterances = np.delete(self.utterances, delete_idx, axis=0)
        else:
            raise ValueError(
                "Attempted to delete route records but either indx, routes or utterances is None."
            )

    def describe(self) -> dict:
        return {
            "type": self.type,
            "dimensions": self.index.shape[1] if self.index is not None else 0,
            "vectors": self.index.shape[0] if self.index is not None else 0,
        }

    def query(self, vector: np.ndarray, top_k: int = 5) -> Tuple[np.ndarray, List[str]]:
        """
        Search the index for the query and return top_k results.
        """
        if self.index is None or self.route_names is None:
            raise ValueError("Index or routes are not populated.")
        sim = similarity_matrix(vector, self.index)
        # extract the index values of top scoring vectors
        scores, idx = top_scores(sim, top_k)
        # get routes from index values
        route_names = self.route_names[idx].copy()
        return scores, route_names

    def delete_index(self):
        """
        Deletes the index, effectively clearing it and setting it to None.
        """
        self.index = None
