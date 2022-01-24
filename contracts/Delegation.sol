// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

interface IDelegate {
  function pwn() external;
}

contract Delegation {

  address public owner;
  IDelegate delegate;

  constructor(address _delegateAddress) public {
    delegate = IDelegate(_delegateAddress);
    owner = msg.sender;
  }

  fallback() external {
    (bool result,) = address(delegate).delegatecall(msg.data);
    if (result) {
      this;
    }
  }
}