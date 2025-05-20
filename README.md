<h1 style="display: flex; justify-content: center; align-items: center; gap: 10px; margin: 0;">
  MathIF: Instruction-Following Benchmark for Large Reasoning Models
</h1>

[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-brightgreen)]() [![CUDA 12.4](https://img.shields.io/badge/CUDA-12.4-red)]() [![License](https://img.shields.io/badge/license-MIT-blue)]()

MathIF is a dedicated benchmark for evaluating the instruction-following capabilities of large reasoning models (LRMs) on mathematical reasoning tasks. It exposes a fundamental trade-off between a model’s problem-solving strength and its ability to comply with user-specified constraints.


<div align="center" style="font-family: Arial, sans-serif; font-size: 16px;">
  <p>
    <!-- <a href="#news" style="text-decoration: none; font-weight: bold;">🎉 News</a> • -->
    <!-- <a href="#links" style="text-decoration: none; font-weight: bold;">🔗 Links</a> • -->
    <a href="#features" style="text-decoration: none; font-weight: bold;">📖 Features</a>
    <a href="#getting-started" style="text-decoration: none; font-weight: bold;">✨ Getting Started</a>
  <!-- </p>
  <p> -->
    <a href="#usage" style="text-decoration: none; font-weight: bold;">🔧 Usage</a>
    <!-- <a href="#evaluation" style="text-decoration: none; font-weight: bold;">📃 Evaluation</a> • -->
    <!-- <a href="#citation" style="text-decoration: none; font-weight: bold;">🎈 Citation</a> • -->
    <a href="#acknowledgement" style="text-decoration: none; font-weight: bold;">🌻 Acknowledgement</a>
    <a href="#contact" style="text-decoration: none; font-weight: bold;">📬 Contact</a>
    <!-- <a href="#star-history" style="text-decoration: none; font-weight: bold;">📈 Star History</a> -->
  </p>
</div>


# 📖 Features

- **Compositional Constraints**  
  15 Python-verifiable constraint types in four categories (length, lexical, format, affix), combined into single, dual, and triple constraints.

- **Diverse Math Sources**  
  Problems drawn from GSM8K, MATH-500, Minerva, Olympiad, and AIME, totaling 420 high-quality evaluation samples.

- **Fine-Grained Metrics**  
  - **Hard Accuracy (HAcc):** fraction of examples satisfying _all_ constraints  
  - **Soft Accuracy (SAcc):** average fraction of satisfied constraints per example

- **vLLM-Powered Inference**  
  Efficient decoding with nucleus sampling (T=1.0, p=0.95) and up to 16k token generation.

# ✨ Getting Started

## Prerequisites

- Python 3.9 or later  
- CUDA 12.4  
- `git`, `bash`

## Installation

```bash
git clone https://github.com/TingchenFu/MathIF.git
cd MathIF

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
````

## Downloading the Dataset

* **Manual**: Download from Hugging Face and place under `data/`
  `https://huggingface.co/datasets/TingchenFu/MathIF`

* **Or run the following script**:

  ```bash
  bash code/scripts/download.sh
  ```

# 🔧 Usage

## Inference

```bash
bash code/scripts/vllm_if.sh
```

## Evaluation

```bash
bash code/scripts/eval_if.sh
```

## Dataset Format

Each line in the JSONL file contains:

| Field             | Description                       |
| ----------------- | --------------------------------- |
| `source`          | Original data source              |
| `id`              | Unique example identifier         |
| `question`        | Math problem statement            |
| `answer`          | Ground-truth solution             |
| `constraint_desc` | Human-readable constraint summary |
| `constraint_name` | Constraint category               |
| `constraint_args` | Arguments used for verification   |

## Project Structure

```
.
├── data/                # MathIF JSONL files
├── code/
│   ├── scripts/         # Inference & evaluation scripts
│   └── ...              # Model wrappers and utilities
├── output/              # Generated predictions & logs
├── requirements.txt     # Python dependencies
└── README.md            # This overview
```

<!-- ## Citation

If you use MathIF, please cite:

```bibtex
@inproceedings{fu2025MathIF,
  title={MathIF: Instruction‐Following Benchmark for Large Reasoning Models},
  author={Fu, Tingchen and Gu, Jiawei and Li, Yafu and Qu, Xiaoye and Cheng, Yu},
  booktitle={NeurIPS},
  year={2025}
}
```

## License

Released under the MIT License. See [LICENSE](LICENSE) for details.

```
``` -->

# 🌻 Acknowledgements

MathIF is inspired by prior work on [IFEval](https://huggingface.co/datasets/google/IFEval) and [ComplexBench](https://github.com/thu-coai/ComplexBench), and leverages [vLLM](https://github.com/vllm-project/vllm) for efficient inference.

# 📬 Contact

For questions, feedback, or collaboration inquiries, please contact:  
- **Yafu Li** · yafuly@gmail.com