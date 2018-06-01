const express = require('express');
const bodyParser = require('body-parser');
const Blockchain = require('./blockchain');
const app = express();

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
    
    const newBlock = coinZ.createNewBlock();
});

app.listen(3000, function(){
    console.log(' Listening on port 3000...');
});