import os
from pathlib import Path

from alembic.config import Config

PROJECT_PATH = Path(__file__).parent.parent.parent


def make_alembic_config(pg_url):
    """
    Создает объект конфигурации alembic.
    """
    path_to_config = os.path.join(PROJECT_PATH, 'alembic.ini')

    config = Config(file_=path_to_config)
    config.set_main_option('sqlalchemy.url', pg_url)

    alembic_location = config.get_main_option('script_location')
    if not os.path.isabs(alembic_location):
        config.set_main_option(
            'script_location', os.path.join(PROJECT_PATH, alembic_location)
        )

    return config
