# pip install web3 streamlit streamlit-js-eval
# config.py - Centralized configuration and business terminology

# 1. Network & Contract Identity
# Public Sepolia RPC used to read data from the blockchain for free
SEPOLIA_RPC_URL = "https://ethereum-sepolia-rpc.publicnode.com"
# The exact deployed address of the VukaChainAdvisory contract
CONTRACT_ADDRESS = "0xc9F186B05aBb47292D1D3D26169667ec12B064CA"
# Chain ID for Sepolia Testnet (used to verify the user is on the right network)
CHAIN_ID = 11155111 

# 2. Application Branding
APP_NAME = "VukaChain Advisory Portal"
TAGLINE = "The smart contract stores key supply chain data, checks required conditions, and automatically processes actions such as validating transactions and releasing payments when those conditions are met."
LOGO_PATH = "logo.png"

# 3. Human-Readable Mappings
# Translates raw numeric status codes from the blockchain into plain English
PURCHASE_ORDER_STATUS = {
    0: "Created (Awaiting Approval)",
    1: "Approved (By Procurement)",
    2: "Confirmed (By Supplier)",
    3: "Dispatched",
    4: "Delivered (Pending Payment)",
    5: "Paid"
}

SUPPLIER_STATUS = {
    0: "Unverified",
    1: "Verified (Eco-Certified)"
}

# 4. Smart Contract ABI
# This tells Python how to communicate with the specific functions in your deployed contract
CONTRACT_ABI = [
    {"inputs":[],"stateMutability":"nonpayable","type":"constructor"},
    {"inputs":[{"internalType":"address","name":"_member","type":"address"}],"name":"addLogisticsTeam","outputs":[],"stateMutability":"nonpayable","type":"function"},
    {"inputs":[{"internalType":"address","name":"_manager","type":"address"}],"name":"addProcurementManager","outputs":[],"stateMutability":"nonpayable","type":"function"},
    {"inputs":[{"internalType":"uint256","name":"_poId","type":"uint256"}],"name":"approvePurchaseOrder","outputs":[],"stateMutability":"nonpayable","type":"function"},
    {"inputs":[{"internalType":"uint256","name":"_poId","type":"uint256"},{"internalType":"uint256","name":"_carbonEmissions","type":"uint256"}],"name":"confirmDelivery","outputs":[],"stateMutability":"nonpayable","type":"function"},
    {"inputs":[{"internalType":"uint256","name":"_poId","type":"uint256"}],"name":"confirmOrderBySupplier","outputs":[],"stateMutability":"nonpayable","type":"function"},
    {"inputs":[{"internalType":"address","name":"_supplier","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"createPurchaseOrder","outputs":[],"stateMutability":"nonpayable","type":"function"},
    {"inputs":[{"internalType":"uint256","name":"_poId","type":"uint256"}],"name":"getPurchaseOrder","outputs":[{"components":[{"internalType":"uint256","name":"id","type":"uint256"},{"internalType":"address","name":"supplier","type":"address"},{"internalType":"address","name":"createdBy","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"enum VukaChainAdvisory.PurchaseOrderStatus","name":"status","type":"uint8"},{"internalType":"uint256","name":"carbonEmissions","type":"uint256"},{"internalType":"uint256","name":"timestamp","type":"uint256"}],"internalType":"struct VukaChainAdvisory.PurchaseOrder","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},
    {"inputs":[{"internalType":"address","name":"_supplierAddress","type":"address"}],"name":"getSupplier","outputs":[{"components":[{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"location","type":"string"},{"internalType":"enum VukaChainAdvisory.SupplierStatus","name":"status","type":"uint8"}],"internalType":"struct VukaChainAdvisory.Supplier","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},
    {"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"logisticsTeam","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},
    {"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},
    {"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"procurementManagers","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},
    {"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"purchaseOrders","outputs":[{"internalType":"uint256","name":"id","type":"uint256"},{"internalType":"address","name":"supplier","type":"address"},{"internalType":"address","name":"createdBy","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"enum VukaChainAdvisory.PurchaseOrderStatus","name":"status","type":"uint8"},{"internalType":"uint256","name":"carbonEmissions","type":"uint256"},{"internalType":"uint256","name":"timestamp","type":"uint256"}],"stateMutability":"view","type":"function"},
    {"inputs":[{"internalType":"uint256","name":"_poId","type":"uint256"}],"name":"recordDispatch","outputs":[],"stateMutability":"nonpayable","type":"function"},
    {"inputs":[{"internalType":"address","name":"_supplierAddress","type":"address"},{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_location","type":"string"}],"name":"registerSupplier","outputs":[],"stateMutability":"nonpayable","type":"function"},
    {"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"suppliers","outputs":[{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"location","type":"string"},{"internalType":"enum VukaChainAdvisory.SupplierStatus","name":"status","type":"uint8"}],"stateMutability":"view","type":"function"},
    {"inputs":[{"internalType":"address","name":"_supplierAddress","type":"address"}],"name":"verifySupplier","outputs":[],"stateMutability":"nonpayable","type":"function"}
]
