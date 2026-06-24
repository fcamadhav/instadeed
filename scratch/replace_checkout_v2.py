with open("test_script.jsx", "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")

# Find indices
start_pay_idx = -1
end_pay_idx = -1
start_click_idx = -1
end_click_idx = -1

for idx, line in enumerate(lines):
    if "const handleOnlinePayment = async () => {" in line:
        start_pay_idx = idx
    if start_pay_idx != -1 and end_pay_idx == -1 and "const loadRazorpayScript = () => {" in line:
        end_pay_idx = idx # Exclusive

    if "// B2C Flow - pre-fill details from active data and show checkout modal" in line:
        start_click_idx = idx
    if start_click_idx != -1 and end_click_idx == -1 and "setShowCheckoutModal(true);" in line:
        end_click_idx = idx + 1 # Inclusive

print(f"Payment function range: {start_pay_idx} to {end_pay_idx}")
print(f"Click handler range: {start_click_idx} to {end_click_idx}")

if start_pay_idx == -1 or end_pay_idx == -1 or start_click_idx == -1 or end_click_idx == -1:
    print("Failed to find some target lines. Exiting.")
    exit(1)

# Let's inspect the target segments to make sure they are correct
print("=== Target Payment Function ===")
print("".join(lines[start_pay_idx : start_pay_idx + 3]))
print("...")
print("".join(lines[end_pay_idx - 3 : end_pay_idx]))

print("\n=== Target Click Handler ===")
print("".join(lines[start_click_idx:end_click_idx]))
