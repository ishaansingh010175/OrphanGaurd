import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load .env file
load_dotenv()


@dataclass
class Config:
    """
    Application configuration.
    """

    # OpenAI
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-5")

    # Kubernetes
    kubeconfig: str | None = os.getenv("KUBECONFIG")

    # Scanner
    min_resource_age_days: int = int(
        os.getenv("MIN_RESOURCE_AGE_DAYS", "7")
    )

    # Delete settings
    dry_run: bool = os.getenv("DRY_RUN", "true").lower() == "true"

    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")


config = Config()