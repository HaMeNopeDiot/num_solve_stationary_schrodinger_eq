IN = report.typ
OUT = report.tex
PDFNAME = report.pdf
PANDOC_KEYS = -f typst -t latex

all:
	cat preamble.tex > $(OUT)
	pandoc $(PANDOC_KEYS) $(IN) >> $(OUT)
	echo "\end{document}" >> $(OUT)
	pdflatex $(OUT) $(PDFNAME)
	rm *.log *.aux


typst:
	typst compile main.typ
	open main.pdf
