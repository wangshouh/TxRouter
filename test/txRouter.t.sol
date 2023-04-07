// SPDX-License-Identifier: MIT
pragma solidity ^0.8.15;

import "foundry-huff/HuffDeployer.sol";
import "forge-std/Test.sol";
import "forge-std/console.sol";

import "./mock/mockERC20.sol";
import "./tool/SigUtils.sol";

contract txRouterTest is Test {
    MockERC20 private token;
    MockERC20 private approveToken;

    TxRouter private txRouter;
    TxRouter private txRouterProxy;

    TxRouterFactory private txRouterFactory;

    SigUtils internal sigUtils;

    function setUp() public {
        token = new MockERC20();
        approveToken = new MockERC20();
        sigUtils = new SigUtils(token.DOMAIN_SEPARATOR());

        txRouter = TxRouter(HuffDeployer.deploy("TxRouter"));

        txRouterFactory = TxRouterFactory(HuffDeployer.deploy("TxRouterFactory"));
        txRouterProxy = TxRouter(txRouterFactory.createTxRouter(address(this), address(txRouter)));

        token.transfer(address(txRouter), 1000 ether);
        token.transfer(address(txRouterProxy), 1000 ether);

        approveToken.approve(address(txRouter), 1000 ether);

        // console.log(address(txRouter));
        // console.log(address(txRouterProxy));
        // console.log(address(this));
    }

    function transferCallDataGenerate(uint256 privateKey, uint96 amount) internal returns (address, uint256) {
        address transferReceiver = vm.addr(privateKey);
        return (transferReceiver, abi.decode(abi.encodePacked(transferReceiver, amount), (uint256)));
    }

    function permitCalldataGenerate(address spender, uint96 deadline, address owner, uint88 value, uint8 v) internal pure returns (uint256, uint256) {
        uint256 spenderDeadline = abi.decode(abi.encodePacked(spender, deadline), (uint256));
        uint256 ownerValueV = abi.decode(abi.encodePacked(owner, value, v), (uint256));
        return (spenderDeadline, ownerValueV);
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

    function test_ProxyTransfer() public {
        (address caller, uint256 transferData) = transferCallDataGenerate(1, 1000);
        uint256[] memory callDataArray = new uint256[](1);
        callDataArray[0] = transferData;
        txRouterProxy.multiTransfer(address(token), callDataArray);
        assertEq(token.balanceOf(caller), 1000);
    }

    function test_NotOwner_Fail() public {
        (address caller, uint256 transferData) = transferCallDataGenerate(1, 1000);
        uint256[] memory callDataArray = new uint256[](1);
        callDataArray[0] = transferData;
        vm.startPrank(address(1));
        vm.expectRevert();
        txRouterProxy.multiTransfer(address(token), callDataArray);
        vm.stopPrank();
    }

    function test_multiAggregate() public {
        uint256 ownerPrivateKey = 0x1;
        address owner = vm.addr(ownerPrivateKey);

        address receiver = address(0xdead);

        token.transfer(owner, 1 ether);

        SigUtils.Permit memory permit = SigUtils.Permit({
            owner: owner,
            spender: address(txRouter),
            value: 1e18,
            nonce: 0,
            deadline: 1 days
        });

        bytes32 digest = sigUtils.getTypedDataHash(permit);

        (uint8 v, bytes32 r, bytes32 s) = vm.sign(ownerPrivateKey, digest);

        (uint256 spenderDDL, uint256 permitCalldata) = permitCalldataGenerate(
            address(txRouter), 1 days, address(owner), 1e18, v
        );

        TxRouter.PermitCall[] memory permitCallDataArray = new TxRouter.PermitCall[](1);

        permitCallDataArray[0] = TxRouter.PermitCall(permitCalldata, r, s);

        txRouter.multiAggregate(address(token), receiver, spenderDDL, permitCallDataArray);

        assertEq(token.balanceOf(receiver), 1e18);
    }
}

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