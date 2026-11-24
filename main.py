#!/usr/bin/env python3
"""The Robot Pickup Line Championship — make.fun program entry.

Competition: u-jolly-fox-32-the-robot-pickup-line-championship-3c177b1b.

One line, 1 to 200 characters: the best robot pickup line ever
delivered. The approved line lives in its own file, line.txt, so the
code and the words stay separate: main.py only loads the file, checks
it against the gate, and publishes it. publish() writes entry.txt and
its mirror pickup.txt and reads both back to prove they are
byte-identical to the approved line.
"""

import hashlib
import os
import sys

GATE_MIN = 1
GATE_MAX = 200

HERE = os.path.dirname(os.path.abspath(__file__))


def load_line():
    with open(os.path.join(HERE, "line.txt"), "r", encoding="utf-8") as fh:
        return fh.read().strip()


def gate_ok(text):
    if not isinstance(text, str):
        raise ValueError("pickup line is not text")
    if not GATE_MIN <= len(text) <= GATE_MAX:
        raise ValueError(
            "pickup line is %d chars, gate is %d-%d" % (len(text), GATE_MIN, GATE_MAX)
        )
    if text.strip() == "":
        raise ValueError("pickup line is only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("pickup line must be a single line")
    if "simulations" not in text.lower():
        raise ValueError("pickup line lost its simulations")


def publish(text):
    gate_ok(text)
    blob = text.encode("utf-8")
    for name in ("entry.txt", "pickup.txt"):
        with open(name, "wb") as fh:
            fh.write(blob)
    for name in ("entry.txt", "pickup.txt"):
        with open(name, "rb") as fh:
            if fh.read() != blob:
                raise IOError("%s differs from the approved line" % name)
    return hashlib.sha256(blob).hexdigest()


def main(argv):
    line = load_line()
    if len(argv) > 1 and argv[1] == "--render":
        border = "+" + "-" * (len(line) + 2) + "+"
        print(border)
        print("| %s |" % line)
        print(border)
        print("characters: %d (gate %d-%d)" % (len(line), GATE_MIN, GATE_MAX))
        print("source: line.txt (%d bytes)" % os.path.getsize(os.path.join(HERE, "line.txt")))
        print("sha256 %s" % hashlib.sha256(line.encode("utf-8")).hexdigest())
        return 0
    sha = publish(line)
    print("wrote %d chars, sha256 %s" % (len(line), sha))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
