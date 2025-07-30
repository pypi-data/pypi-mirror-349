# SpaTranslator
![alt text](Model_Overview.pdf)

**SpaTranslator** is a graph-based generative model for cross-modality prediction in spatial omics data. It enables the in silico generation of missing omics modalities—such as spatial ATAC-seq, RNA-seq, and histone modification profiles—across paired or unpaired tissue sections, by leveraging spatial neighborhood information and adversarial learning.
---

## 🧠 Highlights

- 🔄 **Cross-modality generation** between spatial transcriptomics and epigenomics/proteomics
- 📈 **Superior performance** on 12 benchmark datasets over state-of-the-art methods (multiDGD, JAMIE, scButterfly, scPair)
- 🧬 Supports multiple data types: RNA, ATAC, histone marks (H3K27me3, H3K4me3), protein
- 📍 **Graph Neural Network** integration for spatial structure modeling
- 🧪 Flexible in intra- and inter-dataset prediction tasks

---

## 📂 Datasets

SpaTranslator is benchmarked on:
- **Spatial-ATAC-RNA-seq** (mouse brain)
- **MISAR-seq** (mouse brain at stages E11, E13, E15, E18)
- **10x Visium RNA-Protein** (human tonsil&lymph node)

> Detailed documentation is written in the jupyter notebook
---

## 🚀 Installation Guide

**Install with pip**  
```bash
conda create -n SpaTranslator python==3.10
pip install spatranslator
```
---

## 📄 License

SpaTranslator is released under the [MIT License](LICENSE).  
You are free to use, modify, and distribute this software for academic and non-commercial purposes with proper attribution.

---

## 📬 Contact

If you have questions, feature requests, or would like to contribute:

- 💡 **Issues**: Please submit via the [GitHub Issues Page](https://github.com/ChrisMao0325/SpaTranslator/issues)
- ✉️ **Email**: `maosheng@westlake.edu.cn`/`donghongyu@westlake.edu.cn` 

