const express = require('express');
const bodyParser = require('body-parser');
const Blockchain = require('./blockchain');
const uuid = require('uuid/v1');
const app = express();
const nodeAddress = uuid().split('-').join('');
const port = process.argv[2];
const rp = require('request-promise');

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

// register a node and broadcast it to the network
app.post('/register-and-broadcast-node', function(req, res){
    const newNodeUrl = req.body.newNodeUrl;
    if (coinz.networkNodes.indexOf(newNodeUrl) == -1){
        coinZ.networkNodes.push(newNodeUrl);
    }
    
    const regNodesPromises = [];
    coinZ.networkNodes.forEach(networkNodeUrl => {
        const requestOptions = {
            uri: networkNodeUrl + '/register-node',
            method: 'POST',
            body: { newNodeUrl: newNodeUrl },
            json: true
        };

        regNodesPromises.push(rp(requestOptions));
    });

    Promise.all(regNodesPromises)
    .then(data =>  {
        const bulkRegisterOptions = {
            uri: newNodeUrl + '/register-nodes-bulk',
            method: 'POST',
            body: { allNetworkNodes: [...coinZ.networkNodes, coinZ.currentNodeUrl] },
            json: true
        };

        return rp(bulkRegisterOptions);
    })
    .then(data => {
        res.json({ note: 'New node registered with network successfully.' });
    });
});

// register a node with the network
app.post('/register-node', function(req, res){
    const newNodeUrl = req.body.newNodeUrl;
    const nodeNotAlreadyPresent = coinZ.networkNodes.indexOf(newNodeUrl) == -1;
    const notCurrentNode = coinZ.currentNodeUrl !== newNodeUrl;
    if( nodeNotAlreadyPresent && notCurrentNode) coinZ.networkNodes.push(newNodeUrl);
    res.json({ note: 'New node registered successfully with node.' });
});

// register multiple nodes at once
app.post('/register-nodes-bulk', function(req, res){
    const allNetworkNodes = req.body.allNetworkNodes;
    allNetworkNodes.forEach(networkNodeUrl => {
        const nodeNotAlreadyPresent = coinZ.networkNodes.indexOf(networkNodeUrl) == -1;
        const notCurrentNode = coinZ.currentNodeUrl !== networkNodeUrl;
        if(nodeNotAlreadyPresent && notCurrentNode) coinZ.networkNodes.push(networkNodeUrl);
    });
});

app.listen(port, function(){
    console.log(` Listening on port ${port}...`);
});