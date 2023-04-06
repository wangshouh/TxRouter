// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

library TxRouterFactor {
	// event ProxyCreation(address indexed owner, address indexed implementation); 

	function createProxy(address implementation, address owner) public returns (address instance) {
		assembly {
			mstore(0x00, or(shr(0x50, shl(0x60, owner)), 0x604f8060093d393df37300000000000000000000000000000000000000003314))
			mstore(0x20, or(shr(0x78, shl(0x60, implementation)), 0x1561004757363d3d373d3d3d363d730000000000000000000000000000000000))
			mstore(0x40, or(shl(0xe8, implementation), shr(0x18, shl(0x58, 0x5af43d82803e903d9161004d575b60006000fd5bf3))))
			instance := create(0, 0x00, 0x58)
		}
		require(instance != address(0), "ERC1167: create failed");

		// emit ProxyCreation(owner, implementation);
	}
}


// 604f8060093d393df373
// 7fa9385be102ac3eac297483dd6233d62b3e1496
// 33141561004757363d3d373d3d3d363d73
// ffd4505b3452dc22f8473616d50503ba9e1710ac
// 5af43d82803e903d9161004d575b60006000fd5bf3

// 604f8060093d393df3737fa9385be102ac3eac297483dd6233d62b3e149633141561004757363d3d373d3d3d363d73ffd4505b3452dc22f8473616d50503ba9e1710ac5af43d82803e903d9161004d575b60006000fd5bf3
// 604f8060093d393df3737fa9385be102ac3eac297483dd6233d62b3e149633141561004757363d3d373d3d3d363d73ffd4505b3452dc22f8473616d50503ba9e1710ac5af43d82803e903d9161004d575b60006000fd5bf30000000000000000
// 604f8060093d393df3737fa9385be102ac3eac297483dd6233d62b3e14963314