## Single Ended Operational Amplifier Environments

### Observation and Goal Spaces

The observation space _can_ contain all information returned by
[serafin](https://github.com/augustunderground/serafing). By default
however, it only contains the following performance parameters:

| Parameter   | Description                            |
|-------------|----------------------------------------|
| `a_0`       | DC Gain                                |
| `ugbw`      | Unity Gain Bandwidth                   |
| `pm`        | Phase Margin                           |
| `gm`        | Gain Margin                            |
| `sr_r`      | Slew Rate rising                       |
| `sr_f`      | Slew Rate falling                      |
| `vn_1Hz`    | Output-referred noise density @ 1Hz    |
| `vn_10Hz`   | Output-referred noise density @ 10Hz   |
| `vn_100Hz`  | Output-referred noise density @ 100Hz  |
| `vn_1kHz`   | Output-referred noise density @ 1kHz   |
| `vn_10kHz`  | Output-referred noise density @ 10kHz  |
| `vn_100kHz` | Output-referred noise density @ 100kHz |
| `psrr_p`    | Power Supply Rejection Ratio           |
| `psrr_n`    | Power Supply Rejection Ratio           |
| `cmrr`      | Common Mode Rejection Ratio            |
| `v_il`      | Input Low                              |
| `v_ih`      | Input High                             |
| `v_ol`      | Output Low                             |
| `v_oh`      | Output High                            |
| `i_out_min` | Minimum output current                 |
| `i_out_max` | Maximum output current                 |
| `idd`       | Current consumption                    |
| `iss`       | Current consumption                    |
| `os_r`      | Slew rate overswing rising             |
| `os_f`      | Slew rate overswing falling            |
| `cof`       | Cross over frequency                   |
| `voff_stat` | Statistical Offset                     |
| `voff_syst` | Systematic Offset                      |
| `area`      | Estimated Area                         |

The goal space _must_ be a subset of this.

### Action Spaces and Variants

Action Spaces are _continuous_ and implemented with `gym.spaces.Box`. 
For further details, see the descriptions for specific environments. 

### Electrical Design Space

For using the `*-elec-*` environments, primitive deivce models for converting
electrical characteristics to geometric ones are required. Please see
[prehsept](https://github.com/AugustUnderground/prehsept) on how to create them
for the technology of your choice.

