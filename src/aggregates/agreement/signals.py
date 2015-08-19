from src.libs.common_domain.event_signal import EventSignal

created = EventSignal(
  'created', __name__, 1,
  providing_args=['agreement_uid', 'agreement_name', 'agreement_type']
)

added_ta_topic = EventSignal(
  'added_ta_topic', __name__, 1,
  providing_args=['agreement_uid', 'ta_topic_uid', 'topic_type_id']
)
