# SPDX-FileCopyrightText: Copyright (c) 2019-2025 CQFN.org
# SPDX-License-Identifier: MIT

all: wp.pdf

clean:
	rm -rf *.aux *.bbl *.bcf *.blg *.fdb_latexmk *.fls *.log *.run.xml

%.pdf: %.tex references.bib
	latexmk -pdf $<
