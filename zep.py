# pip install streamlit web3 streamlit-js-eval
import streamlit as st
import json
from streamlit_js_eval import streamlit_js_eval

try:
    from web3 import Web3
except ImportError:
    import web3
    Web3 = web3.Web3

# ================================
# CONFIG - ALREADY FILLED IN
# ================================

class Config:
    RPC_URL = "https://rpc.sepolia.org"
    CONTRACT_ADDRESS = "0xc9F186B05aBb47292D1D3D26169667ec12B064CA"
    LOGO_PATH = "logo.png"
    APP_NAME = "Ithuma Supply Chain"
    APP_TAGLINE = "Decentralized Logistics & Procurement"
    APP_DESCRIPTION = "Manage orders, suppliers, couriers and sustainability on-chain."
    ORDER_STATUS = {0: "Pending", 1: "Approved", 2: "Confirmed", 3: "Dispatched", 4: "In Transit", 5: "Delivered", 6: "Cancelled"}
    SUPPLIER_STATUS = {0: "Unregistered", 1: "Pending", 2: "Verified", 3: "Suspended"}
    COURIER_STATUS = {0: "Offline", 1: "Available", 2: "Busy", 3: "Suspended"}

config = Config()

# ================================
# CONTRACT ABI
# ================================

CONTRACT_ABI = [
    {"inputs":[{"internalType":"address","name":"_addr","type":"address"}],"name":"addLogistics","outputs":[],"stateMutability":"nonpayable","type":"function"},
    {"inputs":[{"internalType":"address","name":"_addr","type":"address"}],"name":"addProcurementManager","outputs":[],"stateMutability":"nonpayable","type":"function"},
    {"inputs":[{"internalType":"uint256","name":"_id","type":"uint256"}],"name":"approveOrder","outputs":[],"stateMutability":"nonpayable","type":"function"},
    {"inputs":[{"internalType":"uint256","name":"_id","type":"uint256"},{"internalType":"address","name":"_courier","type":"address"}],"name":"assignCourier","outputs":[],"stateMutability":"nonpayable","type":"function"},
    {"inputs":[{"internalType":"uint256","name":"_id","type":"uint256"}],"name":"confirmBySupplier","outputs":[],"stateMutability":"nonpayable","type":"function"},
    {"inputs":[{"internalType":"uint256","name":"_id","type":"uint256"},{"internalType":"uint256","name":"_emissions","type":"uint256"}],"name":"confirmDelivery","outputs":[],"stateMutability":"nonpayable","type":"function"},
    {"inputs":[],"stateMutability":"nonpayable","type":"constructor"},
    {"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint256","name":"orderId","type":"uint256"},{"indexed":False,"internalType":"address","name":"courier","type":"address"}],"name":"CourierAssigned","type":"event"},
    {"anonymous":False,"inputs":[{"indexed":False,"internalType":"address","name":"courier","type":"address"}],"name":"CourierRegistered","type":"event"},
    {"inputs":[{"internalType":"address","name":"_supplier","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"createOrder","outputs":[],"stateMutability":"nonpayable","type":"function"},
    {"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint256","name":"orderId","type":"uint256"}],"name":"DeliveryConfirmed","type":"event"},
    {"inputs":[{"internalType":"uint256","name":"_id","type":"uint256"}],"name":"dispatchGoods","outputs":[],"stateMutability":"nonpayable","type":"function"},
    {"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint256","name":"orderId","type":"uint256"}],"name":"GoodsDispatched","type":"event"},
    {"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint256","name":"orderId","type":"uint256"}],"name":"OrderApproved","type":"event"},
    {"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint256","name":"orderId","type":"uint256"}],"name":"OrderCreated","type":"event"},
    {"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint256","name":"orderId","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"PaymentReleased","type":"event"},
    {"inputs":[{"internalType":"address","name":"_addr","type":"address"},{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_vehicle","type":"string"}],"name":"registerCourier","outputs":[],"stateMutability":"nonpayable","type":"function"},
    {"inputs":[{"internalType":"address","name":"_addr","type":"address"},{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_location","type":"string"}],"name":"registerSupplier","outputs":[],"stateMutability":"nonpayable","type":"function"},
    {"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint256","name":"orderId","type":"uint256"}],"name":"SupplierConfirmed","type":"event"},
    {"anonymous":False,"inputs":[{"indexed":False,"internalType":"address","name":"supplier","type":"address"}],"name":"SupplierRegistered","type":"event"},
    {"anonymous":False,"inputs":[{"indexed":False,"internalType":"address","name":"supplier","type":"address"}],"name":"SupplierVerified","type":"event"},
    {"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint256","name":"orderId","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"emissions","type":"uint256"}],"name":"SustainabilityRecorded","type":"event"},
    {"inputs":[{"internalType":"address","name":"_addr","type":"address"}],"name":"verifySupplier","outputs":[],"stateMutability":"nonpayable","type":"function"},
    {"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"couriers","outputs":[{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"vehicleType","type":"string"},{"internalType":"enum IthumaApp.CourierStatus","name":"status","type":"uint8"}],"stateMutability":"view","type":"function"},
    {"inputs":[{"internalType":"address","name":"_addr","type":"address"}],"name":"getCourier","outputs":[{"components":[{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"vehicleType","type":"string"},{"internalType":"enum IthumaApp.CourierStatus","name":"status","type":"uint8"}],"internalType":"struct IthumaApp.Courier","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},
    {"inputs":[{"internalType":"uint256","name":"_id","type":"uint256"}],"name":"getOrder","outputs":[{"components":[{"internalType":"uint256","name":"id","type":"uint256"},{"internalType":"address","name":"supplier","type":"address"},{"internalType":"address","name":"courier","type":"address"},{"internalType":"address","name":"createdBy","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"carbonEmissions","type":"uint256"},{"internalType":"enum IthumaApp.OrderStatus","name":"status","type":"uint8"},{"internalType":"uint256","name":"timestamp","type":"uint256"}],"internalType":"struct IthumaApp.Order","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},
    {"inputs":[{"internalType":"address","name":"_addr","type":"address"}],"name":"getSupplier","outputs":[{"components":[{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"location","type":"string"},{"internalType":"enum IthumaApp.SupplierStatus","name":"status","type":"uint8"}],"internalType":"struct IthumaApp.Supplier","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},
    {"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"logisticsTeam","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},
    {"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"orders","outputs":[{"internalType":"uint256","name":"id","type":"uint256"},{"internalType":"address","name":"supplier","type":"address"},{"internalType":"address","name":"courier","type":"address"},{"internalType":"address","name":"createdBy","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"carbonEmissions","type":"uint256"},{"internalType":"enum IthumaApp.OrderStatus","name":"status","type":"uint8"},{"internalType":"uint256","name":"timestamp","type":"uint256"}],"stateMutability":"view","type":"function"},
    {"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},
    {"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"procurementManagers","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},
    {"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"suppliers","outputs":[{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"location","type":"string"},{"internalType":"enum IthumaApp.SupplierStatus","name":"status","type":"uint8"}],"stateMutability":"view","type":"function"}
]

# ================================
# WEB3 SETUP
# ================================

w3 = Web3(Web3.HTTPProvider(config.RPC_URL))

contract = w3.eth.contract(
    address=w3.to_checksum_address(config.CONTRACT_ADDRESS),
    abi=CONTRACT_ABI
)

# ================================
# HEADER
# ================================

try:
    st.image(config.LOGO_PATH, width=120)
except Exception:
    st.title(config.APP_NAME)

st.caption(config.APP_TAGLINE)
st.write(config.APP_DESCRIPTION)

# ================================
# METAMASK WALLET
# ================================

wallet = streamlit_js_eval(
    js_expressions="""
    async () => {
        if (window.ethereum) {
            const accounts = await window.ethereum.request({ method: 'eth_accounts' });
            return accounts.length > 0 ? accounts[0] : None;
        }
        return None;
    }
    """,
    key="wallet_check"
)

if not wallet:
    if st.button("Connect Wallet"):
        streamlit_js_eval(
            js_expressions="""
            async () => {
                if (window.ethereum) {
                    await window.ethereum.request({ method: 'eth_requestAccounts' });
                    window.location.reload();
                }
            }
            """,
            key="connect_wallet_btn"
        )
    st.warning("Please connect your MetaMask wallet to continue.")
    st.stop()

st.sidebar.write("Wallet:", wallet)

# ================================
# NAVIGATION
# ================================

page = st.sidebar.selectbox("Navigation", [
    "Dashboard",
    "Orders",
    "Suppliers",
    "Couriers",
    "Admin"
])

# ================================
# HELPER: Build TX for MetaMask
# ================================

def build_tx_json(fn_name, args_list, wallet_addr):
    """Encode function call and return JSON-serialized tx object for JS injection."""
    tx_data = contract.encodeABI(fn_name=fn_name, args=args_list)
    tx_obj = {
        "to": config.CONTRACT_ADDRESS,
        "from": wallet_addr,
        "data": tx_data,
        "gas": "0x186A0"  # 100,000 gas
    }
    return json.dumps(tx_obj)

# ================================
# DASHBOARD
# ================================

if page == "Dashboard":
    st.subheader("System Overview")

    col1, col2 = st.columns(2)
    
    with col1:
        try:
            owner = contract.functions.owner().call()
            st.info(f"Contract Owner: `{owner}`")
        except Exception as e:
            st.error(f"Contract read failed: {e}")
    
    with col2:
        try:
            is_manager = contract.functions.procurementManagers(wallet).call()
            is_logistics = contract.functions.logisticsTeam(wallet).call()
            st.write("Your Roles:")
            st.write("- Procurement Manager:", "Yes" if is_manager else "No")
            st.write("- Logistics Team:", "Yes" if is_logistics else "No")
        except Exception as e:
            st.error(f"Role check failed: {e}")

# ================================
# ORDERS
# ================================

elif page == "Orders":
    st.subheader("Order Management")

    tab1, tab2 = st.tabs(["Lookup Order", "Create Order"])

    with tab1:
        order_id = st.number_input("Order ID", min_value=1, step=1, value=1)

        if st.button("Check Order"):
            try:
                order = contract.functions.getOrder(int(order_id)).call()

                st.success("Order loaded")
                c1, c2 = st.columns(2)
                with c1:
                    st.write("**Order ID:**", order[0])
                    st.write("**Supplier:**", order[1])
                    st.write("**Courier:**", order[2])
                    st.write("**Created By:**", order[3])
                with c2:
                    st.write("**Amount:**", order[4])
                    st.write("**Carbon Emissions:**", order[5])
                    st.write("**Status:**", config.ORDER_STATUS.get(order[6], f"Unknown ({order[6]})"))
                    st.write("**Timestamp:**", order[7])
            except Exception as e:
                st.error(f"Order not found: {e}")

    with tab2:
        supplier = st.text_input("Supplier Address", key="create_supplier")
        amount = st.number_input("Amount (wei)", min_value=0, step=1, value=0, key="create_amount")

        if st.button("Create Order"):
            if not supplier or not Web3.is_address(supplier):
                st.error("Please enter a valid supplier address")
            else:
                tx_json = build_tx_json("createOrder", [w3.to_checksum_address(supplier), int(amount)], wallet)

                tx_hash = streamlit_js_eval(
                    js_expressions=f"""
                    async () => {{
                        return await window.ethereum.request({{
                            method: 'eth_sendTransaction',
                            params: [{tx_json}]
                        }});
                    }}
                    """,
                    key=f"tx_create_order_{int(amount)}_{supplier[-6:]}"
                )

                if tx_hash:
                    st.success(f"Tx sent: https://sepolia.etherscan.io/tx/{tx_hash}")

# ================================
# SUPPLIERS
# ================================

elif page == "Suppliers":
    st.subheader("Supplier Management")

    tab1, tab2 = st.tabs(["Lookup Supplier", "Register Supplier"])

    with tab1:
        addr = st.text_input("Supplier Address", key="lookup_supplier")

        if st.button("Check Supplier"):
            if not addr or not Web3.is_address(addr):
                st.error("Please enter a valid address")
            else:
                try:
                    supplier = contract.functions.getSupplier(w3.to_checksum_address(addr)).call()
                    st.success("Supplier found")
                    st.write("**Name:**", supplier[0])
                    st.write("**Location:**", supplier[1])
                    st.write("**Status:**", config.SUPPLIER_STATUS.get(supplier[2], f"Unknown ({supplier[2]})"))
                except Exception as e:
                    st.error(f"Supplier not found: {e}")

    with tab2:
        st.write("Register a new supplier (requires appropriate role)")
        reg_addr = st.text_input("Supplier Wallet Address", key="reg_supplier_addr")
        reg_name = st.text_input("Supplier Name", key="reg_supplier_name")
        reg_location = st.text_input("Location", key="reg_supplier_loc")

        if st.button("Register Supplier"):
            if not reg_addr or not Web3.is_address(reg_addr):
                st.error("Please enter a valid address")
            elif not reg_name or not reg_location:
                st.error("Name and location are required")
            else:
                tx_json = build_tx_json("registerSupplier", [w3.to_checksum_address(reg_addr), reg_name, reg_location], wallet)

                tx_hash = streamlit_js_eval(
                    js_expressions=f"""
                    async () => {{
                        return await window.ethereum.request({{
                            method: 'eth_sendTransaction',
                            params: [{tx_json}]
                        }});
                    }}
                    """,
                    key=f"tx_reg_supplier_{reg_addr[-6:]}"
                )

                if tx_hash:
                    st.success(f"Tx sent: https://sepolia.etherscan.io/tx/{tx_hash}")

# ================================
# COURIERS
# ================================

elif page == "Couriers":
    st.subheader("Courier Management")

    tab1, tab2 = st.tabs(["Lookup Courier", "Register Courier"])

    with tab1:
        addr = st.text_input("Courier Address", key="lookup_courier")

        if st.button("Check Courier"):
            if not addr or not Web3.is_address(addr):
                st.error("Please enter a valid address")
            else:
                try:
                    courier = contract.functions.getCourier(w3.to_checksum_address(addr)).call()
                    st.success("Courier found")
                    st.write("**Name:**", courier[0])
                    st.write("**Vehicle:**", courier[1])
                    st.write("**Status:**", config.COURIER_STATUS.get(courier[2], f"Unknown ({courier[2]})"))
                except Exception as e:
                    st.error(f"Courier not found: {e}")

    with tab2:
        st.write("Register a new courier (requires appropriate role)")
        reg_addr = st.text_input("Courier Wallet Address", key="reg_courier_addr")
        reg_name = st.text_input("Courier Name", key="reg_courier_name")
        reg_vehicle = st.text_input("Vehicle Type", key="reg_courier_vehicle")

        if st.button("Register Courier"):
            if not reg_addr or not Web3.is_address(reg_addr):
                st.error("Please enter a valid address")
            elif not reg_name or not reg_vehicle:
                st.error("Name and vehicle type are required")
            else:
                tx_json = build_tx_json("registerCourier", [w3.to_checksum_address(reg_addr), reg_name, reg_vehicle], wallet)

                tx_hash = streamlit_js_eval(
                    js_expressions=f"""
                    async () => {{
                        return await window.ethereum.request({{
                            method: 'eth_sendTransaction',
                            params: [{tx_json}]
                        }});
                    }}
                    """,
                    key=f"tx_reg_courier_{reg_addr[-6:]}"
                )

                if tx_hash:
                    st.success(f"Tx sent: https://sepolia.etherscan.io/tx/{tx_hash}")

# ================================
# ADMIN
# ================================

elif page == "Admin":
    st.subheader("Admin Panel")

    addr = st.text_input("Wallet Address", key="admin_addr")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Add Procurement Manager"):
            if not addr or not Web3.is_address(addr):
                st.error("Please enter a valid address")
            else:
                tx_json = build_tx_json("addProcurementManager", [w3.to_checksum_address(addr)], wallet)

                tx_hash = streamlit_js_eval(
                    js_expressions=f"""
                    async () => {{
                        return await window.ethereum.request({{
                            method: 'eth_sendTransaction',
                            params: [{tx_json}]
                        }});
                    }}
                    """,
                    key=f"tx_proc_mgr_{addr[-6:]}"
                )

                if tx_hash:
                    st.success(f"Tx: https://sepolia.etherscan.io/tx/{tx_hash}")

    with col2:
        if st.button("Add Logistics"):
            if not addr or not Web3.is_address(addr):
                st.error("Please enter a valid address")
            else:
                tx_json = build_tx_json("addLogistics", [w3.to_checksum_address(addr)], wallet)

                tx_hash = streamlit_js_eval(
                    js_expressions=f"""
                    async () => {{
                        return await window.ethereum.request({{
                            method: 'eth_sendTransaction',
                            params: [{tx_json}]
                        }});
                    }}
                    """,
                    key=f"tx_logistics_{addr[-6:]}"
                )

                if tx_hash:
                    st.success(f"Tx: https://sepolia.etherscan.io/tx/{tx_hash}")

    with col3:
        if st.button("Verify Supplier"):
            if not addr or not Web3.is_address(addr):
                st.error("Please enter a valid address")
            else:
                tx_json = build_tx_json("verifySupplier", [w3.to_checksum_address(addr)], wallet)

                tx_hash = streamlit_js_eval(
                    js_expressions=f"""
                    async () => {{
                        return await window.ethereum.request({{
                            method: 'eth_sendTransaction',
                            params: [{tx_json}]
                        }});
                    }}
                    """,
                    key=f"tx_verify_supplier_{addr[-6:]}"
                )

                if tx_hash:
                    st.success(f"Tx: https://sepolia.etherscan.io/tx/{tx_hash}")
