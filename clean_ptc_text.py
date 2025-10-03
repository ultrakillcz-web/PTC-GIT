#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
clean_ptc_text.py
Remove blocos "Medical References" com DOIs falsos (file-...) e qualquer ocorrência isolada de "— DOI: file-...".
Uso:
  python clean_ptc_text.py input.txt -o output.txt
  cat input.txt | python clean_ptc_text.py > output.txt
"""

import sys
import re
import argparse

def clean_text(text: str) -> str:
    # 1) Remove bloco completo começando por "Medical References:" seguido por linhas numeradas com "DOI: file-..."
    block_pattern = re.compile(
        r'(?:\r?\n|\A)\s*Medical References:\s*(?:\r?\n\s*\d+\.\s*.*?DOI:\s*file-[A-Za-z0-9]+\s*)+',
        flags=re.IGNORECASE
    )
    text = block_pattern.sub('\n', text)

    # 2) Remover qualquer ocorrência isolada de "— DOI: file-xxxxx"
    inline_fake_doi = re.compile(r'\s*—\s*DOI:\s*file-[A-Za-z0-9]+\s*', flags=re.IGNORECASE)
    text = inline_fake_doi.sub('', text)

    # 3) Limpar linhas em branco repetidas
    text = re.sub(r'\n{3,}', '\n\n', text.strip()) + '\n'
    return text

def main():
    parser = argparse.ArgumentParser(description="Remove 'Medical References' falsos (file-...) do texto.")
    parser.add_argument("input", nargs="?", help="Arquivo de entrada (opcional; usa stdin se ausente).")
    parser.add_argument("-o", "--output", help="Arquivo de saída (opcional; padrão: stdout).")
    args = parser.parse_args()

    if args.input:
        with open(args.input, "r", encoding="utf-8", errors="ignore") as f:
            raw = f.read()
    else:
        raw = sys.stdin.read()

    cleaned = clean_text(raw)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(cleaned)
    else:
        sys.stdout.write(cleaned)

if __name__ == "__main__":
    main()
