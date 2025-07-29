# MVKM-ED: Rectified Gaussian Kernel Multi-View K-Means Clustering

## Overview
MVKM-ED is a Python implementation of the Rectified Gaussian Kernel Multi-View K-Means Clustering algorithm. This algorithm effectively handles multiple views of data while automatically learning view importance weights.

## Features
- Privacy-preserving multi-view clustering
- Adaptive view weight learning
- Rectified Gaussian kernel for distance computation
- Automatic parameter adaptation
- Efficient implementation with NumPy

## Requirements
- Python 3.7+
- NumPy >= 1.19.0
- SciPy >= 1.6.0
- scikit-learn >= 0.24.0

## Installation
```bash
pip install mvkm-ed
```

## Usage
```python
import numpy as np
from mvkm_ed import MVKMED, MVKMEDParams

# Create sample data
X1 = np.random.randn(100, 10)  # First view
X2 = np.random.randn(100, 15)  # Second view
X = [X1, X2]

# Set parameters
params = MVKMEDParams(
    cluster_num=3,
    points_view=2,
    alpha=2.0,
    beta=0.1,
    max_iterations=100,
    convergence_threshold=1e-4
)

# Create and fit model
model = MVKMED(params)
model.fit(X)

# Get cluster assignments
cluster_labels = model.index
```

## Parameters
- `cluster_num`: Number of clusters
- `points_view`: Number of data views
- `alpha`: Exponent parameter to control view weights
- `beta`: Distance control parameter
- `max_iterations`: Maximum number of iterations
- `convergence_threshold`: Convergence criterion threshold

## Citation
If you use this code in your research, please cite:
```bibtex
@article{sinaga2024rectified,
  title={Rectified Gaussian Kernel Multi-View K-Means Clustering},
  author={Sinaga, Kristina P. and others},
  journal={arXiv},
  year={2024}
}
```

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contact
- Kristina P. Sinaga
- Email: kristinasinaga41@gmail.com

## Acknowledgments
This work was supported by the National Science and Technology Council, 
Taiwan (Grant Number: NSTC 112-2118-M-033-004)
