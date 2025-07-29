<div style="position: relative; text-align: center;">
  <img src="./auxiliary/LightPollutionSimulation.jpg" style="width:100%; height: auto;">
</div>

# lightPollutionSimulation

lightPollutionSimulation - a project to simulate the night sky brightness from a given point based on the VIIRS data. 

## Pre-requisites
> [!IMPORTANT]  
> The project is written in Python 3.12
> Requirements can be found in `./auxiliary/install_libraries.bat` 

### Map download
The tiff image file containing the VIIRS light irradiance data can be downloaded from the original source: [VIIRS 2023 Raw Data](https://www2.lightpollutionmap.info/data/viirs_2023_raw.zip)

The image should be placed in the folder `./maps/viirs_2023_raw_global.tif`

## Usage
The project can be started by running the `lightPollutionSimulation.py` file located in the `./src` directory.

For a detailed overview of the parameters, run the script with the `-h` parameter.
> [!WARNING]  
> All files must be executed from the root directory of `./lightPollutionSimulation`.
> Otherwise, relative paths may not work as intended.

It is generally advised to use the lightPollutionSimulation with a radius >= 50km and an atmosphere height >= 10km for accurate results. 

## Verification of the simulation results
The complete material covering the verification of the simulation results can be found on our google drive share: [Simulation Results and Sanity Checks](https://drive.google.com/drive/folders/1gn7bZB79wUijw7wcFKBdocx5a3S5DhCD?usp=sharing)
