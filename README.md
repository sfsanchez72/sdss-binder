# SDSS :heart: BinderHub

A Binder is just like running Jupyter notebook on a remote server.

The Flatiron Institute has two Binder servers that host SDSS data:

- [Popeye](https://sdsc-binder.flatironinstitute.org/~acasey/sdss) in San Diego
- [Rusty](https://binder.flatironinstitute.org/~acasey/sdss) in New York

## Access

If you have data access rights in SDSS-V and your institution uses Google to manage email, then you already have access to BinderHub.

If your institution does not use Google to manage email, then you will need to log in to the [SDSS Internal Collaboration Database](https://soji.sdss.utah.edu/collaboration/people/accounts/user) and add a Google-based email address to your profile. Then set the _Flatiron Institute Binder_ email address as your Google-based email address. After you save your profile you will be able to log in to BinderHub within 5-10 minutes.

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

| Notebook | Description | Author |
|---|---|---|---|
|  [![](https://img.shields.io/badge/launch-Jupyter-F37626?logo=jupyter&logoColor=white)](https://sdsc-binder.flatironinstitute.org/~acasey/sdss?urlpath=lab/tree/notebooks/introduction.ipynb) **Getting Started** | Welcome guide covering access, data, storage, compute, and how to use BinderHub | Andy Casey |

## Milky Way Mapper (MWM)

| Notebook | Description | Author |
|---|---|---|---|
| BOSS Explorer | [![](https://img.shields.io/badge/launch-marimo-6925d3?logo=marimo&logoColor=white)](https://sdsc-binder.flatironinstitute.org/~acasey/sdss?urlpath=marimo/edit/notebooks/marimo/mwm_boss_explorer.py) | Interactive explorer for MWM DR20 BOSS spectra — look up sources, view spectra, and export subsets | Kayvon Sharifi |
| APOGEE Demo | [![](https://img.shields.io/badge/launch-Jupyter-F37626?logo=jupyter&logoColor=white)](https://sdsc-binder.flatironinstitute.org/~acasey/sdss?urlpath=lab/tree/notebooks/mwm/ApogeeReduction-jl-demo.ipynb) | Demonstration of working with ApogeeReduction.jl data products (exposures, radial velocities, spectra) | Kevin McKinnon |
| APOGEE Explorer | [![](https://img.shields.io/badge/launch-marimo-6925d3?logo=marimo&logoColor=white)](https://sdsc-binder.flatironinstitute.org/~acasey/sdss?urlpath=marimo/edit/notebooks/marimo/mwm_explorer.py) | Interactive explorer for APOGEE spectra from ApogeeReduction.jl — search sources by SDSS ID, view source information, radial velocity plots with phase folding, and interactive spectrum visualization | Andy Casey |
| APOGEE Exposure Filter | [![](https://img.shields.io/badge/launch-marimo-6925d3?logo=marimo&logoColor=white)](https://sdsc-binder.flatironinstitute.org/~acasey/sdss?urlpath=marimo/edit/notebooks/marimo/mwm_carton_filter.py) | Create subsets of ApogeeReduction.jl-reduced spectra based on SDSS-V targeting flags (cartons and programs), and export the filtered data | Andy Casey |
| Sky Coverage Map | [![](https://img.shields.io/badge/launch-marimo-6925d3?logo=marimo&logoColor=white)](https://sdsc-binder.flatironinstitute.org/~acasey/sdss?urlpath=marimo/edit/notebooks/marimo/sky_map.py) | Interactive all-sky Mollweide visualization of sources with APOGEE spectra — click on points to see source details | Andy Casey |


## Local Volume Mapper (LVM)

| Notebook | Launch | Description | Author |
|---|---|---|---|
| Getting Started | [![](https://img.shields.io/badge/launch-Jupyter-F37626?logo=jupyter&logoColor=white)](https://sdsc-binder.flatironinstitute.org/~acasey/sdss?urlpath=lab/tree/notebooks/lvm/hilder-demo.ipynb) | Getting started with LVM data — reading and plotting calibrated, sky-subtracted spectra from `lvmSFrame` files | Thomas Hilder |
| W28: \[N II\] | [![](https://img.shields.io/badge/launch-Jupyter-F37626?logo=jupyter&logoColor=white)](https://sdsc-binder.flatironinstitute.org/~acasey/sdss?urlpath=lab/tree/notebooks/lvm/W28/1_nii.ipynb) | Spatial-kinematic decomposition of [N II] λ6583 in W28 using spectrospatial models | Thomas Hilder |
| W28: Hα | [![](https://img.shields.io/badge/launch-Jupyter-F37626?logo=jupyter&logoColor=white)](https://sdsc-binder.flatironinstitute.org/~acasey/sdss?urlpath=lab/tree/notebooks/lvm/W28/2_ha.ipynb) | Spatial-kinematic decomposition of Hα in W28 with star masking from [N II] fits | Thomas Hilder |
| W28: \[O III\] | [![](https://img.shields.io/badge/launch-Jupyter-F37626?logo=jupyter&logoColor=white)](https://sdsc-binder.flatironinstitute.org/~acasey/sdss?urlpath=lab/tree/notebooks/lvm/W28/3_oiii.ipynb) | Spatial-kinematic decomposition of [O III] λ5007 in W28 | Thomas Hilder |
| W28: \[S II\] | [![](https://img.shields.io/badge/launch-Jupyter-F37626?logo=jupyter&logoColor=white)](https://sdsc-binder.flatironinstitute.org/~acasey/sdss?urlpath=lab/tree/notebooks/lvm/W28/4_sii.ipynb) | Spatial-kinematic decomposition of [S II] λ6716 in W28 | Thomas Hilder |

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
