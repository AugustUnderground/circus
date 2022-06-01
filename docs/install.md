## Installation and Setup

### On-Site Installation via Script

When working at E&D, the 
[install script](https://gitlab-forschung.reutlingen-university.de/plasma/circus-installer)
**should** be used.

```bash
git clone git@gitlab-forschung.reutlingen-university.de:plasma/circus-installer.git $HOME/.ace && \
    pushd $HOME/.ace && \
    ./bin/ace-install && \
    popd
```

### Manual Installation

```bash
$ pip install git+https://github.com/augustunderground/circus.git
```

Or clone and install a local copy

```bash
$ git clone https://github.com/augustunderground/gace.git
$ pip install .
```

#### Backend Setup

After installing [AC²E](https://github.com/electronics-and-drives/ace) and
[HAC²E](https://github.com/AugustUnderground/hace), including all dependencies,
a _home_ directory for `circus` must be created.

**Make sure AC²E is installed and functions properly before continuing!**

Create a symlink from the `resource` directory of the AC²E repository, which
contains all the backends as git submodules, to `~/.ace`.  `circus` will
automatically look for PDK data and transformation models there.

```bash
$ ln -s /path/to/ace/resource $HOME/.ace
```

It should look something like this:

```
$HOME/.ace
├── sky130-1V8
│   ├── LICENSE
│   ├── nand4
│   │   ├── input.scs
│   │   └── properties.json
│   ├── op1
│   │   ├── input.scs
│   │   └── properties.json
│   ├── op2
│   │   ├── input.scs
│   │   └── properties.json
│   ├── op3
│   │   ├── input.scs
│   │   └── properties.json
│   ├── op4
│   │   ├── input.scs
│   │   └── properties.json
│   ├── op5
│   │   ├── input.scs
│   │   └── properties.json
│   ├── op6
│   │   ├── input.scs
│   │   └── properties.json
│   ├── pdk
│   │   ├── cells
│   │   │   ├── nfet_01v8
│   │   │   │   ├── sky130_fd_pr__nfet_01v8__mismatch.corner.scs
│   │   │   │   ├── sky130_fd_pr__nfet_01v8__tt.corner.scs
│   │   │   │   └── sky130_fd_pr__nfet_01v8__tt.pm3.scs
│   │   │   └── pfet_01v8
│   │   │       ├── sky130_fd_pr__pfet_01v8__mismatch.corner.scs
│   │   │       ├── sky130_fd_pr__pfet_01v8__tt.corner.scs
│   │   │       └── sky130_fd_pr__pfet_01v8__tt.pm3.scs
│   │   ├── models
│   │   │   ├── all.scs
│   │   │   ├── corners
│   │   │   │   └── tt
│   │   │   │       └── nofet.scs
│   │   │   ├── parameters
│   │   │   │   └── lod.scs
│   │   │   └── sky130.scs
│   │   ├── README.md
│   │   └── tests
│   │       ├── nfet_01v8_tt.scs
│   │       └── pfet_01v8_tt.scs
│   ├── nmos -> /path/to/sky130-nmos
│   ├── pmos -> /path/to/sky130-pmos
│   ├── README.md
│   └── st1
│       ├── input.scs
│       └── properties.json
└── xh035-3V3
    ├── LICENSE
    ├── nand4
    │   ├── input.scs
    │   └── properties.json
    ├── op1
    │   ├── input.scs
    │   └── properties.json
    ├── op2
    │   ├── input.scs
    │   └── properties.json
    ├── op3
    │   ├── input.scs
    │   └── properties.json
    ├── op4
    │   ├── input.scs
    │   └── properties.json
    ├── op5
    │   ├── input.scs
    │   └── properties.json
    ├── op6
    │   ├── input.scs
    │   └── properties.json
    ├── op8
    │   ├── input.scs
    │   └── properties.json
    ├── op9
    │   ├── input.scs
    │   └── properties.json
    ├── pdk -> /path/to/pdk/XKIT/xh035/cadence/v6_6/spectre/v6_6_2/mos
    ├── nmos -> /path/to/xh035-nmos
    ├── pmos -> /path/to/xh035-pmos
    ├── README.md
    └── st1
        ├── input.scs
        └── properties.json
```

#### Machine Learning Models for elec Environments

The models used for `elec` envs are trained with
[precept](https://github.com/electronics-and-drives/precept) and _must_ have
the following mapping:

```
[ gmoverid          [ log₁₀(idoverw)
, log₁₀(fug)   ↦    , L
, Vds               , log₁₀(gdsoverw)
, Vbs ]             , Vgs ]
```

$$
\begin{bmatrix}
    g_{\mathrm{m}}/I_{\mathrm{d}} \\
    f_{\mathrm{ug}} \\
    V_{\mathrm{ds}} \\
    V_{\mathrm{bs}}
\end{bmatrix}
\mapstop
\begin{bmatrix}
    I_{\mathrm{d}}/W \\
    L \\
    g_{\mathrm{ds}}/W \\
    V_{\mathrm{gs}}
\end{bmatrix}
$$

The paths (`nmos_path`, `pmos_path`) _must_ be structured like this:

```
nmos_path
├── model.ckpt  # Optional
├── model.pt    # TorchScript model produced by precept
├── scale.X     # Scikit MinMax Scaler for inputs
└── scale.Y     # Scikit MinMax Scaler for outputs
```

The `model.pt` _must_ be a
[torchscript](https://pytorch.org/tutorials/recipes/torchscript_inference.html)
module adhering to the specified input and output dimensions. The scalers
`scale.<X|Y>` _must_ be
[MinMaxScalers](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MinMaxScaler.html)
dumped with joblib.
