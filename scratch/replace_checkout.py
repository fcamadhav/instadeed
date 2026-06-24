with open("test_script.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Locate the handleOnlinePayment definition and body to replace
# We find: const handleOnlinePayment = async () => {
# and replace it with the parameter-friendly one.
# Let's write the exact search block and replacement.
search_pay_fn = """            const handleOnlinePayment = async () => {
                trackEvent('form_complete', activeTab, '');
                trackEvent('checkout_start', activeTab, '');
                trackEvent('payment_initiated', activeTab, '');
                const payload = getActiveDataPayload();
                try {
                    // Dynamic pricing based on document type
                    const docPrices = {
                        RENT: 300,
                        ATS: 300,
                        REG_RENT: 5000,
                        MUTATION: 4000,
                        KYA: 0,
                        GNIDA: 0,
                        GNIDA_REGISTRY: 10000,
                        GNIDA_PTM: 7500,
                        GNIDA_PACKAGE: 40000,
                        TM_APP: 2000,
                        TM48: 500,
                        NOIDA_TRANSFER: 2000,
                    };
                    const orderAmount = docPrices[activeTab] || 499;
                    // 1. Create order on backend
                    const res = await fetch(`${API_BASE}/create-order`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            amount: orderAmount,
                            service_type: activeTab,
                            customer_name: checkoutDetails.name || 'B2C Client',
                            customer_phone: checkoutDetails.phone || '0000000000',
                            customer_email: checkoutDetails.email || 'b2c@client.com',
                            form_data: payload
                        })
                    });
                    
                    if (!res.ok) throw new Error("Order creation failed");
                    const orderData = await res.json();
                    
                    // 2. Open Razorpay or simulate if mock
                    if (orderData.order_id.startsWith('MOCK_ORD_')) {
                        addToast("Processing mock payment...", 'info');
                        const verifyRes = await fetch(`${API_BASE}/verify-payment`, {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                                razorpay_order_id: orderData.order_id,
                                razorpay_payment_id: 'mock_pay_' + Math.random().toString(36).substr(2, 9),
                                razorpay_signature: 'mock_signature'
                            })
                        });
                        
                        if (verifyRes.ok) {
                            setShowCheckoutModal(false);
                            addToast("Payment successful! Opening document...", 'success');
                            triggerPrint();
                        }
                    } else {
                        // Load Razorpay Script dynamically and process payment
                        const loaded = await loadRazorpayScript();
                        if (!loaded) {
                            addToast("Failed to load Razorpay. Check connection.", 'error');
                            return;
                        }
                        
                        let razorpayKey = '';
                        try {
                            const cfgRes = await fetch(`${API_BASE}/api/config`);
                            if (cfgRes.ok) {
                                const cfg = await cfgRes.json();
                                razorpayKey = cfg.razorpay_key || '';
                            }
                        } catch(e) {}
                        if (!razorpayKey) { addToast("Payment configuration error. Please contact support.", 'error'); return; }
                        
                        const options = {
                            key: razorpayKey,
                            amount: orderData.amount,
                            currency: orderData.currency,
                            name: 'INSTADEED',
                            description: 'Legal Agreement Drafting Fee',
                            order_id: orderData.order_id,
                                            handler: async function (response) {
                                                try {
                                                    trackEvent('payment_complete', activeTab, response.razorpay_order_id);
                                                    const verifyRes = await fetch(`${API_BASE}/verify-payment`, {
                                                        method: 'POST',
                                                        headers: { 'Content-Type': 'application/json' },
                                                        body: JSON.stringify({
                                                            razorpay_order_id: response.razorpay_order_id,
                                                            razorpay_payment_id: response.razorpay_payment_id,
                                                            razorpay_signature: response.razorpay_signature
                                                        })
                                                    });
                                                    if (verifyRes.ok) {
                                                        setShowCheckoutModal(false);
                                                        addToast("Payment verified! Downloading document...", 'success');
                                                        triggerPrint();
                                                    } else {
                                                        addToast("Payment verification failed. Contact support.", 'error');
                                                    }
                                                } catch (e) {
                                                    addToast("Payment verification error: " + e.message, 'error');
                                                }
                                            },
                            prefill: {
                                name: checkoutDetails.name,
                                email: checkoutDetails.email,
                                contact: checkoutDetails.phone
                            },
                            theme: { color: '#2563EB' }
                        };
                        const rzp = new window.Razorpay(options);
                        rzp.open();
                    }
                } catch (e) {
                    console.error("Online checkout failed:", e);
                    addToast("Payment failed: " + e.message, 'error');
                }
            };"""

replace_pay_fn = """            const handleOnlinePayment = async (directDetails = null) => {
                trackEvent('form_complete', activeTab, '');
                trackEvent('checkout_start', activeTab, '');
                trackEvent('payment_initiated', activeTab, '');
                const payload = getActiveDataPayload();
                
                const customerName = directDetails ? directDetails.name : (checkoutDetails.name || 'B2C Client');
                const customerPhone = directDetails ? directDetails.phone : (checkoutDetails.phone || '0000000000');
                const customerEmail = directDetails ? directDetails.email : (checkoutDetails.email || 'b2c@client.com');
                
                try {
                    // Dynamic pricing based on document type
                    const docPrices = {
                        RENT: 300,
                        ATS: 300,
                        REG_RENT: 5000,
                        MUTATION: 4000,
                        KYA: 0,
                        GNIDA: 0,
                        GNIDA_REGISTRY: 10000,
                        GNIDA_PTM: 7500,
                        GNIDA_PACKAGE: 40000,
                        TM_APP: 2000,
                        TM48: 500,
                        NOIDA_TRANSFER: 2000,
                    };
                    const orderAmount = docPrices[activeTab] || 499;
                    // 1. Create order on backend
                    const res = await fetch(`${API_BASE}/create-order`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            amount: orderAmount,
                            service_type: activeTab,
                            customer_name: customerName,
                            customer_phone: customerPhone,
                            customer_email: customerEmail,
                            form_data: payload
                        })
                    });
                    
                    if (!res.ok) throw new Error("Order creation failed");
                    const orderData = await res.json();
                    
                    // 2. Open Razorpay or simulate if mock
                    if (orderData.order_id.startsWith('MOCK_ORD_')) {
                        addToast("Processing mock payment...", 'info');
                        const verifyRes = await fetch(`${API_BASE}/verify-payment`, {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                                razorpay_order_id: orderData.order_id,
                                razorpay_payment_id: 'mock_pay_' + Math.random().toString(36).substr(2, 9),
                                razorpay_signature: 'mock_signature'
                            })
                        });
                        
                        if (verifyRes.ok) {
                            setShowCheckoutModal(false);
                            addToast("Payment successful! Opening document...", 'success');
                            triggerPrint();
                        }
                    } else {
                        // Load Razorpay Script dynamically and process payment
                        const loaded = await loadRazorpayScript();
                        if (!loaded) {
                            addToast("Failed to load Razorpay. Check connection.", 'error');
                            return;
                        }
                        
                        let razorpayKey = '';
                        try {
                            const cfgRes = await fetch(`${API_BASE}/api/config`);
                            if (cfgRes.ok) {
                                const cfg = await cfgRes.json();
                                razorpayKey = cfg.razorpay_key || '';
                            }
                        } catch(e) {}
                        if (!razorpayKey) { addToast("Payment configuration error. Please contact support.", 'error'); return; }
                        
                        const options = {
                            key: razorpayKey,
                            amount: orderData.amount,
                            currency: orderData.currency,
                            name: 'INSTADEED',
                            description: 'Legal Agreement Drafting Fee',
                            order_id: orderData.order_id,
                                            handler: async function (response) {
                                                try {
                                                    trackEvent('payment_complete', activeTab, response.razorpay_order_id);
                                                    const verifyRes = await fetch(`${API_BASE}/verify-payment`, {
                                                        method: 'POST',
                                                        headers: { 'Content-Type': 'application/json' },
                                                        body: JSON.stringify({
                                                            razorpay_order_id: response.razorpay_order_id,
                                                            razorpay_payment_id: response.razorpay_payment_id,
                                                            razorpay_signature: response.razorpay_signature
                                                        })
                                                    });
                                                    if (verifyRes.ok) {
                                                        setShowCheckoutModal(false);
                                                        addToast("Payment verified! Downloading document...", 'success');
                                                        triggerPrint();
                                                    } else {
                                                        addToast("Payment verification failed. Contact support.", 'error');
                                                    }
                                                } catch (e) {
                                                    addToast("Payment verification error: " + e.message, 'error');
                                                }
                                            },
                            prefill: {
                                name: customerName,
                                email: customerEmail,
                                contact: customerPhone
                            },
                            theme: { color: '#2563EB' }
                        };
                        const rzp = new window.Razorpay(options);
                        rzp.open();
                    }
                } catch (e) {
                    console.error("Online checkout failed:", e);
                    addToast("Payment failed: " + e.message, 'error');
                }
            };"""

# 2. Locate B2C click handler block to replace
search_click_handler = """                                        // B2C Flow - pre-fill details from active data and show checkout modal
                                        const details = extractCustomerDetails();
                                        setCheckoutDetails({
                                            name: details.name || '',
                                            phone: details.phone || '',
                                            email: details.email || ''
                                        });
                                        setShowCheckoutModal(true);"""

replace_click_handler = """                                        // B2C Flow - pre-fill details from active data, check session and do Express Checkout if complete
                                        const details = extractCustomerDetails();
                                        const savedSession = localStorage.getItem('instadeed_user_session');
                                        let sessionUser = {};
                                        try {
                                            if (savedSession) sessionUser = JSON.parse(savedSession);
                                        } catch(e) {}
                                        
                                        const name = details.name || sessionUser.name || '';
                                        const phone = (details.phone || sessionUser.phone || '').replace(/\\D/g, '').slice(-10);
                                        const email = details.email || sessionUser.email || '';
                                        
                                        if (name && phone.length === 10 && email) {
                                            // Express Checkout
                                            addToast("Initiating Express Checkout...", 'info');
                                            handleOnlinePayment({ name, phone, email });
                                        } else {
                                            // Fallback to regular checkout modal
                                            setCheckoutDetails({ name, phone, email });
                                            setShowCheckoutModal(true);
                                        }"""

# Clean spaces for search and run replacement
import re
def clean_spaces(text):
    return re.sub(r'\s+', ' ', text).strip()

normalized_content = clean_spaces(content)

# We check if search_pay_fn normalized exists in normalized_content
if clean_spaces(search_pay_fn) in normalized_content:
    print("Found handleOnlinePayment function match!")
    # Replace handleOnlinePayment function
    # To do it safely, we escape special regex characters and replace spacing with \s*
    pattern_fn = re.escape(search_pay_fn).replace(r'\ ', r'\s*').replace(r'\$', r'\$')
    content = re.sub(pattern_fn, replace_pay_fn, content)
    print("handleOnlinePayment replaced!")
else:
    print("Could not find handleOnlinePayment match. Skipping.")

# We check if search_click_handler normalized exists in normalized_content
if clean_spaces(search_click_handler) in normalized_content:
    print("Found B2C click handler match!")
    pattern_click = re.escape(search_click_handler).replace(r'\ ', r'\s*').replace(r'\$', r'\$')
    content = re.sub(pattern_click, replace_click_handler, content)
    print("B2C click handler replaced!")
else:
    print("Could not find B2C click handler match. Skipping.")

# Write updated content back to test_script.jsx
with open("test_script.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("test_script.jsx updated successfully!")
