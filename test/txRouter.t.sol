// SPDX-License-Identifier: MIT
pragma solidity ^0.8.15;

import "foundry-huff/HuffDeployer.sol";
import "forge-std/Test.sol";
import "./mock/mockERC20.sol";

contract txRouterTest is Test {
    MockERC20 private token;
    MockERC20 private approveToken;
    TxRouter private txRouter;

    function setUp() public {
        token = new MockERC20();
        approveToken = new MockERC20();

        txRouter = TxRouter(HuffDeployer.deploy("TxRouter"));

        token.transfer(address(txRouter), 1000 ether);
        approveToken.approve(address(txRouter), 1000 ether);
    }

    function transferCallDataGenerate(uint256 privateKey, uint96 amount) internal returns (address, uint256) {
        address transferReceiver = vm.addr(privateKey);
        return (transferReceiver, abi.decode(abi.encodePacked(transferReceiver, amount), (uint256)));
    }

    function test_multiTransfer(uint256 n) public {

        n = bound(n, 1, 1024);

        address[] memory callerArray = new address[](n);
        uint256[] memory callDataArray = new uint256[](n);

        for (uint96 i = 0; i < n; i++) {
            uint256 pk = i + 1;
            (address caller, uint256 mockCalldata) = transferCallDataGenerate(pk, i * 1000);
            callerArray[i] = caller;
            callDataArray[i] = mockCalldata;
        }

        txRouter.multiTransfer(address(token), callDataArray);

        for (uint256 i = 0; i < n; i++) {
            address caller = callerArray[i];
            assertEq(token.balanceOf(caller), i * 1000);
        }
    }

    function test_multiApproveTransfer(uint256 n) public {

        n = bound(n, 1, 1024);

        address[] memory callerArray = new address[](n);
        uint256[] memory callDataArray = new uint256[](n); 


        for (uint96 i = 0; i < n; i++) {
            uint256 pk = i + 1;
            (address caller, uint256 mockCalldata) = transferCallDataGenerate(pk, i * 1000);
            callerArray[i] = caller;
            callDataArray[i] = mockCalldata;
        } 

        txRouter.multiApproveTransfer(address(this), address(approveToken), callDataArray);

        for (uint96 i = 0; i < n; i++) {
            address caller = callerArray[i];
            assertEq(approveToken.balanceOf(caller), i * 1000);
        }
   } 
}

interface TxRouter {
    function multiTransfer(address, uint256[] memory) external;
    function multiApproveTransfer(address, address, uint256[] memory) external;
}