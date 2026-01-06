import app.services.dummy_client as dummy_client
import app.services.google_client as google_client

from app.core.config import settings

genai_services = {
  "dummy": dummy_client,
  "google": google_client
}

default_client = genai_services[settings.GENAI_SERVICE_DEFAULT]

