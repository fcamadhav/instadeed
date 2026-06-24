import re

with open("landing.html", "r", encoding="utf-8") as f:
    content = f.read()

# Target block containing user chip and dropdown
old_user_block = """<!-- User chip (shown after sign-in) -->
<div class="user-chip" id="userChip" onclick="toggleUserMenu()">
<div class="user-avatar" id="userAvatar">U</div>
<span class="user-name" id="userName">User</span>
<i class="fa-solid fa-chevron-down" style="font-size:.55rem;color:var(--g400);margin-left:.15rem"></i>
</div>
<!-- User dropdown -->
<div id="userMenu" style="display:none;position:absolute;top:calc(100% + 10px);right:1.5rem;background:#fff;border:1px solid var(--g200);border-radius:var(--rl);padding:.5rem;min-width:190px;box-shadow:0 20px 40px rgba(0,0,0,.12);z-index:400">
<div style="padding:.55rem .7rem;font-size:.78rem;color:var(--g500);border-bottom:1px solid var(--g100);margin-bottom:.35rem" id="userMenuEmail"></div>
<div style="display:flex;align-items:center;gap:.5rem;padding:.5rem .7rem;font-size:.82rem;font-weight:500;color:var(--g700);border-radius:8px;cursor:pointer" onmouseover="this.style.background='var(--g50)'" onmouseout="this.style.background='transparent'" onclick="scrollToSection('pricing')"><i class="fa-solid fa-file-contract" style="color:var(--blue-l);width:14px"></i> My Documents</div>
<div style="display:flex;align-items:center;gap:.5rem;padding:.5rem .7rem;font-size:.82rem;font-weight:500;color:var(--rose);border-radius:8px;cursor:pointer" onmouseover="this.style.background='#FFF5F5'" onmouseout="this.style.background='transparent'" onclick="signOut()"><i class="fa-solid fa-right-from-bracket" style="width:14px"></i> Sign out</div>
</div>"""

new_user_block = """<!-- User chip (shown after sign-in) -->
<div class="user-chip" id="userChip" onclick="toggleUserMenu()">
  <div class="user-avatar" id="userAvatar">U</div>
  <span class="user-name" id="userName">User</span>
  <i class="fa-solid fa-chevron-down" style="font-size:.55rem;margin-left:.15rem"></i>
</div>
<!-- User dropdown -->
<div class="user-menu" id="userMenu" style="display:none;">
  <div class="user-menu-header" id="userMenuEmail"></div>
  <div class="user-menu-item" onclick="scrollToSection('pricing')">
    <i class="fa-solid fa-file-contract" style="color:var(--blue-l);width:14px;margin-right:0.5rem;"></i> My Documents
  </div>
  <div class="user-menu-item" style="color:var(--rose);" onclick="signOut()">
    <i class="fa-solid fa-right-from-bracket" style="color:var(--rose);width:14px;margin-right:0.5rem;"></i> Sign out
  </div>
</div>"""

# Replace in content
if old_user_block in content:
    new_content = content.replace(old_user_block, new_user_block)
    print("User block replaced successfully!")
else:
    # Try normalized spacing replacement
    normalized_old = re.sub(r'\s+', ' ', old_user_block)
    normalized_content = re.sub(r'\s+', ' ', content)
    if normalized_old in normalized_content:
        print("Block matches but has different whitespace. Running regex replace...")
        # A simple string match with broad spacing
        pattern = re.escape(old_user_block).replace(r'\ ', r'\s*')
        new_content = re.sub(pattern, new_user_block, content)
        print("Regex replaced successfully!")
    else:
        new_content = content
        print("User block not found. Skipping.")

with open("landing.html", "w", encoding="utf-8") as f:
    f.write(new_content)
