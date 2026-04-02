import sys
from logging.config import fileConfig
from os.path import abspath, dirname

from alembic import context
from sqlalchemy import engine_from_config, pool

# Adiciona o caminho do projeto ao sys.path para que os imports do 'app' funcionem
sys.path.insert(0, abspath(dirname(dirname(__file__))))

from app.infrastructure.schemas import Base
from app.settings import get_settings

# este é o objeto de configuração do Alembic
config = context.config

# Configura o logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Aqui passamos o metadata dos seus modelos
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Executa migrações no modo 'offline'."""
    settings = get_settings()
    url = settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Executa migrações no modo 'online'."""
    settings = get_settings()

    # Sobrescreve a URL do sqlalchemy no config do alembic com a vinda do seu .env
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = settings.DATABASE_URL

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
