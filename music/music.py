import time
from threading import Thread, Lock
import sys
import os
import locale
import argparse
import shutil

# Minimal, clean version: terminal-only song display.

# Configure terminal for Unicode output and font (best-effort)
if os.name == 'nt':  # For Windows
    try:
        # Ensure font rendering is enabled
        os.system(r'reg add "HKCU\Console" /v FontFamily /t REG_DWORD /d 54 /f >NUL')
    except Exception:
        pass

# Set locale (best-effort)
try:
    locale.setlocale(locale.LC_ALL, '')
except Exception:
    pass

# Try to ensure stdout uses UTF-8
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    try:
        sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)
    except Exception:
        pass

lock = Lock()

# Simple ASCII banner to show a pretty header
HEADER = r"""
  __   __ ___   _  _  _____ 
  \ \ / // _ \ | \| ||_   _|
   \ V /| (_) || .` |  | |  
    |_|  \___/ |_|\_|  |_|  

    ~ Sai Seng Zawm Fah [ ၼ မ်ႉတႃ ယို င်ႈ ႁူၺ်ႇ ] ~
"""

def print_header():
    """Print a centered, colored ASCII header if terminal supports it."""
    try:
        cols = shutil.get_terminal_size().columns
    except Exception:
        cols = 80
    lines = HEADER.splitlines()
    for line in lines:
        padding = max((cols - len(line)) // 2, 0)
        # ANSI bold cyan for header (works in modern Windows terminals)
        sys.stdout.write('\033[1;36m' + ' ' * padding + line + '\033[0m\n')
    print()

def animate_text(text, delay=0.1, scale=1):
    """Print text to the terminal one drawable unit at a time (thread-safe).

    For complex scripts (like Shan/Myanmar) printing codepoints one-by-one
    can break shaping because combining marks must follow their base
    character. To avoid that, we group base+combining marks into
    "clusters" and animate per-cluster instead of per-codepoint. When a
    non-complex script is used and "scale" > 1 we insert horizontal
    spacing between printable clusters to simulate larger text.

    scale: integer >=1 - controls spacing between printable clusters.
    """
    import unicodedata

    # Helper: group characters into base+combining clusters. This is a
    # simple approximation of grapheme clusters good enough for many
    # scripts: start a new cluster when the character is not a combining
    # mark.
    clusters = []
    current = ''
    for ch in text:
        if current == '':
            current = ch
        elif unicodedata.combining(ch):
            # combining mark -> attach to current cluster
            current += ch
        else:
            clusters.append(current)
            current = ch
    if current:
        clusters.append(current)

    # Detect Myanmar block (contains Shan/Myanmar characters). If present,
    # avoid inserting extra spaces because that will break glyph shaping.
    contains_myanmar = any('\u1000' <= ch <= '\u109F' for ch in text)

    # Build printable units with optional spacing for scaling. We operate
    # on clusters not raw codepoints to avoid breaking combining sequences.
    if scale <= 1 or contains_myanmar:
        units = clusters
    else:
        spacer = ' ' * (scale - 1)
        units = []
        for unit in clusters:
            if unit.isspace():
                units.append(unit)
            else:
                units.append(unit + spacer)

    with lock:
        # Animate printing each unit (cluster or cluster+spacer)
        for u in units:
            sys.stdout.write(u)
            sys.stdout.flush()
            time.sleep(delay)
        print()

        # Note: we intentionally do not re-print the whole line vertically here
        # to avoid duplicating entire lines (which can look like a bug). If
        # vertical repetition is desired, we can add a separate --vscale flag.


def sing_song(scale=1, show_header=True):
    lyrics = [
        ("ၵေႃႉလႆႈ ၶၢမ်ႇ ၼႆႉ မၢၵ်ႇ ႁူဝ် ၸႂ် ပဵၼ် ၾႆး ယူႇ", 0.14),
        ("\n""ၸူႉ ၶႂ်ႈ ပၢႆႊ ႁူႉ ဝႃႈ ပေႉ ၸႂ် သိူ ဝ်း ၸႂ် ၶၢတ်ႇ ယ ဝ်ႉ ", 0.13),
        ("\n""တေ ဢ ဝ် ၸႂ် ႁၵ်ႉ ပႅင်း ႁဵတ်း ၼ မ်ႉ တႃ ", 0.1),
        ("\n""ၵူၼ်း ၸၢႆး ၶႂ်ႈ ယွ ၼ်း တွ ၼ်ႈ ထို င် ", 0.1),
        ("\n""ၶေႃႈ ၵႂၢမ်း တို ၼ်း ဢ မ်ႇ လႅ ၼ် သ င်ႁၵ်ႉ မႂ်းသု တ်း ပိူၼ်ႈ ........", 0.1),
        ("\n""လ မ်ႇ ၽဵ င်း ၵႂၢမ်း ႁၵ်ႉ သိူ ဝ်း မူၼ်ႈ ......", 0.11),
        ("\n""တေ လႆႈ လႅ ၵ်ႈ ၶေႃႈ ၵႂၢမ်း ပဵၼ် ၼ မ်ႉ တႃ ", 0.08),
         ("\n""ႁႆႇ တို င်ႈ သေ ႁွင်ႉ ၽဵ င်း ၵႂၢမ်း ၵေႃႈ", 0.09),
        ("\n""ဢ မ်ႇ ၸ ပ်း လွ ၵ်း ၸ ပ်း လၢႆး သ င် ", 0.08),
        ("\n""ဢ မ်ႇ ႁူႉ တေ ႁဵတ်း ၸိူ င်ႉ ၼႆ လႆႈ တိူ ဝ်ႉ ၸႂ်.............", 0.12),
        ("\n""တေႃႇ ၼ မ်ႉ တႃ ၵူၼ်း ၸၢႆး ပေႃး လႆႈ ယို င်ႈ ႁူၺ်ႇ မႃး ..........", 0.13),
        ("\n""Editing By ♡ Sai Yont Sein♡ ", 0.2),
    ]

    delays = [0.2, 0.3, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4]

    if show_header:
        print_header()

    threads = []
    for i in range(len(lyrics)):
        lyric, speed = lyrics[i]
        t = Thread(target=sing_lyric, args=(lyric, delays[i], speed, scale))
        threads.append(t)
        t.start()

    for thread in threads:
        thread.join()


def sing_lyric(lyric, delay_start, char_delay, scale):
    """Display a single line of lyrics with animation after a delay.
    
    Args:
        lyric: The text to display
        delay_start: How long to wait before starting this line
        char_delay: Delay between each character
        scale: Text scale factor
    """
    time.sleep(delay_start)
    animate_text(lyric, delay=char_delay, scale=scale)

def parse_and_run():
    parser = argparse.ArgumentParser(description='Sing song in terminal')
    parser.add_argument('--scale', type=int, default=1, help='Repeat each character horizontally to simulate larger text (integer)')
    parser.add_argument('--no-header', action='store_true', help='Do not print the ASCII header')
    args = parser.parse_args()

    sing_song(scale=max(1, args.scale), show_header=not args.no_header)


if __name__ == "__main__":
    parse_and_run()