// SPDX-License-Identifier: Unlicense
pragma solidity ^0.8.15;

import "foundry-huff/HuffDeployer.sol";
import "forge-std/Script.sol";

import "../test/mock/mockERC20.sol";

interface TxRouter {
    struct PermitCall {
        uint256 ownerValueV;
        bytes32 r;
        bytes32 s; 
    }

    function multiTransfer(address, uint256[] memory) external;
    function multiApproveTransfer(address, address, uint256[] memory) external;
    function multiAggregate(address, address, uint256, PermitCall[] memory) external;
}

contract Deploy is Script {
  function run() external  {
    vm.startBroadcast();
    MockERC20 token = new MockERC20();
    vm.stopBroadcast();
  }
}
