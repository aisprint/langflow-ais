class SharedComponentCacheService(ThreadingInMemoryCache):
    """
    A caching service shared across components.
    """

    name = "shared_component_cache_service"
