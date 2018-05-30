const sha256 = require('sha256');

class Blockchain{
    /*
    constructor function
    if you dont have a class then you can do -> function Blockchain(){ this.chain = []; etc }
     */
    constructor(){
        this.chain = [];
        this.pendingTransactions = [];

        // Genesis block, the first block in a blockchain
    //     createNewBlock(69, '0', '0');
    // }

    /**
      nonce comes from proof of work (just a number) -> proof that the block was created 
      another way to write it is -> Blockchain.prototype.createNewBlock = function(nonce, previousBlockHash, hash) 
     */
    createNewBlock(nonce, previousBlockHash, hash){
        const newBlock = {
            index: this.chain.length + 1,
            timestamp: Date.now(),
            transactions: this.pendingTransactions,
            nonce: nonce,
            hash: hash,
            previousBlockHash: previousBlockHash
        };

        this.pendingTransactions = [];
        this.chain.push(newBlock);

        return newBlock;
    }

    // another way to write it is -> Blockchain.prototype.getLastBlock = function(){ // code }
    getLastBlock(){
        return this.chain[this.chain.length - 1];
    }

    /**
     * newTransaction Object 
     * pendingTransactions.push() -> pushes the newTransaction to the pendingTransaction
     * getLastBlock() returns nunber of the block that newTransaction will be added to
     */
    createNewTransaction(amount, sender, recipient){
        const newTransaction = {
            amount: amount,
            sender: sender,
            recipient: recipient
        };

        this.pendingTransactions.push(newTransaction);

        // index of the lastBlock of the chain 
        return this.getLastBlock()['index'] + 1;
    }

    // previousBlockHash = string, currentBlockData = json object, nonce = int 
    hashBlock(previousBlockHash, currentBlockData, nonce){
        const dataAsString = previousBlockHash + String(nonce) + JSON.stringify(currentBlockData);
        const hash = sha256(dataAsString);
        return hash;
    }

    // nonce is basically the proofOfWOrk
    proofOfWork(previousBlockHash, currentBlockData){
        let nonce = 0;
        let hash = this.hashBlock(previousBlockHash, currentBlockData, nonce);
        while(hash.substring(0, 4) !== '0000'){
            nonce ++;
            hash = this.hashBlock(previousBlockHash, currentBlockData, nonce);
        }
        
        return nonce;
    }
}

//export blockchain constructor function
module.exports = Blockchain;