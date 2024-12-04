#!/bin/bash

PYPROG="
import mrm.ansi_term
import sys

print(mrm.ansi_term.as_pango_markup(sys.stdin.read()))
"
BASENAME=`date +%s`

python3 -c "$PYPROG" > $BASENAME.mark
pango-view --font="JetBrains Mono" --markup $BASENAME.mark -qo $BASENAME.png
