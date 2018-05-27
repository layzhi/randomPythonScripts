// requiring the .js file
const Blockchain = require('./blockchain');

// instance of the function 
const bitcoin = new Blockchain();

// test the createBlock method
bitcoin.createNewBlock(2389, '2V124VDFG', '21DSGAG1332154SDF');
bitcoin.createNewBlock(2, 'ASDV2V124VDFG', 'FCSAF12SADA 21DSGAG1332154SDF');

console.log(bitcoin);