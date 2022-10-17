A collection of [gym](https://gym.openai.com/) environments for analog 
integrated circuit design, based on
[serafin](https://github.com/augustunderground/serafin) and inspired by
[AC²E](https://github.com/electronics-and-drives/ace).

## Table of Contents

- [Installation](./install.md)
- [API Documentation](./circus/index.html)
- [REST API](./rest.md)
- [Examples and Basic Usage](./usage.md)
- [Environments](./env.md)
    + [X] [SYM: Symmetrical Amplifier](./sym.md)
    + [X] [MIL: Miller Operational Amplifier](./mil.md)
    + [ ] [FFA: Feed-Forward Operational Amplifier]()
    + [X] [FCA: Folded Cascode Amplifier](./fca.md)
    + [X] [RFA: Rail-To-Rail Folded Cascode Amplifier with Wide-Swing Current Mirror](./rfa.md)
- [Development](./dev.md)

## Availability Matrix

<table>
<tr>
<th></th>
<th>xh035</th>
<th>xh018</th>
<th>xt018</th>
<th>sky130</th>
<th>gpdk180</th>
<th>gpdk090</th>
<th>gpdk045</th>
</tr>
<tr>
<th><a href="./sym.html">SYM</a></th>
<td>✘</td> <td>✔</td> <td>✔</td> <td>✘</td> <td>✔</td> <td>✔</td> <td>✔</td>
</tr>
<tr>
<th><a href="./mil.html">MIL</a></th>
<td>✘</td> <td>✔</td> <td>✔</td> <td>✘</td> <td>✔</td> <td>✔</td> <td>✔</td>
</tr>
<tr>
<th><a href="./fca.html">FCA</a></th>
<td>✘</td> <td>✔</td> <td>✔</td> <td>✘</td> <td>✔</td> <td>✔</td> <td>✔</td>
</tr>
<tr>
<th><a href="./ffa.html">FFA</a></th>
<td>✘</td> <td>✔</td> <td>✔</td> <td>✘</td> <td>✔</td> <td>✔</td> <td>✔</td>
</tr>
<tr>
<th><a href="./rfa.html">RFA</a></th>
<td>✘</td> <td>✔</td> <td>✔</td> <td>✘</td> <td>✔</td> <td>✔</td> <td>✔</td>
</tr>
</table>

