from pathlib import Path

class Config:
    # Paths
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    LOGS_DIR = BASE_DIR / "logs"
    DOCS_DIR = BASE_DIR / "docs"
    # Ensure directories exist
    for dir_path in [DATA_DIR, LOGS_DIR]:
        dir_path.mkdir(exist_ok=True)

    # System settings
    TEMPERATURE_RANGE = (2, 8)  # Celsius
    REORDER_THRESHOLD = 0.2
    MAX_BATCH_SIZE = 1000

    # API settings
    API_TIMEOUT = 30
    MAX_RETRIES = 3

    # LLM settings
    LLM_PROVIDER = "ollama"
    LLM_MODEL = "llama2"

    # Logging settings
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
