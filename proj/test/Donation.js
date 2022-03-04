const { expect } = require("chai");
require("@nomiclabs/hardhat-web3");


describe("Donation contract", function () {
  it("Balance smart-contract == 0", async function () {
    const [owner, addr1,addr2] = await ethers.getSigners();

    const Donation = await ethers.getContractFactory("Donation");

    const Contract = await Donation.deploy();

    const Balance = await Contract.balanceContract();
    expect(await Contract.balanceContract()).to.equal(0);
  });




  it("Withdrawal working addr1 = 1", async function () {
    const [owner, addr1,addr2] = await ethers.getSigners();

    const Donation = await ethers.getContractFactory("Donation");

    const Contract = await Donation.deploy();
    
    const Donat = await Contract.connect(owner).withdrawal(1,addr1.address);
    expect(await Contract.balanceContract()).to.equal(1);

  });

  it("You not owner accept", async function () {

    const [owner, addr1, addr2] = await ethers.getSigners();

    const Donation = await ethers.getContractFactory("Donation");

    const Contract = await Donation.deploy();
    
    const Owner = await Contract.connect(addr1).withdrawal(70,Contract.address);
    
  });

   it("Value to addr", async function () {

    const [owner, addr1, addr2] = await ethers.getSigners();

    const Donation = await ethers.getContractFactory("Donation");

    const Contract = await Donation.deploy();
    
    await Contract.connect(addr1).seePay(addr2);
    expect(await Contract.seePay()).to.equal(1);

});

it("working", async function () {

    const [owner, addr1, addr2] = await ethers.getSigners();

    const Donation = await ethers.getContractFactory("Donation");

    const Contract = await Donation.deploy();

    await Contract.seeAddress();
    expect(await Contract.seeAddress()).to.equal([]);

});

});
