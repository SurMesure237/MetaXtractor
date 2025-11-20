# Optical STEM detection for scanning electron microscopy
Arent J. Kievits, 13-07-2023

This repository contains the code for analysis of the experimental data from the publication titled 'Optical STEM detection for scanning electron microscopy'. The results of the publication can be verified and visualized using Jupyter Notebooks. 
The data can be found in the 4TU.Research repository: [10.4121/9c98aee1-608e-4c71-8b89-dcb1e8eb3e5e](https://doi.org/10.4121/9c98aee1-608e-4c71-8b89-dcb1e8eb3e5e)

### Installation

It is recommended (and currently only supported) to install this repository with `conda` (https://docs.conda.io/en/latest/miniconda.html) via the command line. Install `miniconda` first and then open the terminal. In Windows, search for `anaconda prompt` in the search bar and in Mac OS search for `terminal` in the finder. Enter the following commands in the terminal:

* Install `git` with `conda` to be able to clone the GitHub repository
```bash
conda install git
```

* Clone GitHub repository into suitable directory
```bash
git clone https://github.com/arentkievits/Kievits-OSTEM-2023
```

* Create and activate new `conda` environment called `ostem`
```bash
conda env create --file=environment.yml
conda activate ostem
```

* Install package from GitHub
```bash
pip install git+git://github.com/arentkievits/Kievits-OSTEM-2023
```

### Use

To start the environment, use the command line to get to the `git` folder and type `jupyter lab` or search `jupyter notebook` via the Windows/Mac programs tab and go to the respective repository location. The notebook can be executed at once by hitting the `play` button or by selecting `Run` > 'Run All Cells'. 

### /data
Directory that contains the experimental data. Replace with data from Repository.

* `1_Optimization-OSTEM` -- OSTEM images acquired at different landing energies (LEs), to find the optimal landing energy (Figure 2). 5 images per landing energy.

| LE (keV) | Dwell (ns) | Pixel size (nm/px) |
|:--------:|:----------:|:------------------:|
| 2.5<br>3.0<br>3.5<br>4.0<br>4.5<br>5.0<br>5.5<br>6.0<br>6.5<br>7.0<br>7.5<br>8.0| 0<br>100<br>200<br>500<br>1000<br>1500<br>2000<br>3000 | 1 |

* `2_Qualitative-comparison` -- Backscattered electron images (BSD) and optical scanning transmission electron microscopy images of rat pancreas and zebrafish larval tissue.

| LE (keV) | Dwell (ns) | Pixel size (nm/px) |
|:--------:|:----------:|:------------------:|
| 1.5<br>2.0<br>4.0| 5000<br>10000 | 4 |

* `3_SNR-comparison-detectors` -- Backscattered electron images acquired with the CBS detector (BSD), Secondary electron images acquired with the through-the-lens or Everhart-Thornley detector (SE), backscatter electron images acquired with stage bias (BSE-SB) and optical scanning transmission electron microscopy images acquired with the photon detector (OSTEM). 5 images per setting. Both field-free (HR) and immersion modes (UHR).

| Detection mode | LE (keV) | Dwell (ns) | Pixel size (nm/px) |
|:--------------:|:--------:|:----------:|:------------------:|
| BSD<br>BSD-SB<br>SE<br>OSTEM<br>ADF-STEM | 1.5 (BSD, BSD-SB, SE)<br>4 (OSTEM)<br>25 (ADF-STEM)| 100<br>200<br>300<br>500<br>1000<br>3000<br>5000<br>10000 | 1 |

* `4_Image-resolution-detectors` -- Backscattered electron images acquired with the CBS detector (BSD), Secondary electron images acquired with the through-the-lens detector (SE) and optical scanning transmission electron microscopy images acquired with the photon detector (OSTEM). Immersion mode (UHR).

| Detection mode | LE (keV) | Dwell (ns) | Pixel size (nm/px) |
|:--------------:|:-------:|:----------:|:------------------:|
| BSD<br>SE<br>OSTEM<br>ADF-STEM | 1.5<br>4 (BSD, SE)<br>4 (OSTEM)<br>25 (ADF-STEM) | 10000<br>20000 (BSD, SE, OSTEM)<br>3000 (ADF-STEM) | 0.5 (BSD, SE, OSTEM)<br>0.2 (ADF-STEM) |

* `5_Current-SNR-relation` -- Optical scanning transmission electron microscopy images acquired with increasing dwell times and increasing currents

| LE (keV) | Current (nA) | Dwell (ns) | Pixel size (nm/px) |
|:--------:|:------------:|:----------:|:------------------:|
| 4 | 0.05<br>0.1<br>0.2<br>0.4<br>0.8 | 100<br>200<br>300<br>500<br>1000<br>3000<br>5000<br>10000<br> | 1 |

### /code
Contains the code used in the notebooks

### /notebooks
Contains the notebooks used to analyze the data and plot the results

* `1_Optimization-OSTEM` -- Performs the landing energy optimization by calculating the SNR and plots the SNR vs landing energy and histogram of selected images (Figure 2)
* `2_Qualitative-comparison` -- Visualizes backscattered electron images (BSD) and optical scanning transmission electron microscopy images of the same biological tissues (Figure 3). 
* `3_SNR-comparison-detectors` -- Computes SNR for all detection methods and plots comparison (Figure 4, Figure S3).
* `4_Image-resolution-detectors` -- Computes histogram of edgewidths from FEI Image (Figure 5).
* `5_Current-SNR-relation` -- Computes SNR for all images and plots SNR vs dwell time and beam current (Figure 6).
* `A1_SSNR_streaking_analysis.ipynb` -- Computes SNR with and without streaking effect and shows streaking effect in Fourier Transform (Figure S1 and S2).
