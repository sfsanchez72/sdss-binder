# SDSS :heart: BinderHub

A Binder is just like running Jupyter notebook on a remote server.

The Flatiron Institute has two Binder servers that host SDSS data:

- [Popeye](https://sdsc-binder.flatironinstitute.org/~acasey/sdss) in San Diego
- [Rusty](https://binder.flatironinstitute.org/~acasey/sdss) in New York

## Access

**As of Feb 2026:**

Ask Andy Casey to make sure you have access. He will need your google-based email address.

**As of ~April 2026 (expected):**

Popeye and Rusty both use Google authentication. If you are an approved SDSS-V member with data access rights, and if Google manages your institution email account, then you should be able to access BinderHub already.

If your institution does not use Google to manage email accounts, then you will need to add your personal Google email address as an affiliated email address in the [SDSS Internal Collaboration Database](https://soji.sdss.utah.edu/collaboration/home) (ICDB).

Access lists are synchronized from the ICDB and propagated to both Rusty and Popeye every five minutes.

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

# Getting Started

See `notebooks/introduction.ipynb`

## LVM + spectrospatial models

See `notebooks/lvm/README`

# Contributing

Please add any notebooks that you think might help the collaboration to do science! You can open a pull request to the `main` branch of this repository. Once it is merged, your notebooks will be propagated to both the Rusty and Popeye clusters within five minutes, so other people will be able to use your notebooks.

Similarly, any changes to the following on the `main` branch:

- `requirements.txt`
- `notebooks/`
- or the `users` list in `.public_binder`

will be automatically propagated to both the Rusty and Popeye instances within five minutes.
