// requiring the .js file
const Blockchain = require('./blockchain');

// instance of the function 
const bitcoin = new Blockchain();

// Mining blocks and placing the transcations into those blocks
// bitcoin.createNewBlock(2389, '2V124VDFG', '21DSGAG1332154SDF');
// bitcoin.createNewTransaction(1, 'SAM123FSD123F', 'ALEX124DFB324DFG');
// bitcoin.createNewTransaction(2, 'SAM124FDG235FDH', 'LAP123FDGREYT234');
// the above transactions will go into a new block once created
// bitcoin.createNewBlock(2341, '214DSAG5325SAF', 'SDGAW12523SFSD');

// Testing the hash function
// const previousBlockHash = 'SDF123421SFSA';
// const currentBlockData = [
//     {
//         amount: 10,
//         sender: 'ALEX12125DSAGA123',
//         recipient: 'LAM125235SDGASDG123SA'
//     },
//     {
//         amount: 1,
//         sender: 'BON123AWFGN54',
//         recipient: 'KIN12356DFGA1234'
//     }
// ];

// proofOfWork, finds the correct nonce to find a hash with 4 0's
// Check for a valid block, Hash the current block's data with the previous block hash and the nonce generated from the proofOfWork when mined. (valid block if hash begins with 4 0's with hashBlock method)
// console.log(bitcoin.proofOfWork(previousBlockHash, currentBlockData));

// console.log(bitcoin);
// console.log(bitcoin.chain[2]);
// console.log(bitcoin.hashBlock(previousBlockHash, currentBlockData, nonce));