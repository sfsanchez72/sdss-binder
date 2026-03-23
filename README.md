# SDSS ❤️ BinderHub

BinderHub is like running Jupyter notebook on a remote server.

The Flatiron Institute has two BinderHubs that host SDSS data:

- [Popeye](https://sdsc-binder.flatironinstitute.org/~acasey/sdss) in San Diego
- [Rusty](https://binder.flatironinstitute.org/~acasey/sdss) in New York

## Access

**Note, these instructions changed on 2026-03-11. You will need to specify a Gmail.com account as your Flatiron Institute Binder.**

To access BinderHub:
1. Log in to the [SDSS Internal Collaboration Database](https://soji.sdss.utah.edu/collaboration/people/accounts/user) and add a Gmail domain to your profile (e.g., me@gmail.com).
2. Set the _Flatiron Institute Binder_ email address as to your Gmail address, and save your profile.

<p align="center">
  <img src="https://github.com/user-attachments/assets/ddfe47f2-8d8c-437f-a918-b224d3349c5d" width="70%">
</p>

You will be able to log in to both BinderHubs within 5-10 minutes. If you don't have a Gmail address, or you prefer to use your institution-based email address that Google manages, please [open an issue](https://github.com/andycasey/sdss-binder/issues/new).

## Which Binder server should I use?

You should try [Popeye](https://sdsc-binder.flatironinstitute.org/~acasey/sdss) first. If it has all the data products you need, then stick with Popeye. If it doesn't have all the data you need, then use [Rusty](https://binder.flatironinstitute.org/~acasey/sdss).

Here is a summary of the key differences:

**Data availability**

| | Popeye | Rusty |
|---|---|---|
| **Overall** | Most recent final data products only | More complete — includes raw data and intermediate products |
| DR17 | None | Complete |
| DR19 | Astra summary files; `mwmVisit` and `mwmStar` files | Complete |
| DR20 | Astra summary files; spectrum block files | Complete |
| MWM/ApogeeReduction.jl | 0.2.0 only | Complete |
| LVM/DRP | 1.2.0 `lvmSFrame` files | 1.2.0 `lvmSFrame` files |

**Server characteristics**

| | Popeye | Rusty |
|---|---|---|
| **Compute** | More compute available | Standard |
| **Demand** | Less heavily used | Busier; higher chance of collisions (your server may not spawn if resources are saturated) |
| **Best for** | Work requiring more compute with fewer interruptions | Work requiring raw or intermediate data products |

There is some flexibility about what is mirrored at Popeye, and expansion is possible. Tell Andy what products you need!

# Notebooks
## General
| Launch | Notebook |
|---|---|
| [![](https://img.shields.io/badge/launch-Jupyter-F37626?logo=jupyter&logoColor=white)](https://sdsc-binder.flatironinstitute.org/~acasey/sdss?urlpath=lab/tree/notebooks/introduction.ipynb) | **Getting Started**: A welcome guide covering access, data, storage, compute, and how to use BinderHub, by _Andy Casey_ |

## Milky Way Mapper (MWM)
| Launch | Notebook |
|---|---|
| [![](https://img.shields.io/badge/launch-marimo-6925d3?logo=marimo&logoColor=white)](https://sdsc-binder.flatironinstitute.org/~acasey/sdss?urlpath=marimo/edit/notebooks/marimo/mwm_boss_explorer.py) | **BOSS Explorer**: Interactive explorer for MWM DR20 BOSS spectra — look up sources, view spectra, and export subsets, by _Kayvon Sharifi_ |
| [![](https://img.shields.io/badge/launch-marimo-6925d3?logo=marimo&logoColor=white)](https://sdsc-binder.flatironinstitute.org/~acasey/sdss?urlpath=marimo/edit/notebooks/marimo/mwm_boss_clusters.py) | **BOSS Star Cluster Explorer**: Interactive explorer for MWM DR20 BOSS spectra of stars in clusters and moving groups — filter by stellar association, view and export spectra by _Kayvon Sharifi_ |
| [![](https://img.shields.io/badge/launch-Jupyter-F37626?logo=jupyter&logoColor=white)](https://sdsc-binder.flatironinstitute.org/~acasey/sdss?urlpath=lab/tree/notebooks/mwm/ApogeeReduction-jl-demo.ipynb) | **APOGEE Demo**: Demonstration of working with ApogeeReduction.jl data products (exposures, radial velocities, spectra), by _Kevin McKinnon_ |
| [![](https://img.shields.io/badge/launch-marimo-6925d3?logo=marimo&logoColor=white)](https://sdsc-binder.flatironinstitute.org/~acasey/sdss?urlpath=marimo/edit/notebooks/marimo/mwm_explorer.py) | **APOGEE Explorer**: Interactive explorer for APOGEE spectra from ApogeeReduction.jl — search sources by SDSS ID, view source information, radial velocity plots with phase folding, and interactive spectrum visualization, by _Andy Casey_ |
| [![](https://img.shields.io/badge/launch-marimo-6925d3?logo=marimo&logoColor=white)](https://sdsc-binder.flatironinstitute.org/~acasey/sdss?urlpath=marimo/edit/notebooks/marimo/mwm_carton_filter.py) | **APOGEE Exposure Filter**: Create subsets of ApogeeReduction.jl-reduced spectra based on SDSS-V targeting flags (cartons and programs), and export the filtered data, by _Andy Casey_ |
| [![](https://img.shields.io/badge/launch-marimo-6925d3?logo=marimo&logoColor=white)](https://sdsc-binder.flatironinstitute.org/~acasey/sdss?urlpath=marimo/edit/notebooks/marimo/mwm_white_dwarfs.py) | **White Dwarf Spectrum Fitter**: JAX-based DA-type white dwarf spectrum fitter with bicubic grid interpolation, Levenberg-Marquardt optimization, and Hessian-based uncertainties, by _Andy Casey_ |

## Local Volume Mapper (LVM)

See the [LVM notebooks README](notebooks/lvm/README.md) for more detailed descriptions of each notebook.

| Launch | Notebook |
|---|---|
| [![](https://img.shields.io/badge/launch-Jupyter-F37626?logo=jupyter&logoColor=white)](https://sdsc-binder.flatironinstitute.org/~acasey/sdss?urlpath=lab/tree/notebooks/lvm/hilder-demo.ipynb) | **Getting Started**: Getting started with LVM data — reading and plotting calibrated, sky-subtracted spectra from `lvmSFrame` files, by _Thomas Hilder_ |

### `spectracles` (spectrospatial modelling)

#### Single emission line tutorial
| Launch | Notebook |
|---|---|
| [![](https://img.shields.io/badge/launch-Jupyter-F37626?logo=jupyter&logoColor=white)](https://sdsc-binder.flatironinstitute.org/~acasey/sdss?urlpath=lab/tree/notebooks/lvm/spectracles_single_line/1_fit_model.ipynb) | **Fit Model**: Fit a spectrospatial model to a single emission line in LVM data, by _Thomas Hilder_ |
| [![](https://img.shields.io/badge/launch-Jupyter-F37626?logo=jupyter&logoColor=white)](https://sdsc-binder.flatironinstitute.org/~acasey/sdss?urlpath=lab/tree/notebooks/lvm/spectracles_single_line/2_plot_results.ipynb) | **Plot Results**: Visualise the results of the single emission line fit, by _Thomas Hilder_ |

#### W28
| Launch | Notebook |
|---|---|
| [![](https://img.shields.io/badge/launch-Jupyter-F37626?logo=jupyter&logoColor=white)](https://sdsc-binder.flatironinstitute.org/~acasey/sdss?urlpath=lab/tree/notebooks/lvm/spectracles_W28/1_nii.ipynb) | **W28: [N II]**: Spatial-kinematic decomposition of [N II] λ6583 in W28 using spectrospatial models, by _Thomas Hilder_ |
| [![](https://img.shields.io/badge/launch-Jupyter-F37626?logo=jupyter&logoColor=white)](https://sdsc-binder.flatironinstitute.org/~acasey/sdss?urlpath=lab/tree/notebooks/lvm/spectracles_W28/2_ha.ipynb) | **W28: Hα**: Spatial-kinematic decomposition of Hα in W28 with star masking from [N II] fits, by _Thomas Hilder_ |
| [![](https://img.shields.io/badge/launch-Jupyter-F37626?logo=jupyter&logoColor=white)](https://sdsc-binder.flatironinstitute.org/~acasey/sdss?urlpath=lab/tree/notebooks/lvm/spectracles_W28/3_oiii.ipynb) | **W28: [O III]**: Spatial-kinematic decomposition of [O III] λ5007 in W28, by _Thomas Hilder_ |
| [![](https://img.shields.io/badge/launch-Jupyter-F37626?logo=jupyter&logoColor=white)](https://sdsc-binder.flatironinstitute.org/~acasey/sdss?urlpath=lab/tree/notebooks/lvm/spectracles_W28/4_sii.ipynb) | **W28: [S II]**: Spatial-kinematic decomposition of [S II] λ6716 in W28, by _Thomas Hilder_ |

# Storage

BinderHub lets you drag-and-drop to upload or download files. It's very handy. However, **there is no persistent storage**.

You should only ever save things to your `home/` directory. If you save things anywhere else, **it will be deleted when your notebook server finishes**. Please try to keep things stored in your `home/` directory to be less than 1 TB.

Do not store any sensitive or critical data on this service. Anything you put in your <code>home/</code> directory may be made available to Flatiron Institute researchers for the purpose of collaboration. All storage and resources should be considered best-effort scratch space and come with no guarantees or backups. Your entire account, including files in your <code>home/</code> directory will be removed after 7 days of inactivity.

# Contributing

Please add any notebooks that you think might help the collaboration to do science! You can open a pull request to the `main` branch of this repository. Once it is merged, your notebooks will be propagated to both the Rusty and Popeye clusters within five minutes, so other people will be able to use your notebooks.

Similarly, any changes to the following on the `main` branch:

- `requirements.txt`
- `notebooks/`
- or the `users` list in `.public_binder`

will be automatically propagated to both the Rusty and Popeye instances within five minutes.

# Automation

One computer has a cron job every five minutes to sync the ICDB:
```
*/5 * * * * cd <path_to_binder_hub> && bash sync_icdb.sh > icdb.log
```

If the Flatiron BinderHub email addresses in the ICDB have changed then they will be committed to the `.public_binder` file on the `main` branch. When that is pushed, GitHub Actions will sync all notebooks, access lists, and Python requirements to the `rusty` and `popeye` branches. Rusty and Popeye then have a cron job that runs every five minutes just to sync their branch from GitHub.
```
*/5 * * * * cd <path_to_binder_hub> && git pull
```

That means any change to the ICDB will be propagated to both BinderHubs within ten minutes. 
