// SPDX-License-Identifier: MIT
pragma solidity ^0.8.15;

import "foundry-huff/HuffDeployer.sol";
import "forge-std/Test.sol";
import "./mock/mockERC20.sol";

contract txRouterTest is Test {
    MockERC20 private token;
    TxRouter private txRouter;

    function setUp() public {
        token = new MockERC20();
        txRouter = TxRouter(HuffDeployer.deploy("TxRouter"));
        token.transfer(address(txRouter), 1000 ether);

    }

    function transferCallDataGenerate(uint256 privateKey, uint96 amount) internal returns (address, uint256) {
        address transferReceiver = vm.addr(privateKey);
        return (transferReceiver, abi.decode(abi.encodePacked(transferReceiver, amount), (uint256)));
    }

    function test_OnePersonTransfer() public {
        (address caller, uint256 mockCalldata) = transferCallDataGenerate(1, 1000);
        // console.log(mockCalldata);
        // console.log(caller);
        uint256[] memory callDataArray = new uint256[](1);
        callDataArray[0] = mockCalldata;

        txRouter.multiTransfer(address(token), callDataArray);
        assertEq(token.balanceOf(caller), 1000);
    }
    
}

interface TxRouter {
    function multiTransfer(address, uint256[] memory) external;
}