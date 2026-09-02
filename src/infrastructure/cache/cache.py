import time
import redis
import os
import json
from dotenv import load_dotenv
from src.domain.interfaces import CacheServiceUsername


class CacheServices(CacheServiceUsername):
    
    def __init__(self, redis_client):
        self._client = redis_client
        self._local_fallback = {} 

    def _get_client(self):
        return self._client

    def set_token_username(self, token: str, username: str, user_id: int, ttl_seconds: int = 1800):
        """Guarda el usuario con un tiempo de vida (TTL)."""
        client = self._get_client()
        data_store = json.dumps({"username": username, "user_id": user_id})
        try:
            if client:
                client.set(f"user:{token}", data_store,  ex=ttl_seconds)
            else:
                self._local_fallback[token] = data_store
        except redis.RedisError as e:
            self._local_fallback[token] = data_store
            return None

    def get_username(self, token: str):
        """Obtiene el usuario. Si Redis falla, intenta buscar en el respaldo."""
        client = self._get_client()
        try:
            if client:
                raw_data = client.get(f"user:{token}")
                return json.loads(raw_data)
            return self._local_fallback.get(token)
        except redis.RedisError as e:
            return self._local_fallback.get(token)

    def delete_username(self, token: str):
        """Elimina el usuario (ideal para invalidar caché al cerrar sesión)."""
        client = self._get_client()
        # Eliminar del respaldo local
        self._local_fallback.pop(token, None)
        # Eliminar de Redis
        try:
            if client:
                client.delete(f"user:{token}")
        except redis.RedisError as e:
            return None