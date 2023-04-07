// SPDX-License-Identifier: Unlicense
pragma solidity ^0.8.15;

import "foundry-huff/HuffDeployer.sol";
import "forge-std/Script.sol";

import "../test/mock/mockERC20.sol";

contract Deploy is Script {
  function run() external  {
    vm.startBroadcast();
    MockERC20 token = new MockERC20();
    vm.stopBroadcast();
  }
}
