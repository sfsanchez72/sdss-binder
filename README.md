# SDSS BinderHub

A Binder is just like running Jupyter notebook on a remote server.

The Flatiron Institute has two Binder servers that host SDSS data:

- Popeye: https://sdsc-binder.flatironinstitute.org/~acasey/sdss
- Rusty: https://sdsc-binder.flatironinstitute.org/~acasey/sdss

## Getting Started 

See `notebooks/introduction.ipynb`

## Which Binder server should I use?

You should try [popeye](https://sdsc-binder.flatironinstitute.org/~acasey/sdss) first. If it has all the data products you need, then stick with popeye. If it doesn't have all the data you need, then use [rusty](https://binder.flatironinstitute.org/~acasey/sdss). Here is a summary of some of the differences: 


| | Rusty | Popeye |
|---|---|---|
| **Data completeness** | More complete — includes raw data and intermediate products | Less complete — most recent final data products only |
| **Compute** | Standard | More compute available |
| **Demand** | Busier; higher chance of collisions (your server may not spawn if resources are saturated) | Less heavily used |
| **Best for** | Work requiring raw or intermediate data products | Work requiring more compute with fewer interruptions |

# Contributing

Any changes to the following on the `main` branch:

- `requirements.txt`
- `notebooks/`
- or the `users` list in `.public_binder`

will be automatically propagated to both the rusty and popeye instances within five minutes.

