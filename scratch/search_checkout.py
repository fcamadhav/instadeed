import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("test_script.jsx", "r", encoding="utf-8") as f:
    for idx, line in enumerate(f):
        line_strip = line.strip()
        if "checkout" in line_strip.lower() or "payment" in line_strip.lower() or "razorpay" in line_strip.lower() or "paynow" in line_strip.lower() or "createorder" in line_strip.lower():
            # Print matching lines with line numbers
            print(f"{idx+1}: {line_strip[:120]}")
