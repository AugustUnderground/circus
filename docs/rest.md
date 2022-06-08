## REST API

Circus comes with a REST API which can be instatiated with the _carnival_
command. It supports the following arguments:

```bash
usage: carnival [-h] [--host HOST] [-p PORT] [-e ENV] [-s SPACE] [-v VAR] [-n NUM] [-t STEP] [-c] [--pdk PDK]

optional arguments:
  -h, --help            show this help message and exit
  --host HOST           Host address
  -p PORT, --port PORT  Server Port
  -e ENV, --env ENV     ACE Environment ID, see Circus doc for what's available
  -s SPACE, --space SPACE
                        Circus Action Space, see Circus doc for what's available
  -v VAR, --var VAR     Circus Environment variant, see Circus doc for what's available
  -n NUM, --num NUM     Number of Pooled Envs
  -t STEP, --step STEP  Number of Steps per Episode
  -c, --scale           Circus Action Space, see Circus doc for what's available
  --pdk PDK             ACE backend, see Circus doc for what's available

```

