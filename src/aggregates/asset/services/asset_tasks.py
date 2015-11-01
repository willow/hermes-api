from src.aggregates.asset.services import asset_service
import logging
from django_rq import job
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@job('high')
def create_asset_task(asset_path, asset_content_type, asset_original_name):
  log_message = (
    "Create asset task for asset_original_name: %s",
    asset_original_name
  )

  with log_wrapper(logger.info, *log_message):
    return asset_service.create_asset(asset_path, asset_content_type, asset_original_name).asset_id
