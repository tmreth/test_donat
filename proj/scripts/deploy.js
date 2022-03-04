const hre = require("hardhat")
const ethers = hre.ethers

async function main() {
  const [signer] = await ethers.getSigners();
  // We get the contract to deploy
  const Greeter = await ethers.getContractFactory("Donation",signer);
  const greeter = await Greeter.deploy();
  await greeter.deployed();

  console.log("Greeter deployed to:", greeter.address);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
