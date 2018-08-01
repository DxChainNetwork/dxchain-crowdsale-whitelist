# DxChain(https://www.dxchain.com) crowdsale whitelist 

[![license](https://img.shields.io/github/license/mashape/apistatus.svg?style=flat-square)](https://opensource.org/licenses/MIT)

## Whitelist lottery algorithm

DxChain team will release the lottery code, whiltelist data and random generator seed to all community in github.

## Random generator seed

The seed will be the hash value of first Bitcoin block after 08/01/2018 12:00PM PST(08/01/2018 7PM UTC).  Check details at [https://www.blockchain.com/explorer](https://www.blockchain.com/explorer)

## Code

[lottery.py](lottery.py)

## Data
please check out 'user_list.csv' for details

## Lottery program

The first block after 08/01/2018 7PM UTC is 
[Block #534729 2018-08-01 19:00:36 UTC](https://www.blockchain.com/btc/block/00000000000000000029f07d1d5bcebf1af17b1cc0062bb445f54a58fd971205)

```
# Block #534729, 2018-08-01 19:00:36 UTC
# lottery seed: 00000000000000000029f07d1d5bcebf1af17b1cc0062bb445f54a58fd971205

$ python lottery.py 00000000000000000029f07d1d5bcebf1af17b1cc0062bb445f54a58fd971205
----------------------------------------------------------------------------------------
round A
cut off point: 59
----------------------------------------------------------------------------------------
round B
cut off point: 20
----------------------------------------------------------------------------------------
round C
cut off point: 2
result file: dxchain-crowdsale-whitelist/winners.csv
```

## Winners list
[winners.csv](winners.csv)