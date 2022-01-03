// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

contract SimpleStorage {
    uint256 favouriteNumber;

    struct People {
        uint256 favouriteNumber;
        string name;
    }

    mapping(string => uint256) public nameToNumber;

    People[] public persons;

    function store(uint256 _favouriteNumber) public {
        favouriteNumber = _favouriteNumber;
    } 

    function retrieve() public view returns (uint256) {
        return favouriteNumber;
    }

    function addPerson(string memory _name, uint256 _favouriteNumber) public {
        persons.push(People({name: _name, favouriteNumber: _favouriteNumber}));

        nameToNumber[_name] = _favouriteNumber;
    }
}
