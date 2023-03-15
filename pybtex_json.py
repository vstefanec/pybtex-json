from __future__ import unicode_literals

from collections import OrderedDict

import json
from pybtex.database.output import BaseWriter


class JSONWriter(BaseWriter):
    def _to_dict(self, bib_data):
        def process_person_roles(entry):
            for role, persons in entry.persons.items():
                yield role, list(process_persons(persons))

        def process_person(person):
            for type in ('first', 'middle', 'prelast', 'last', 'lineage'):
                name = person.get_part_as_text(type)
                if name:
                    yield type, name

        def process_persons(persons):
            for person in persons:
                yield OrderedDict(process_person(person))

        def process_entries(bib_data):
            for key, entry in bib_data.items():
                fields = OrderedDict([('type', entry.original_type)])
                fields.update(entry.fields)
                fields.update(process_person_roles(entry))
                yield key, fields

        data = {'entries': OrderedDict(process_entries(bib_data.entries))}
        if bib_data.preamble:
            data['preamble'] = bib_data.preamble
        return data

    def _dump(self, bib_data, stream=None):
        if stream:
            return json.dump(
                bib_data,
                stream,
                indent=4,
            )

        return json.dumps(bib_data)

    def write_stream(self, bib_data, stream):
        return self._dump(self._to_dict(bib_data), stream=stream)

    def to_string(self, bib_data):
        return self._dump(self._to_dict(bib_data))

    def to_bytes(self, bib_data):
        return self._dump(self._to_dict(bib_data))
