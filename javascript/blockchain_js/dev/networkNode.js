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
    const newTransaction = req.body;
    const blockIndex = coinZ.addTransactionToPendingTransactions(newTransaction);
    res.json ({ note: `Transaction will be added in block ${blockIndex}.` });
});

app.post('/transaction/broadcast', function(req, res){
    const newTransaction = coinZ.createNewTransaction(req.body.amount, req.body.sender, req.body.recipient);
    coinZ.addTransactionToPendingTransactions(newTransaction);

    const requestPromises = [];
    coinZ.networkNodes.forEach(networkNodeUrl => {
        const requestOptions = {
            uri: networkNodeUrl + '/transaction',
            method: 'POST',
            body: newTransaction,
            json: true
        };

        requestPromises.push(rp(requestOptions));
    });

    Promise.all(requestPromises)
    .then(data => {
        res.json({ note: 'Transaction created and broadcast successfully.' });
    });
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
    const newBlock = coinZ.createNewBlock(nonce, previousBlockHash, blockHash);

    const requestPromises = [];
    coinZ.networkNodes.forEach(networkNodeUrl => {
        const requestOptions = {
            uri: networkNodeUrl + '/receive-new-block',
            method: 'POST',
            body: { newBlock: newBlock },
            json: true
        };
        
        requestPromises.push(rp(requestOptions));
    });

    Promise.all(requestPromises)
    .then(data => {
        const requestOptions = {
            uri: coinZ.currentNodeUrl + '/transaction/broadcast',
            method: 'POST',
            body: {
                amount: 12.5,
                sender: "00",
                recipient: nodeAddress
            },
            json: true
        };
        return rp(requestOptions)
    })
    .then(data => {
        res.json({
            note: "New block mined & broadcast successfully",
            block: newBlock
        });  
    });

});

app.post('/receive-new-block', function(req, res){
    const newBlock = req.body.newBlock;
    const lastBlock = coinZ.getLastBlock();
    const correctHash = lastBlock.hash === newBlock.previousBlockHash;
    const correctIndex = lastBlock['index'] + 1 === newBlock['index'];

    if(correctHash && correctIndex){
        coinZ.chain.push(newBlock);
        coinZ.pendingTransactions = [];
        res.json({ 
            note: 'New block received and accepted.',
            newBlock: newBlock
         });
    } else {
        res.json({ 
            note: 'New Block rejected.',
            newBlock: newBlock
        });
    }
});

// register a node and broadcast it to the network
app.post('/register-and-broadcast-node', function(req, res){
    const newNodeUrl = req.body.newNodeUrl;
    if (coinZ.networkNodes.indexOf(newNodeUrl) == -1){
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

    res.json({ note: 'Bulk registration successful.' });
});

app.listen(port, function(){
    console.log(` Listening on port ${port}...`);
});

