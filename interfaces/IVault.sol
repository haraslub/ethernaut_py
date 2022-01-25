// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

interface IVault {
    function unlock(bytes32 _password) external;
}