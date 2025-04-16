#!/bin/bash

# prepare_arxiv.sh - Prepare a submission package for arXiv
# By Brandon Barclay

# Set colors for terminal output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Preparing arXiv Submission Package ===${NC}"

# First run the compile script to ensure everything is up-to-date
echo -e "${BLUE}Running compilation...${NC}"
./compile.sh

# Create arxiv directory structure if it doesn't exist
mkdir -p arxiv_submission

# 1. Clean the directory to ensure we only include necessary files
echo -e "${BLUE}Cleaning arXiv directory...${NC}"
rm -rf arxiv_submission/*

# 2. Copy main files
echo -e "${BLUE}Copying main files...${NC}"
cp main.tex arxiv_submission/
cp -r sections arxiv_submission/
cp -r bibliography arxiv_submission/

# 3. Copy figures and other resources
echo -e "${BLUE}Copying figures and resources...${NC}"
if [ -d "visualizations" ]; then
    cp -r visualizations arxiv_submission/
fi

# 4. Copy the compiled PDF for reference
echo -e "${BLUE}Copying compiled PDF...${NC}"
cp main.pdf arxiv_submission/

# 5. Copy README for arXiv
echo -e "${BLUE}Adding arXiv README...${NC}"
cp arxiv_README.txt arxiv_submission/00README.XXX

# 6. Make sure files are properly named (arXiv conventions)
echo -e "${BLUE}Applying arXiv naming conventions...${NC}"
cd arxiv_submission
# Rename main.tex to binary_padic_theory.tex if desired
# mv main.tex binary_padic_theory.tex
cd ..

# 7. Create the tarball
echo -e "${BLUE}Creating submission tarball...${NC}"
TIMESTAMP=$(date +"%Y%m%d")
TARBALL="binary_padic_theory_arxiv_${TIMESTAMP}.tar.gz"
tar -czf "$TARBALL" -C arxiv_submission .

echo -e "${GREEN}arXiv submission package created: $TARBALL${NC}"
echo -e "${GREEN}Size: $(du -h "$TARBALL" | cut -f1)${NC}"

# 8. Final instructions
echo -e "${BLUE}=== arXiv Submission Instructions ===${NC}"
echo -e "1. Go to https://arxiv.org/submit"
echo -e "2. Upload the tarball: $TARBALL"
echo -e "3. Select primary category: Mathematics > Algebraic Geometry (math.AG)"
echo -e "4. Select additional categories as appropriate:"
echo -e "   - Commutative Algebra (math.AC)"
echo -e "   - Number Theory (math.NT)"
echo -e "5. Add the abstract from your paper"
echo -e "6. Review the compiled PDF after upload to verify formatting"
echo -e "${GREEN}Good luck with your submission!${NC}"
