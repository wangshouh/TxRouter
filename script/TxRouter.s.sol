// SPDX-License-Identifier: MIT
pragma solidity ^0.8.15;

import "foundry-huff/HuffDeployer.sol";
import "forge-std/Script.sol";

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

interface TxRouterFactory {
    function createTxRouter(address, address) external returns (address);
}

contract Deploy is Script {
  function run() public returns (TxRouter txRouter, TxRouterFactory txRouterFactory) {
    txRouter = TxRouter(HuffDeployer.broadcast("TxRouter"));
    txRouterFactory = TxRouterFactory(HuffDeployer.broadcast("TxRouterFactory"));
  }
}