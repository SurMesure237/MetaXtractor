![Java](https://img.shields.io/badge/java-%23ED8B00.svg?style=plastic&logo=openjdk&logoColor=white) ![GitHub](https://img.shields.io/github/license/Ramy-Badr-Ahmed/bendingStiffness?style=plastic)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.12808969.svg)](https://doi.org/10.5281/zenodo.12808969) [![SWH](https://archive.softwareheritage.org/badge/swh:1:dir:65f4716d51672926f9ae328ea314d969e37534c6/)](https://archive.softwareheritage.org/swh:1:dir:65f4716d51672926f9ae328ea314d969e37534c6;origin=https://github.com/Ramy-Badr-Ahmed/bendingStiffness;visit=swh:1:snp:cf3a5710e567c74b08a7144be79796fb78e9743c;anchor=swh:1:rev:ae6455bbac2db3f8838eb0d69b5ba09e5f50d06e) 

### Summary

A java code analysing the Bending Stiffness of Actin Filament Experiment.

- Reads coordinates from `snake.txt` of a measured filament (an example is in the `images` directory)
- Calculates the mean squared displacement (MSD) and contour length from data
- Error calculation in persistence length and contour length are saved in `mathematica` directory.
- (optional) Modify `config.properties` as needed.

### Running the Demo

1. Place your `snake.txt` and `elongation.txt` files in the `data` directory (an example exists).
2. Compile and run the `Snake` class.

```sh
javac -d out src/Snake.java
java -cp out Snake
