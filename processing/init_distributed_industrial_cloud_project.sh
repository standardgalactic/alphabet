#!/usr/bin/env bash
set -e

PROJECT="distributed-industrial-cloud"

echo "Creating project structure..."

mkdir -p "$PROJECT"/{frontmatter,chapters,appendices,figures}

cd "$PROJECT"

############################################
# PREAMBLE
############################################

cat > preamble.tex <<'EOF'
\usepackage{fontspec}

\setmainfont{TeX Gyre Pagella}
\setsansfont{TeX Gyre Heros}
\setmonofont{TeX Gyre Cursor}

\usepackage{geometry}
\geometry{margin=1in, headheight=15pt}

\usepackage{microtype}
\usepackage{setspace}
\onehalfspacing

\usepackage{csquotes}
\usepackage{epigraph}

\usepackage{mathtools}
\usepackage{amssymb}
\usepackage{bm}

\usepackage{graphicx}

\usepackage{tikz}
\usetikzlibrary{arrows.meta, positioning, calc, shapes.geometric, fit}

\usepackage{booktabs}
\usepackage{longtable}
\usepackage{siunitx}

\usepackage[
backend=biber,
style=authoryear,
sorting=nyt,
doi=false,
url=false,
isbn=false
]{biblatex}

\addbibresource{cloud-references.bib}

\usepackage{hyperref}

\usepackage{titlesec}

\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[LE,RO]{\thepage}
\fancyhead[RE]{\small\textit{\leftmark}}
\fancyhead[LO]{\small\textit{\rightmark}}

\usepackage{makeidx}
\makeindex

\usepackage{amsthm}

\newtheorem{theorem}{Theorem}[chapter]
\newtheorem{proposition}[theorem]{Proposition}
\newtheorem{definition}[theorem]{Definition}
EOF

############################################
# MAIN DOCUMENT
############################################

cat > main.tex <<'EOF'
\documentclass[12pt]{book}

\input{preamble.tex}

\title{Toward a Distributed Industrial Cloud}
\author{Flyxion}
\date{\today}

\begin{document}

\frontmatter

\maketitle
\tableofcontents

\input{frontmatter/preface}

\mainmatter

\part{Centralized Infrastructure}

\include{chapters/01_political_economy}
\include{chapters/02_enshittification}
\include{chapters/03_material_foundations}

\part{Distributed Systems Foundations}

\include{chapters/04_p2p_architectures}
\include{chapters/05_edge_computing}
\include{chapters/06_material_friction}
\include{chapters/07_reconstruction}


\part{Bootstrapping the Network}

\include{chapters/10_paper_recycling}
\include{chapters/11_scanning_storage}
\include{chapters/12_compute_nodes}
\include{chapters/13_fermentation}

\part{Data and Optimization}

\include{chapters/14_sensor_networks}
\include{chapters/15_data_infrastructure}

\part{Governance}

\include{chapters/16_cooperatives}
\include{chapters/17_protocol_governance}

\part{Long Term Evolution}

\include{chapters/18_hardware_innovation}
\include{chapters/19_industrial_internet}

\part{Industrial Cloud Architecture}

\include{chapters/20_system_architecture}
\include{chapters/21_energy_flows}
\include{chapters/22_network_protocol}

\part{Scaling and Simulation}

\include{chapters/23_scaling_analysis}
\include{chapters/24_simulation_models}
\include{chapters/25_conclusion}


\appendix

\include{appendices/storage_protocols}
\include{appendices/thermal_engineering}
\include{appendices/regulation}
\include{appendices/node_designs}
\include{appendices/math_models}

\backmatter

\printbibliography[heading=bibintoc]

\printindex

\end{document}
EOF

############################################
# PREFACE
############################################

cat > frontmatter/preface.tex <<'EOF'
\chapter*{Preface}
\addcontentsline{toc}{chapter}{Preface}

This monograph explores the possibility of a distributed industrial
cloud in which computation, storage, and material production are
coordinated through decentralized networks. The project integrates
ideas from distributed systems, industrial ecology, cooperative
economics, and edge computing.
EOF

############################################
# CHAPTER PLACEHOLDERS
############################################

chapters=(
01_political_economy
02_enshittification
03_material_foundations
04_p2p_architectures
05_edge_computing
06_material_friction
07_reconstruction
10_paper_recycling
11_scanning_storage
12_compute_nodes
13_fermentation
14_sensor_networks
15_data_infrastructure
16_cooperatives
17_protocol_governance
18_hardware_innovation
19_industrial_internet
20_conclusion
21_system_architecture
22_energy_flows
23_network_protocol
24_scaling_analysis
25_simulation_models
)

for c in "${chapters[@]}"; do
cat > "chapters/$c.tex" <<EOF
\\chapter{${c//_/ }}

This chapter will be developed in the full monograph.
EOF
done

############################################
# APPENDIX PLACEHOLDERS
############################################

appendices=(
storage_protocols
thermal_engineering
regulation
node_designs
math_models
)

for a in "${appendices[@]}"; do
cat > "appendices/$a.tex" <<EOF
\\chapter{${a//_/ }}

Appendix placeholder.
EOF
done

############################################
# SAMPLE FIGURE
############################################

cat > figures/bootstrap_graph.tex <<'EOF'
\begin{tikzpicture}
\node (paper) [draw,rectangle] {Paper Recycling};
\node (scan) [draw,rectangle,right=3cm of paper] {Scanning};
\node (compute) [draw,rectangle,right=3cm of scan] {Compute};
\draw[->] (paper) -- (scan);
\draw[->] (scan) -- (compute);
\end{tikzpicture}
EOF

############################################
# BIBLIOGRAPHY FILE
############################################

cat > cloud-references.bib <<'EOF'
@book{Ostrom1990,
  author={Ostrom, Elinor},
  title={Governing the Commons},
  year={1990},
  publisher={Cambridge University Press}
}
EOF

echo "Project created."
echo ""
echo "Compile with:"
echo "  xelatex main"
echo "  biber main"
echo "  xelatex main"
echo "  xelatex main"
