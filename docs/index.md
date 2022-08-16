A collection of [gym](https://gym.openai.com/) environments for analog 
integrated circuit design, based on
[AC²E](https://github.com/electronics-and-drives/ace) /
[HAC²E](https://github.com/AugustUnderground/hace).

## Availability Matrix

<table>
<tr>
<th></th>
<th>
<a href="https://gitlab-forschung.reutlingen-university.de/eda/ace-xh035-3v3">xh035</a>
</th>
<th>
<a href="https://gitlab-forschung.reutlingen-university.de/eda/ace-xh018-1v8">xh018</a>
</th>
<th>
<a href="https://gitlab-forschung.reutlingen-university.de/eda/ace-xt018-1v8">xt018</a>
</th>
<th>
<a href="https://github.com/matthschw/ace-sky130-1V8">sky130</a>
</th>
<th>
<a href="https://github.com/AugustUnderground/ace-gpdk180-1V8">gpdk180</a>
</th>
<th>
<a href="https://github.com/AugustUnderground/ace-ptm">ptm130</a>
</th>
</tr>
<tr>
<th>
<a href="https://raw.githubusercontent.com/matthschw/ace/main/figures/op1.png">op1</a>
</th>
<td>elec, geom, (non-)goal</td> <td>elec, geom, (non-)goal</td> <td>N/A</td> <td>N/A</td> <td>N/A</td> <td>N/A</td>
</tr>
<tr>
<th>
<a href="https://raw.githubusercontent.com/matthschw/ace/main/figures/op2.png">op2</a>
</th>
<td>elec, geom, (non-)goal</td> <td>elec, geom, (non-)goal</td> <td>N/A</td> <td>N/A</td> <td>N/A</td> <td>N/A</td>
</tr>
<tr>
<th>
<a href="https://raw.githubusercontent.com/matthschw/ace/main/figures/op3.png">op3</a>
</th>
<td>N/A</td> <td>N/A</td> <td>N/A</td> <td>N/A</td> <td>N/A</td> <td>N/A</td>
</tr>
<tr>
<th>
<a href="https://raw.githubusercontent.com/matthschw/ace/main/figures/op4.png">op4</a>
</th>
<td>N/A</td> <td>N/A</td> <td>N/A</td> <td>N/A</td> <td>N/A</td> <td>N/A</td>
</tr>
<tr>
<th>
<a href="https://raw.githubusercontent.com/matthschw/ace/main/figures/op5.png">op5</a>
</th>
<td>N/A</td> <td>N/A</td> <td>N/A</td> <td>N/A</td> <td>N/A</td> <td>N/A</td>
</tr>
<tr>
<th>
<a href="https://raw.githubusercontent.com/matthschw/ace/main/figures/op6.png">op6</a>
</th>
<td>N/A</td> <td>N/A</td> <td>N/A</td> <td>N/A</td> <td>N/A</td> <td>N/A</td>
</tr>
<tr>
<th>
<a href="https://raw.githubusercontent.com/matthschw/ace/main/figures/op7.png">op7</a>
</th>
<td>N/A</td> <td>N/A</td> <td>N/A</td> <td>N/A</td> <td>N/A</td> <td>N/A</td>
</tr>
<tr>
<th>
<a href="https://raw.githubusercontent.com/matthschw/ace/main/figures/op8.png">op8</a>
</th>
<td>elec, geom, (non-)goal</td> <td>elec, geom, (non-)goal</td> <td>N/A</td> <td>N/A</td> <td>N/A</td> <td>N/A</td>
</tr>
<tr>
<th>
<a href="https://raw.githubusercontent.com/matthschw/ace/main/figures/op9.png">op9</a>
</th>
<td>N/A</td> <td>N/A</td> <td>N/A</td> <td>N/A</td> <td>N/A</td> <td>N/A</td>
</tr>
<tr>
<th>
<a href="https://raw.githubusercontent.com/matthschw/ace/main/figures/op10.png">op10</a>
</th>
<td>N/A</td> <td>N/A</td> <td>N/A</td> <td>N/A</td> <td>N/A</td> <td>N/A</td>
</tr>
<tr>
<th>
<a href="https://raw.githubusercontent.com/matthschw/ace/main/figures/op11.png">op11</a>
</th>
<td>elec, geom, (non-)goal</td> <td>elec, geom, (non-)goal</td> <td>N/A</td> <td>N/A</td> <td>N/A</td> <td>N/A</td>
</tr>
</table>

## Table of Contents

- [Installation](./install.md)
- [API Documentation](./circus/index.html)
- [REST API](./rest.md)
- [Basic Usage](./usage.md)
- [Environments](./env.md)
    + [X] [OP1: Miller Operational Amplifier](./op1.md)
    + [X] [OP2: Symmetrical Amplifier](./op2.md)
    + [ ] [OP3: Un-Symmetrical Amplifier]()
    + [ ] [OP4: Symmetrical Cascode Amplifier]()
    + [ ] [OP5: Un-Symmetrical Cascode Amplifier]()
    + [ ] [OP6: Miller Amplifier w/o Passives]()
    + [ ] [OP7: Feed-Forward Operational Amplifier]()
    + [X] [OP8: Folded Cascode Amplifier](./op8.md)
    + [ ] [OP9: Amplifier with Cascode Wideswing Current Mirror]()
    + [ ] [OP10: Rail-To-Rail Folded Cascode Amplifier]()
    + [X] [OP11: Rail-To-Rail Folded Cascode Amplifier with Wide-Swing Current Mirror](./op11.md)
