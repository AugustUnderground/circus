## Installation and Setup

### Automatic Installer

A script for automatically putting up the
[circus-tent](https://github.com/electronics-and-drives/circus-tent) is
available. This will install circus with the GPDK180 environments available.
Additionally there are instructions for manual installation.

### On-Site Installation at E&D

When working at E&D, the 
[install script](https://gitlab-forschung.reutlingen-university.de/plasma/circus-installer)
**should** be used.

```bash
git clone git@gitlab-forschung.reutlingen-university.de:plasma/circus-installer.git \
    pushd ./circus-installer && ./install.sh && popd
```

### Manual Installation

See [circus-tent](https://github.com/electronics-and-drives/circus-tent).

### Machine Learning Models for `elec` Environments

The models used for `elec` envs are trained with
[precept](https://github.com/electronics-and-drives/precept) and _must_ have
the following mapping:

```
[ gmoverid    [ idoverw
, fug      ↦  , L
, Vds         , gdsoverw
, Vbs ]       , Vgs ]
```

These models (`nmos.pt` and `pmos.pt`) must be located in the corresponding PDK
sub-directory:

```
~/.circus
├── ckt
│   ├── fca.yml
│   ├── ffa.yml
│   ├── mil.yml
│   ├── rfa.yml
│   └── sym.yml
├── pdk
│   ├── gpdk180
│   │   ├── fca.scs
│   │   ├── ffa.scs
│   │   ├── mil.scs
│   │   ├── nmos.pt
│   │   ├── pmos.pt
│   │   ├── rfa.scs
│   │   └── sym.scs
│   ├── gpdk180.yml
│   ├── ...
```

These files _must_ be a
[torchscript](https://pytorch.org/tutorials/recipes/torchscript_inference.html)
module adhering to the specified input and output dimensions. The scalers

