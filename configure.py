# ================================
# APP SETTINGS
# ================================

APP_NAME = "iThuma Logistics Demo"

APP_TAGLINE = "Blockchain Supply Chain System"

APP_DESCRIPTION = "Track suppliers, couriers, and procurement on-chain."

LOGO_PATH = "logo.png"

# ================================
# NETWORK SETTINGS
# ================================

RPC_URL = "https://rpc.sepolia.org"

CONTRACT_ADDRESS = "0xYourContractAddress"

# ================================
# SMART CONTRACT ABI
# ================================

CONTRACT_ABI = [
    {
        "inputs": [],
        "name": "owner",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_id",
                "type": "uint256"
            }
        ],
        "name": "getOrder",
        "outputs": [
            {
                "components": [
                    {
                        "internalType": "uint256",
                        "name": "id",
                        "type": "uint256"
                    },
                    {
                        "internalType": "address",
                        "name": "supplier",
                        "type": "address"
                    },
                    {
                        "internalType": "address",
                        "name": "courier",
                        "type": "address"
                    },
                    {
                        "internalType": "address",
                        "name": "createdBy",
                        "type": "address"
                    },
                    {
                        "internalType": "uint256",
                        "name": "amount",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "carbonEmissions",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint8",
                        "name": "status",
                        "type": "uint8"
                    },
                    {
                        "internalType": "uint256",
                        "name": "timestamp",
                        "type": "uint256"
                    }
                ],
                "internalType": "tuple",
                "name": "",
                "type": "tuple"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

# ================================
# STATUS MAPS
# ================================

ORDER_STATUS = {
    0: "Created",
    1: "Approved",
    2: "Assigned",
    3: "Dispatched",
    4: "Delivered"
}

SUPPLIER_STATUS = {
    0: "Pending",
    1: "Verified",
    2: "Blocked"
}

COURIER_STATUS = {
    0: "Available",
    1: "Busy",
    2: "Offline"
}
