// SPDX-License-Identifier: MIT
pragma solidity ^0.8.15;

import "solmate/tokens/ERC20.sol";

contract MockERC20 is ERC20 {
    uint256 public constant MAX_SUPPLY = 1_000_000 ether;

    constructor() ERC20("ERC20Mock", "E20M", 18) {
        _mint(msg.sender, MAX_SUPPLY);
    }
}
