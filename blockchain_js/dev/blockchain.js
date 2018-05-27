
class Blockchain{
    /*
    constructor function
    if you dont have a class then you can do -> function Blockchain(){ this.chain = []; etc }
     */
    constructor(){
        this.chain = [];
        this.pendingTransactions = [];
    }

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


    
}

//export blockchain constructor function
module.exports = Blockchain;