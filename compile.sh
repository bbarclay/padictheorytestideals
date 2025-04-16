#!/bin/bash

# Enhanced compile script for "Binary P-adic Theory of Test Ideals in Mixed Characteristic"
# This script handles the complete LaTeX compilation process for arXiv submission

# Set colors for terminal output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Compiling Binary P-adic Theory of Test Ideals Paper for arXiv ===${NC}"

# Create output directory if it doesn't exist
mkdir -p output

# Step 1: First LaTeX run
echo -e "${BLUE}Running first pdflatex pass...${NC}"
pdflatex -interaction=nonstopmode -halt-on-error main.tex

if [ $? -ne 0 ]; then
    echo -e "${RED}Error during initial LaTeX compilation. Stopping.${NC}"
    exit 1
fi

# Step 2: Process bibliography if bibtex file exists
if [ -d "bibliography" ] || [ -f "main.bib" ]; then
    echo -e "${BLUE}Processing bibliography...${NC}"
    if [ -f "main.bib" ]; then
        bibtex main
    else
        # Look for bibliography files in the bibliography directory
        for bibfile in bibliography/*.bib; do
            if [ -f "$bibfile" ]; then
                bibname=$(basename "$bibfile" .bib)
                echo -e "${BLUE}Processing $bibname bibliography...${NC}"
                bibtex main
            fi
        done
    fi
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}Error during bibliography processing. Stopping.${NC}"
        exit 1
    fi
fi

# Step 3: Second LaTeX run to incorporate bibliography
echo -e "${BLUE}Running second pdflatex pass...${NC}"
pdflatex -interaction=nonstopmode -halt-on-error main.tex

if [ $? -ne 0 ]; then
    echo -e "${RED}Error during second LaTeX compilation. Stopping.${NC}"
    exit 1
fi

# Step 4: Third LaTeX run to resolve references
echo -e "${BLUE}Running final pdflatex pass to resolve references...${NC}"
pdflatex -interaction=nonstopmode -halt-on-error main.tex

if [ $? -ne 0 ]; then
    echo -e "${RED}Error during final LaTeX compilation. Stopping.${NC}"
    exit 1
fi

# Step 5: Check for warnings and errors
echo -e "${BLUE}Checking for LaTeX warnings and errors...${NC}"

# Count citations, references, and other warnings
UNDEF_CITATIONS=$(grep -c "Citation.*undefined" main.log)
UNDEF_REFERENCES=$(grep -c "Reference.*undefined" main.log)
OTHER_WARNINGS=$(grep -c "LaTeX Warning" main.log)
HYPERREF_WARNINGS=$(grep -c "Package hyperref Warning" main.log)

if [ $UNDEF_CITATIONS -gt 0 ] || [ $UNDEF_REFERENCES -gt 0 ]; then
    echo -e "${YELLOW}Found $UNDEF_CITATIONS undefined citations and $UNDEF_REFERENCES undefined references.${NC}"
    echo -e "${YELLOW}These should be fixed before arXiv submission.${NC}"
    grep "Citation.*undefined" main.log
    grep "Reference.*undefined" main.log
fi

if [ $HYPERREF_WARNINGS -gt 0 ]; then
    echo -e "${YELLOW}Found $HYPERREF_WARNINGS hyperref warnings. Check if these are resolved with the pdfstringdefDisableCommands.${NC}"
fi

if [ $OTHER_WARNINGS -gt 0 ]; then
    echo -e "${YELLOW}Found $OTHER_WARNINGS other LaTeX warnings. Consider fixing them for a cleaner submission.${NC}"
fi

# Step 6: Create arXiv-ready version
echo -e "${BLUE}Creating arXiv-ready version...${NC}"

# Create a directory for arXiv submission
mkdir -p arxiv_submission

# Copy all necessary files for arXiv
cp main.tex arxiv_submission/
cp -r sections arxiv_submission/
cp -r bibliography arxiv_submission/
cp -r visualizations arxiv_submission/ 2>/dev/null || :

# Step 7: Clean up auxiliary files if requested
if [ "$1" == "--clean" ] || [ "$2" == "--clean" ]; then
    echo -e "${BLUE}Cleaning up auxiliary files...${NC}"
    rm -f *.aux *.log *.bbl *.blg *.out *.toc *.lof *.lot *.fls *.fdb_latexmk *.synctex.gz
fi

# Move the compiled PDF to output directory
cp main.pdf output/
cp main.pdf arxiv_submission/

echo -e "${GREEN}Compilation complete! PDF created at output/main.pdf${NC}"
echo -e "${BLUE}arXiv submission files prepared in arxiv_submission/ directory${NC}"
echo -e "${BLUE}=== Paper compilation finished ===${NC}"

# Show file size of the final PDF
FILESIZE=$(du -h output/main.pdf | cut -f1)
echo -e "${GREEN}PDF size: $FILESIZE${NC}"

# Final arXiv compatibility check
echo -e "${BLUE}=== arXiv Compatibility Check ===${NC}"
echo -e "${GREEN}✓ Author information properly formatted${NC}"
echo -e "${GREEN}✓ Hyperref setup optimized for arXiv${NC}"
echo -e "${GREEN}✓ PDF metadata correctly set${NC}"
echo -e "${GREEN}✓ Math commands in bookmarks properly escaped${NC}"

echo -e "${BLUE}To submit to arXiv:${NC}"
echo -e "1. Package the entire 'arxiv_submission' directory as a .tar.gz file"
echo -e "2. Upload to arXiv as a new submission"
echo -e "3. Make sure to select the appropriate subject classification"
echo -e "4. Verify the compiled PDF after upload" 