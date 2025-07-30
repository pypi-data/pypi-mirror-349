from typing import Tuple

from ..interfaces import IAudioRecord


class AudioSearchService(object):
    @staticmethod
    def search_by_tags(
        records: Tuple[IAudioRecord, ...], tags: list[str], match_all: bool = False
    ) -> Tuple[IAudioRecord, ...]:
        """
        Search audio records by tags.

        :param records: Audio records to search.
        :param tags: List of tags to search for.
        :param match_all: True if record must contain all tags.
        :return: Tuple of matching audio records.
        :raises ValueError: If tags is empty or invalid.
        """
        tags = [tag.lower() for tag in tags]

        def matches(record: IAudioRecord) -> bool:
            if match_all:
                return all(tag in record.tags for tag in tags)
            return any(tag in record.tags for tag in tags)

        return tuple(record for record in records if matches(record))

    @staticmethod
    def search_by_name(
        records: Tuple[IAudioRecord, ...], name: str
    ) -> Tuple[IAudioRecord, ...]:
        """
        Search audio records by name.

        :param records: Audio records to search.
        :param name: Record name to match.
        :return: Tuple of matching audio records.
        :raises ValueError: If name is invalid.
        """
        name = name.lower()

        return tuple(record for record in records if name in record.record_name.lower())
