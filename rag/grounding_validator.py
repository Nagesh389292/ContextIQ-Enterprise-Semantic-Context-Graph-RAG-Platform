"""
ContextIQ — Grounding & Citation Validator
Evaluates LLM generated answers for citation presence, factual alignment, claim support, and grounding score calculation.
"""

import re
from typing import Dict, Any, List


class GroundingValidator:
    """Validates citation presence and evaluates faithfulness of generated RAG responses against retrieved context."""

    def validate(self, answer: str, context_bundle: Dict[str, Any]) -> Dict[str, Any]:
        """Audit answer text for citations, claim alignment, and return detailed grounding metrics."""
        top_chunks: List[Dict[str, Any]] = context_bundle.get("top_chunks", [])
        valid_chunk_ids = set(c.get("chunk_id") for c in top_chunks if c.get("chunk_id"))

        # 1. Extract Citation Markers
        chunk_citations = re.findall(r"\[(DOC-\d{3}_CHUNK_\d{2})\]", answer)
        entity_citations = re.findall(r"\[(Machine|Plant|Supplier|Sensor|Material|Order):([A-Za-z0-9_-]+)\]", answer)

        valid_citations = [c for c in chunk_citations if c in valid_chunk_ids]
        invalid_citations = [c for c in chunk_citations if c not in valid_chunk_ids]

        # 2. Check for Insufficient Evidence Fallback Statement
        has_fallback_phrase = "Information not available in enterprise context" in answer or "insufficient evidence" in answer.lower()

        # 3. Analyze Claim Support & Sentences
        sentences = [s.strip() for s in re.split(r"[.!?]\s+", answer) if s.strip() and len(s.strip()) > 15]

        supported_claims_count = 0
        unsupported_claims_count = 0

        if not top_chunks:
            # Scenario C: No retrieved evidence
            if has_fallback_phrase:
                grounding_score = 1.0  # Correctly identified lack of data
                status = "PASS_INSUFFICIENT_DATA"
            else:
                grounding_score = 0.0  # Ungrounded answer generated without retrieved context
                status = "FAIL_NO_CONTEXT"
                unsupported_claims_count = len(sentences)
        elif has_fallback_phrase:
            grounding_score = 1.0
            status = "PASS_EXPLICIT_FALLBACK"
        else:
            # Count claims with citations or keywords matching retrieved chunks
            corpus_text = " ".join([c.get("text", "") for c in top_chunks]).lower()

            for sent in sentences:
                sent_citations = re.findall(r"\[DOC-\d{3}_CHUNK_\d{2}\]", sent)
                if sent_citations:
                    supported_claims_count += 1
                else:
                    # Check key noun/code overlap with retrieved text
                    tokens = set(re.findall(r"\b[A-Z0-9]{3,}\b", sent))
                    if tokens and any(tok.lower() in corpus_text for tok in tokens):
                        supported_claims_count += 1
                    else:
                        unsupported_claims_count += 1

            total_claims = supported_claims_count + unsupported_claims_count
            if total_claims > 0:
                raw_score = supported_claims_count / total_claims
                # Apply penalty if invalid citations exist
                if invalid_citations:
                    raw_score *= 0.5
                grounding_score = round(raw_score, 2)
            else:
                grounding_score = 0.50

            status = "PASS_GROUNDED" if grounding_score >= 0.70 else "FLAGGED_LOW_GROUNDING"

        citation_coverage = round(supported_claims_count / max(1, len(sentences)), 2) if sentences else 1.0

        return {
            "grounding_score": grounding_score,
            "is_grounded": grounding_score >= 0.70,
            "status": status,
            "total_sentences_count": len(sentences),
            "supported_claims_count": supported_claims_count,
            "unsupported_claims_count": unsupported_claims_count,
            "citation_coverage": citation_coverage,
            "valid_chunk_citations": list(set(valid_citations)),
            "invalid_chunk_citations": list(set(invalid_citations)),
            "entity_citations_found": [f"{e[0]}:{e[1]}" for e in entity_citations],
            "total_citations_count": len(chunk_citations) + len(entity_citations),
        }
