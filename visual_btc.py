import streamlit as st
import hashlib
import ecdsa
import base58
import qrcode
from io import BytesIO
import numpy as np
import random

def create_qr_code(data):
    """Creates a QR code and returns it as an image"""
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf

def private_key_to_wif(private_key_hex, compressed=True):
    """Converts a private key in hexadecimal format to WIF"""
    # Add mainnet prefix (0x80)
    extended_key = '80' + private_key_hex
    
    # Add compression flag if needed
    if compressed:
        extended_key += '01'
    
    # Calculate double SHA256
    first_sha = hashlib.sha256(bytes.fromhex(extended_key)).hexdigest()
    second_sha = hashlib.sha256(bytes.fromhex(first_sha)).hexdigest()
    
    # Take first 4 bytes as checksum
    checksum = second_sha[:8]
    
    # Concatenate and encode in base58
    final_key = extended_key + checksum
    wif = base58.b58encode(bytes.fromhex(final_key)).decode()
    
    return wif

def private_key_to_public_key(private_key_hex, compressed=True):
    """Converts private key to public key"""
    sk = ecdsa.SigningKey.from_string(bytes.fromhex(private_key_hex), curve=ecdsa.SECP256k1)
    public_key = sk.verifying_key.to_string()
    
    if compressed:
        # Compressed public key format
        x = int.from_bytes(public_key[:32], 'big')
        y = int.from_bytes(public_key[32:], 'big')
        prefix = '02' if y % 2 == 0 else '03'
        return prefix + x.to_bytes(32, 'big').hex()
    else:
        # Uncompressed public key format
        return '04' + public_key.hex()

def private_key_to_address(private_key_hex, compressed=True):
    """Converts private key to Bitcoin address"""
    public_key_hex = private_key_to_public_key(private_key_hex, compressed)
    
    # SHA256 hash of public key
    sha256_pk = hashlib.sha256(bytes.fromhex(public_key_hex)).digest()
    
    # RIPEMD160 hash
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(sha256_pk)
    public_key_hash = ripemd160.digest()
    
    # Add network prefix (0x00 for mainnet)
    versioned_payload = b'\x00' + public_key_hash
    
    # Double SHA256 for checksum
    checksum = hashlib.sha256(hashlib.sha256(versioned_payload).digest()).digest()[:4]
    
    # Encode in base58
    address = base58.b58encode(versioned_payload + checksum).decode()
    
    return address

def grid_to_hex(grid):
    """Converts bit grid to hexadecimal"""
    binary_string = ''.join(['1' if cell else '0' for row in grid for cell in row])
    hex_value = hex(int(binary_string, 2))[2:].upper().zfill(64)
    return hex_value

def hex_to_grid(hex_string):
    """Converts hexadecimal to bit grid"""
    binary_string = bin(int(hex_string, 16))[2:].zfill(256)
    grid = []
    for i in range(16):
        row = []
        for j in range(16):
            bit_index = i * 16 + j
            row.append(binary_string[bit_index] == '1')
        grid.append(row)
    return grid

# Page configuration
st.set_page_config(
    page_title="VisualBTC - Visual Bitcoin Private Key Generator",
    page_icon="₿",
    layout="wide"
)

st.title("₿️ VisualBTC - Visual Bitcoin Private Key Generator")
st.markdown("### Create Bitcoin private keys visually using a 16x16 grid")

# Initialize session state
if 'grid' not in st.session_state:
    st.session_state.grid = [[False for _ in range(16)] for _ in range(16)]
if 'compressed' not in st.session_state:
    st.session_state.compressed = True

# Create columns for controls
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("🎲 Random", help="Generate random pattern"):
        st.session_state.grid = [[random.choice([True, False]) for _ in range(16)] for _ in range(16)]
        st.rerun()

with col2:
    if st.button("❌ Clear", help="Clear entire grid"):
        st.session_state.grid = [[False for _ in range(16)] for _ in range(16)]
        st.rerun()

with col3:
    if st.button("🔄 Inverse", help="Invert all bits"):
        st.session_state.grid = [[not cell for cell in row] for row in st.session_state.grid]
        st.rerun()

with col4:
    if st.button("↩️ Rotate", help="Rotate grid 90 degrees"):
        # Rotate 90 degrees clockwise
        new_grid = [[False for _ in range(16)] for _ in range(16)]
        for i in range(16):
            for j in range(16):
                new_grid[j][15-i] = st.session_state.grid[i][j]
        st.session_state.grid = new_grid
        st.rerun()

with col5:
    if st.button("🪙 Flip Coin", help="Fill random empty cell"):
        empty_cells = []
        for i in range(16):
            for j in range(16):
                if not st.session_state.grid[i][j]:
                    empty_cells.append((i, j))
        if empty_cells:
            i, j = random.choice(empty_cells)
            st.session_state.grid[i][j] = True
            st.rerun()

# Compression toggle
st.markdown("---")
col_comp1, col_comp2, col_comp3 = st.columns([2, 1, 2])
with col_comp2:
    compressed = st.toggle("🔐 Compressed Keys", value=st.session_state.compressed, help="Toggle between compressed and uncompressed keys")
    if compressed != st.session_state.compressed:
        st.session_state.compressed = compressed
        st.rerun()

st.markdown("---")

# Create interactive grid with smaller cells
st.markdown("### Visual Grid (16x16 = 256 bits)")
st.markdown("Click cells to toggle bits. **Black = 1, White = 0**")

# Custom CSS for smaller grid
st.markdown("""
<style>
.grid-container {
    display: grid;
    grid-template-columns: repeat(16, 20px);
    grid-template-rows: repeat(16, 20px);
    gap: 1px;
    justify-content: center;
    margin: 20px 0;
}
.grid-cell {
    width: 20px;
    height: 20px;
    border: 1px solid #ccc;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
}
.grid-cell-active {
    background-color: #000;
    color: white;
}
.grid-cell-inactive {
    background-color: #fff;
    color: black;
}
</style>
""", unsafe_allow_html=True)

# Create the grid using columns but with smaller spacing
grid_cols = st.columns(16, gap="small")
for i in range(16):
    for j in range(16):
        col_idx = j
        with grid_cols[col_idx]:
            if st.session_state.grid[i][j]:
                if st.button("⬛", key=f"cell_{i}_{j}", help=f"Row {i+1}, Col {j+1} - Bit: 1", 
                           use_container_width=True):
                    st.session_state.grid[i][j] = False
                    st.rerun()
            else:
                if st.button("⬜", key=f"cell_{i}_{j}", help=f"Row {i+1}, Col {j+1} - Bit: 0", 
                           use_container_width=True):
                    st.session_state.grid[i][j] = True
                    st.rerun()

st.markdown("---")

# Generate private key and other data
hex_key = grid_to_hex(st.session_state.grid)

if hex_key != '0' * 64:  # Only generate if at least one bit is active
    try:
        wif_key = private_key_to_wif(hex_key, compressed=st.session_state.compressed)
        public_key = private_key_to_public_key(hex_key, compressed=st.session_state.compressed)
        btc_address = private_key_to_address(hex_key, compressed=st.session_state.compressed)
        
        # Show results
        st.markdown("### 🔐 Generated Private Key and Address")
        
        # Create tabs for better organization
        tab1, tab2 = st.tabs(["📝 Keys & Address", "📲 QR Codes"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Private Key (HEX):**")
                st.code(hex_key, language="text")
                
                st.markdown("**Private Key (WIF):**")
                st.code(wif_key, language="text")
                
                st.markdown("**Bitcoin Address:**")
                st.code(btc_address, language="text")
            
            with col2:
                key_type = "Compressed" if st.session_state.compressed else "Uncompressed"
                st.markdown(f"**Public Key ({key_type}):**")
                st.code(public_key, language="text")
                
                st.markdown("**Key Information:**")
                st.write(f"🔑 **Type:** {key_type}")
                st.write(f"📏 **Public Key Length:** {len(public_key)} chars")
                st.write(f"📍 **Address Type:** Legacy (P2PKH)")
        
        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**QR Code - Private Key (WIF):**")
                qr_private = create_qr_code(wif_key)
                st.image(qr_private, width=250)
                
                # Download button for private key QR
                st.download_button(
                    label="📥 Download Private Key QR",
                    data=qr_private.getvalue(),
                    file_name=f"private_key_qr_{hex_key[:8]}.png",
                    mime="image/png"
                )
            
            with col2:
                st.markdown("**QR Code - Bitcoin Address:**")
                qr_address = create_qr_code(btc_address)
                st.image(qr_address, width=250)
                
                # Download button for address QR
                st.download_button(
                    label="📥 Download Address QR",
                    data=qr_address.getvalue(),
                    file_name=f"address_qr_{btc_address[:8]}.png",
                    mime="image/png"
                )
        
        # Statistics
        st.markdown("### 📊 Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        total_bits = sum(sum(row) for row in st.session_state.grid)
        entropy_level = 'High' if total_bits > 100 else 'Medium' if total_bits > 50 else 'Low'
        
        with col1:
            st.metric("Active Bits", f"{total_bits}/256")
        
        with col2:
            st.metric("Percentage", f"{total_bits/256*100:.1f}%")
        
        with col3:
            st.metric("Entropy Level", entropy_level)
        
        with col4:
            st.metric("Key Format", "Compressed" if st.session_state.compressed else "Uncompressed")
        
    except Exception as e:
        st.error(f"Error generating key: {str(e)}")
else:
    st.info("⚠️ Activate at least one bit in the grid to generate a valid private key.")

# Security information
st.markdown("---")
st.markdown("### ⚠️ Important Security Information")
st.warning(
    "**WARNING:** This is an educational example. For real Bitcoin use:\n\n"
    "• Ensure sufficient entropy (randomness)\n"
    "• Use an offline and secure environment\n"
    "• Never share your private key\n"
    "• Make secure paper backups\n"
    "• Consider using proven wallets for production key generation"
)

st.markdown("### 📖 How it works")
st.markdown(
    "1. **Visual Grid:** Each cell represents one bit (0 or 1) of your 256-bit private key\n"
    "2. **Interaction:** Click cells to create your unique pattern\n"
    "3. **Generation:** Bits are converted to a hexadecimal private key\n"
    "4. **Conversion:** Key is converted to WIF format and Bitcoin address is generated\n"
    "5. **QR Codes:** QR codes are created for easy use with mobile wallets\n"
    "6. **Compression:** Toggle between compressed and uncompressed key formats"
)

# Key format explanation
st.markdown("### 🔑 Key Format Differences")
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Compressed Keys:**")
    st.markdown("• Public key: 33 bytes (66 hex chars)")
    st.markdown("• Address starts with '1'")
    st.markdown("• More efficient, recommended")
    st.markdown("• WIF starts with 'K' or 'L'")

with col2:
    st.markdown("**Uncompressed Keys:**")
    st.markdown("• Public key: 65 bytes (130 hex chars)")
    st.markdown("• Address starts with '1'")
    st.markdown("• Legacy format")
    st.markdown("• WIF starts with '5'")