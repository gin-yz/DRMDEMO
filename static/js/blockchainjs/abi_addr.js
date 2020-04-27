const abi =[
	{
		"constant": false,
		"inputs": [
			{
				"name": "_name",
				"type": "string"
			},
			{
				"name": "_hashLink",
				"type": "string"
			},
			{
				"name": "_demoLink",
				"type": "string"
			},
			{
				"name": "_desc",
				"type": "string"
			},
			{
				"name": "_status",
				"type": "bool"
			},
			{
				"name": "_price",
				"type": "uint256[]"
			}
		],
		"name": "addProductToStorage",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "_addr",
				"type": "address"
			},
			{
				"name": "_judge",
				"type": "bool"
			}
		],
		"name": "modifyKeyManager",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "_productId",
				"type": "uint256"
			},
			{
				"name": "_status",
				"type": "bool"
			}
		],
		"name": "modifyProductAdmin",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "_productId",
				"type": "uint256"
			},
			{
				"name": "_status",
				"type": "bool"
			}
		],
		"name": "modifyProductDrmer",
		"outputs": [],
		"payable": true,
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "_projectname",
				"type": "string"
			},
			{
				"name": "_productId",
				"type": "uint256"
			},
			{
				"name": "_permission",
				"type": "uint256"
			}
		],
		"name": "purchase",
		"outputs": [],
		"payable": true,
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "_purchaseId",
				"type": "uint256"
			}
		],
		"name": "refundMoney",
		"outputs": [],
		"payable": true,
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "_projectname",
				"type": "string"
			},
			{
				"name": "_purchaseId",
				"type": "uint256"
			},
			{
				"name": "_newPermission",
				"type": "uint256"
			}
		],
		"name": "update",
		"outputs": [],
		"payable": true,
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "_purchaseId",
				"type": "uint256"
			},
			{
				"name": "_licenseHash",
				"type": "string"
			}
		],
		"name": "uploadLicense",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "_status",
				"type": "bool"
			}
		],
		"name": "vaildProducer",
		"outputs": [],
		"payable": true,
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"name": "_commissionCharge",
				"type": "uint256[]"
			},
			{
				"name": "_bondmoney",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"name": "_from",
				"type": "address"
			},
			{
				"indexed": false,
				"name": "_id",
				"type": "uint256"
			},
			{
				"indexed": false,
				"name": "_name",
				"type": "string"
			},
			{
				"indexed": false,
				"name": "_hashLink",
				"type": "string"
			},
			{
				"indexed": false,
				"name": "_demoLink",
				"type": "string"
			},
			{
				"indexed": false,
				"name": "_status",
				"type": "bool"
			},
			{
				"indexed": false,
				"name": "_desc",
				"type": "string"
			},
			{
				"indexed": false,
				"name": "_price",
				"type": "uint256[]"
			}
		],
		"name": "sendAddMsg",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"name": "_form",
				"type": "address"
			},
			{
				"indexed": false,
				"name": "_type",
				"type": "uint256"
			},
			{
				"indexed": false,
				"name": "_id",
				"type": "uint256"
			},
			{
				"indexed": false,
				"name": "_productId",
				"type": "uint256"
			},
			{
				"indexed": false,
				"name": "_permission",
				"type": "uint256"
			},
			{
				"indexed": false,
				"name": "_timestamp",
				"type": "uint256"
			},
			{
				"indexed": false,
				"name": "_money",
				"type": "uint256"
			},
			{
				"indexed": false,
				"name": "_projectname",
				"type": "string"
			}
		],
		"name": "sendPurchaseMsg",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"name": "_from",
				"type": "address"
			},
			{
				"indexed": false,
				"name": "_type",
				"type": "uint256"
			},
			{
				"indexed": false,
				"name": "_msg",
				"type": "uint256"
			}
		],
		"name": "sendMsg",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"name": "_purchaseId",
				"type": "uint256"
			},
			{
				"indexed": false,
				"name": "_ipfshash",
				"type": "string"
			}
		],
		"name": "senduploadMsg",
		"type": "event"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "_purchaseId",
				"type": "uint256"
			}
		],
		"name": "askVaild",
		"outputs": [
			{
				"name": "",
				"type": "bool"
			},
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "bondmoney",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "getBalance",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "_addr",
				"type": "address"
			}
		],
		"name": "getKeyManagerStatus",
		"outputs": [
			{
				"name": "",
				"type": "bool"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "_purchaseId",
				"type": "uint256"
			}
		],
		"name": "getLicenseBypurchaseId",
		"outputs": [
			{
				"name": "",
				"type": "string"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "_addr",
				"type": "address"
			}
		],
		"name": "getOwnerBalance",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			},
			{
				"name": "",
				"type": "uint256"
			},
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "_ownaddress",
				"type": "address"
			}
		],
		"name": "getProductIdStorageByAddress",
		"outputs": [
			{
				"name": "",
				"type": "uint256[]"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "_productId",
				"type": "uint256"
			}
		],
		"name": "getProductPriceById",
		"outputs": [
			{
				"name": "",
				"type": "uint256[]"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "_productId",
				"type": "uint256"
			}
		],
		"name": "getProductStorageById",
		"outputs": [
			{
				"name": "",
				"type": "string"
			},
			{
				"name": "",
				"type": "string"
			},
			{
				"name": "",
				"type": "string"
			},
			{
				"name": "",
				"type": "bool"
			},
			{
				"name": "",
				"type": "address"
			},
			{
				"name": "",
				"type": "string"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "_productId",
				"type": "uint256"
			}
		],
		"name": "getPurchaseIdByProduceId",
		"outputs": [
			{
				"name": "",
				"type": "uint256[]"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "_ownaddress",
				"type": "address"
			}
		],
		"name": "getPurchaseIdStorageByAddress",
		"outputs": [
			{
				"name": "",
				"type": "uint256[]"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "_purchaseId",
				"type": "uint256"
			}
		],
		"name": "getPurchaseStorageById",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			},
			{
				"name": "",
				"type": "uint256"
			},
			{
				"name": "",
				"type": "uint256"
			},
			{
				"name": "",
				"type": "uint256"
			},
			{
				"name": "",
				"type": "address"
			},
			{
				"name": "",
				"type": "bool"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "_addr",
				"type": "address"
			}
		],
		"name": "isProducer",
		"outputs": [
			{
				"name": "",
				"type": "bool"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "productIndex",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "purchaseIndex",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	}
]
const addresss = '0x6205b5f841e5ab8efdc9cfba364c75ff3ffff2e9'