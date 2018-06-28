const sha256 = require('sha256');
const currentNodeUrl = process.argv[3];
const uuid = require('uuid/v1');

class Blockchain{
    /*
    constructor function
    if you dont have a class then you can do -> function Blockchain(){ this.chain = []; etc }
     */
    constructor(){
        this.chain = [];
        this.pendingTransactions = [];

        this.currentNodeUrl = currentNodeUrl;
        this.networkNodes = [];

        // Genesis block, the first block in a blockchain
        this.createNewBlock(69, '0', '0');
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
    };

    // another way to write it is -> Blockchain.prototype.getLastBlock = function(){ // code }
    getLastBlock(){
        return this.chain[this.chain.length - 1];
    };

    /**
     * newTransaction Object 
     * pendingTransactions.push() -> pushes the newTransaction to the pendingTransaction
     * getLastBlock() returns nunber of the block that newTransaction will be added to
     */
    createNewTransaction(amount, sender, recipient){
        const newTransaction = {
            amount: amount,
            sender: sender,
            recipient: recipient,
            transactionId: uuid().split('-').join('')
        };
        
        return newTransaction;
    };

    // Add new create transaction to pending and the index
    addTransactionToPendingTransactions(transactionObj){
        this.pendingTransactions.push(transactionObj);
        return this.getLastBlock()['index'] + 1;
    };

    // previousBlockHash = string, currentBlockData = json object, nonce = int 
    hashBlock(previousBlockHash, currentBlockData, nonce){
        const dataAsString = previousBlockHash + String(nonce) + JSON.stringify(currentBlockData);
        const hash = sha256(dataAsString);
        return hash;
    };

    // nonce is basically the proofOfWOrk
    proofOfWork(previousBlockHash, currentBlockData){
        let nonce = 0;
        let hash = this.hashBlock(previousBlockHash, currentBlockData, nonce);
        while(hash.substring(0, 4) !== '0000'){
            nonce ++;
            hash = this.hashBlock(previousBlockHash, currentBlockData, nonce);
        }
        
        return nonce;
    };

    // validate whether a block chain is valid or not (iterate through the blockchain and make sure the previous hash is the same)
    chainIsValid(blockchain){
        let validChain = true;

        // Go through entire chain and rehash and confirm block
        for (var i = 1; i < blockchain.length; i ++){
            const currentBlock = blockchain[i];
            const prevBlock = blockchain[i - 1];
            const blockHash = this.hashBlock(prevBlock['hash'], { transactions: currentBlock['transactions'], index: currentBlock['index'] }, currentBlock['nonce']);
            if (blockHash.substring(0,4) !== '0000'){
                validChain = false;
            }
            if (currentBlock['previousBlockHash'] !== prevBlock['hash']){
                validChain = false;
            }
        };

        // Checking genesis block
        const genesisBlock = blockchain[0];
        const correctNonce = genesisBlock['nonce'] === 69;
        const correctPreviousBlockHash = genesisBlock['previousBlockHash'] === '0';
        const correctHash = genesisBlock['hash'] === '0';
        const correctTransactions = genesisBlock['transactions'].length === 0;

        if(!correctNonce || !correctPreviousBlockHash || !correctHash || !correctTransactions){
            validChain = false;
        }

        return validChain;

    };

    getBLock(blockHash){
        let correctBlock = null;
        this.chain.forEach(block => {
            if(block.hash === blockHash){
                correctBlock = block;
            }
        });
        return correctBlock;
    };

    getTransaction(transactionId){
        let correctTransaction = null;
        let correctBlock = null;
        this.chain.forEach(block => {
            block.transactions.forEach(transaction => {
                if(transaction.transactionId === transactionId){
                    correctTransaction = transaction;
                    correctBlock = block;
                };
            });
        });

        return {
            transaction: correctTransaction,
            block: correctBlock
        }
    };

    getAddressData(address){
        const addressTransactions = [];
        this.chain.forEach(block => {
            block.transactions.forEach(transaction => {
                if(transaction.sender === address || transaction.recipient === address){
                    addressTransactions.push(transaction);
                };
            });
        });

        let balance = 0;
        addressTransactions.forEach(transaction => {
            if(transaction.recipient === address){
                balance += transaction.amount;
            } else if (transaction.sender === address){
                balance -= transaction.amount;
            }
        });

        return {
            addressTransactions: addressTransactions,
            addressBalance: balance
        };
    };

}

//export blockchain constructor function
module.exports = Blockchain;