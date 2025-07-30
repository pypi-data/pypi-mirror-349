#!/usr/bin/env python3
#
# Copyright (c) 2017 University Of Helsinki (The National Library Of Finland)
# Copyright (c) 2025 Universität für angewandte Kunst Wien (University of Applied Arts Vienna)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""Module for accessing Skosmos REST API."""

import rdflib
import requests
from rdflib.namespace import SKOS

# Default API base URL
API_BASE = 'https://voc.uni-ak.ac.at/skosmos/rest/v1/'

REQUESTS_TIMEOUT = 10


class SkosmosConcept:
    """Class for representing and providing operations for a single concept
    from a Skosmos API."""

    def __init__(self, api_base, vocid, uri):
        self.api_base = api_base
        self.vocid = vocid
        self.uri = uri

    def _request(self, route, key, lang=None, limit=None):
        payload = {'uri': self.uri}
        if lang is not None:
            payload['lang'] = lang
        if limit is not None:
            payload['limit'] = limit
        req = requests.get(
            self.api_base + self.vocid + route,
            params=payload,
            timeout=REQUESTS_TIMEOUT,
        )
        req.raise_for_status()
        data = req.json()
        return data[key]

    def label(self, lang=None):
        return self._request('/label', 'prefLabel', lang)

    def broader(self, lang=None):
        return self._request('/broader', 'broader', lang)

    def broaderTransitive(self, lang=None, limit=None):  # noqa: N802
        return self._request('/broaderTransitive', 'broaderTransitive', lang, limit)

    def narrower(self, lang=None):
        return self._request('/narrower', 'narrower', lang)

    def narrowerTransitive(self, lang=None, limit=None):  # noqa: N802
        return self._request('/narrowerTransitive', 'narrowerTransitive', lang, limit)

    def related(self, lang=None):
        return self._request('/related', 'related', lang)


class SkosmosClient:
    """Client class for accessing Skosmos REST API operations."""

    def __init__(self, api_base=API_BASE):
        self.api_base = api_base

    def vocabularies(self, lang):
        """Get a list of vocabularies available on the API endpoint.

        Vocabulary titles will be returned in the given language.
        """

        payload = {'lang': lang}
        req = requests.get(
            self.api_base + 'vocabularies',
            params=payload,
            timeout=REQUESTS_TIMEOUT,
        )
        req.raise_for_status()
        return req.json()['vocabularies']

    def search(
        self,
        query,
        lang=None,
        labellang=None,
        vocabs=None,
        type_=None,
        parent=None,
        group=None,
        maxhits=100,
        offset=0,
        fields=None,
        unique=False,
    ):
        """Search for concepts either within specified vocabularies or globally
        in all vocabularies."""

        payload = {
            'query': query,
            'maxhits': maxhits,
            'offset': offset,
            'unique': unique,
        }

        if lang is not None:
            payload['lang'] = lang
        if labellang is not None:
            payload['labellang'] = lang
        if vocabs is not None:
            if isinstance(vocabs, str):
                payload['vocab'] = vocabs
            else:  # a sequence such as a list?
                payload['vocab'] = ' '.join(vocabs)
        if type_ is not None:
            payload['type'] = type_
        if parent is not None:
            payload['parent'] = parent
        if group is not None:
            payload['group'] = group

        req = requests.get(
            self.api_base + 'search',
            params=payload,
            timeout=REQUESTS_TIMEOUT,
        )
        req.raise_for_status()
        return req.json()['results']

    def data(self, uri, vocid=None):
        """Return all information about a particular URI.

        If a vocabulary ID is given, look up the information from that
        vocabulary; otherwise, let Skosmos decide. The data is returned
        as an rdflib Graph.
        """

        payload = {'uri': uri, 'format': 'application/rdf+xml'}

        if vocid is not None:
            url = self.api_base + vocid + '/data'
        else:
            url = self.api_base + 'data'

        req = requests.get(url, params=payload, timeout=REQUESTS_TIMEOUT)
        req.raise_for_status()
        graph = rdflib.Graph()
        graph.parse(data=req.content, format='xml')
        return graph

    def types(self, lang, vocid=None):
        """Return information about concept and collection types available on
        the API endpoint, either from within a given vocabulary or globally.

        Type labels will be returned in the given language.
        """

        if vocid is not None:
            url = self.api_base + vocid + '/types'
        else:
            url = self.api_base + 'types'
        payload = {'lang': lang}
        req = requests.get(url, params=payload, timeout=REQUESTS_TIMEOUT)
        req.raise_for_status()
        return req.json()['types']

    def get_vocabulary(self, vocid, lang=None):
        """Get information about a vocabulary by vocabulary ID.

        Labels will be returned in the given language.
        """

        payload = {}
        if lang is not None:
            payload['lang'] = lang
        req = requests.get(
            self.api_base + vocid + '/',
            params=payload,
            timeout=REQUESTS_TIMEOUT,
        )
        if req.status_code == 404:
            raise ValueError(req.text)
        req.raise_for_status()
        return req.json()

    def top_concepts(self, vocid, lang=None, scheme=None):
        """Get the top concepts of a vocabulary.

        Labels will be returned in the given language. An optional
        concept scheme URI can be specified to retrieve the top concepts
        within that scheme.
        """

        payload = {}
        if lang is not None:
            payload['lang'] = lang
        if scheme is not None:
            payload['scheme'] = scheme
        req = requests.get(
            self.api_base + vocid + '/topConcepts',
            params=payload,
            timeout=REQUESTS_TIMEOUT,
        )
        if req.status_code == 404:
            raise ValueError(req.text)
        req.raise_for_status()
        return req.json()['topconcepts']

    def lookup(self, vocid, label, lang=None):
        """Return information about a concept by its label.

        The results will be returned as a list, with the best match
        first. If a language is given, restrict matching to labels in
        that language.
        """

        payload = {'label': label}
        if lang is not None:
            payload['lang'] = lang

        req = requests.get(
            self.api_base + vocid + '/lookup',
            params=payload,
            timeout=REQUESTS_TIMEOUT,
        )
        if req.status_code == 404:
            raise ValueError(req.text)
        req.raise_for_status()
        return req.json()['result']

    def groups(self, vocid, lang=None):
        """Get the thematic groups of a vocabulary.

        Labels will be returned in the given language.
        """

        payload = {}
        if lang is not None:
            payload['lang'] = lang
        req = requests.get(
            self.api_base + vocid + '/groups',
            params=payload,
            timeout=REQUESTS_TIMEOUT,
        )
        if req.status_code == 404:
            raise ValueError(req.text)
        req.raise_for_status()
        return req.json()['groups']

    def get_concept(self, vocid, uri):
        """Get a Concept for performing concept-specific operations."""
        return SkosmosConcept(self.api_base, vocid, uri)

    def __str__(self):
        """Return a string representation of this object."""
        return f"SkosmosClient(api_base='{self.api_base}')"


if __name__ == '__main__':
    print('Demonstrating usage of SkosmosClient')  # noqa: T201

    print()  # noqa: T201

    print('* Creating a SkosmosClient object')  # noqa: T201
    skosmos = SkosmosClient(api_base='https://api.finto.fi/rest/v1/')
    print('Now we have a SkosmosClient object:', skosmos)  # noqa: T201
    print()  # noqa: T201
    print('* Finding the available vocabularies')  # noqa: T201
    for vocab in skosmos.vocabularies(lang='en'):
        print('Vocabulary id: {:<16} title: {}'.format(vocab['id'], vocab['title']))  # noqa: T201

    print()  # noqa: T201

    print('* Searching for concepts globally in all vocabularies')  # noqa: T201
    for result in skosmos.search('Stockholm*', lang='en'):
        print(result)  # noqa: T201

    print()  # noqa: T201

    print('* Searching for concepts within a single vocabulary')  # noqa: T201
    for result in skosmos.search('cosmolog*', vocabs='yso', lang='en'):
        print(result)  # noqa: T201

    print()  # noqa: T201
    print('* Looking up all information about a particular concept')  # noqa: T201
    graph = skosmos.data('http://www.yso.fi/onto/yso/p7160')
    print(f'Got {len(graph)} triples of data')  # noqa: T201
    # Let's look at the preferred labels within that graph
    for uri, label in graph.subject_objects(SKOS.prefLabel):
        if label.language == 'en':
            print(f'<{uri}> has label "{label}"@{label.language}')  # noqa: T201

    print()  # noqa: T201
    print('* Looking up information about types within a vocabulary')  # noqa: T201
    for typeinfo in skosmos.types('en', vocid='yso'):
        print(typeinfo)  # noqa: T201

    print()  # noqa: T201
    print('* Looking up information about a particular vocabulary')  # noqa: T201
    yso = skosmos.get_vocabulary('yso', lang='en')
    for key, val in sorted(yso.items()):
        if key in ('@context', 'uri'):
            continue
        print(f'{key:<20}: {val}')  # noqa: T201

    print()  # noqa: T201
    print('* Looking up top level concepts for a vocabulary')  # noqa: T201
    for top_concept in skosmos.top_concepts('yso', lang='en'):
        print(top_concept)  # noqa: T201

    print()  # noqa: T201
    print('* Looking up a concept by its label')  # noqa: T201
    lookup_results = skosmos.lookup('yso', 'cosmology', lang='en')
    print(lookup_results)  # noqa: T201

    print()  # noqa: T201
    print('* Looking up the thematic groups of a vocabulary')  # noqa: T201
    for group in skosmos.groups('yso', lang='en'):
        print(group)  # noqa: T201

    print()  # noqa: T201
    print('* Performing operations on single concepts')  # noqa: T201
    prams = skosmos.get_concept('yso', 'http://www.yso.fi/onto/yso/p12345')
    print("YSO concept 'prams' label in the default language:", prams.label())  # noqa: T201
    print("YSO concept 'prams' label in English:", prams.label('en'))  # noqa: T201
    print("Broader concepts of 'prams' in YSO:")  # noqa: T201
    for bc in prams.broader('en'):
        print(bc)  # noqa: T201
    print("Transitive broader concepts of 'prams' in YSO:")  # noqa: T201
    for btc in prams.broaderTransitive('en'):
        print(btc)  # noqa: T201

    print("Narrower concepts of 'Hanko' in YSO places:")  # noqa: T201
    hanko = skosmos.get_concept('yso-paikat', 'http://www.yso.fi/onto/yso/p94126')
    for nc in hanko.narrower():
        print(nc)  # noqa: T201
    print("Related concepts of 'prams' in YSO:")  # noqa: T201
    for rc in prams.related('en'):
        print(rc)  # noqa: T201
