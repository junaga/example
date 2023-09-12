for [lumie](https://github.com/LumieOwO)

```sh
git --version # 2
node --version # 16
python --version # 3
```

## `$ node ./roulette-game.mjs`

A simple loop that shows why the [Martingale strategy](<https://en.wikipedia.org/wiki/Martingale_(betting_system)>) does not work indefinitely. If you start playing with a `balance` you can never get out `2 * balance`. After enough coinflips, there will be a **losing streak** long enough to exhaust `balance`, including previous profits. This issue can not be bypassed through iteration. It's not possible to reset "luck". History is written.

However, it is possible to get a guranteed `fraction` of `balance`, where `fraction < balance == true`. - _more code required_

## `$ python ./port-scanner.py`

Find random servers on the internet. Generates a random IPv4 address and connects to TCP ports 1-1023.
