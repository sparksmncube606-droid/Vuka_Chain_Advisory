import streamlit as st
from web3 import Web3
from streamlit_js_eval import streamlit_js_eval
import config

# --- 1. BLOCKCHAIN INITIALIZATION ---
# Connect to the Sepolia network using our public endpoint so we can read data freely
w3 = Web3(Web3.HTTPProvider(config.RPC_URL))
# Create a local representation of our smart contract
contract = w3.eth.contract(address=config.CONTRACT_ADDRESS, abi=config.CONTRACT_ABI)

# --- 2. USER INTERFACE HEADER ---
st.set_page_config(page_title=config.APP_NAME, layout="wide")

try:
    # Attempt to load a real logo image for a professional feel
    st.image(config.LOGO_PATH, width=150)
except:
    # Fallback to plain text if the image file is missing
    st.title(f"🏢 {config.APP_NAME}")
st.caption(config.TAGLINE)
st.divider()

# --- 3. METAMASK SECURITY & BRIDGE ---
st.sidebar.header("🔐 User Authentication")
# Inject JavaScript to check if a wallet (like MetaMask) is currently connected to the browser
wallet_address = streamlit_js_eval(js_expressions="window.ethereum ? window.ethereum.selectedAddress : null", key="wallet")
# Check which network the wallet is connected to
chain_id = streamlit_js_eval(js_expressions="window.ethereum ? window.ethereum.chainId : null", key="chain")

is_ready = False
if not wallet_address:
    st.sidebar.warning("Please connect your Web3 Wallet to interact.")
    if st.sidebar.button("Connect MetaMask"):
        # Prompt MetaMask to open and ask for user permission
        streamlit_js_eval(js_expressions="window.ethereum.request({ method: 'eth_requestAccounts' })")
else:
    # 0xaa36a7 is the hexadecimal representation of the Sepolia Chain ID (11155111)
    if chain_id != "0xaa36a7":
        st.sidebar.error(f"Wrong Network! Switch to Sepolia (ID: {config.CHAIN_ID}) in your wallet.")
    else:
        st.sidebar.success(f"Connected as: {wallet_address[:6]}...{wallet_address[-4:]}")
        is_ready = True

# --- 4. TRANSACTION HELPER ---
def send_transaction(func_name, *args):
    """Encodes a smart contract call and passes it to the browser for MetaMask to sign."""
    if not is_ready:
        st.error("Cannot perform action: Wallet not connected or on wrong network.")
        return
        
    try:
        # Checksum ensures the address is mathematically valid for Ethereum
        user_addr = w3.to_checksum_address(wallet_address)
        # Prepare the raw data of the function call (Intent)
        tx_data = contract.encodeABI(fn_name=func_name, args=args)
        
        # Build JavaScript to trigger a transaction popup directly in the user's browser
        js_code = f"""
        window.ethereum.request({{
            method: 'eth_sendTransaction',
            params: [{{
                from: '{user_addr}',
                to: '{config.CONTRACT_ADDRESS}',
                data: '{tx_data}'
            }}]
        }}).then((hash) => alert('Transaction Sent! View on Etherscan: ' + hash))
          .catch((err) => alert('Transaction Failed or Rejected by user.'));
        """
        st.info("Check your browser extension to confirm the transaction.")
        streamlit_js_eval(js_expressions=js_code, key=f"tx_{func_name}")
    except Exception as e:
        st.error(f"Failed to build transaction: {e}")

# --- 5. NAVIGATION ---
menu = st.sidebar.radio(
    "Main Menu", 
    [
        "Analytics Dashboard", 
        "Record Lookup",
        "System Administration", 
        "Procurement Actions", 
        "Supplier Portal",
        "Logistics & Delivery"
    ]
)

# --- 6. PAGE ROUTING & LOGIC ---

if menu == "Analytics Dashboard":
    st.subheader("📊 Network & Contract Overview")
    with st.spinner("Syncing with Sepolia Testnet..."):
        try:
            # Read public variables directly from the contract
            owner_address = contract.functions.owner().call()
            
            col1, col2 = st.columns(2)
            col1.metric("Contract Administrator", f"{owner_address[:8]}...")
            col2.metric("Network Status", "Online (Sepolia)")
            
            st.info("The dashboard is currently reading live data securely from the blockchain.")
        except Exception as e:
            st.error("Failed to connect to the smart contract. Verify the configuration.")

elif menu == "Record Lookup":
    st.subheader("🔍 Blockchain Explorer Tools")
    
    tab1, tab2 = st.tabs(["Find Purchase Order", "Find Supplier"])
    
    with tab1:
        st.write("Retrieve the immutable history of a specific order.")
        po_id = st.number_input("Purchase Order ID Number", min_value=1, step=1)
        if st.button("Search Order"):
            with st.spinner("Searching blockchain ledger..."):
                try:
                    # Fetching structured data tuple from the contract
                    po_data = contract.functions.getPurchaseOrder(po_id).call()
                    if po_data[1] == "0x0000000000000000000000000000000000000000":
                        st.warning("No order found with this ID.")
                    else:
                        st.success(f"Order #{po_data[0]} Details")
                        st.write(f"**Supplier:** {po_data[1]}")
                        st.write(f"**Created By:** {po_data[2]}")
                        st.write(f"**Amount:** {po_data[3]}")
                        st.write(f"**Status:** {config.PURCHASE_ORDER_STATUS.get(po_data[4], 'Unknown')}")
                        st.write(f"**Carbon Footprint:** {po_data[5]} CO2e")
                except Exception as e:
                    st.error(f"Error reading order: {e}")

    with tab2:
        st.write("Verify a supplier's status and sustainability certification.")
        sup_address = st.text_input("Supplier Wallet Address", help="e.g., 0x123...")
        if st.button("Search Supplier"):
            try:
                sup_addr_checksum = w3.to_checksum_address(sup_address)
                sup_data = contract.functions.getSupplier(sup_addr_checksum).call()
                if not sup_data[0]:
                    st.warning("Supplier not registered on the network.")
                else:
                    st.success("Supplier Found")
                    st.write(f"**Company Name:** {sup_data[0]}")
                    st.write(f"**Location:** {sup_data[1]}")
                    st.write(f"**Verification:** {config.SUPPLIER_STATUS.get(sup_data[2], 'Unknown')}")
            except Exception as e:
                st.error("Invalid address format or network error.")

elif menu == "System Administration":
    st.subheader("⚙️ Administrator Console")
    st.caption("Restricted: Only the contract owner can execute these commands.")
    
    with st.expander("Register New Supplier", expanded=True):
        with st.form("register_supplier"):
            sup_addr = st.text_input("Supplier Wallet Address", help="Must be an Ethereum address (0x...)")
            sup_name = st.text_input("Company Name")
            sup_location = st.text_input("Geographic Location")
            if st.form_submit_button("Register Supplier"):
                try:
                    send_transaction("registerSupplier", w3.to_checksum_address(sup_addr), sup_name, sup_location)
                except Exception as e:
                    st.error("Invalid input.")

    with st.expander("Verify Supplier Credentials"):
        with st.form("verify_supplier"):
            v_addr = st.text_input("Supplier Wallet Address to Verify")
            if st.form_submit_button("Grant Verification Status"):
                try:
                    send_transaction("verifySupplier", w3.to_checksum_address(v_addr))
                except Exception as e:
                    st.error("Invalid input.")
                    
    with st.expander("Manage Roles (Add Personnel)"):
        with st.form("add_roles"):
            role_type = st.radio("Select Role to Assign", ["Procurement Manager", "Logistics Team"])
            emp_addr = st.text_input("Employee Wallet Address")
            if st.form_submit_button("Assign Role"):
                try:
                    emp_addr_clean = w3.to_checksum_address(emp_addr)
                    if role_type == "Procurement Manager":
                        send_transaction("addProcurementManager", emp_addr_clean)
                    else:
                        send_transaction("addLogisticsTeam", emp_addr_clean)
                except Exception as e:
                    st.error("Invalid address.")

elif menu == "Procurement Actions":
    st.subheader("💼 Procurement Dashboard")
    st.caption("Restricted: For Authorized Procurement Managers Only.")
    
    with st.form("create_po"):
        st.write("Draft New Purchase Order")
        po_supplier = st.text_input("Assigned Supplier Wallet", help="Supplier must be registered and verified.")
        po_amount = st.number_input("Order Amount (Wei)", min_value=0, step=1000)
        if st.form_submit_button("Submit Draft Order"):
            try:
                send_transaction("createPurchaseOrder", w3.to_checksum_address(po_supplier), int(po_amount))
            except Exception as e:
                st.error("Invalid address format.")

    with st.form("approve_po"):
        st.write("Approve Pending Order")
        app_po_id = st.number_input("Order ID Number", min_value=1, step=1)
        if st.form_submit_button("Sign Approval"):
            send_transaction("approvePurchaseOrder", int(app_po_id))

elif menu == "Supplier Portal":
    st.subheader("🏭 Supplier Operations Center")
    st.caption("Restricted: For the Supplier assigned to the specific order.")
    
    with st.form("confirm_order"):
        st.write("Acknowledge & Confirm Order")
        conf_po_id = st.number_input("Order ID Number", min_value=1, step=1, key="sup_conf")
        if st.form_submit_button("Confirm Order"):
            send_transaction("confirmOrderBySupplier", int(conf_po_id))
            
    with st.form("dispatch_goods"):
        st.write("Log Goods Dispatch")
        disp_po_id = st.number_input("Order ID Number", min_value=1, step=1, key="sup_disp")
        if st.form_submit_button("Mark as Dispatched"):
            send_transaction("recordDispatch", int(disp_po_id))

elif menu == "Logistics & Delivery":
    st.subheader("🚚 Logistics Control Center")
    st.caption("Restricted: For Authorized Logistics Personnel Only.")
    
    with st.form("confirm_delivery"):
        st.write("Record Physical Delivery & Sustainability Metrics")
        del_po_id = st.number_input("Order ID Number", min_value=1, step=1)
        del_carbon = st.number_input("Measured Carbon Emissions (CO2e)", min_value=0, step=1)
        st.caption("Note: Confirming delivery will automatically trigger the payment release clause.")
        if st.form_submit_button("Confirm Delivery & Release Funds"):
            send_transaction("confirmDelivery", int(del_po_id), int(del_carbon))
