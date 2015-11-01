from src.libs.common_domain.event_signal import EventSignal

created = EventSignal(
  'created', __name__, 1,
  providing_args=['asset_id', 'asset_path', 'asset_content_type', 'asset_original_name', 'asset_system_created_date']
)
