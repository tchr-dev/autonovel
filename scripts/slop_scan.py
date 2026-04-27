#!/usr/bin/env python3
"""Mechanical slop scanner. No LLM calls — regex + statistics only.

Reads a markdown file (chapter or planning doc) from argv or stdin and emits a
JSON report listing AI-tell hits, em-dash density, sentence-length variation,
transition-opener abuse, telling-violations, and a composite slop_penalty 0-10.

Usage:
  python slop_scan.py path/to/ch_05.md
  python slop_scan.py novels/<tag>/chapters/ch_05.md --json    # machine-readable
"""
import argparse
import json
import re
import sys
from pathlib import Path

TIER1_BANNED = [
    "delve", "utilize", "leverage", "facilitate", "elucidate",
    "embark", "endeavor", "encompass", "multifaceted", "tapestry",
    "paradigm", "synergy", "synergize", "holistic", "catalyze",
    "catalyst", "juxtapose", "myriad", "plethora",
]

TIER2_SUSPICIOUS = [
    "robust", "comprehensive", "seamless", "seamlessly", "cutting-edge",
    "innovative", "streamline", "empower", "foster", "enhance", "elevate",
    "optimize", "pivotal", "intricate", "profound", "resonate",
    "underscore", "harness", "cultivate", "bolster", "galvanize",
    "cornerstone", "game-changer", "scalable",
]

TIER3_FILLER = [
    r"it'?s worth noting that",
    r"it'?s important to note that",
    r"^importantly,?\s",
    r"^notably,?\s",
    r"^interestingly,?\s",
    r"let'?s dive into",
    r"let'?s explore",
    r"as we can see",
    r"^furthermore,?\s",
    r"^moreover,?\s",
    r"^additionally,?\s",
    r"in today'?s .*(fast-paced|digital|modern)",
    r"at the end of the day",
    r"it goes without saying",
    r"when it comes to",
    r"one might argue that",
    r"not just .+, but",
]

TRANSITION_OPENERS = [
    "however", "furthermore", "additionally", "moreover",
    "nevertheless", "consequently", "nonetheless", "similarly",
]

FICTION_AI_TELLS = [
    r"a sense of \w+",
    r"couldn'?t help but feel",
    r"the weight of \w+",
    r"the air was thick with",
    r"eyes widened",
    r"a wave of \w+ washed over",
    r"a pang of \w+",
    r"heart pounded in (?:his|her|their) chest",
    r"(?:raven|dark|golden|silver) (?:hair|tresses) (?:spilled|cascaded|tumbled|fell)",
    r"piercing (?:blue|green|gray|grey|dark) eyes",
    r"a knowing (?:smile|grin|look|glance)",
    r"(?:he|she|they) felt a (?:surge|rush|wave|pang|flicker) of",
    r"the silence (?:was|hung|stretched|grew) (?:heavy|thick|oppressive|deafening)",
    r"let out a breath (?:he|she|they) didn'?t (?:know|realize)",
    r"something (?:dark|ancient|primal|unnamed) stirred",
]

STRUCTURAL_AI_TICS = [
    r"(?:I'm|I am) not (?:saying|asking|suggesting) .{3,40}(?:I'm|I am) (?:saying|asking|suggesting)",
    r"(?:which|that) means either .{3,40} or ",
    r"[Tt]here'?s a (?:difference|distinction)\.",
    r"[Tt]hose are (?:different|not the same) things\.",
    r"[Nn]ot (?:just|merely|simply) .{3,40}, but ",
    r"[Nn]ot (?:from|by|because of) .{3,40}, but (?:from|by|because)",
]

TELLING_PATTERNS = [
    r"\b(?:he|she|they|I|we|[A-Z]\w+) (?:felt|was|seemed|looked|appeared) (?:angry|sad|happy|scared|nervous|excited|jealous|guilty|anxious|lonely|desperate|furious|terrified|elated|miserable|hopeful|confused|relieved|horrified|disgusted|ashamed|proud|bitter|defeated|triumphant)\b",
    r"\b(?:angrily|sadly|happily|nervously|excitedly|desperately|furiously|anxiously|guiltily|bitterly|wearily|miserably)\b",
]


def scan(text: str) -> dict:
    words = text.lower().split()
    word_count = len(words) or 1

    tier1_hits = []
    for w in TIER1_BANNED:
        c = sum(1 for token in words if token.strip(".,;:!?\"'()") == w)
        if c > 0:
            tier1_hits.append([w, c])

    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    tier2_hits = []
    tier2_cluster_count = 0
    for w in TIER2_SUSPICIOUS:
        c = sum(1 for token in words if token.strip(".,;:!?\"'()") == w)
        if c > 0:
            tier2_hits.append([w, c])
    for para in paragraphs:
        para_lower = para.lower()
        hits_in_para = sum(1 for w in TIER2_SUSPICIOUS if w in para_lower)
        if hits_in_para >= 3:
            tier2_cluster_count += 1

    tier3_hits = []
    for pattern in TIER3_FILLER:
        matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
        if matches:
            tier3_hits.append([pattern, len(matches)])

    em_dashes = text.count("—") + text.count("--")
    em_dash_density = (em_dashes / word_count) * 1000

    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip().split()) > 2]
    if len(sentences) > 2:
        lengths = [len(s.split()) for s in sentences]
        mean_len = sum(lengths) / len(lengths)
        variance = sum((l - mean_len) ** 2 for l in lengths) / len(lengths)
        std_len = variance ** 0.5
        sentence_length_cv = std_len / mean_len if mean_len > 0 else 0
    else:
        sentence_length_cv = 0.5

    transition_starts = 0
    for para in paragraphs:
        first_word = para.split()[0].lower().strip(".,;:!?\"'()") if para.split() else ""
        if first_word in TRANSITION_OPENERS:
            transition_starts += 1
    transition_ratio = transition_starts / len(paragraphs) if paragraphs else 0

    fiction_tells = []
    for pattern in FICTION_AI_TELLS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            fiction_tells.append([pattern[:40], len(matches)])
    fiction_tell_count = sum(c for _, c in fiction_tells)

    telling_count = 0
    for pattern in TELLING_PATTERNS:
        telling_count += len(re.findall(pattern, text, re.IGNORECASE))

    structural_tics = []
    for pattern in STRUCTURAL_AI_TICS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            structural_tics.append([pattern[:40], len(matches)])
    structural_tic_count = sum(c for _, c in structural_tics)

    penalty = 0.0
    penalty += min(len(tier1_hits) * 1.5, 4.0)
    penalty += min(tier2_cluster_count * 1.0, 2.0)
    penalty += min(sum(c for _, c in tier3_hits) * 0.3, 2.0)
    if em_dash_density > 15:
        penalty += min((em_dash_density - 15) * 0.3, 1.0)
    if sentence_length_cv < 0.3:
        penalty += 1.0
    if transition_ratio > 0.3:
        penalty += min(transition_ratio * 2, 1.0)
    penalty += min(fiction_tell_count * 0.3, 2.0)
    penalty += min(telling_count * 0.2, 1.5)
    penalty += min(structural_tic_count * 0.5, 2.0)
    penalty = min(penalty, 10.0)

    return {
        "word_count": word_count,
        "tier1_hits": tier1_hits,
        "tier2_hits": tier2_hits,
        "tier2_clusters": tier2_cluster_count,
        "tier3_hits": tier3_hits,
        "fiction_ai_tells": fiction_tells,
        "structural_ai_tics": structural_tics,
        "telling_violations": telling_count,
        "em_dash_density": round(em_dash_density, 2),
        "sentence_length_cv": round(sentence_length_cv, 3),
        "transition_opener_ratio": round(transition_ratio, 3),
        "slop_penalty": round(penalty, 2),
    }


def main():
    p = argparse.ArgumentParser(description="Mechanical slop scanner")
    p.add_argument("path", nargs="?", help="File to scan (omit to read stdin)")
    p.add_argument("--json", action="store_true", help="Emit JSON only")
    args = p.parse_args()

    text = Path(args.path).read_text() if args.path else sys.stdin.read()
    report = scan(text)
    if args.json:
        print(json.dumps(report, indent=2))
        return

    print(f"words: {report['word_count']}  slop_penalty: {report['slop_penalty']}/10")
    print(f"  tier1 banned: {report['tier1_hits'] or 'none'}")
    print(f"  tier2 clusters: {report['tier2_clusters']}")
    print(f"  fiction AI tells: {report['fiction_ai_tells'] or 'none'}")
    print(f"  structural AI tics: {report['structural_ai_tics'] or 'none'}")
    print(f"  telling violations: {report['telling_violations']}")
    print(f"  em-dash density: {report['em_dash_density']}/1k words")
    print(f"  sentence length CV: {report['sentence_length_cv']} (>0.3 is good)")
    print(f"  transition openers: {report['transition_opener_ratio']*100:.0f}%")


if __name__ == "__main__":
    main()
