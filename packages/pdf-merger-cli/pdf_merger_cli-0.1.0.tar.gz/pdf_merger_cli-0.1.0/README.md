# 📎 pdf-merger-cli

Un semplice tool CLI per unire file PDF in Python.

## 📦 Installation

```bash
pip install pdf-merger-cli
```

## 🛠️ How to use

```bash
pdfmerge file1.pdf file2.pdf -o output.pdf
```

Even entire directories:

```bash
pdfmerge ./documenti/ -o merged.pdf
```

With manual ordering:

```bash
pdfmerge 3.pdf 1.pdf 2.pdf -o merged.pdf --ordered
```

🧪 Unit Tests

```bash
pip install .
pdfmerge ...
```

## 🐍 Requirements

* Python ≥ 3.7