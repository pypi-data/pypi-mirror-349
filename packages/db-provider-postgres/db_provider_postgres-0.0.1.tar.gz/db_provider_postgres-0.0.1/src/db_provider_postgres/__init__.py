"""
Database provider library for connecting to various database systems.
"""

from db_provider.providers.postgres import PostgresDatabaseProvider

__all__ = ['PostgresDatabaseProvider']
__version__ = '0.1.0'