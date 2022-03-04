require("@nomiclabs/hardhat-waffle");
require("solidity-coverage");
require("dotenv").config();
require("@nomiclabs/hardhat-web3");





module.exports = {
  solidity: "0.8.0",
  networks: {
    rinkeby: {
      url:'https://eth-rinkeby.alchemyapi.io/v2/rHsv2KyJ01ncUv3_q1JCdZJ7kGSUFlvm',
      accounts:[process.env.PRIVATE_KEY],
      gas: 210,
      gasPrice: 800,
      saveDeployments: true
  },
    hardhat:{
      chainID:1337
  }

 },

};

