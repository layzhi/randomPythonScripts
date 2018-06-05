const express = require('express');
const bodyParser = require('body-parser');
const Blockchain = require('./blockchain');
const uuid = require('uuid/v1');
const app = express();
const nodeAddress = uuid().split('-').join('');
const port = process.argv[2];

const coinZ = new Blockchain();

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false}));

app.get('/blockchain', function (req, res){
    res.send(coinZ);
});

// create a new transaction
app.post('/transaction', function (req, res){
    const blockIndex = coinZ.createNewTransaction(req.body.amount, req.body.sender, req.body.recipient);
    res.json({ note: `Transaction will be added in block ${blockIndex}.` });
});

// mine a block
app.get('/mine', function (req, res){
    const lastBlock = coinZ.getLastBlock();
    const previousBlockHash = lastBlock['hash'];
    const currentBlockData = {
        transactions: coinZ.pendingTransactions,
        index: lastBlock['index'] + 1
    };

    const nonce = coinZ.proofOfWork(previousBlockHash, currentBlockData);
    const blockHash = coinZ.hashBlock(previousBlockHash, currentBlockData, nonce);

    coinZ.createNewTransaction(12.5, "00", nodeAddress);

    const newBlock = coinZ.createNewBlock(nonce, previousBlockHash, blockHash);
    res.json({
        note: "New block mined successfully",
        block: newBlock
    });

});

app.listen(port, function(){
    console.log(` Listening on port ${port}...`);
});