import sys
sys.stdout.reconfigure(encoding='utf-8')

content = open('test_script.jsx', 'r', encoding='utf-8').read()

checks = {
    'form_start tracking': "trackEvent('form_start'" in content,
    'form_step tracking': "trackEvent('form_step'" in content,
    'form_complete tracking': "trackEvent('form_complete'" in content,
    'checkout_start tracking': "trackEvent('checkout_start'" in content,
    'section-opened dispatch': "dispatchEvent(new CustomEvent('section-opened'" in content,
    'section-opened listener': "addEventListener('section-opened'" in content,
    'CRM top-level route': "activeTab === 'CRM' ?" in content and "renderCrmDashboard()" in content,
    'Terracotta palette (#9A3B2E)': '#9A3B2E' in content,
    'Master OTP in server': False,  # check separately
    'sanitize_phone in server': False,  # check separately
}

server = open('server.py', 'r', encoding='utf-8').read()
checks['Master OTP in server'] = '123456' in server
checks['sanitize_phone in server'] = 'sanitize_phone' in server

print("=" * 50)
print("  DEED PLATFORM — DELIVERABLE STATUS")
print("=" * 50)
all_pass = True
for k, v in checks.items():
    status = "✅ PASS" if v else "❌ FAIL"
    if not v:
        all_pass = False
    print(f"  {status}  {k}")

print("=" * 50)
if all_pass:
    print("  ALL CHECKS PASSED — READY TO SHIP")
else:
    print("  SOME CHECKS FAILED — NEEDS ATTENTION")
print("=" * 50)
