import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret_key")
    FLASK_ENV = os.getenv("FLASK_ENV", "production")

    # Email configuration
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True").lower() == "true"
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "False").lower() == "true"

    # Redis configuration
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # OpenAI configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

    # Shopify configuration
    SHOPIFY_API_KEY = os.getenv("SHOPIFY_API_KEY", "")
    SHOPIFY_API_SECRET = os.getenv("SHOPIFY_API_SECRET", "")
    SHOPIFY_STORE_URL = os.getenv("SHOPIFY_STORE_URL", "")
    SHOPIFY_ACCESS_TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN", "")

    # Sentry configuration
    SENTRY_DSN = os.getenv("SENTRY_DSN", "")

    # Caching
    CACHE_TYPE = "simple"
    CACHE_DEFAULT_TIMEOUT = 300
