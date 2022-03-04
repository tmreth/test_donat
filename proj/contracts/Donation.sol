// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;


contract Donation{
    address owner;

    address[] addressPay;
    
    mapping(address => uint) addrsee;
    

    constructor(){
        owner = msg.sender;
    }

    modifier onlyOwner{
        require(owner == msg.sender,"Caller is not owner");
        _;
    }

    function seeAddress() public view returns(address[]memory){
        return addressPay;
    }

    function seePay(address payAdd) public view returns(uint){
        return addrsee[payAdd];
    }

    
    function donat() external payable{
        require(msg.sender.balance > msg.value,"No balance");
        addrsee[msg.sender] = msg.value;
        bool succes;
        if (addressPay.length > 0){
            for(uint i; i < addressPay.length;i++){
                if(addressPay[i] == msg.sender){
                    addrsee[msg.sender] += msg.value;
                    succes = true;
                    break;
                }
            }
            if(succes == false){
                addressPay.push(msg.sender);
            }
        }   
        
        else{
            addressPay.push(msg.sender);
        }        
        
    }

    function withdrawal(uint sum, address payable sender) external  onlyOwner {
        require(address(this).balance >= sum,"Insufficient funds");
        payable(sender).transfer(sum);
    }
    
    function balanceContract() external view returns(uint){
        return address(this).balance;
    }

}
