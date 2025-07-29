from __future__ import annotations
from wowool.annotation import Concept, Token
from wowool.quotes.app_id import APP_ID
from wowool.diagnostic import Diagnostics
from wowool.document.analysis.document import AnalysisDocument
from collections import defaultdict
from wowool.annotation.token import TokenNone
from wowool.string import to_text
from typing import List, Optional
from wowool.utility.apps.decorators import (
    exceptions_to_diagnostics,
    requires_analysis,
    check_requires_concepts,
)


uris = set(["Quotation", "QuotationAuthor"])


def is_quotation_scope(concept):
    return concept.uri == "QuotationScope"


def is_quote_part(concept):
    return concept.uri in uris


def end_on_quote(tokens):
    if tokens[-1].has_pos("Punct-Quote"):
        return True
    return tokens[-1].has_pos("Punct-Quote")


class Quotes:
    ID = APP_ID

    def __init__(self, mentions: Optional[List[str]] = None):
        """
        Initialize the Quotes application.

        :param mentions: A list of concepts that are mentioned in the quote
        :type mentions: ``list[str]``
        """

        self.mentions = set(mentions) if mentions != None else None

    def is_entity(self, concept: Concept) -> bool:
        assert self.mentions
        return concept.uri in self.mentions

    @exceptions_to_diagnostics
    @requires_analysis
    def __call__(self, document: AnalysisDocument, diagnostics: Diagnostics) -> AnalysisDocument:
        """
        :param document:  The document we want to enrich with your quotes.
        :type document: AnalysisDocument

        :returns: The given document with the quotes. See the :ref:`json format <json_apps_quotes>`

        """
        check_requires_concepts(self.ID, document, diagnostics, uris)

        quotes = []
        assert document.analysis != None, f"Missing Document analysis for {document.id}"
        for sidx, sent in enumerate(document.analysis):
            for scope in Concept.iter(sent, is_quotation_scope):
                extra_quotation_sentences = set()
                quote = {}
                entities = defaultdict(set)

                for concept in Concept.iter(scope, is_quote_part):
                    if concept.uri == "QuotationAuthor":
                        quote["author"] = concept.canonical
                    elif concept.uri == "Quotation":
                        quotation = concept
                        begin_offset = end_offset = 0
                        if self.mentions is not None:
                            for entity in Concept.iter(concept, self.is_entity):
                                entities[entity.uri].add(entity.canonical)

                        text = []
                        tokens = [token for token in Token.iter(quotation)]
                        if len(tokens) > 2 and tokens[0].has_pos("Punct-Quote") and end_on_quote(tokens):
                            text.extend(quotation.tokens)
                            begin_offset = quotation.begin_offset
                            end_offset = quotation.end_offset
                        else:
                            scope_range = None
                            if quotation.scope is None:
                                scope_range = 3
                            else:
                                scope_range = int(quotation.scope)
                            if scope_range < 0:
                                # we are going to look the sentences before
                                psidx = sidx - 1
                                end_offset = scope.end_offset
                                limit_sidx = max(0, sidx + scope_range)
                                while psidx >= 0 and psidx >= limit_sidx:
                                    prev_sent = document.analysis[psidx]
                                    extra_quotation_sentences.add(psidx)
                                    first_token = TokenNone
                                    for token in Token.iter(prev_sent):
                                        first_token = token
                                        break
                                    if first_token.has_pos("Punct-Quote"):
                                        text.append(prev_sent)
                                        begin_offset = first_token.begin_offset
                                        break

                                    psidx -= 1
                                    text.append(prev_sent)

                                if psidx < limit_sidx:
                                    text.clear()
                                else:
                                    text = text[::-1]
                                text.extend(quotation.tokens)
                            else:
                                # we are going to look the sentences after this one.
                                begin_offset = quotation.begin_offset
                                text.extend(quotation.tokens)
                                nsidx = sidx + 1
                                nrof_sentence = len(document.analysis.sentences)
                                limit_sidx = min(nrof_sentence, sidx + scope_range)
                                while nsidx < nrof_sentence and nsidx < limit_sidx:
                                    next_sent = document.analysis[nsidx]
                                    tokens = [token for token in Token.iter(next_sent)]

                                    last_token = tokens[-1]
                                    if last_token.has_pos("Punct-Quote"):
                                        text.append(next_sent)
                                        end_offset = last_token.end_offset
                                        break
                                    elif last_token.has_pos("Punct-Sent"):
                                        try:
                                            last_token = tokens[-2]
                                            if last_token and last_token.has_pos("Punct-Quote"):
                                                text.append(next_sent)
                                                end_offset = last_token.end_offset
                                        except Exception:
                                            pass
                                        break
                                    extra_quotation_sentences.add(nsidx)
                                    text.append(next_sent)
                                    nsidx += 1

                        if self.mentions:
                            for quote_sentence_index in extra_quotation_sentences:
                                for entity in Concept.iter(
                                    document.analysis[quote_sentence_index],
                                    self.is_entity,
                                ):
                                    entities[entity.uri].add(entity.canonical)

                        quote["text"] = to_text(text)
                        quote["begin_offset"] = begin_offset
                        quote["end_offset"] = end_offset
                        if entities:
                            _entities = []
                            for uri, data in entities.items():
                                for entity_text in data:
                                    _entities.append({"uri": uri, "text": entity_text})
                            quote["mentions"] = _entities

                quotes.append(quote)
        document.add_results(APP_ID, quotes)
        return document
